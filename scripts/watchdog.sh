#!/usr/bin/env bash
# Сторожок для agent-intensiv-starter.service.
#
# Systemd (Type=forking) запоминает PID tmux-сервера при старте, но не следит
# за ним постоянно — если tmux-сессия падает сама по себе, служба формально
# остаётся "active", а бот молчит, пока кто-то не перезапустит вручную.
#
# Этого мало: 18 августа 2026 сервис пережил ~6-часовое зависание, где tmux-
# сессия была жива (has-session отвечал "да"), а бот внутри так и не поднялся
# после перезапуска — ни одного сообщения, ни одного лога. Формально всё
# "работало", по факту — тишина. Поэтому здесь два уровня проверки:
#
#   1. tmux-сессия вообще есть?            (ловит явный краш)
#   2. процесс из state/telegram/bot.pid жив?  (ловит зависание внутри сессии)
#
# bot.pid пишет сам поллер прямо перед стартом long-polling (см.
# src/telegram/poller.ts) — это PID процесса, который реально общается с
# Telegram. Если tmux-сессия жива, а этот PID не отвечает (или файла ещё
# нет) дольше STALL_GRACE секунд — считаем сессию "зомби" и перезапускаем.
#
# STALL_GRACE даёт свежему старту время подняться (bun ставится не мгновенно),
# чтобы не перезапускать сервис по кругу на каждом ровном месте.
#
# Этот скрипт запускается раз в минуту через cron.
set -euo pipefail

SESSION="agent-intensiv-starter"
LOG="/root/intensiv-starter/scripts/watchdog.log"
NOTIFY="/root/intensiv-starter/scripts/reminders/send-telegram.sh"
CHAT_ID="936853282"
PID_FILE="/root/intensiv-starter/dashi-plugin-claude-code/plugin/state/telegram/bot.pid"
STALL_STAMP="/root/intensiv-starter/scripts/watchdog.stall-since"
STALL_GRACE=180

ts() { date '+%Y-%m-%d %H:%M:%S %Z'; }

restart_and_notify() {
  local reason="$1"
  local msg="$2"
  echo "[$(ts)] $reason — перезапускаю $SESSION.service" >> "$LOG"
  systemctl restart "${SESSION}.service" >> "$LOG" 2>&1
  rm -f "$STALL_STAMP"
  "$NOTIFY" "$CHAT_ID" "$msg" || true
}

# 1. tmux-сессии нет вообще — явный краш, перезапускаем сразу (как раньше).
if ! tmux -L "$SESSION" has-session -t "$SESSION" 2>/dev/null; then
  restart_and_notify "tmux-сессия не найдена" \
    "⚠️ Сторожок заметил, что я упала (tmux-сессия исчезла), и перезапустила меня. Простой — не больше минуты (сработало в $(ts))."
  exit 0
fi

# 2. tmux-сессия есть — проверяем, что бот внутри неё реально жив (а не завис).
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE" 2>/dev/null || echo 0)" 2>/dev/null; then
  rm -f "$STALL_STAMP"
  exit 0
fi

# Бот не отвечает. Даём свежему старту время подняться, прежде чем бить тревогу.
NOW="$(date +%s)"
if [ ! -f "$STALL_STAMP" ]; then
  echo "$NOW" > "$STALL_STAMP"
  exit 0
fi
SINCE="$(cat "$STALL_STAMP")"
if [ "$(( NOW - SINCE ))" -lt "$STALL_GRACE" ]; then
  exit 0
fi

restart_and_notify "бот завис (tmux жива, но не отвечает Telegram уже дольше ${STALL_GRACE}с)" \
  "⚠️ Сторожок заметил, что я зависла (tmux была жива, но бот внутри не отвечал больше ${STALL_GRACE}с), и перезапустила меня. Простой мог быть дольше минуты — сработало в $(ts)."
