#!/bin/bash
# terminal-command Install Script (Linux/macOS)
# This script installs the 'tc' command to /usr/local/bin (or a user-specified directory).
# Usage: ./install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Installing terminal-command (tc) on Linux/macOS..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found. Please install Python 3 and re-run this script."
    exit 1
fi

# Ensure script is run with root privileges, or supply a custom install location
INSTALL_DIR="/usr/local/bin"
if [ "$EUID" -ne 0 ]; then
    echo "Warning: Script not running as root. Attempting to install to ${INSTALL_DIR} may fail."
    echo "Press Ctrl+C to cancel, or Enter to continue as non-root."
    read
fi

# Create a small wrapper script 'tc' that points to the Python entry point
WRAPPER_SCRIPT="#!/usr/bin/env bash
python3 \"${PROJECT_ROOT}/src/main.py\" \"\$@\"
"

# Write wrapper script to a temporary location, then move to /usr/local/bin
TMP_WRAPPER="$(mktemp)"
echo "${WRAPPER_SCRIPT}" > "${TMP_WRAPPER}"
chmod +x "${TMP_WRAPPER}"

# Move the wrapper script to INSTALL_DIR
sudo mv "${TMP_WRAPPER}" "${INSTALL_DIR}/tc"

echo "Installation complete! 'tc' is now available in ${INSTALL_DIR}."
echo "Usage: tc \"list active docker containers\""
