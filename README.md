# Asamflix Bot

This repository contains the Asamflix Telegram bot code.

Important: do NOT commit your bot token or other secrets. Use environment variables (see `.env.example`).

Setup (local / PythonAnywhere)

1. Create a virtual environment and install dependencies

```powershell
# Windows / PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On PythonAnywhere, use the Bash console and `python3.x -m venv ~/venvs/asamflixenv` then `source ~/venvs/asamflixenv/bin/activate`.

2. Provide your bot token via environment variable

Create a `.env` file (copy `.env.example`) or set the environment variable in your hosting provider.

Example `.env` (DO NOT COMMIT):

```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF
#ADMIN_IDS=8221911290,7235130481
```

3. Run the bot

```powershell
# from repo root
python main.py
```

4. Validate stored file IDs

Use the admin command `/validate_files` from the bot (as an admin) or run `python validate_files.py` in the project directory.

Hosting on GitHub (quick steps from PowerShell)

1. Initialize git and commit

```powershell
cd "E:\Programming files\project work\Asamflixbot"
git init
git add .
git commit -m "Initial commit: asamflix bot"
```

2. Create a GitHub repository (via web UI) and then add the remote and push

```powershell
# replace <username> and <repo> with your values
git remote add origin https://github.com/<username>/<repo>.git
git branch -M main
git push -u origin main
```

Security and best practices

- Remove any hard-coded tokens and use `TELEGRAM_BOT_TOKEN` env var (this repo already requires that).
- Keep `movie_files.json` and other generated data out of the repo (they are listed in `.gitignore`).
- If you need to share `movie_files.json` across hosting environments, use a private storage or database.

PythonAnywhere deployment notes

- Upload or `git clone` the repo into your PythonAnywhere project directory.
- Create and activate a virtualenv matching your Python version, install requirements.
- Set `TELEGRAM_BOT_TOKEN` in the PythonAnywhere web UI (or use `.env` carefully).
- Start the bot via an Always-on task or run `python main.py` in a console and use their task scheduler.

If you'd like, I can:
- create a GitHub Actions workflow to run lint/tests (simple), or
- prepare a one-click setup script that initializes the repo and pushes to GitHub from your machine.

Developing with GitHub Codespaces / Devcontainers
------------------------------------------------

This repository includes a `.devcontainer/devcontainer.json` so you can open it in GitHub Codespaces or as a local devcontainer in VS Code.

Recommended flow in Codespaces:

1. Open the repo in GitHub Codespaces (or in VS Code use "Remote-Containers: Open Folder in Container").
2. The container image provides Python 3.11 and the configured VS Code extensions. After creation the container runs `pip install -r requirements.txt`.
3. Provide secrets (do NOT commit `.env`): in GitHub Codespaces you can add repository secrets via the Codespaces settings and map them to ENV in the Codespaces UI. Alternatively, create a local `.env` inside the container (it will not be pushed if `.gitignore` contains `.env`).

Secure token handling:

- Use Codespaces secrets or GitHub repository secrets when possible. Avoid writing your real token into the git-tracked files.
- Locally, copy `.env.example` to `.env` and fill in `TELEGRAM_BOT_TOKEN=...`.

Running the bot inside Codespaces

```bash
# inside the Codespace (or container):
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# create .env from example and edit
cp .env.example .env || true
# put your token into .env (or export TELEGRAM_BOT_TOKEN in the terminal)
./start_bot.sh
```

If you'd like, I can also:
- add a small GitHub Actions workflow to run lint/tests on PRs,
- or create a Codespaces devcontainer feature that injects a masked startup log showing that a token was found.

Windows service
----------------

If you want the bot to run continuously on Windows, there are helper scripts included:

- `install_windows_service.ps1` — create and start a Windows Service named `AsamflixBot` (run as Administrator).
- `uninstall_windows_service.ps1` — remove the service.

Usage (Administrator PowerShell):

```powershell
Set-Location "F:\Programming files\project work\Asamflixbot"
# make sure .env contains TELEGRAM_BOT_TOKEN or you'll be prompted
.\install_windows_service.ps1
```

If the service fails to start, check the Windows Event Viewer and the service properties. The service runs `start_bot.ps1` which reads `.env` in the repository root.

PythonAnywhere hosting
----------------------

PythonAnywhere is a simple, reliable option for running the bot 24/7 in the cloud (uses free or paid tier).

**Quick Setup (5 minutes)**

1. Create a free PythonAnywhere account at https://www.pythonanywhere.com
2. Log in and open the "Bash console" (or "$ Bash console" button).
3. Clone this repository (or upload the files):
   ```bash
   git clone https://github.com/<your-username>/asamflixbot.git
   cd asamflixbot
   ```
   (Or use the Web tab to upload files if not using git.)
4. Create a virtual environment and install dependencies:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 asamflixbot
   pip install -r requirements.txt
   ```
   (Adjust Python version if needed; check PythonAnywhere's available versions.)
5. Set your bot token in `.env`:
   ```bash
   cp .env.example .env
   # Edit .env with your token
   nano .env
   # Press Ctrl+X, then Y, then Enter to save
   ```
6. Go to the "Always on" tab (or "Scheduled tasks" if you have a free account) and create a new task:
   - Command: `/home/yourusername/.virtualenvs/asamflixbot/bin/python /home/yourusername/asamflixbot/main.py`
   - Adjust the path to your actual username and repo location.
7. Save and start the task. Check the task log to confirm it's running.

**To stop the bot:**
- Go to the "Always on" tab and click "Stop".

**To view logs:**
- In PythonAnywhere, go to the "Always on" or "Scheduled tasks" tab and click "View log".
- Logs are typically stored in the task's output file (e.g., `~/.asamflixbot.log` or shown inline).

**Notes:**
- Free tier accounts run tasks for limited hours (typically 1-2 hours/day); upgrade to a paid plan for 24/7 uptime.
- Make sure `.env` is in the repo root and contains `TELEGRAM_BOT_TOKEN`.
- If the task stops unexpectedly, check the log for errors and ensure your token is valid.
- To update the bot code, pull/upload new files and restart the task.
