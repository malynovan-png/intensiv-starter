#!/usr/bin/env bash
# Сторожок для agent-intensiv-starter.service.
#
# Systemd (Type=forking) запоминает PID tmux-сервера при старте, но не следит
# за ним постоянно — если tmux-сессия падает сама по себе, служба формально
# остаётся "active", а бот молчит, пока кто-то не перезапустит вручную.
#
# Этот скрипт запускается раз в минуту через cron: проверяет, жива ли
# tmux-сессия, и если нет — перезапускает сервис и присылает уведомление
# в Telegram, что был простой.
set -euo pipefail

SESSION="agent-intensiv-starter"
LOG="/root/intensiv-starter/scripts/watchdog.log"
NOTIFY="/root/intensiv-starter/scripts/reminders/send-telegram.sh"
CHAT_ID="936853282"

if tmux -L "$SESSION" has-session -t "$SESSION" 2>/dev/null; then
  exit 0
fi

TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "[$TS] tmux-сессия не найдена — перезапускаю $SESSION.service" >> "$LOG"

systemctl restart "${SESSION}.service" >> "$LOG" 2>&1

"$NOTIFY" "$CHAT_ID" "⚠️ Сторожок заметил, что я упала (tmux-сессия исчезла), и перезапустила меня. Простой — не больше минуты (сработало в $TS)." || true
