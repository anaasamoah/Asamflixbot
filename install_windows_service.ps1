<#
Install the Asamflix bot as a Windows Service.

Notes:
- Requires Administrator privileges to create a Windows service.
- The service will run PowerShell which executes the repository's `start_bot.ps1` script.
- Ensure `.env` exists in the repo root with `TELEGRAM_BOT_TOKEN` or the script will prompt.

Usage (run as Administrator):
  Set-Location "F:\Programming files\project work\Asamflixbot"
  .\install_windows_service.ps1

If the service fails to start, open Services.msc to inspect the error or run
`Get-Service -Name AsamflixBot | Select-Object *` and check the event log.
#>

Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$startScript = Join-Path $projectRoot 'start_bot.ps1'

if (-not (Test-Path $startScript)) {
    Write-Error "start_bot.ps1 not found at $startScript. Make sure you're running this from the repo root."
    exit 1
}

$powershellPath = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$binPath = "`"$powershellPath`" -NoProfile -ExecutionPolicy Bypass -File `"$startScript`""

Write-Host "Creating Windows service 'AsamflixBot' pointing to: $binPath"

# Create the service (if exists, delete first)
try {
    sc.exe query AsamflixBot > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Service 'AsamflixBot' already exists. Deleting it first..."
        sc.exe delete AsamflixBot | Out-Null
        Start-Sleep -Seconds 1
    }
} catch {
    # continue
}

Write-Host "Creating service using sc.exe"
# sc.exe requires the binPath value to follow immediately after the '=' and the executable path must be quoted.
$escapedBinPath = $binPath -replace '"', '"'  # keep as-is; we'll wrap in quotes below
$createArgs = "create AsamflixBot binPath=\"$escapedBinPath\" start= auto DisplayName=\"Asamflix Bot\""
Write-Host "sc.exe $createArgs"
sc.exe $createArgs

Write-Host "Attempting to start service 'AsamflixBot'..."
sc.exe start AsamflixBot

Write-Host "Done. If the service failed to start you may need to run this script as Administrator or check the Event Viewer for details."
