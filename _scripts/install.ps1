# terminal-command Install Script (Windows)
# This script installs the 'tc' command on Windows by copying a small wrapper script (tc.cmd)
# into a directory that should be on the user's PATH.

Write-Host "Installing terminal-command (tc) on Windows..."

$ScriptDir = Split-Path $MyInvocation.MyCommand.Definition -Parent
$ProjectRoot = Join-Path $ScriptDir ".."
$InstallDir = "C:\\Windows\\System32" # default location
$TargetFile = Join-Path $InstallDir "tc.cmd"

# Check if the user has administrative privileges
if (-not ([bool](Test-Path $InstallDir))) {
    Write-Error "Error: Installation directory does not exist or is inaccessible. Please ensure you have administrative privileges."
    exit 1
}

# Check if a different 'tc.cmd' already exists in the InstallDir
$Signature = "REM TC_SIGNATURE_MARKER_e33cf818-5952-4c8d-8fc2-2daacaa7575d" # signature to identify the script when updating
if (Test-Path $TargetFile) {
    if (-not (Select-String -Path $TargetFile -Pattern $Signature -Quiet)) {
        Write-Host "A file named 'tc.cmd' already exists in the target directory ($TargetFile)."
        $Response = Read-Host "Do you want to replace the existing file and continue with the installation? [y/n]"
        if ($Response -ne "y") {
            Write-Host "Installation aborted. To proceed, please remove or rename the existing '$TargetFile' and run the installer again, or consider installing manually to a different location."
            exit 1
        }
    } else {
        Write-Host "A previous installation of 'tc' is found and will be replaced."
    }
}

# Check if Python is installed and in PATH
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Error "Error: python3 is not found or not in PATH. Please install Python 3 and ensure it is added to PATH."
    exit 1
}

# Create virtual environment
$EnvDir = Join-Path $ProjectRoot "env"
if (-not (Test-Path $EnvDir)) {
    Write-Host "Creating virtual environment in $EnvDir..."
    python3 -m venv $EnvDir
}

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..."
Write-Host ""
& "$EnvDir\Scripts\pip" install -r "$ProjectRoot\requirements.txt"
Write-Host ""

$ScriptDir = Split-Path $MyInvocation.MyCommand.Definition -Parent
$ProjectRoot = Join-Path $ScriptDir ".."

# Generate the tc.cmd script
$WrapperScript = @"
@echo off
"$EnvDir\Scripts\python" "$ProjectRoot\main.py" %*
"@

# Create a temp file, set contents
$TempFile = [IO.Path]::GetTempFileName() + ".cmd"
Set-Content -Path $TempFile -Value $WrapperScript -Force

# Copy to InstallDir
Copy-Item $TempFile -Destination $TargetFile -Force
Remove-Item $TempFile -Force
Add-Content -Path $TargetFile -Value $Signature

# Check if config.yaml exists in the project's root directory
$ConfigFile = Join-Path $ProjectRoot "config.yaml"
$TemplateConfigFile = Join-Path $ProjectRoot "_templates\config.yaml"

if (-not (Test-Path $ConfigFile)) {
    Copy-Item $TemplateConfigFile -Destination $ConfigFile -Force
    Write-Host "config.yaml is copied from the templates to the project's root directory. Please add you LLM provider API key to it."
} else {
    Write-Host "config.yaml already exists in the project's root directory. Skipping copy."
}

Write-Host 'Installation complete.'
Write-Host 'For help: tc -h'
