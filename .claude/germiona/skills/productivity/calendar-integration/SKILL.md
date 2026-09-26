---
name: calendar-integration
description: "Use when calendars must be read or edited. Use tools first."
version: 1.0.0
author: Hermes Agent
tags: [calendar, caldav, mcp, productivity, scheduling]
---

# Calendar integration

Use when an agent must read, add, update, delete, or summarize calendar events.

## Core rule
Prefer a real calendar tool over screenshots, manual copy/paste, or bridge text. Call the calendar tool first, then answer from tool output.

## Recommended workflow
1. Identify the calendar backend: iCloud CalDAV, Google Calendar, or another source.
2. Expose four operations as first-class tools:
   - `list_events(day)`
   - `add_event(...)`
   - `update_event(...)`
   - `delete_event(...)`
3. If using Hermes MCP, register the calendar server in the active profile config and restart the gateway so tools are discovered at startup.
4. For read queries, return a simple list of events.
5. Highlight time conflicts separately instead of forcing morning/day/evening buckets unless the user explicitly asks for that format.
6. For add/update/delete, ask only for missing fields: date, time, title, calendar name, or match text.

## Recurrence handling
- Expand recurring events to the requested day, not just the master event start date.
- Daily reminders and repeated events should still appear on future dates.
- Be careful with all-day events, date-only DTSTART values, and RRULEs.

## Verification
- Test a known date with at least one event and confirm it appears in `list_events`.
- Compare the tool output to the source calendar if the user says an event is missing.
- If a result is empty but the user insists there are events, inspect recurrence expansion and the raw calendar response before concluding the calendar is empty.

## Pitfalls
- XML namespace and CDATA wrappers in CalDAV responses can hide events from naive parsers.
- Do not assume a date-only DTSTART is malformed; parse it explicitly.
- If the agent says the calendar is unavailable but the MCP/tool is already connected, update the agent persona so it calls the tool first.
- Do not turn a tool's empty result into a confident factual claim.

## Output style
- For calendar answers, keep the response short and factual.
- Default to a list of events.
- Show conflicts separately.
- Avoid extra narrative unless the user asks for a summary or plan.

## See also
- `references/caldav-mcp-session.md` — compact notes from a real Hermes + iCloud CalDAV integration, including recurrence and parser fixes.
