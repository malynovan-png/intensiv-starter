#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from types import SimpleNamespace

from mcp.server import MCPServer

ROOT = Path("/root/intensiv-starter")
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import calendar_tool as ct  # noqa: E402

mcp = MCPServer(
    name="owla_calendar",
    title="Owla Calendar",
    description="Read and edit Natalie's iCloud calendar",
)


@mcp.tool(
    name="list_events",
    description="List calendar events for a day. Use today, tomorrow, or YYYY-MM-DD.",
)
def list_events(day: str = "today") -> str:
    events = ct.list_events(day)
    label = ct.parse_day(day).strftime("%d.%m.%Y")
    if not events:
        return f"События на {label}: ничего не найдено"
    lines = [f"События на {label}:"]
    for i, ev in enumerate(events, 1):
        dt = ct.to_datetime(ev.dtstart, ev.tzid)
        end = ct.to_datetime(ev.dtend, ev.tzid) if ev.dtend else None
        time_part = ct.local_str(dt)
        if end:
            time_part += f"–{end.astimezone(ct.tz.gettz(ct.DEFAULT_TZ)).strftime('%H:%M')}"
        lines.append(f"{i}. {time_part} — {ev.summary} [{ev.cal_name}]")
    return "\n".join(lines)


@mcp.tool(
    name="add_event",
    description="Create a calendar event. start/end format: YYYY-MM-DD HH:MM.",
)
def add_event(summary: str, start: str, end: str, calendar: str = "work", tz: str = "Europe/Moscow") -> str:
    args = SimpleNamespace(summary=summary, start=start, end=end, calendar=calendar, tz=tz)
    rc = ct.create_event(args)
    if rc != 0:
        return "ERROR: create failed"
    return f"OK: created — {summary} ({start} to {end})"


@mcp.tool(
    name="update_event",
    description="Update a calendar event by matching uid or unique summary text.",
)
def update_event(match: str, date: str | None = None, summary: str | None = None, start: str | None = None, end: str | None = None, calendar: str | None = None, tz: str = "Europe/Moscow") -> str:
    args = SimpleNamespace(match=match, date=date, summary=summary, start=start, end=end, calendar=calendar, tz=tz)
    result = ct.update_event(args)
    if result != 0:
        return "NOT FOUND"
    return "OK: updated"


@mcp.tool(
    name="delete_event",
    description="Delete a calendar event by matching uid or unique summary text.",
)
def delete_event(match: str, date: str | None = None, calendar: str | None = None) -> str:
    args = SimpleNamespace(match=match, date=date, calendar=calendar)
    result = ct.delete_event(args)
    if result != 0:
        return "NOT FOUND"
    return "OK: deleted"


async def main() -> None:
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
