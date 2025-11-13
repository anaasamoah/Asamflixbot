import json
import os
import asyncio
from telegram import Bot

MOVIE_FILES = "movie_files.json"
REPORT_FILE = "file_validation_report.json"

# Load token from main.py by importing; if import fails, ask user to set TOKEN env variable
TOKEN = None
try:
    from main import TOKEN
except Exception:
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("Telegram token not found. Set TELEGRAM_BOT_TOKEN or ensure main.py defines TOKEN.")
    raise SystemExit(1)

async def validate():
    bot = Bot(TOKEN)
    if not os.path.exists(MOVIE_FILES):
        print(f"{MOVIE_FILES} not found.")
        return
    with open(MOVIE_FILES, 'r', encoding='utf-8') as f:
        movies = json.load(f)
    invalid = []
    checked = 0
    for title, info in movies.items():
        file_id = info.get('file_id')
        if not file_id:
            invalid.append({'title': title, 'reason': 'missing file_id'})
            continue
        checked += 1
        try:
            await bot.get_file(file_id)
        except Exception as e:
            invalid.append({'title': title, 'reason': str(e)})
    report = {
        'checked': checked,
        'invalid_count': len(invalid),
        'invalid': invalid
    }
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Validation complete. Checked {checked}. Invalid: {len(invalid)}. Report: {REPORT_FILE}")

if __name__ == '__main__':
    asyncio.run(validate())
