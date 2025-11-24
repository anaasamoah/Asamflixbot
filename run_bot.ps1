Param(
    [string]$Token,
    [switch]$Tail
)

# Stops stray python processes, sets TELEGRAM_BOT_TOKEN optionally, then starts main.py
# Usage examples:
#   .\run_bot.ps1 -Token "123:ABC" -Tail
#   .\run_bot.ps1 -Tail
#   .\run_bot.ps1

# 1) Stop stray processes to avoid Telegram 'Conflict' errors
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process pythonw -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 2) Set token if provided
if ($Token) {
    $env:TELEGRAM_BOT_TOKEN = $Token
    Write-Host "TELEGRAM_BOT_TOKEN set for this session."
} else {
    if (-not $env:TELEGRAM_BOT_TOKEN) {
        Write-Host "No TELEGRAM_BOT_TOKEN set in env; you can pass -Token or set the variable before running." -ForegroundColor Yellow
    } else {
        Write-Host "Using existing TELEGRAM_BOT_TOKEN from environment."
    }
}

# 3) Determine Python executable (prefer venv .\.venv\Scripts\python.exe)
$venvPython = Join-Path -Path (Get-Location) -ChildPath ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonExe = $venvPython
    Write-Host "Using venv python: $pythonExe"
} else {
    $pythonExe = "python"
    Write-Host "Using system 'python' (no .venv found)."
}

# 4) Start the bot in a new process so we can tail logs in this window
$startInfo = @{ FilePath = $pythonExe; ArgumentList = '.\main.py'; WorkingDirectory = (Get-Location) }
try {
    $proc = Start-Process @startInfo -PassThru
    Write-Host "Started bot (PID $($proc.Id))."
} catch {
    Write-Host "Failed to start bot process: $_" -ForegroundColor Red
    exit 1
}

# 5) Optionally tail the bot.log in this window
if ($Tail) {
    # Wait briefly for log file to be created
    Start-Sleep -Seconds 1
    if (Test-Path .\bot.log) {
        Write-Host "Tailing .\bot.log (CTRL+C to stop)."
        Get-Content .\bot.log -Wait -Tail 200
    } else {
        Write-Host "Log file .\bot.log not found yet. Waiting..."
        while (-not (Test-Path .\bot.log)) { Start-Sleep -Milliseconds 200 }
        Write-Host "Tailing .\bot.log (CTRL+C to stop)."
        Get-Content .\bot.log -Wait -Tail 200
    }
} else {
    Write-Host "Run 'Get-Content .\bot.log -Wait -Tail 200' in another terminal to follow logs." -ForegroundColor Cyan
}
