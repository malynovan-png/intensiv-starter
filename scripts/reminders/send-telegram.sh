#!/usr/bin/env bash
# Отправляет сообщение в Telegram напрямую через Bot API — не зависит от
# того, жив ли сейчас процесс агента (claude). Используется системным
# cron'ом для по-настоящему 24/7 напоминаний.
#
# Использование: send-telegram.sh <chat_id> <text>
set -euo pipefail

ENV_FILE="/root/intensiv-starter/secrets/channel.env"
CHAT_ID="${1:?usage: send-telegram.sh <chat_id> <text>}"
TEXT="${2:?usage: send-telegram.sh <chat_id> <text>}"

TOKEN="$(grep -E '^TELEGRAM_BOT_TOKEN=' "$ENV_FILE" | head -1 | cut -d= -f2-)"

curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  --data-urlencode text="${TEXT}" \
  > /dev/null
