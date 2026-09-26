---
name: voice-stt-troubleshooting
description: "Use when voice messages fail to transcribe. Diagnose STT."
version: 1.0.1
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [voice, stt, transcription, troubleshooting, telegram, groq]
---

# Voice STT Troubleshooting

Use when voice messages fail to transcribe. Diagnose STT.

## When to Use

Use this when a bot or agent receives voice messages but replies with a transcription failure, a generic "could not be transcribed", or stays silent after a voice note.

## Quick triage

1. Read the gateway or app logs for the exact STT error.
2. Classify the failure:
   - `No STT provider available` → nothing usable is installed or configured.
   - `401 Invalid API Key` / auth error → the provider key is wrong, revoked, or from the wrong service.
   - decode / ffmpeg / media errors → the audio pipeline is broken before STT.
3. Fix the smallest missing piece, then restart the gateway or service from a separate shell.
4. Re-test with a fresh voice message.

## Hermes-specific checks

- `stt.enabled` must be true.
- `stt.provider` must point to a real provider or local STT path.
- If Russian voice is transcribed in English, check `stt.language` as well; Hermes will happily transcribe with the wrong language hint if it is left on `en`.
- For Hermes, voice credentials belong in `~/.hermes/.env` unless the platform docs say otherwise.
- If voice still fails after editing env/config, restart the gateway; changes do not apply mid-session.
- If the gateway refuses to restart from inside the live Hermes session, use a separate SSH shell or service manager session.
- If `faster_whisper` is missing but `ffmpeg` is present, install `faster-whisper` into the Hermes Python environment with `uv pip install faster-whisper --python /usr/local/lib/hermes-agent/venv/bin/python` and restart before re-testing.

## Decision tree

### 1) `No STT provider available`

This means Hermes could not find any usable transcription backend.

Check, in this order:
- Is STT enabled in config?
- Is a provider selected?
- Is a local backend installed and importable?
- If using API STT, is the correct API key present in the active Hermes env file?

Prefer local `faster-whisper` when you want a free, self-contained path.

### 2) `401 Invalid API Key`

This means the provider was found, but rejected the credential.

Check:
- the key belongs to the right service
- the key was copied fully and has no whitespace
- the key has not been revoked
- the active service was restarted after changing the key

### 3) Local faster-whisper path

If `faster_whisper` is missing but `ffmpeg` is present, install the package into the Hermes Python environment and restart the gateway from a separate shell. This is the simplest free fallback when API STT keeps failing.

## Verification

After the fix:
- send a new voice message
- confirm it is transcribed to text
- confirm the bot responds to the transcribed text, not to the audio attachment itself

## Reference

See `references/voice-stt-diagnostics.md` for a compact field guide with the patterns seen in Hermes Telegram voice setups.
