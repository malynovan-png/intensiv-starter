---
name: hermes-telegram-agent-setup
description: "Use when wiring a Hermes profile to Telegram."
version: 1.0.0
author: Hermes + Natalie
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, telegram, gateway, systemd, profile, env, allowlist]
    related_skills: [hermes-agent]
---

# Hermes Telegram Agent Setup

Use this skill when creating or fixing a Hermes profile that should answer in Telegram.

## When to Use

- A new Hermes profile needs its own Telegram bot.
- A profile is running but Telegram is silent.
- You need to connect a profile env file, systemd service, and bot allowlist.
- You need to clone an existing gateway service and switch it to a new profile.

## Core workflow
1. Create a separate profile directory for the agent.
2. Create a separate Telegram bot in BotFather.
3. Prepare a dedicated env file for that profile.
4. Ensure the service unit loads the profile env file with `EnvironmentFile=`.
5. Replace the profile name and paths in the systemd unit.
6. If a new or edited local skill was added, validate it before touching the live gateway: run an isolated profile query with `HERMES_HOME=~/.hermes/profiles/<profile> hermes chat -s <skill-slug> -q "<key rule>"` and confirm the expected rule is applied.
7. When the task scope authorizes a live reload, restart the gateway from a separate shell with `systemctl --user restart hermes-gateway-<profile>.service`.
8. Verify the same user-scope unit is active with `systemctl --user is-active hermes-gateway-<profile>.service`, then test the real Telegram path.

## Important rules
- One profile = one bot token = one webhook port.
- Do not reuse another agent's bot token or port.
- Do not run restart commands from inside the same live gateway process.
- If Telegram is silent but the service is running, suspect env loading or allowlist configuration first.
- If a bot token or secret appears in a terminal screenshot, treat it as exposed and rotate it.

## Required checks
- `systemctl --user status hermes-gateway-<profile>.service`
- `journalctl --user -u hermes-gateway-<profile>.service -n 80 --no-pager`
- confirm the unit has an `EnvironmentFile=` line for the profile `.env`
- confirm the profile `.env` has the expected bot ID, user allowlist, and webhook port

## Troubleshooting patterns
- If the gateway says allowlists are missing, the profile env is probably not loaded.
- If the profile env is loaded but Telegram is still silent, check the allowlist names used by the installed Hermes build and compare them to the service docs.
- If a restart command is blocked, use a separate shell or SSH session.

## Supporting file
- `references/telegram-agent-setup.md`
