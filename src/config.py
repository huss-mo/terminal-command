import os
import yaml


DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "config.yaml"
)


def load_config(config_path=DEFAULT_CONFIG_PATH):
    """
    Loads the config.yaml file containing LLM provider settings.
    Returns a dictionary of configuration settings.
    If the file doesn't exist, returns an empty dict.
    """
    
    if not os.path.isfile(config_path):
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        if data is None:
            data = {}
        return data
