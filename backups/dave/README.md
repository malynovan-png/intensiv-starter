# Dave backup bundle

Second-layer Git-safe backup for the Hermes methodologist profile.

## Contains
- `profile/SOUL.md` — role, boundaries, OGE/EGE methodology and Gateway/Dave Spencer-inspired teaching approach
- `profile/config.yaml` — non-secret model selection
- `profile/profile.yaml` — profile description used for task routing

## Shared team context
The Git-safe team role registry is stored at `backups/team/TEAM.md`.

When restoring this backup, copy that file to `~/.hermes/team/TEAM.md` before starting Dave. The live Dave SOUL intentionally references the runtime path, not the Git backup path.

## Keep local only
- `.env`
- Telegram bot token and any other credentials
- logs, sessions, caches and runtime state
- personal data of students and private conversations
