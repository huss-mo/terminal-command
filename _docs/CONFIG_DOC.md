# Configuration File Documentation

This document provides details about the parameters in `config.yaml`, which controls the behavior of the terminal-command (tc) application.

## Parameters

### `default_provider`
- **Description**: Specifies the LLM provider to use when generating commands.
- **Type**: String
- **Default**: `"openai"`
- **Valid Values**: Any provider defined in the `providers` section
- **Example**: `default_provider: "openai"`

### `verbosity`
- **Description**: Controls the level of output verbosity.
- **Type**: Integer
- **Default**: `2`
- **Valid Values**: `0`, `1`, `2`
- **Example**: `verbosity: 1`

### `prompt_template`
- **Description**: Template for generating terminal commands based on user requests. It must contain the two placeholders _{user_query}_ and _{os}_
- **Type**: Multiline String
- **Example**:
  ```yaml
  prompt_template: |
    Generate a terminal command to accomplish the following user request on the given operating system
    User Request: {user_query}
    Operating System: {os}
  ```

### `providers`
#### `openai`
- **Description**: Configuration for the OpenAI provider.
- **Type**: Object
  - **`api_key`**: String
  - **`model`**: String (Default: `"gpt-4o-mini"`)
  - **`api_url`**: String
- **Example**:
  ```yaml
  openai:
    api_key: "OPENAI_API_KEY"
    model: "gpt-4o-mini"
    api_url: "https://api.openai.com/v1/chat/completions"
  ```

#### `litellm`
- **Description**: Configuration for the LiteLLM provider.
- **Type**: Object
  - **`api_key`**: String
  - **`model`**: String
  - **`api_url`**: String
- **Example**:
  ```yaml
  litellm:
    api_key: "LITELLM_API_KEY"
    model: "LITELLM_MODEL"
    api_url: "127.0.0.1:4000/v1/chat/completions"
  ```

### `suspicious_command_detection`
#### `suspicious_substrings`
- **Description**: List of substrings considered suspicious in terminal commands.
- **Type**: List of Strings
- **Example**:
  ```yaml
  suspicious_substrings:
    - "rm -rf /"
    - "mkfs"
    - ":(){:|:&};:"
  ```

#### `provider_detection`
- **Description**: Configuration for detecting suspicious commands using an LLM provider.
- **Type**: Object
  - **`enabled`**: Boolean (Default: `False`)
  - **`provider`**: String (Default: `"openai"`)
  - **`prompt_template`**: Multiline String. It must contain the placeholder _{command}_
- **Example**:
  ```yaml
  provider_detection:
    enabled: True
    provider: "openai"
    prompt_template: "Analyze the following terminal command and determine if it is potentially dangerous. Return 'True' if it is dangerous, otherwise 'False'. Command: {command}"
  ```