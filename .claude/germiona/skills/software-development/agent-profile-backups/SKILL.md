---
name: agent-profile-backups
description: "Use when backing up agent profiles and committing them."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# Agent Profile Backups

Use this when you need a **two-layer backup** for a Hermes agent or any similar agent profile: one local working copy, one GitHub-safe backup copy.

## What this skill covers

- preserving an agent personality/profile
- snapshotting non-secret config and tool code
- creating a clean GitHub-ready backup tree
- committing changes regularly without leaking secrets

## Core workflow

1. **Separate secrets from everything else.**
   - Never commit `.env`, tokens, passwords, app-specific passwords, or any file containing secrets.
   - Keep secrets in the live runtime location only.

2. **Create a Git-friendly backup layer.**
   - Store the safe parts of the agent in a dedicated folder such as `backups/<agent>/`.
   - Include personality, style guides, non-secret config snapshots, tool code, and skill snapshots.

3. **Keep the working profile live.**
   - The running agent can keep using its live profile under `~/.hermes/...`.
   - The backup layer is for versioning and recovery, not for runtime secrets.

4. **Commit only the safe layer.**
   - Commit the backup folder, style guides, scripts, and skill text.
   - Exclude secrets by design.

5. **Verify before every commit.**
   - Run `git status --short`.
   - Search for accidental secrets (`grep -R`, `search_files`, or equivalent).
   - Confirm the backup tree contains only safe files.

## Practical layout

- `backups/<agent>/profile/` — `SOUL.md`, non-secret `config.yaml`, and `profile.yaml` routing metadata
- `backups/<agent>/style/` — writing/style guides
- `backups/<agent>/tools/` or `calendar/` — deterministic helper scripts
- `backups/<agent>/skills/` — skill snapshots or exports
- `backups/<agent>/README.md` — what this backup contains and what must stay out
- `backups/team/TEAM.md` — safe cross-agent role registry and handoff rules; never use it for private sessions or credentials

See `references/backup-layout.md` for the concrete Owla example used in this session.

## Pitfalls

- Do **not** treat the live profile as the backup. Live profile changes are easy to lose.
- Do **not** commit runtime caches, logs, or generated state unless they are explicitly meant to be part of the backup.
- Do **not** copy secrets into the backup tree “just for convenience”.
- Do **not** assume a working local copy is backed up until you verify the commit.

## Verification

Before telling the user the backup is ready:

- confirm the safe files exist in the backup folder
- confirm the repo sees them as tracked or staged
- confirm no secret files are staged
- confirm the backup README explains what is included and excluded
