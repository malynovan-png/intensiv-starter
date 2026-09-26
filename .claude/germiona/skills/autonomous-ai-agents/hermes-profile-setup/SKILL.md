---
name: hermes-profile-setup
description: "Use when restoring a Hermes profile agent."
---

# Hermes profile setup and restoration

Use this when a user wants to create a new Hermes agent profile, restore an old persona, or move an assistant from another stack onto Hermes.

## Workflow

1. **Find the source of truth first**
   - Look for an existing project repo, personality file, memory files, and bot secrets.
   - Common artifacts: `CLAUDE.md`, `SOUL.md`, `USER.md`, `core/memory/`, `secrets/channel.env`, git remotes.
   - If the old assistant lived on a server, inspect that repo before recreating anything from scratch.

2. **Create or inspect a Hermes profile**
   - Create a dedicated profile when the assistant should be isolated from the main one:
     - `hermes profile create NAME`
   - Inspect it:
     - `hermes profile show NAME`
   - The profile layout lives under `~/.hermes/profiles/NAME/`.
   - The profile wrapper is usually created automatically as a command named after the profile.

3. **Put personality in the profile SOUL**
   - Edit `~/.hermes/profiles/NAME/SOUL.md` for the agent’s identity, tone, boundaries, and role.
   - Keep it short, direct, and role-based.
   - Use `SOUL.md` for the agent’s own identity; keep project-specific rules elsewhere.

4. **Keep project context separate**
   - Use the project repo for context files like `CLAUDE.md`, `AGENTS.md`, `.hermes.md`, `USER.md`, and memory notes.
   - Do not merge all project rules into the global identity file.

5. **Run setup one screen at a time**
   - Start the profile wizard:
     - `NAME setup`
   - Prefer **Full setup** when the user supplies their own keys.
   - Drive the wizard incrementally: one question, one answer, verify the next screen before continuing.
   - Common choices in a Hermes profile setup:
     - Provider: OpenRouter or the user’s chosen provider
     - Model: a balanced default unless the user wants cheap or strongest
     - Terminal backend: keep `local` unless the user explicitly needs remote execution
     - Telegram: configure the messaging platform if the agent should live in Telegram

6. **Telegram bot setup**
   - If the wizard asks how to create the bot, choose the manual path when the user already has a BotFather token.
   - Keep the bot token in the profile `.env`, not in the chat.
   - Add `EnvironmentFile=<profile>/.env` to the systemd unit if the profile should read env directly.
   - After setup, verify with `NAME gateway status` and a test message.
   - If Telegram responds with `httpx.ReadError`, inspect the live journal during a real message before changing anything else.
   - If the profile keeps colliding with the shared kanban dispatcher lock and must operate independently, give it its own `HERMES_KANBAN_HOME` root.
   - If the gateway says `No LLM provider configured`, confirm the unit loads the profile env and any global provider env before assuming the model is broken.

### Adding or updating a local skill in a live Telegram profile

1. Save the skill under `$HERMES_HOME/skills/<skill-slug>/SKILL.md` with a valid lowercase slug in frontmatter.
2. Verify discovery in a fresh profile process: `HERMES_HOME=<profile-home> hermes skills list` must show the skill as `local / enabled`.
3. Exercise one decisive rule with `HERMES_HOME=<profile-home> hermes chat -s <skill-slug> -q "..."`; do not rely on file presence alone.
4. Restart the profile gateway from a separate shell, then send `/new` to the Telegram bot before testing it. A gateway restart does not erase a persisted chat session, and that session can retain its previous skill catalog.
5. Ask the fresh Telegram session to list its skills or apply a decisive rule. Only report activation after this real-path check.

## Fast rebuild fallback
- When a profile has accumulated multiple fixes, env edits, and lock workarounds, it is often faster to clone a clean profile from the last known-good one than to keep patching the broken instance.
- The rebuild should keep the last known-good persona and replace only the mechanics: profile name, bot token, webhook port, env loading, and kanban root.
- See `references/telegram-gateway-rebuild.md` for the minimal rebuild recipe and lock/env pitfalls.

7. **Voice / STT setup**
   - If voice messages are not transcribing:
     - check `stt.enabled`
     - check `stt.provider`
     - ensure the selected provider key exists in the profile `.env`
   - Hermes can use local faster-whisper or a cloud STT provider.
   - If Groq fails with invalid key, either refresh the key or switch to local STT.
   - For local STT, install `faster-whisper` into the Hermes runtime and restart the gateway from a separate shell.

8. **Verify after every meaningful step**
   - Confirm profile state with `NAME profile show NAME`.
   - Confirm gateway health with `NAME gateway status`.
   - Read logs when behavior does not match expectations.
   - Test the real path: send a Telegram message or voice note and check the agent’s reply.

## Pitfalls

- Do not assume the wizard wrote the key if the next step still reports authentication errors.
- Do not edit secrets in the chat; use the profile `.env` file or the wizard.
- Do not guess which model/provider is active—read the current screen or config.
- If a restart command is blocked from the current shell because the gateway is the process executing it, rerun the restart from a separate SSH/session shell.
- If the user wants an existing persona restored, preserve the old personality language and only adapt the mechanics to Hermes.

## Verification

- `hermes profile show NAME` shows the profile path, `SOUL.md`, `.env`, and gateway state.
- `NAME gateway status` shows the service running.
- A Telegram text or voice message produces the expected reply.

## Related reference

See `references/profile-restoration-notes.md` for a concrete recovery flow and voice/STT troubleshooting notes.
