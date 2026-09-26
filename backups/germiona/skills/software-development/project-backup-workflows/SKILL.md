---
name: project-backup-workflows
description: "Use when keeping local and GitHub snapshots in sync."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [git, github, backup, snapshot, secrets, workflow, profile, restore]
    related_skills: [github-repo-management, github-auth, github-pr-workflow]
---

# Project Backup Workflows

Use this skill when a user wants to preserve an agent, profile, or project in **two layers**:

1. a **local live copy** that keeps secrets and runtime state
2. a **GitHub-safe snapshot** that stores only durable, non-secret artifacts

## Core rule

Keep the running system local. Commit only what is safe to share.

### Local live layer
Store here:
- `.env` files
- tokens
- app-specific passwords
- runtime locks/markers
- live gateway/session state
- machine-specific temporary files

### GitHub snapshot layer
Store here:
- personalities / SOUL files
- user preference files
- style guides
- skills
- safe scripts and tools
- calendar or other tools that do not contain secrets
- README files documenting the snapshot structure

## Workflow

1. Inventory the working set.
2. Scrub secrets before staging.
3. Stage only durable artifacts.
4. Commit with a clear snapshot message.
5. Push only after verifying auth.

## Commit this

- profile personality files
- safe config snapshots without secrets
- reusable scripts/tools
- style guides and prompt guides
- safe skill snapshots

## Keep local only

- `.env` files
- bot tokens
- API keys
- Apple app-specific passwords
- runtime markers like `*.lock`, `*.pid`, `*.sock`, `*.stall-since`
- logs unless the user explicitly wants them archived
- hidden local-only project metadata such as `.claude/` unless the user explicitly wants to archive the old Claude-side layer

## Pitfalls

- Do not commit live credentials.
- Do not mix runtime junk into the snapshot.
- Do not assume every local project folder should be tracked.
- If the user wants a two-layer backup, keep the layers intentionally different.
- `scripts/watchdog.stall-since` is runtime state, not durable project knowledge.

## Verification

Before telling the user the backup is ready:

- snapshot files are present
- secrets were excluded
- `git status` contains only the intended files
- the commit message describes the snapshot
- the push completed successfully

## Support file

See `references/backup-policy.md` for the Owla-specific backup split and file list.