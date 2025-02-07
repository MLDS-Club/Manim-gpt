import json
import os

def getConfigKey(keyName):
    """
    Retrieves the API key from a configuration file. 
    
    Also checks to ensure that all required keys specified in configTemplate.json are present.
    Args:
        name (str): The name of the key to retrieve (not used in the current implementation).
    Returns:
        str: The API key retrieved from the configuration file.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        KeyError: If the 'api_key' is not found in the configuration file.
        json.JSONDecodeError: If the configuration file contains invalid JSON.
    """
    
    config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    template_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configTemplate.json')

    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}") # ensure that the configuration file exists

    if not os.path.exists(template_file_path):
        raise FileNotFoundError(f"Configuration file not found: {template_file_path}") # ensure that the template file exists

    with open(config_file_path, 'r') as config_file:
        config_data = json.load(config_file)

    with open(template_file_path, 'r') as template_file:
        template_data = json.load(template_file)

    for required_key in template_data:
        if required_key not in config_data:
            raise KeyError(f"Required key '{required_key}' not found in configuration file (config.py). If this is an error, change configTemplate.json")

    for existing_key in config_data:
        if existing_key not in template_data:
            print(f"WARNING: '{existing_key}' only exists in config.json, not configTemplate.json! Please fix Abhiram!")

    if keyName not in config_data:
        raise KeyError(f"Key '{keyName}' not found in configuration file.")

    return config_data[keyName]