<#
PowerShell helper to start the bot using the workspace venv.
It will read environment variables from a local `.env` file if present,
or prompt for the TELEGRAM_BOT_TOKEN if it's missing.

Usage:
  - Double-click in Explorer or run from PowerShell:
      .\start_bot.ps1
  - The script runs the project venv Python directly, it does not activate the shell.
#>

Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$envFile = Join-Path $projectRoot '.env'

if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^[\s#]*$') { return }
        if ($_ -match '^[\s#]*([^=\s]+)\s*=\s*(.*)$') {
            $name = $matches[1]
            $value = $matches[2].Trim()
            # remove surrounding quotes if any
            if ($value.StartsWith('"') -and $value.EndsWith('"')) { $value = $value.Trim('"') }
            if ($value.StartsWith("'") -and $value.EndsWith("'")) { $value = $value.Trim("'") }
            $env:$name = $value
        }
    }
}

if (-not $env:TELEGRAM_BOT_TOKEN) {
    Write-Host "TELEGRAM_BOT_TOKEN not found in environment or .env."
    $secure = Read-Host -Prompt 'Enter TELEGRAM_BOT_TOKEN (input hidden)' -AsSecureString
    if ($secure.Length -eq 0) {
        Write-Host "No token provided. Aborting." -ForegroundColor Red
        exit 1
    }
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try { $plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
    $env:TELEGRAM_BOT_TOKEN = $plain
}

# prefer the workspace venv python if present
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (Test-Path $venvPython) {
    $pythonExe = $venvPython
} else {
    Write-Host ".venv python not found, falling back to system python in PATH." -ForegroundColor Yellow
    $pythonExe = 'python'
}

Write-Host "Using Python: $pythonExe"
Write-Host "Starting bot (press Ctrl+C to stop)..."

& $pythonExe (Join-Path $projectRoot 'main.py')
