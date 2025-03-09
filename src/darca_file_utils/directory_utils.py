"""
directory_utils.py

A utility module for managing directory operations.
Provides methods to check for the existence, creation, listing, removal,
renaming, moving, and copying of directories.
Each method is documented with its purpose, parameters, and return values.
"""

import os
import shutil

from common.logging import log_debug, log_error


class DirectoryUtils:
    @staticmethod
    def directory_exist(path: str) -> bool:
        """
        Check if a directory exists.

        Args:
            path (str): The directory path to check.

        Returns:
            bool: True if the directory exists, False otherwise.

        Example:
            >>> DirectoryUtils.directory_exist("/tmp")
            True
        """
        exists = os.path.isdir(path)
        log_debug(f"Checked directory existence for '{path}': {exists}")
        return exists

    @staticmethod
    def create_directory(path: str) -> bool:
        """
        Create a directory at the specified path if it does not exist.

        Args:
            path (str): The directory path to create.

        Returns:
            bool: True if the directory was created or already exists, False otherwise.

        Example:
            >>> DirectoryUtils.create_directory("/tmp/new_folder")
            True
        """
        if DirectoryUtils.directory_exist(path):
            log_debug(f"Directory already exists: {path}")
            return True
        try:
            os.makedirs(path)
            log_debug(f"Directory created: {path}")
            return True
        except Exception as e:
            log_error(f"Error creating directory '{path}': {e}")
            return False

    @staticmethod
    def list_directory(path: str, recursive: bool = False) -> list:
        """
        List all entries in the specified directory.

        Args:
            path (str): The directory path to list.
            recursive (bool, optional): If True, returns all file paths recursively (relative to `path`).
                                        Defaults to False.

        Returns:
            list: If recursive is False, returns a list of entries (files and directories) directly within `path`.
                  If recursive is True, returns a list of file paths (relative to `path`) for all files found recursively.
                  Returns an empty list if the directory does not exist or an error occurs.

        Example:
            >>> DirectoryUtils.list_directory("/tmp", recursive=True)
            ['subfolder/file1.txt', 'subfolder/file2.txt', 'file3.txt']
        """
        if not DirectoryUtils.directory_exist(path):
            log_error(f"Directory does not exist: {path}")
            return []
        try:
            if not recursive:
                contents = os.listdir(path)
                log_debug(f"Directory '{path}' contents: {contents}")
                return contents
            else:
                collected_files = []
                for root, _, files in os.walk(path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        relative_path = os.path.relpath(full_path, path)
                        collected_files.append(relative_path)
                log_debug(
                    f"Recursively collected file paths in '{path}': {collected_files}"
                )
                return collected_files
        except Exception as e:
            log_error(f"Error listing directory '{path}': {e}")
            return []

    @staticmethod
    def remove_directory(path: str) -> bool:
        """
        Remove a directory and all its contents recursively.

        Args:
            path (str): The directory path to remove.

        Returns:
            bool: True if the directory was removed successfully, False otherwise.

        Example:
            >>> DirectoryUtils.remove_directory("/tmp/old_folder")
            True
        """
        if not DirectoryUtils.directory_exist(path):
            log_error(f"Directory does not exist: {path}")
            return False
        try:
            shutil.rmtree(path)
            log_debug(f"Removed directory: {path}")
            return True
        except Exception as e:
            log_error(f"Error removing directory '{path}': {e}")
            return False

    @staticmethod
    def rename_directory(src: str, dst: str) -> bool:
        """
        Rename a directory from the source path to the destination path.

        Args:
            src (str): The current directory path.
            dst (str): The new directory path.

        Returns:
            bool: True if the directory was renamed successfully, False otherwise.

        Example:
            >>> DirectoryUtils.rename_directory("/tmp/old_name", "/tmp/new_name")
            True
        """
        if not DirectoryUtils.directory_exist(src):
            log_error(f"Source directory does not exist: {src}")
            return False
        if DirectoryUtils.directory_exist(dst):
            log_error(f"Destination directory already exists: {dst}")
            return False
        try:
            os.rename(src, dst)
            log_debug(f"Renamed directory from '{src}' to '{dst}'")
            return True
        except Exception as e:
            log_error(f"Error renaming directory from '{src}' to '{dst}': {e}")
            return False

    @staticmethod
    def move_directory(src: str, dst: str) -> bool:
        """
        Move a directory from the source path to the destination path.

        Args:
            src (str): The source directory path.
            dst (str): The destination directory path.

        Returns:
            bool: True if the directory was moved successfully, False otherwise.

        Example:
            >>> DirectoryUtils.move_directory("/tmp/folder", "/var/folder")
            True
        """
        if not DirectoryUtils.directory_exist(src):
            log_error(f"Source directory does not exist: {src}")
            return False
        try:
            shutil.move(src, dst)
            log_debug(f"Moved directory from '{src}' to '{dst}'")
            return True
        except Exception as e:
            log_error(f"Error moving directory from '{src}' to '{dst}': {e}")
            return False

    @staticmethod
    def copy_directory(src: str, dst: str) -> bool:
        """
        Recursively copy a directory from the source to the destination.

        Note:
            If the destination directory already exists, this function will not proceed.

        Args:
            src (str): The source directory path.
            dst (str): The destination directory path.

        Returns:
            bool: True if the directory was copied successfully, False otherwise.

        Example:
            >>> DirectoryUtils.copy_directory("/tmp/source_folder", "/tmp/destination_folder")
            True
        """
        if not DirectoryUtils.directory_exist(src):
            log_error(f"Source directory does not exist: {src}")
            return False
        if DirectoryUtils.directory_exist(dst):
            log_error(f"Destination directory already exists: {dst}")
            return False
        try:
            shutil.copytree(src, dst)
            log_debug(f"Copied directory from '{src}' to '{dst}'")
            return True
        except Exception as e:
            log_error(f"Error copying directory from '{src}' to '{dst}': {e}")
            return False
