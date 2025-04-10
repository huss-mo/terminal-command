# terminal-command Install Script (Windows)
# This script installs the 'tc' command on Windows by copying a small wrapper script (tc.cmd)
# into a directory that should be on the user's PATH.

Write-Host "Installing terminal-command (tc) on Windows..."

param(
    [string]$InstallDir = "C:\\Windows\\System32"  # default location
)

# Check if the user has administrative privileges
if (-not ([bool](Test-Path $InstallDir))) {
    Write-Error "Error: InstallDir does not exist or is inaccessible. Please ensure you have administrative privileges."
    exit 1
}

# Check if Python is installed and in PATH
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Error: Python is not found or not in PATH. Please install Python 3 and ensure it is added to PATH."
    exit 1
}

# Create virtual environment
$ScriptDir = Split-Path $MyInvocation.MyCommand.Definition -Parent
$ProjectRoot = Join-Path $ScriptDir ".."
$EnvDir = Join-Path $ProjectRoot "env"
if (-not (Test-Path $EnvDir)) {
    Write-Host "Creating virtual environment in $EnvDir..."
    python -m venv $EnvDir
}

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..."
& "$EnvDir\Scripts\pip" install -r "$ProjectRoot\requirements.txt"

$ScriptDir = Split-Path $MyInvocation.MyCommand.Definition -Parent
$ProjectRoot = Join-Path $ScriptDir ".."
Write-Host "ProjectRoot: $ProjectRoot"

# Generate the tc.cmd script
$WrapperScript = @"
@echo off
"$EnvDir\Scripts\python" "$ProjectRoot\src\main.py" %*
"@

# Create a temp file, set contents
$TempFile = [IO.Path]::GetTempFileName() + ".cmd"
Set-Content -Path $TempFile -Value $WrapperScript -Force
# Make it executable
# (On Windows, .cmd files don't usually need explicit chmod, but let's keep it consistent.)
# Copy to InstallDir
Copy-Item $TempFile -Destination (Join-Path $InstallDir "tc.cmd") -Force
Remove-Item $TempFile -Force


Write-Host "Usage: tc \"list active docker containers\""
