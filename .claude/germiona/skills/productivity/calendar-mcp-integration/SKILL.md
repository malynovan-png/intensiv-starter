---
name: calendar-mcp-integration
description: Use when wiring calendar access into Hermes.
---

# Calendar MCP Integration

Use when a Hermes agent must read or edit a real calendar and answer calendar questions directly in chat.

## What this skill covers
- Build a CalDAV-backed calendar script first.
- Wrap it in an MCP server so Hermes can discover the tools.
- Register the MCP server in the active Hermes profile.
- Teach the assistant persona to call the calendar tool first instead of apologizing.

## Workflow

1. **Inventory the calendar source.**
   - Confirm the secret env file, CalDAV endpoint, and calendar IDs.
   - For iCloud, verify the calendar tree with `PROPFIND` before querying events.
   - If the user says they already have events but the tool says empty, distrust the answer and inspect the raw CalDAV response.

2. **Build a standalone calendar script.**
   - Keep the actual calendar logic in a plain Python module.
   - Support at least:
     - `list today|tomorrow|YYYY-MM-DD`
     - `add`
     - `update`
     - `delete`
   - Make the script runnable from the terminal before adding MCP.

3. **Parse CalDAV carefully.**
   - Expect Apple/iCloud responses to use `<![CDATA[ ... ]]>` wrappers.
   - Do not hardcode only one XML namespace form.
   - Unfold ICS lines before extracting fields.
   - Be timezone-aware when converting DTSTART/DTEND.
   - Handle all-day dates (`YYYYMMDD`) as well as timed events.
   - Expand recurring events before declaring a day empty; daily RRULE events are an easy place to get false negatives.

4. **Wrap the script in MCP.**
   - Use Hermes' native MCP client/server flow.
   - Expose explicit tools like `list_events`, `add_event`, `update_event`, `delete_event`.
   - Run the server over stdio for Hermes discovery.
   - After registering the server, check logs for `tools.mcp_tool` registration lines.

5. **Register the server in the profile.**
   - Add an `mcp_servers` entry in the profile `config.yaml`.
   - Restart the profile gateway after changes.
   - Verify discovery with `hermes mcp list`.
   - If the profile answers from stale context, force a clean gateway restart, then retest the same question.

6. **Teach the persona to use the tool.**
   - Calendar questions should call the MCP tool first.
   - For "что у меня на завтра?" return events, not a bridge/scanner explanation.
   - If the MCP returns no events, say that honestly.
   - If the MCP returns events but the assistant still says empty, update the persona text so the tool output wins over cached narrative.

## Common pitfalls
- CalDAV queries returning nothing because the XML parser only matches one namespace form.
- Searching the wrong calendar collection ID.
- Forgetting to restart the gateway after config or SOUL changes.
- Leaving stale wording like "I can't see the calendar" after the tool is already connected.

## Verification
- The standalone script lists tomorrow's events correctly.
- The MCP server registers in gateway logs.
- `hermes mcp list` shows the calendar server.
- Telegram answers a calendar query without asking for a screenshot.

## Support files
- `references/caldav-mcp-notes.md` — the recovery pattern, parser quirks, and verification sequence from this session.
