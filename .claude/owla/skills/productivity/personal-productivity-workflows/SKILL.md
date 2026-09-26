---
name: personal-productivity-workflows
description: Manage calendar and task-list workflows.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [calendar, task-list, productivity, telegram, reminders]
---

# Personal productivity workflows

Use this skill for Natalie’s short calendar queries, calendar edits, and Task-list management. It applies when she asks for “Что на завтра?”, adds items to “✅ Natalie’s Task-list”, or requests updates, deletes, or daily summaries. Keep replies short, concrete, and formatted for Telegram.

See `references/task-list-and-calendar-cues.md` for the exact cues and preferred examples.

## When to Use

- “Что на завтра?” / “Что на сегодня?” / “Что на неделе?”
- Add, move, or delete calendar events
- “добавь в Task-list …”
- Mark tasks done
- Reorganize the Task-list into work and personal sections

## Workflow

1. For calendar queries, read events for the requested day and answer with only the list.
2. For calendar edits, change the event, then verify by reading the day again.
3. For Task-list additions, preserve category and add an emoji that matches the task meaning.
4. If a task is completed, set status to `✔️ done`.
5. If the request is ambiguous, ask one short clarification in a separate message.
6. When replying with the Task-list, show only the list itself. Do not add extra notes below it.

## Task-list format

- Section headers:
  - 👩‍💻 Рабочие
  - 🧑‍🧑‍🧒‍🧒 Личные
- Keep tasks under the right header.
- Preserve user wording when possible.
- Use compact bullets only.

## Calendar format

- Prefer short Russian summaries.
- If asked “Что на завтра?”, treat it as a next-day calendar summary.
- Use the verified calendar source; never guess.
- After add/update/delete, verify by re-reading the calendar.

## Pitfalls

- Do not place clarification notes below a finished list.
- Do not dump explanations when the user asked for the list only.
- Do not accept or store secrets.

## Verification

- Calendar changes are verified by reading the day again.
- Task-list changes are verified by showing the updated grouped list.
