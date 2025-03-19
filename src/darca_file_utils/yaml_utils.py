"""
yaml_utils.py

A utility module for managing YAML file operations.
Provides methods to load and write YAML files.
Each method is documented with its purpose, parameters, and return values.
"""

import yaml
from darca_log_facility.logger import DarcaLogger

from darca_file_utils.file_utils import (
    FileUtils,  # Reusing file operations from FileUtils
)

# Initialize the logger
logger = DarcaLogger(name="yaml_utils").get_logger()


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
        """
        content = FileUtils.read_file(file_path)
        if not content:
            logger.error(f"YAML file '{file_path}' is empty or unreadable.")
            return {}

        try:
            data = yaml.safe_load(content)
            if data is None:
                data = {}
            logger.debug(
                f"Loaded YAML file '{file_path}' successfully: " f"{data}"
            )
            return data
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file '{file_path}': {e}")
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
        """
        try:
            yaml_content = yaml.safe_dump(data, default_flow_style=False)
            logger.debug(f"Serialized data to YAML format for '{file_path}'.")
        except yaml.YAMLError as e:
            logger.error(
                f"Error serializing data to YAML for '{file_path}': " f"{e}"
            )
            return False

        if FileUtils.write_file(file_path, yaml_content):
            logger.debug(
                f"Written YAML content to file '{file_path}' " f"successfully."
            )
            return True
        else:
            logger.error(f"Failed to write YAML content to '{file_path}'.")
            return False
