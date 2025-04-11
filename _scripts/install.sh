#!/bin/bash
# terminal-command Install Script (Linux/macOS)
# This script installs the 'tc' command to /usr/local/bin
# Usage: ./install.sh

set -e

echo "Installing terminal-command (tc) on Linux/macOS..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
INSTALL_DIR="/usr/local/bin"

# Ensure script is run with root privileges
if [ "$EUID" -ne 0 ]; then
    echo "Error: This script must be run as root. Attempting to install to ${INSTALL_DIR} may fail. Please re-run with sudo or as root."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found or not in PATH. Please install Python 3 and ensure it is added to PATH."
    exit 1
fi

# Create virtual environment
ENV_DIR="${PROJECT_ROOT}/env"
if [ ! -d "${ENV_DIR}" ]; then
    echo "Creating virtual environment in ${ENV_DIR}..."
    python3 -m venv "${ENV_DIR}"
fi

# Install dependencies
echo "Installing dependencies from requirements.txt..."
echo ""
"${ENV_DIR}/bin/pip" install -r "${PROJECT_ROOT}/requirements.txt"
echo ""

# Create a small wrapper script 'tc' that points to the Python entry point
WRAPPER_SCRIPT="#!/usr/bin/env bash
\"${PROJECT_ROOT}/env/bin/python\" \"${PROJECT_ROOT}/main.py\" \"\$@\"
"

# Write wrapper script to a temporary location (And make it executable without root privilege), then move to /usr/local/bin
TMP_WRAPPER="$(mktemp)"
echo "${WRAPPER_SCRIPT}" > "${TMP_WRAPPER}"
chmod 755 "${TMP_WRAPPER}"

# Move the wrapper script to INSTALL_DIR
sudo mv "${TMP_WRAPPER}" "${INSTALL_DIR}/tc"

# Check if config.yaml exists in the project's root directory
CONFIG_FILE="${PROJECT_ROOT}/config.yaml"
TEMPLATE_CONFIG_FILE="${PROJECT_ROOT}/_templates/config.yaml"

if [ ! -f "${CONFIG_FILE}" ]; then
    cp "${TEMPLATE_CONFIG_FILE}" "${CONFIG_FILE}"
    echo "config.yaml is copied from the templates to the project's root directory. Please add you LLM provider API key to it."
else
    echo "config.yaml already exists in the project's root directory. Skipping copy."
fi

echo "Installation complete. 'tc' is now available in ${INSTALL_DIR}."
echo "For help: tc -h"
