"""
yaml_utils.py

A utility module for managing YAML file operations.
Provides methods to load and write YAML files.
Each method is documented with its purpose, parameters, and return values.
"""

import yaml
from common.logging import log_debug, log_error
from file_utils import FileUtils  # Reusing file operations from FileUtils


class YamlUtils:
    @staticmethod
    def load_yaml_file(file_path: str) -> dict:
        """
        Loads a YAML file and returns its content as a dictionary.

        This method uses FileUtils.read_file to read the file content and
          then parses the content using PyYAML.

        Args:
            file_path (str): The path to the YAML file.

        Returns:
            dict: A dictionary representing the YAML content.
                  Returns an empty dictionary if the file does not exist or
                  an error occurs during reading or parsing.

        Example:
            >>> config = YamlUtils.load_yaml_file("config.yaml")
            >>> print(config)
            {'key': 'value'}
        """
        content = FileUtils.read_file(file_path)
        if not content:
            log_error(
                f"YAML file '{file_path}' is empty or could not be read."
            )
            return {}
        try:
            data = yaml.safe_load(content)
            log_debug(f"Loaded YAML file '{file_path}' successfully.")
            return data if data is not None else {}
        except Exception as e:
            log_error(f"Error parsing YAML file '{file_path}': {e}")
            return {}

    @staticmethod
    def write_yaml_file(file_path: str, data: dict) -> bool:
        """
        Serializes a dictionary to a YAML formatted string and writes it
          to a file.

        This method converts the provided dictionary into YAML format using
         PyYAML's safe_dump, then writes the content to the specified file
         using FileUtils.write_file.

        Args:
            file_path (str): The path to the YAML file.
            data (dict): The dictionary data to be serialized and written.

        Returns:
            bool: True if the YAML file was written successfully,
                    False otherwise.

        Example:
            >>> success = YamlUtils.write_yaml_file("config.yaml",
                                                    {"key": "value"})
            >>> print(success)
            True
        """
        try:
            yaml_content = yaml.safe_dump(data, default_flow_style=False)
            log_debug(
                f"Serialized data to YAML format for file '{file_path}'."
            )
        except Exception as e:
            log_error(
                f"Error serializing data to YAML for file '{file_path}': {e}"
            )
            return False

        if FileUtils.write_file(file_path, yaml_content):
            log_debug(
                f"Written YAML content to file '{file_path}' successfully."
            )
            return True
        else:
            log_error(f"Failed to write YAML content to file '{file_path}'.")
            return False
