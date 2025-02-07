import json
import os

def getConfigKey(keyName):
    """
    Retrieves the API key from a configuration file.
    Args:
        name (str): The name of the key to retrieve (not used in the current implementation).
    Returns:
        str: The API key retrieved from the configuration file.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        KeyError: If the 'api_key' is not found in the configuration file.
        json.JSONDecodeError: If the configuration file contains invalid JSON.
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config[keyName]

