# terminal-command

A Python-based CLI tool named "tc" for generating and executing shell commands using an LLM. This project supports:

- **LLM Integration**: It queries the configured LLM provider (e.g., OpenAI or LiteLLM) to generate terminal commands based on natural language input.
- **Configurable Endpoints and Models**: Endpoints are configurable via `config.yaml`. OpenAI-like endpoints are supported (ex. LiteLLM)
- **Suspicious Command Detection**: Utilizes both local substring checks and an LLM-based detection method to flag potentially dangerous commands. The list of suspicious substrings and the LLM detection prompt are configurable in `config.yaml`.
- **Command Execution**: The tool can either print the generated command or execute it automatically using the `--execute` (or `-e`) flag.

## Installation

First, copy config.yaml from _templates directory to the projects root directory and set the API keys. Then:

For **Linux/macOS**, run:
```bash
chmod +x ./_scripts/install.sh
./_scripts/install.sh
```

For **Windows**, run:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
```

## Configuration

The `config.yaml` file allows you to configure:
- **Default LLM Provider and Endpoints**: Configure the default provider (e.g., "openai" or "litellm"), API endpoints, and credentials.
- **Prompt Template**: A template to guide the LLM in producing structured JSON output containing `command` and `explanation`.
- **Suspicious Command Detection**: 
  - A list of local suspicious substrings to quickly flag dangerous commands.
  - LLM-based detection settings, including the provider and a prompt template used to analyze command safety.

Example `tc-config.yaml`:
```yaml
default_provider: "openai"

prompt_template: |
  You are an AI that returns JSON with the following keys:
  command (the final command to run) and explanation (a brief summary).
  Do not include extra keys.

suspicious_command_detection:
  suspicious_substrings:
    - "rm -rf /"
    - "mkfs"
    - ":(){:|:&};:"
  provider_detection:
    enabled: True
    provider: "openai"
    prompt: "Analyze the following command and determine if it is potentially dangerous. Return 'True' if it is dangerous, otherwise 'False'. Command: {command}"

providers:
  openai:
    api_key: "YOUR_OPENAI_API_KEY"
    model: "gpt-4o-mini"
    api_url: "https://api.openai.com/v1/chat/completions"
  litellm:
    api_key: "YOUR_LITELLM_API_KEY"
    model: "gpt-4o-mini"
    api_url: "https://api.litellm.org/v1/generate"
```

## Usage

To generate a command based on a natural language request:
```bash
tc "list active docker containers"
```
This prints the proposed command and explanation to the terminal.

To automatically execute the generated command, add the `--execute` flag:
```bash
tc "list active docker containers" --execute
```

## Disclaimer

This is an AI-powered tool. Use it at your own risk. The developer is not responsible for any consequences.
