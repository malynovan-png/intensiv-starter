---
name: hermes-profile-recovery
description: Use when restoring old assistants onto Hermes.
---

# Hermes Profile Recovery

Use when the user wants to bring back an old Claude-era assistant, clone it into Hermes, or split one working agent into separate Hermes profiles.

## When to Use
- The user wants to bring back an old Claude-era assistant.
- The user wants to clone or split an existing assistant into a separate Hermes profile.
- The user has an old repo with persona files, memory notes, or a Telegram bot to recover.

## Core workflow
1. Inspect the old project/repo first and recover the source persona files.
2. Extract identity and user-preference facts from the project files, especially `CLAUDE.md`, `SOUL.md`, `core/USER.md`, and any memory notes.
3. Create a separate Hermes profile for the restored agent:
   - `hermes profile create <name>`
4. Replace the profile identity file:
   - `~/.hermes/profiles/<name>/SOUL.md`
5. Run the profile setup wizard:
   - `<name> setup`
6. Choose **Full setup** when the user brings their own keys.
7. Keep terminal backend on **local** unless the user explicitly needs another backend.
8. Select the intended provider and model, then configure Telegram manually when a BotFather token already exists.
9. Verify the profile and gateway before declaring success:
   - `<name> profile show <name>`
   - `<name> gateway status`

## Voice / STT pattern
- For Telegram voice, prefer `stt.enabled: true` plus a local STT fallback when possible.
- If voice fails, distinguish between:
  - no STT provider installed/configured
  - a provider key present but rejected by the provider
- A useful fallback is `faster-whisper` in the Hermes runtime, followed by a gateway restart from a separate shell.
- If the gateway restart is attempted from inside the same running gateway context, Hermes may block it. Use a separate SSH/session shell.

## Common pitfalls
- Do not assume a repo commit means the files were pushed; verify the remote and commit range.
- Do not confuse the OpenRouter key, the BotFather token, and unrelated app-specific passwords.
- If the profile wrapper command is not behaving in the current shell, use the full path or a fresh shell.
- Keep the restored agent in a separate Hermes profile instead of overwriting the current working agent.

## Verify
- `hermes profile show <name>`
- `<name> gateway status`
- Telegram test message
- Voice test message after STT changes

## Notes
- Session-specific recovery details and example logs live in `references/profile-restoration-notes.md`.
