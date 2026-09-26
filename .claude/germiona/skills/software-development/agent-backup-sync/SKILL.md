---
name: agent-backup-sync
description: Use when syncing live agent layers and GitHub archives.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [agents, backup, github, archive, sync, profiles, skills, configuration]
---

# Agent Backup Sync

Use this skill when maintaining an AI agent across multiple layers:

- **Live layer** — the running profile that actually answers users.
- **Backup layer** — safe, non-secret files committed to GitHub.
- **Archive layer** — parallel Claude-side snapshots for future restore.
- **Secret-only local layer** — tokens, keys, passwords, and `.env` files that never leave the machine.

Reference map: `references/layer-map.md`.

## Core rule

Keep the live agent current first, then mirror only safe artifacts to backup/archive layers. Never commit secrets, runtime markers, cache, logs, or session state.

Reference map: `references/layer-map.md`.

## When to use

Use for tasks like:

- updating an agent personality or SOUL file
- merging Claude-style personality prompts into the current Hermes agent
- adding a new skill or changing a skill snapshot
- adding a new tool or workflow (calendar, MCP, voice, post-writing)
- keeping Hermes and Claude versions in parallel
- preparing a GitHub commit for the agent state

## Workflow

1. **Update the live layer first.**
   - Hermes profile: `~/.hermes/profiles/<agent>/`
   - Claude layer if relevant: `.claude/`
2. **Classify the change.**
   - Safe to archive: personality, prompts, skill text, tool code, templates, style guides, redacted configs.
   - Keep local only: `.env`, keys, tokens, passwords, app-specific passwords.
   - Usually ignore: logs, caches, sessions, watchdog markers, temp files.
3. **Mirror safe files to the backup bundle.**
   - Example pattern: `backups/<agent>/profile/`, `backups/<agent>/style/`, `backups/<agent>/skills/`, `backups/<agent>/calendar/`
4. **Mirror reusable Claude-side artifacts when the user wants a parallel Claude archive.**
   - Keep this as an archive, not a live runtime dependency.
5. **Verify secrets are absent before staging.**
   - Search staged files for secret markers (`API_KEY`, `TOKEN`, `PASSWORD`, `SECRET`).
   - Check `git status` for runtime-only leftovers.
6. **Commit in meaningful checkpoints.**
   - Commit after a real improvement: persona update, new skill, calendar integration, style-guide update, or backup sync.
7. **Tell the user what was saved.**
   - Call out whether the change landed in live layer, backup layer, Claude archive, or local-only secrets.

## Practical backup pattern

A useful default structure is:

- `~/.hermes/profiles/<agent>/` — live agent runtime
- `/root/intensiv-starter/backups/<agent>/` — GitHub-safe backup bundle
- `/root/intensiv-starter/.claude/` — Claude archive layer
- `~/.hermes/profiles/<agent>/.env` and `secrets/*.env` — local only

## Proactive reminder behavior

When a user says they want an agent kept in sync, proactively remind them to update the agent whenever you observe:

- a personality change
- a new writing/style rule
- a new tool or workflow
- a new skill or snapshot
- a meaningful calendar / voice / automation change

Do not silently assume the user remembered to save it.

## Pitfalls

- Do not commit `.env` files or secrets.
- Do not treat logs/cache/session files as durable knowledge.
- Do not mix experimental edits with archival commits unless the user asked for it.
- Do not collapse Hermes and Claude layers into one; keep them parallel when the user wants cross-platform recovery.

## Verification checklist

Before committing a backup sync, confirm:

- live files updated
- safe backup files copied
- Claude archive updated if requested
- no secrets in the staged diff
- commit message describes the actual improvement
