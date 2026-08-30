#!/usr/bin/env python3
"""
check_reminders.py — сканирует iCloud-календарь Natalie (CalDAV) и шлёт
напоминания в Telegram за день и за 15 минут до события.

Работает независимо от основного агента (claude) — вызывается системным
cron'ом напрямую, как и scripts/reminders/send-telegram.sh, поэтому
напоминания приходят, даже если сам агент завис или перезапускается.

Запуск: cron каждые 5 минут (см. crontab, тег CALENDAR_REMINDERS).
"""
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dateutil import tz
from dateutil.rrule import rrulestr

ROOT = Path("/root/intensiv-starter")
ENV_FILE = ROOT / "secrets/icloud-caldav.env"
STATE_FILE = ROOT / "dashi-plugin-claude-code/plugin/state/calendar/reminders-sent.json"
CHAT_ID = "936853282"
BASE = "https://p147-caldav.icloud.com:443/10161366510/calendars"
CALENDARS = {
    "D2C9CAA9-4186-4470-9138-E722C49D1FC4": "Calendar",
    "home": "Домашний",
    "work": "Рабочий",
}

DAY_BEFORE_WINDOW = (timedelta(hours=23, minutes=50), timedelta(hours=24, minutes=10))
FIFTEEN_MIN_WINDOW = (timedelta(minutes=10), timedelta(minutes=20))
LOOKAHEAD = timedelta(hours=26)
STATE_MAX_AGE_DAYS = 3


def load_env():
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def caldav_report(cal_id: str, auth_header: str, start: datetime, end: datetime) -> str:
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<C:calendar-query xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
  <D:prop><D:getetag/><C:calendar-data/></D:prop>
  <C:filter>
    <C:comp-filter name="VCALENDAR">
      <C:comp-filter name="VEVENT">
        <C:time-range start="{start.strftime('%Y%m%dT%H%M%SZ')}" end="{end.strftime('%Y%m%dT%H%M%SZ')}"/>
      </C:comp-filter>
    </C:comp-filter>
  </C:filter>
</C:calendar-query>"""
    req = urllib.request.Request(
        f"{BASE}/{cal_id}/",
        data=body.encode("utf-8"),
        method="REPORT",
        headers={
            "Depth": "1",
            "Content-Type": "application/xml",
            "Authorization": auth_header,
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_events(xml_text: str):
    """Very small regex-based extractor — avoids depending on an XML+ICS
    stack that may not be installed. Good enough for Apple's CalDAV output."""
    events = []
    for block in re.findall(r"<calendar-data[^>]*>(.*?)</calendar-data>", xml_text, re.S):
        ics = block.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        for vevent in re.findall(r"BEGIN:VEVENT.*?END:VEVENT", ics, re.S):
            def field(name):
                m = re.search(rf"^{name}([^:\n]*):(.*)$", vevent, re.M)
                return (m.group(1), m.group(2).strip()) if m else (None, None)

            _, summary = field("SUMMARY")
            dtstart_params, dtstart = field("DTSTART")
            _, rrule = field("RRULE")
            _, uid = field("UID")
            if not dtstart or not uid:
                continue
            tzid_m = re.search(r"TZID=([^;:]+)", dtstart_params or "")
            tzid = tzid_m.group(1) if tzid_m else None
            events.append(
                {
                    "summary": (summary or "(без названия)").replace("\\,", ",").replace("\\n", " "),
                    "dtstart": dtstart,
                    "tzid": tzid,
                    "rrule": rrule,
                    "uid": uid,
                }
            )
    return events


def to_datetime(dtstart: str, tzid: str | None) -> datetime:
    if dtstart.endswith("Z"):
        return datetime.strptime(dtstart, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    dt = datetime.strptime(dtstart, "%Y%m%dT%H%M%S")
    zone = tz.gettz(tzid) if tzid else tz.gettz("Europe/Moscow")
    return dt.replace(tzinfo=zone)


def occurrences_in_window(ev, window_start: datetime, window_end: datetime):
    base_dt = to_datetime(ev["dtstart"], ev["tzid"])
    if not ev["rrule"]:
        if window_start <= base_dt <= window_end:
            yield base_dt
        return
    try:
        rule = rrulestr(f"RRULE:{ev['rrule']}", dtstart=base_dt)
    except Exception:
        return
    for occ in rule.between(window_start, window_end, inc=True):
        yield occ


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            return {}
    return {}


def save_state(state: dict, now: datetime):
    cutoff = now - timedelta(days=STATE_MAX_AGE_DAYS)
    pruned = {k: v for k, v in state.items() if datetime.fromisoformat(v) > cutoff}
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(pruned, ensure_ascii=False, indent=2))


def send_telegram(text: str):
    subprocess.run(
        [str(ROOT / "scripts/reminders/send-telegram.sh"), CHAT_ID, text],
        check=False,
    )


def main():
    env = load_env()
    token = base64.b64encode(f"{env['APPLE_ID']}:{env['APPLE_APP_PASSWORD']}".encode()).decode()
    auth_header = f"Basic {token}"

    now = datetime.now(timezone.utc)
    window_start = now
    window_end = now + LOOKAHEAD

    state = load_state()
    changed = False

    for cal_id, cal_name in CALENDARS.items():
        try:
            xml_text = caldav_report(cal_id, auth_header, window_start, window_end)
        except urllib.error.URLError as e:
            print(f"WARN: {cal_name}: {e}", file=sys.stderr)
            continue

        for ev in parse_events(xml_text):
            for occ in occurrences_in_window(ev, window_start, window_end):
                delta = occ - now
                key_base = f"{ev['uid']}:{occ.isoformat()}"
                local = occ.astimezone(tz.gettz("Europe/Moscow"))
                when = local.strftime("%d.%m %H:%M")

                if DAY_BEFORE_WINDOW[0] <= delta <= DAY_BEFORE_WINDOW[1]:
                    key = f"{key_base}:day"
                    if key not in state:
                        send_telegram(f"📅 Завтра в {when} — {ev['summary']} ({cal_name})")
                        state[key] = now.isoformat()
                        changed = True

                if FIFTEEN_MIN_WINDOW[0] <= delta <= FIFTEEN_MIN_WINDOW[1]:
                    key = f"{key_base}:15min"
                    if key not in state:
                        send_telegram(f"⏰ Через 15 минут — {ev['summary']} ({when}, {cal_name})")
                        state[key] = now.isoformat()
                        changed = True

    if changed:
        save_state(state, now)


if __name__ == "__main__":
    main()
