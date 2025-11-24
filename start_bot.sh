#!/usr/bin/env bash
# start_bot.sh - activate venv and run the bot, writing logs to bot.log
set -euo pipefail

# move to repo root (script expected to live in project root)
cd "$(dirname "$0")"

if [ -d ".venv" ]; then
  # use local venv if present
  source .venv/bin/activate
fi

# If an environment file exists, load it (do not commit .env to git)
if [ -f .env ]; then
  # shellcheck disable=SC1091
  set -a
  # shellcheck disable=SC1090
  . .env
  set +a
fi

echo "Starting Asamflixbot... (logs: bot.log)"
exec python main.py >> bot.log 2>&1
