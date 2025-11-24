# Quick Start for PythonAnywhere

Copy and paste these commands into your PythonAnywhere Bash console to set up the bot in ~3 minutes.

```bash
# 1. Clone the repo (or cd to it if already uploaded)
cd ~
git clone https://github.com/anaasamoah/Asamflixbot.git
cd Asamflixbot

# 2. Create and activate a virtual environment
mkvirtualenv --python=/usr/bin/python3.11 asamflixbot
workon asamflixbot

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up .env with your token
cp .env.example .env
# Edit .env with nano or your editor and add your TELEGRAM_BOT_TOKEN
nano .env

# 5. Test the bot locally (optional, Ctrl+C to stop)
# python main.py

# 6. Create the always-on task (see PYTHONANYWHERE_SETUP.md for details)
# Go to Dashboard → Always on → Create new task
# Command: /home/yourusername/.virtualenvs/asamflixbot/bin/python /home/yourusername/asamflixbot/main.py

# Done! Start the task in the Dashboard and test in Telegram.
```

For detailed instructions, see `PYTHONANYWHERE_SETUP.md`.
