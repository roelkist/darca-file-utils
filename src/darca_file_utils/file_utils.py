"""
file_utils.py

A utility module for managing file operations.
Provides methods to check for file existence, write, read, remove, rename,
move, and copy files.
Each method is documented with its purpose, parameters, and return values.
"""

import os
import shutil

from darca_log_facility.logger import DarcaLogger

from darca_file_utils.directory_utils import (
    DirectoryUtils,  # Importing directory utilities
)

# Initialize the logger
logger = DarcaLogger(name="file_utils").get_logger()


class FileUtils:
    @staticmethod
    def file_exist(path: str) -> bool:
        """
        Check if a file exists.

        Args:
            path (str): The file path to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        exists = os.path.isfile(path)
        logger.debug(f"Checked file existence for '{path}': {exists}")
        return exists

    @staticmethod
    def write_file(
        file_path: str, content: str, mode: str = "w", encoding: str = "utf-8"
    ) -> bool:
        """
        Write the given content to a file.

        Args:
            file_path (str): The path to the file.
            content (str): The content to be written.
            mode (str, optional): The file opening mode (default is "w").
            encoding (str, optional): The file encoding (default is "utf-8").

        Returns:
            bool: True if the file was written successfully, False otherwise.
        """
        directory = os.path.dirname(file_path)
        if directory and not DirectoryUtils.directory_exist(directory):
            logger.warning(
                f"Directory does not exist for file: {directory}, "
                f"creating it."
            )
            DirectoryUtils.create_directory(directory)

        try:
            with open(file_path, mode, encoding=encoding) as f:
                f.write(content)
            logger.debug(f"Wrote content to file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing to file '{file_path}': {e}")
            return False

    @staticmethod
    def read_file(
        file_path: str, mode: str = "r", encoding: str = "utf-8"
    ) -> str:
        """
        Read and return the content of the specified file.

        Args:
            file_path (str): The path to the file.
            mode (str, optional): The file opening mode (default is "r").
            encoding (str, optional): The file encoding (default is "utf-8").

        Returns:
            str: The content of the file. Returns an empty string if the file
                 does not exist or an error occurs.
        """
        if not FileUtils.file_exist(file_path):
            logger.error(f"File does not exist: {file_path}")
            return ""

        try:
            with open(file_path, mode, encoding=encoding) as f:
                content = f.read()
            logger.debug(f"Read content from file: {file_path}")
            return content
        except Exception as e:
            logger.error(f"Error reading file '{file_path}': {e}")
            return ""

    @staticmethod
    def remove_file(file_path: str) -> bool:
        """
        Remove the specified file.

        Args:
            file_path (str): The path to the file to be removed.

        Returns:
            bool: True if the file was removed successfully, False otherwise.
        """
        if not FileUtils.file_exist(file_path):
            logger.error(f"File does not exist: {file_path}")
            return False

        try:
            os.remove(file_path)
            logger.debug(f"Removed file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error removing file '{file_path}': {e}")
            return False

    @staticmethod
    def rename_file(src: str, dst: str) -> bool:
        """
        Rename a file from the source path to the destination path.

        Args:
            src (str): The current file path.
            dst (str): The new file path.

        Returns:
            bool: True if the file was renamed successfully, False otherwise.
        """
        if not FileUtils.file_exist(src):
            logger.error(f"Source file does not exist: {src}")
            return False
        if FileUtils.file_exist(dst):
            logger.error(f"Destination file already exists: {dst}")
            return False

        try:
            os.rename(src, dst)
            logger.debug(f"Renamed file from '{src}' to '{dst}'")
            return True
        except Exception as e:
            logger.error(f"Error renaming file from '{src}' to '{dst}': {e}")
            return False

    @staticmethod
    def move_file(src: str, dst: str) -> bool:
        """
        Move a file from the source path to the destination path.

        Args:
            src (str): The current file path.
            dst (str): The destination file path.

        Returns:
            bool: True if the file was moved successfully, False otherwise.
        """
        if not FileUtils.file_exist(src):
            logger.error(f"Source file does not exist: {src}")
            return False

        try:
            shutil.move(src, dst)
            logger.debug(f"Moved file from '{src}' to '{dst}'")
            return True
        except Exception as e:
            logger.error(f"Error moving file from '{src}' to '{dst}': {e}")
            return False

    @staticmethod
    def copy_file(src: str, dst: str) -> bool:
        """
        Copy a file from the source path to the destination path.

        Args:
            src (str): The source file path.
            dst (str): The destination file path.

        Returns:
            bool: True if the file was copied successfully, False otherwise.
        """
        if not FileUtils.file_exist(src):
            logger.error(f"Source file does not exist: {src}")
            return False
        if FileUtils.file_exist(dst):
            logger.error(f"Destination file already exists: {dst}")
            return False

        try:
            shutil.copy2(src, dst)
            logger.debug(f"Copied file from '{src}' to '{dst}'")
            return True
        except Exception as e:
            logger.error(f"Error copying file from '{src}' to '{dst}': {e}")
            return False
