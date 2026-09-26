---
name: hermes-voice-stt
description: "Use when setting up Hermes voice/STT in Telegram."
category: autonomous-ai-agents
---

# Hermes Voice/STT Setup

Use this skill when the user wants Hermes to understand voice messages in Telegram or similar messaging gateways.

## What this covers
- STT setup for Hermes messaging gateways.
- Groq-based speech recognition.
- The Hermes config/env files that actually matter.
- Restart + verification steps.

## Style for this workflow
- Be concise, step-by-step.
- For this user, mirror their mixed Russian/English style when explaining setup.
- Do not bury the key path or the restart step.

## Canonical workflow

1. **Confirm the active Hermes home**
   - Use `hermes config env-path`.
   - For Hermes, the env file is usually `~/.hermes/.env` (or the profile-specific `$HERMES_HOME/.env`).
   - Do not send users to `secrets/channel.env` for Hermes voice/STT setup.

2. **Set STT on the Hermes config**
   - Enable STT:
     - `hermes config set stt.enabled true`
   - Select a provider:
     - `hermes config set stt.provider groq`
   - Verify with:
     - `hermes config get stt.enabled`
     - `hermes config get stt.provider`

3. **Add the Groq key to Hermes env**
   - Put the API key in `~/.hermes/.env`:
     - `GROQ_API_KEY=...`
   - If the key already exists, leave it in place and verify the file path.
   - Never repeat the secret back to the user.

4. **Restart the gateway so changes take effect**
   - If Hermes runs as a gateway/service, restart it.
   - In the gateway chat, `/restart` is the usual user-facing action.
   - After config changes, do not assume the new provider is live until the restart is done.

5. **Use the voice commands**
   - `/voice on` — voice-to-voice / voice messages enabled.
   - `/voice tts` — always reply with voice.
   - `/voice off` — text only.
   - `/voice status` — show current voice mode.

6. **Verify the result**
   - Send a short voice message in Telegram.
   - Hermes should transcribe it into text and answer.
   - If it does not work, re-check `stt.enabled`, the provider, the env file path, and the restart.

## Pitfalls
- The wrong env file is the most common mistake: Hermes uses its own `HERMES_HOME`-scoped `.env`.
- A saved config value is not enough; the gateway usually needs a restart.
- Do not instruct the user to paste secrets into chat.
- Keep the explanation short and practical; this workflow is operational, not theoretical.

## Quick command bundle
```bash
hermes config env-path
hermes config set stt.enabled true
hermes config set stt.provider groq
hermes config get stt.enabled
hermes config get stt.provider
```

## Related notes
- The authoritative docs live in the Hermes documentation.
- If the user asks for the broader Hermes configuration story, pair this skill with the main `hermes-agent` skill and the configuration docs.
