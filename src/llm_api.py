import json
import platform
import requests

from src.config import load_config


def call_llm_api(api_url: str, headers: dict, payload: dict) -> str:
    """
    Makes a POST request to the LLM API and returns the response content.
    
    Args:
        api_url (str): The API endpoint URL.
        headers (dict): The headers for the request.
        payload (dict): The JSON payload for the request.

    Returns:
        str: The content of the response.
    """

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]
    except (requests.RequestException, KeyError, IndexError) as e:
        return json.dumps({
            "command": "echo 'Could not retrieve command from LLM'",
            "explanation": f"Error: {e}"
        })


def _build_user_prompt(user_query: str) -> str:
    """
    Constructs the final prompt to be sent to the LLM.
    It loads the prompt template from the configuration and appends the user's query.
    
    Args:
        user_query (str): The user's natural language query.

    Returns:
        str: The complete prompt to be sent to the LLM.
    """

    config = load_config()

    prompt_template = config.get("prompt_template", "")
    os = platform.system()
    
    user_prompt = prompt_template.format(
        user_query = user_query,
        os = os
    )

    return user_prompt

def get_command_from_llm(user_query: str) -> str:
    """
    Sends the user_query (which should already be constructed as the final prompt)
    to the configured LLM provider and returns a JSON string containing:
        {
            "command": "<some terminal command>",
            "explanation": "<brief explanation>"
        }
    This implementation only supports the OpenAI provider.
    
    Args:
        user_query (str): The user query used to generate the prompt.

    Returns:
        str: A JSON string with the command and explanation.
    """

    config = load_config()
    provider_name = config.get("default_provider", "openai")
    provider_config = config.get("providers", {}).get(provider_name, {})

    if len(provider_config) > 0:
        api_key = provider_config.get("api_key", "")
        model = provider_config.get("model", "gpt-4o-mini")
        api_url = provider_config.get("api_url", "https://api.openai.com/v1/chat/completions")

        user_prompt = _build_user_prompt(user_query)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an AI that returns JSON with the following keys:\n"
                        "command (the final command to run) and explanation (a brief summary). "
                        "Do not include extra keys."
                    )
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "temperature": 0.0
        }

        return call_llm_api(api_url, headers, payload)
    else:
        return json.dumps({
            "command": "echo 'Unknown provider'",
            "explanation": f"Provider '{provider_name}' is not configured."
        })

def detect_suspicious_command(command: str) -> bool:
    """
    Determines if a command is potentially dangerous by:
      1. Checking local suspicious substrings from the configuration.
      2. Optionally, using an LLM call to further analyze the command if enabled.
    Returns True if the command is detected as suspicious, otherwise False.
    This implementation only supports the OpenAI provider for LLM-based detection.
    
    Args:
        command (str): The command to be analyzed for potential danger.

    Returns:
        bool: True if the command is suspicious, False otherwise.
    """

    config = load_config()
    
    # Retrieve suspicious command detection configuration.
    detection_conf = config.get("suspicious_command_detection", {})
    
    # Local check using configured suspicious substrings under detection_conf.
    local_substrings = detection_conf.get("suspicious_substrings", [])

    for substr in local_substrings:
        if substr in command: return True

    # Check if provider-based detection is enabled.
    provider_detection = detection_conf.get("provider_detection", {})

    if provider_detection.get("enabled", False):
        provider_name = provider_detection.get("provider", "openai")
        provider_config = config.get("providers", {}).get(provider_name, {})
        
        if len(provider_config) > 0:
            api_key = provider_config.get("api_key", "")
            model = provider_config.get("model", "gpt-4o-mini")
            api_url = provider_config.get("api_url", "https://api.openai.com/v1/chat/completions")

            detection_prompt_template = provider_detection.get("prompt_template", "Analyze command: {command}")
            prompt = detection_prompt_template.format(command = command)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert in shell command safety analysis. Answer strictly with 'True' if a command is dangerous, else 'False'."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.0
            }
            answer = call_llm_api(api_url, headers, payload)
            return answer.lower() == "true"
        else:
            # If detection provider is not recognized, default to suspicious.
            return True
    else:
        # If LLM detection is disabled, rely solely on local substring check.
        return False
