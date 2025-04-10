import argparse
import json
import subprocess
import sys

from src.config import load_config
from src.llm_api import get_command_from_llm, detect_suspicious_command


def main():
    """
    Main function to parse command-line arguments and execute the terminal-command tool.
    It constructs the prompt, queries the LLM, checks for suspicious commands, and optionally executes the command.
    """

    parser = argparse.ArgumentParser(
        prog = "tc",
        description = "terminal-command (tc): A CLI tool that suggests and executes shell commands using AI"
    )
    parser.add_argument(
        "query",
        type = str,
        nargs = "+",
        help = "The natural language description of what you want to do."
    )
    parser.add_argument(
        "-e", "--execute",
        action = "store_true",
        help = "Automatically execute the returned command."
    )
    args = parser.parse_args()

    # Load configuration
    config = load_config()
    verbosity = config.get("verbosity", 2)
    if verbosity < 0: verbosity = 0

    # Get command from LLM
    user_query = " ".join(args.query)
    llm_response = get_command_from_llm(user_query)

    # Check validity
    try:
        data = json.loads(llm_response)
        command = data.get("command", "")
        explanation = data.get("explanation", "No explanation provided.")
    except json.JSONDecodeError:
        if verbosity >= 2:
            print("Error: Could not parse LLM response as JSON.", file = sys.stderr)
            print("Raw response:", llm_response, file = sys.stderr)

        return
    
    # Check if the command is suspicious
    suspicious_command = detect_suspicious_command(command)
    threat_level = "suspicious" if suspicious_command else "safe"

    if verbosity >= 1: print(f"Command ({threat_level}): {command}", file = sys.stderr)
    if verbosity >= 2: print(f"Explanation: {explanation}", file = sys.stderr)

    # Execute the command if the execute flag is set and the command is not suspicious
    if args.execute and not suspicious_command:
        if verbosity >= 2: print("Executing command...", file = sys.stderr)

        try: subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e: 
            if verbosity >= 2: print(f"Command failed: {e}", file = sys.stderr)


if __name__ == "__main__":
    main()
