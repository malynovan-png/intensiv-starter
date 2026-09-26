---
name: hermes-profile-restoration
description: "Use when restoring a Hermes profile agent."
---

# Hermes Profile Restoration

Use when an old assistant already has files on disk or in git and you need to rebuild it as a Hermes profile.

## Goal
Restore a separate Hermes profile from an existing assistant repository, preserving identity, owner preferences, and live gateway behavior.

## Steps
1. **Find the source repo first.**
   - Look for identity files like `CLAUDE.md`, `SOUL.md`, `core/USER.md`, `core/memory/*`, and any bot/config files.
   - Verify whether the repo is actually a git repo and whether it has a remote.

2. **Extract the durable pieces.**
   - Owner preferences: name, tone, language mix, fixed schedule, safety boundaries.
   - Assistant identity: name, role, character, response style, hard limits.
   - Active project context: memory notes, task lists, special workflows.

3. **Create a separate Hermes profile.**
   - Use `hermes profile create <name>` for the restored assistant.
   - Keep the current profile intact; do not overwrite the main assistant profile.

4. **Replace the profile personality.**
   - Edit the profile's `SOUL.md` to reflect the restored assistant identity.
   - Keep it short, direct, and role-focused.

5. **Run the profile setup wizard.**
   - Use the profile-specific wrapper (for example `owla setup`).
   - Prefer `Full setup` when you need explicit keys and manual control.
   - Keep terminal backend local unless there is a clear reason to change it.

6. **Choose the brain deliberately.**
   - Use OpenRouter when you want one key for many models.
   - Pick a balanced default model for an assistant/coder profile.
   - Avoid leaving the profile without a valid provider/key pair.
   - For an existing profile, change settings through its isolated home rather than the default profile:
     ```bash
     profile_home="$HOME/.hermes/profiles/<profile>"
     HERMES_HOME="$profile_home" hermes config set model.provider <provider>
     HERMES_HOME="$profile_home" hermes config set model.default <model>
     HERMES_HOME="$profile_home" hermes auth status <provider>
     HERMES_HOME="$profile_home" hermes chat -q 'Reply with exactly: PROFILE_OK'
     ```
   - Back up `config.yaml` before changing an important model configuration, then confirm both effective keys and a real one-shot request. Do not declare Telegram updated until its profile gateway has reloaded the configuration.

7. **Connect Telegram manually when needed.
   - Use a real BotFather token, not an app password or unrelated API key.
   - Verify the token format before assuming the wizard is wrong.

8. **Verify the profile and gateway.**
   - Check the profile with `hermes profile show <name>`.
   - Check service health with `hermes gateway status`.
   - Test with a simple Telegram message before declaring success.

## Common pitfalls
- Do not treat the main `SOUL.md` as the place to restore a separate assistant if a dedicated profile is appropriate.
- Do not confuse OpenRouter keys, Groq keys, Telegram bot tokens, and app-specific passwords.
- If the gateway is already running under systemd, restart it from a separate shell rather than trying to relaunch it inside the same live process.
- If the wrapper command is missing in a shell, check the active profile context or open a fresh shell before assuming the profile failed.

## Verification
- `hermes profile show <name>` reports the profile path, SOUL, env file, and gateway state.
- `hermes gateway status` shows the service is running.
- Telegram replies arrive from the restored profile with the expected identity and tone.

## See also
- `references/profile-recovery.md` — practical recovery notes and a reusable checklist.
