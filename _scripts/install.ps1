# terminal-command Install Script (Windows)
# This script installs the 'tc' command on Windows by copying a small wrapper script (tc.cmd)
# into a directory that should be on the user's PATH.

param(
    [string]$InstallDir = "C:\\Windows\\System32"  # default location
)

Write-Host "Installing terminal-command (tc) on Windows..."

if (-not (Get-Command python | Out-Null)) {
    Write-Error "Error: Python is not found. Please install Python 3 and re-run this script."
    exit 1
}

$ScriptDir = Split-Path $MyInvocation.MyCommand.Definition -Parent
$ProjectRoot = Join-Path $ScriptDir ".."
Write-Host "ProjectRoot: $ProjectRoot"

# Generate the wc.cmd script
$WrapperScript = @"
@echo off
python "$ProjectRoot\src\main.py" %*
"@

# Create a temp file, set contents
$TempFile = [IO.Path]::GetTempFileName() + ".cmd"
Set-Content -Path $TempFile -Value $WrapperScript -Force
# Make it executable
# (On Windows, .cmd files don't usually need explicit chmod, but let's keep it consistent.)
# Copy to InstallDir
Copy-Item $TempFile -Destination (Join-Path $InstallDir "tc.cmd") -Force

Write-Host "Installation complete! 'tc' is now available in $InstallDir as tc.cmd."
Write-Host "Usage: tc \"list active docker containers\""

# Optionally remind user to ensure $InstallDir is in PATH
Write-Host "`nNote: Make sure $InstallDir is in your PATH environment variable."
