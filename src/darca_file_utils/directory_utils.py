"""
directory_utils.py

A utility module for managing directory operations.
Provides methods to check for the existence, creation, listing, removal,
renaming, moving, and copying of directories.
Each method is documented with its purpose, parameters, and return values.
"""

import os
import shutil

from darca_log_facility.logger import DarcaLogger

# Initialize the logger
logger = DarcaLogger(name="directory_utils").get_logger()


class DirectoryUtils:
    @staticmethod
    def directory_exist(path: str) -> bool:
        """
        Check if a directory exists.

        Args:
            path (str): The directory path to check.

        Returns:
            bool: True if the directory exists, False otherwise.
        """
        exists = os.path.isdir(path)
        logger.debug(f"Checked directory existence for '{path}': {exists}")
        return exists

    @staticmethod
    def create_directory(path: str) -> bool:
        """
        Create a directory at the specified path if it does not exist.

        Args:
            path (str): The directory path to create.

        Returns:
            bool: True if the directory was created or already exists,
                  False otherwise.
        """
        if DirectoryUtils.directory_exist(path):
            logger.debug(f"Directory already exists: {path}")
            return True
        try:
            os.makedirs(path)
            logger.debug(f"Directory created: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory '{path}': {e}")
            return False

    @staticmethod
    def list_directory(path: str, recursive: bool = False) -> list:
        """
        List all entries in the specified directory.

        Args:
            path (str): The directory path to list.
            recursive (bool, optional): If True, returns all file paths
                                        recursively (relative to `path`).

        Returns:
            list: If recursive is False, returns a list of entries
                  (files and directories) directly within `path`.
                  If recursive is True, returns a list of file paths
                  (relative to `path`) for all files found recursively.
                  Returns an empty list if the directory does not exist
                  or an error occurs.
        """
        if not DirectoryUtils.directory_exist(path):
            logger.error(f"Directory does not exist: {path}")
            return []

        try:
            if not recursive:
                contents = os.listdir(path)
                logger.debug(f"Directory '{path}' contents: {contents}")
                return contents

            collected_files = []
            for root, _, files in os.walk(path):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, path)
                    collected_files.append(relative_path)
            logger.debug(
                f"Recursively collected files in '{path}': "
                f"{collected_files}"
            )
            return collected_files

        except Exception as e:
            logger.error(f"Error listing directory '{path}': {e}")
            return []

    @staticmethod
    def remove_directory(path: str) -> bool:
        """
        Remove a directory and all its contents recursively.

        Args:
            path (str): The directory path to remove.

        Returns:
            bool: True if the directory was removed successfully,
                  False otherwise.
        """
        if not DirectoryUtils.directory_exist(path):
            logger.error(f"Directory does not exist: {path}")
            return False
        try:
            shutil.rmtree(path)
            logger.debug(f"Removed directory: {path}")
            return True
        except Exception as e:
            logger.error(f"Error removing directory '{path}': {e}")
            return False

    @staticmethod
    def rename_directory(src: str, dst: str) -> bool:
        """
        Rename a directory from the source path to the destination path.

        Args:
            src (str): The current directory path.
            dst (str): The new directory path.

        Returns:
            bool: True if the directory was renamed successfully,
                  False otherwise.
        """
        if not DirectoryUtils.directory_exist(src):
            logger.error(f"Source directory does not exist: {src}")
            return False
        if DirectoryUtils.directory_exist(dst):
            logger.error(f"Destination directory already exists: {dst}")
            return False
        try:
            os.rename(src, dst)
            logger.debug(f"Renamed directory from '{src}' to '{dst}'")
            return True
        except Exception as e:
            logger.error(
                f"Error renaming directory from '{src}' to '{dst}': {e}"
            )
            return False

    @staticmethod
    def move_directory(src: str, dst: str) -> bool:
        """
        Move a directory from the source path to the destination path.

        Args:
            src (str): The source directory path.
            dst (str): The destination directory path.

        Returns:
            bool: True if the directory was moved successfully,
                  False otherwise.
        """
        if not DirectoryUtils.directory_exist(src):
            logger.error(f"Source directory does not exist: {src}")
            return False
        try:
            shutil.move(src, dst)
            logger.debug(f"Moved directory from '{src}' to '{dst}'")
            return True
        except Exception as e:
            logger.error(
                f"Error moving directory from '{src}' to '{dst}': {e}"
            )
            return False

    @staticmethod
    def copy_directory(src: str, dst: str) -> bool:
        """
        Recursively copy a directory from the source to the destination.

        Note:
            If the destination directory already exists, this function
            will not proceed.

        Args:
            src (str): The source directory path.
            dst (str): The destination directory path.

        Returns:
            bool: True if the directory was copied successfully,
                  False otherwise.
        """
        if not DirectoryUtils.directory_exist(src):
            logger.error(f"Source directory does not exist: {src}")
            return False
        if DirectoryUtils.directory_exist(dst):
            logger.error(f"Destination directory already exists: {dst}")
            return False
        try:
            shutil.copytree(src, dst)
            logger.debug(f"Copied directory from '{src}' to '{dst}'")
            return True
        except Exception as e:
            logger.error(
                f"Error copying directory from '{src}' to '{dst}': {e}"
            )
            return False
