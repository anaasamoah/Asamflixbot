<#
Remove the AsamflixBot Windows service.

Usage (run as Administrator):
  Set-Location "F:\Programming files\project work\Asamflixbot"
  .\uninstall_windows_service.ps1
#>

Set-StrictMode -Version Latest

Write-Host "Stopping and deleting service 'AsamflixBot' (if present)"
try {
    sc.exe stop AsamflixBot | Out-Null
} catch { }
Start-Sleep -Seconds 1
try {
    sc.exe delete AsamflixBot | Out-Null
    Write-Host "Service deleted (or did not exist)."
} catch {
    Write-Error "Failed to delete service. You may need to run this script as Administrator."
}
