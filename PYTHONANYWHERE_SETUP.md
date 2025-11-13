# PythonAnywhere Deployment Guide

This guide walks you through deploying the Asamflix Bot on PythonAnywhere for 24/7 hosting.

## Prerequisites

- A PythonAnywhere account (https://www.pythonanywhere.com) — free tier available.
- Your Telegram bot token (from `@BotFather` on Telegram).
- This repository (clone via git or upload files).

## Step-by-Step Setup

### 1. Create a PythonAnywhere Account

Visit https://www.pythonanywhere.com and sign up for a free account. You get:
- 1 always-on task (or limited scheduled tasks on free tier).
- 100 MB storage.
- Free SSL.

Upgrade anytime for more resources.

### 2. Open a Bash Console

Log in to PythonAnywhere → Dashboard → "$ Bash console" → Open.

### 3. Clone or Upload the Repository

**Option A: Clone via Git (recommended)**

```bash
cd ~
git clone https://github.com/<your-username>/asamflixbot.git
cd asamflixbot
```

(If the repo is private, you'll need SSH keys; see PythonAnywhere docs.)

**Option B: Upload Files via Web Interface**

1. Dashboard → "Files" tab.
2. Create a folder `asamflixbot`.
3. Upload all files from your local machine.

### 4. Create a Virtual Environment

In the Bash console, run:

```bash
mkvirtualenv --python=/usr/bin/python3.11 asamflixbot
```

(Check available Python versions with `ls /usr/bin/python*` if 3.11 is unavailable.)

Activate the venv:

```bash
workon asamflixbot
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `python-telegram-bot==20.4` and other required packages.

### 6. Set Up Environment Variables

Copy `.env.example` to `.env` and add your bot token:

```bash
cd ~/asamflixbot
cp .env.example .env
nano .env
```

Edit the file:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

Save: press `Ctrl+X`, then `Y`, then `Enter`.

### 7. Create an Always-On Task (or Scheduled Task)

**For Paid Accounts (Always-on):**

1. Dashboard → "Always on" tab.
2. Click "Create new always-on task".
3. Enter the command:
   ```
   /home/yourusername/.virtualenvs/asamflixbot/bin/python /home/yourusername/asamflixbot/main.py
   ```
   Replace `yourusername` with your PythonAnywhere username.
4. Click "Create".
5. Click the play button to start the task.

**For Free Accounts (Scheduled Tasks):**

1. Dashboard → "Scheduled tasks".
2. Click "Create new scheduled task".
3. Set the time to run (e.g., "00:00" for midnight).
4. Enter the command:
   ```
   /home/yourusername/.virtualenvs/asamflixbot/bin/python /home/yourusername/asamflixbot/main.py
   ```
5. Set "Repeats" to "Every 24 hours" (runs at that time daily, but only for ~1-2 hours on free tier).

For 24/7 uptime, upgrade to a paid plan.

### 8. Verify the Bot is Running

1. Dashboard → "Always on" or "Scheduled tasks" tab.
2. Click "View log" to see the latest output.
3. Expected output:
   ```
   Starting bot...
   polling...
   ```

If you see an error, check:
- `.env` exists and `TELEGRAM_BOT_TOKEN` is set.
- The token is valid (test in Telegram by messaging your bot).
- Dependencies installed successfully (run `pip list` to verify).

### 9. Test the Bot

Open Telegram and message your bot:

```
/start
/help
/movie avatar
```

If the bot responds, it's working!

## Managing the Bot

### Stop the Bot

Dashboard → "Always on" (or "Scheduled tasks") → Click the stop/pause button next to the task.

### View Logs

Dashboard → "Always on" → Click "View log".

### Update the Bot Code

1. Pull the latest changes:
   ```bash
   cd ~/asamflixbot
   git pull origin main
   ```
2. If dependencies changed:
   ```bash
   workon asamflixbot
   pip install -r requirements.txt
   ```
3. Restart the task:
   - Stop it, then start it again.

### Debugging

If the bot stops unexpectedly:

1. Check the log for errors.
2. Verify the token is valid.
3. Ensure you have storage available (`du -sh ~/asamflixbot`).
4. If using free tier, check that task hours haven't been exceeded.

## Costs

| Plan      | Always-On Tasks | Storage | Bandwidth | Cost     |
|-----------|-----------------|---------|-----------|----------|
| Free      | Up to 1hr/day   | 100 MB  | Limited   | Free     |
| Paid      | Unlimited       | 512 MB+ | Generous  | $5-9/mo  |

For a small bot, the free tier is enough; upgrade if you need 24/7 uptime.

## Troubleshooting

**Q: The task stops after 1-2 hours (free tier)**
- Upgrade to a paid plan for 24/7, or use a Scheduled Task that runs daily.

**Q: "Token rejected by server" error**
- Verify your token is correct. Test by sending it manually to Telegram API:
  ```bash
  curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
  ```

**Q: No response from bot in Telegram**
- Check the task is running (click "View log").
- Verify the bot token in `.env` matches the token you created with `@BotFather`.

**Q: Storage full**
- Free tier gets 100 MB. Check usage: `du -sh ~`
- Remove old logs or unused files, or upgrade.

**Q: Git clone fails (private repo)**
- Use SSH keys. PythonAnywhere docs: https://help.pythonanywhere.com/pages/UsingGitandMercurial

## Quick Commands

```bash
# View logs
tail -f ~/.asamflixbot.log

# Check bot process
ps aux | grep main.py

# Check disk usage
du -sh ~/asamflixbot

# Reinstall dependencies
workon asamflixbot && pip install --upgrade -r requirements.txt
```

## Next Steps

- Configure admin commands: `/admin`, `/delete`, `/stats` (see `main.py` for details).
- Set up a GitHub Actions workflow to auto-deploy on push (advanced).
- Monitor the bot's performance and uptime.

---

Questions? Check PythonAnywhere docs: https://help.pythonanywhere.com
