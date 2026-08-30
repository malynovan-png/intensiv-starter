#!/usr/bin/env python3
"""Calendar tool for Owla.

Supports:
  list [today|tomorrow|YYYY-MM-DD]
  add --summary TEXT --start "YYYY-MM-DD HH:MM" --end "YYYY-MM-DD HH:MM" [--calendar work|home|<id>] [--tz Europe/Moscow]
  update --match TEXT [--date YYYY-MM-DD] [--summary TEXT] [--start ...] [--end ...] [--calendar ...]
  delete --match TEXT [--date YYYY-MM-DD] [--calendar ...]

Uses iCloud CalDAV credentials from secrets/icloud-caldav.env.
"""
from __future__ import annotations

import argparse
import base64
import os
import re
import sys
import textwrap
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from dateutil import tz

ROOT = Path("/root/intensiv-starter")
ENV_FILE = ROOT / "secrets/icloud-caldav.env"
BASE = "https://p147-caldav.icloud.com:443/10161366510/calendars"
DEFAULT_TZ = "Europe/Moscow"
CALENDARS = {
    "calendar": "D2C9CAA9-4186-4470-9138-E722C49D1FC4",
    "home": "home",
    "work": "work",
}


@dataclass
class Event:
    cal_name: str
    cal_id: str
    href: str
    uid: str
    summary: str
    dtstart: str
    dtend: str | None
    tzid: str | None
    rrule: str | None = None


# ---------- Env / HTTP helpers ----------

def load_env() -> dict[str, str]:
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def auth_header() -> str:
    env = load_env()
    token = base64.b64encode(f"{env['APPLE_ID']}:{env['APPLE_APP_PASSWORD']}".encode()).decode()
    return f"Basic {token}"


def cal_url(cal_id: str, href: str = "") -> str:
    if href:
        href = href.lstrip("/")
        return f"{BASE}/{cal_id}/{href}"
    return f"{BASE}/{cal_id}/"


def request(url: str, method: str, body: bytes | None = None, headers: dict[str, str] | None = None):
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    return urllib.request.urlopen(req, timeout=30)


# ---------- Date helpers ----------

def parse_day(s: str) -> date:
    s = s.strip().lower()
    if s in {"today", "сегодня"}:
        return datetime.now(tz.gettz(DEFAULT_TZ)).date()
    if s in {"tomorrow", "завтра"}:
        return (datetime.now(tz.gettz(DEFAULT_TZ)) + timedelta(days=1)).date()
    return datetime.strptime(s, "%Y-%m-%d").date()


def parse_dt(s: str, tz_name: str = DEFAULT_TZ) -> datetime:
    # Accept "YYYY-MM-DD HH:MM" or ISO-ish "YYYY-MM-DDTHH:MM"
    s = s.strip().replace("T", " ")
    dt = datetime.strptime(s, "%Y-%m-%d %H:%M")
    return dt.replace(tzinfo=tz.gettz(tz_name))


def ical_dt(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz.gettz(DEFAULT_TZ))
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def local_str(dt: datetime) -> str:
    return dt.astimezone(tz.gettz(DEFAULT_TZ)).strftime("%d.%m %H:%M")


# ---------- CalDAV parsing ----------

def unfold_ics(text: str) -> str:
    lines = text.splitlines()
    out = []
    for line in lines:
        if line.startswith((" ", "\t")) and out:
            out[-1] += line[1:]
        else:
            out.append(line)
    return "\n".join(out)


def get_field(block: str, name: str) -> tuple[str | None, str | None]:
    m = re.search(rf"^{name}([^:\n]*):(.*)$", block, re.M)
    if not m:
        return None, None
    return m.group(1), m.group(2).strip()


def parse_events(xml_text: str, cal_name: str, cal_id: str) -> list[Event]:
    events: list[Event] = []
    # Match each response entry; href may be absent in some responses but is useful if present.
    responses = re.findall(r"<[^:>]*:response>(.*?)</[^:>]*:response>", xml_text, re.S)
    if not responses:
        responses = re.findall(r"<response[^>]*>(.*?)</response>", xml_text, re.S)
    for resp in responses:
        href_m = re.search(r"<[^:>]*:href>(.*?)</[^:>]*:href>", resp, re.S)
        href = href_m.group(1).strip() if href_m else ""
        for block in re.findall(r"<calendar-data[^>]*>(.*?)</calendar-data>", resp, re.S):
            ics = block.replace("<![CDATA[", "").replace("]]>", "")
            ics = ics.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            ics = unfold_ics(ics)
            for vevent in re.findall(r"BEGIN:VEVENT.*?END:VEVENT", ics, re.S):
                _, summary = get_field(vevent, "SUMMARY")
                dtstart_params, dtstart = get_field(vevent, "DTSTART")
                _, dtend = get_field(vevent, "DTEND")
                _, uid = get_field(vevent, "UID")
                _, rrule = get_field(vevent, "RRULE")
                if not dtstart or not uid:
                    continue
                tzid_m = re.search(r"TZID=([^;:]+)", dtstart_params or "")
                tzid = tzid_m.group(1) if tzid_m else None
                events.append(
                    Event(
                        cal_name=cal_name,
                        cal_id=cal_id,
                        href=href,
                        uid=uid,
                        summary=(summary or "(без названия)").replace("\\,", ",").replace("\\n", " "),
                        dtstart=dtstart,
                        dtend=dtend,
                        tzid=tzid,
                        rrule=rrule,
                    )
                )
    return events


def to_datetime(dtstart: str, tzid: str | None) -> datetime:
    if dtstart.endswith("Z"):
        return datetime.strptime(dtstart, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    for fmt in ("%Y%m%dT%H%M%S", "%Y%m%d"):
        try:
            dt = datetime.strptime(dtstart, fmt)
            return dt.replace(tzinfo=tz.gettz(tzid or DEFAULT_TZ))
        except ValueError:
            pass
    raise ValueError(f"Unsupported DTSTART format: {dtstart!r}")


def window_for_day(day: date) -> tuple[datetime, datetime]:
    start = datetime(day.year, day.month, day.day, 0, 0, tzinfo=tz.gettz(DEFAULT_TZ))
    end = start + timedelta(days=1)
    return start.astimezone(timezone.utc), end.astimezone(timezone.utc)


def occurrences_in_window(ev: Event, window_start: datetime, window_end: datetime):
    base_dt = to_datetime(ev.dtstart, ev.tzid)
    if not ev.rrule:
        if window_start <= base_dt < window_end:
            yield base_dt
        return
    try:
        from dateutil.rrule import rrulestr
        rule = rrulestr(f"RRULE:{ev.rrule}", dtstart=base_dt)
    except Exception:
        return
    for occ in rule.between(window_start, window_end, inc=True):
        yield occ
    # Fall back to daily projection for malformed/limited CalDAV recurrences.
    if ev.rrule and "FREQ=DAILY" in ev.rrule.upper():
        daily_occ = datetime(
            window_start.astimezone(base_dt.tzinfo).year,
            window_start.astimezone(base_dt.tzinfo).month,
            window_start.astimezone(base_dt.tzinfo).day,
            base_dt.hour,
            base_dt.minute,
            base_dt.second,
            base_dt.microsecond,
            tzinfo=base_dt.tzinfo,
        )
        if window_start <= daily_occ.astimezone(timezone.utc) < window_end:
            yield daily_occ


# ---------- Listing ----------

def report(cal_id: str, start_utc: datetime, end_utc: datetime) -> str:
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<C:calendar-query xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
  <D:prop><D:getetag/><D:href/><C:calendar-data/></D:prop>
  <C:filter>
    <C:comp-filter name="VCALENDAR">
      <C:comp-filter name="VEVENT">
        <C:time-range start="{start_utc.strftime('%Y%m%dT%H%M%SZ')}" end="{end_utc.strftime('%Y%m%dT%H%M%SZ')}"/>
      </C:comp-filter>
    </C:comp-filter>
  </C:filter>
</C:calendar-query>"""
    with request(
        cal_url(cal_id),
        "REPORT",
        body=body.encode(),
        headers={
            "Depth": "1",
            "Content-Type": "application/xml",
            "Authorization": auth_header(),
        },
    ) as resp:
        return resp.read().decode("utf-8", "replace")


def list_events(day_s: str) -> list[Event]:
    day = parse_day(day_s)
    # Fetch a wider window so we can expand recurring events whose master start
    # falls before the requested day (e.g. daily reminders created months ago).
    request_start = datetime(day.year - 1 if day.month == 1 and day.day == 1 else day.year, 1, 1, tzinfo=tz.gettz(DEFAULT_TZ))
    if day.month != 1 or day.day != 1:
        request_start = datetime(day.year - 1, day.month, day.day, tzinfo=tz.gettz(DEFAULT_TZ))
    start_utc = request_start.astimezone(timezone.utc)
    end_utc = (datetime(day.year, day.month, day.day, 23, 59, 59, tzinfo=tz.gettz(DEFAULT_TZ)) + timedelta(days=1)).astimezone(timezone.utc)
    window_start, window_end = window_for_day(day)
    found: list[Event] = []
    seen: set[tuple[str, str]] = set()
    for cal_name, cal_id in CALENDARS.items():
        try:
            xml = report(cal_id, start_utc, end_utc)
        except urllib.error.URLError as e:
            print(f"WARN: {cal_name}: {e}", file=sys.stderr)
            continue
        for ev in parse_events(xml, cal_name, cal_id):
            for occ in occurrences_in_window(ev, window_start, window_end):
                key = (ev.uid, occ.isoformat())
                if key in seen:
                    continue
                seen.add(key)
                found.append(
                    Event(
                        cal_name=ev.cal_name,
                        cal_id=ev.cal_id,
                        href=ev.href,
                        uid=ev.uid,
                        summary=ev.summary,
                        dtstart=occ.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
                        dtend=(occ + (to_datetime(ev.dtend, ev.tzid) - to_datetime(ev.dtstart, ev.tzid))).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ") if ev.dtend else None,
                        tzid=ev.tzid,
                    )
                )
    found.sort(key=lambda e: to_datetime(e.dtstart, e.tzid))
    return found


def print_events(day_s: str) -> int:
    day = parse_day(day_s)
    events = list_events(day_s)
    label = day.strftime("%d.%m.%Y")
    print(f"События на {label}:")
    if not events:
        print("— ничего не найдено")
        return 0
    for i, ev in enumerate(events, 1):
        dt = to_datetime(ev.dtstart, ev.tzid)
        end = to_datetime(ev.dtend, ev.tzid) if ev.dtend else None
        time_part = local_str(dt)
        if end:
            time_part += f"–{end.astimezone(tz.gettz(DEFAULT_TZ)).strftime('%H:%M')}"
        print(f"{i}. {time_part} — {ev.summary} [{ev.cal_name}] UID={ev.uid}")
    return 0


# ---------- Write / update / delete ----------

def pick_calendar(name_or_id: str) -> tuple[str, str]:
    key = name_or_id.strip().lower()
    if key in CALENDARS:
        return key, CALENDARS[key]
    # allow raw calendar id
    return key, name_or_id


def build_ics(summary: str, dtstart: datetime, dtend: datetime, uid: str, tz_name: str = DEFAULT_TZ) -> str:
    tzid = tz_name
    safe_summary = summary.replace("\\", "\\\\").replace(",", "\\,").replace("\n", " ")
    ics = textwrap.dedent(
        f"""\
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:-//Hermes//Owla Calendar Tool//EN
        CALSCALE:GREGORIAN
        BEGIN:VEVENT
        UID:{uid}
        DTSTAMP:{ical_dt(datetime.now(timezone.utc))}
        DTSTART;TZID={tzid}:{dtstart.astimezone(tz.gettz(tzid)).strftime('%Y%m%dT%H%M%S')}
        DTEND;TZID={tzid}:{dtend.astimezone(tz.gettz(tzid)).strftime('%Y%m%dT%H%M%S')}
        SUMMARY:{safe_summary}
        END:VEVENT
        END:VCALENDAR
        """
    )
    return ics.replace("\n", "\r\n")


def put_event(cal_id: str, uid: str, ics: str):
    href = f"{uid}.ics"
    with request(
        cal_url(cal_id, href),
        "PUT",
        body=ics.encode(),
        headers={
            "Content-Type": "text/calendar; charset=utf-8",
            "Authorization": auth_header(),
        },
    ) as resp:
        return resp.status


def create_event(args) -> int:
    cal_name, cal_id = pick_calendar(args.calendar)
    dtstart = parse_dt(args.start, args.tz)
    dtend = parse_dt(args.end, args.tz)
    uid = str(uuid.uuid4())
    ics = build_ics(args.summary, dtstart, dtend, uid, args.tz)
    status = put_event(cal_id, uid, ics)
    print(f"OK: created in {cal_name} ({status})")
    print(f"{local_str(dtstart)} — {args.summary}")
    return 0


def find_matching_event(match: str, day_s: str | None, calendar: str | None) -> Event | None:
    pool = list_events(day_s or "today") if day_s else []
    if not pool:
        # search wider
        pool = list_events("today") + list_events("tomorrow")
    if calendar:
        cal_name, _ = pick_calendar(calendar)
        pool = [e for e in pool if e.cal_name == cal_name]
    m = match.strip().lower()
    exact_uid = [e for e in pool if e.uid.lower() == m]
    if exact_uid:
        return exact_uid[0]
    candidates = [e for e in pool if m in e.summary.lower()]
    if len(candidates) == 1:
        return candidates[0]
    return candidates[0] if candidates else None


def update_event(args) -> int:
    ev = find_matching_event(args.match, args.date, args.calendar)
    if not ev:
        print("NOT FOUND")
        return 1
    summary = args.summary or ev.summary
    dtstart = parse_dt(args.start, args.tz) if args.start else to_datetime(ev.dtstart, ev.tzid)
    dtend = parse_dt(args.end, args.tz) if args.end else (to_datetime(ev.dtend, ev.tzid) if ev.dtend else dtstart + timedelta(hours=1))
    uid = ev.uid
    cal_name, cal_id = pick_calendar(args.calendar or ev.cal_name)
    ics = build_ics(summary, dtstart, dtend, uid, args.tz)
    status = put_event(cal_id, uid, ics)
    print(f"OK: updated in {cal_name} ({status})")
    print(f"{local_str(dtstart)} — {summary}")
    return 0


def delete_event(args) -> int:
    ev = find_matching_event(args.match, args.date, args.calendar)
    if not ev:
        print("NOT FOUND")
        return 1
    cal_name, cal_id = pick_calendar(args.calendar or ev.cal_name)
    href = ev.href or f"{ev.uid}.ics"
    with request(
        cal_url(cal_id, href),
        "DELETE",
        headers={"Authorization": auth_header()},
    ) as resp:
        print(f"OK: deleted from {cal_name} ({resp.status})")
        return 0


# ---------- CLI ----------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Owla calendar tool")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List events for a day")
    p_list.add_argument("day", nargs="?", default="today", help="today|tomorrow|YYYY-MM-DD")

    p_add = sub.add_parser("add", help="Create an event")
    p_add.add_argument("--summary", required=True)
    p_add.add_argument("--start", required=True, help='"YYYY-MM-DD HH:MM"')
    p_add.add_argument("--end", required=True, help='"YYYY-MM-DD HH:MM"')
    p_add.add_argument("--calendar", default="work", help="calendar name or id")
    p_add.add_argument("--tz", default=DEFAULT_TZ)

    p_upd = sub.add_parser("update", help="Update an event by uid or summary match")
    p_upd.add_argument("--match", required=True, help="UID or unique text match")
    p_upd.add_argument("--date", default=None, help="YYYY-MM-DD (optional hint)")
    p_upd.add_argument("--summary")
    p_upd.add_argument("--start", help='"YYYY-MM-DD HH:MM"')
    p_upd.add_argument("--end", help='"YYYY-MM-DD HH:MM"')
    p_upd.add_argument("--calendar", default=None)
    p_upd.add_argument("--tz", default=DEFAULT_TZ)

    p_del = sub.add_parser("delete", help="Delete an event by uid or summary match")
    p_del.add_argument("--match", required=True, help="UID or unique text match")
    p_del.add_argument("--date", default=None, help="YYYY-MM-DD (optional hint)")
    p_del.add_argument("--calendar", default=None)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "list":
        return print_events(args.day)
    if args.cmd == "add":
        return create_event(args)
    if args.cmd == "update":
        return update_event(args)
    if args.cmd == "delete":
        return delete_event(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
