import os

from darca_file_utils.directory_utils import (
    DirectoryUtils,
)


def test_directory_exist(tmp_path):
    # Create a directory and check for its existence
    dir_path = tmp_path / "dir_exist"
    dir_path.mkdir()
    assert DirectoryUtils.directory_exist(str(dir_path)) is True

    # Test for a non-existent directory
    non_exist_dir = tmp_path / "nonexist_dir"
    assert DirectoryUtils.directory_exist(str(non_exist_dir)) is False


def test_create_directory(tmp_path):
    new_dir = tmp_path / "new_folder"
    # Ensure directory does not exist initially
    assert not new_dir.exists()
    # Create the directory
    assert DirectoryUtils.create_directory(str(new_dir)) is True
    assert new_dir.exists()


def test_list_directory(tmp_path):
    test_dir = tmp_path / "list_test"
    test_dir.mkdir()
    # Create files in the directory
    (test_dir / "file1.txt").write_text("content1")
    (test_dir / "file2.txt").write_text("content2")
    # Create a subdirectory with a file inside
    sub_dir = test_dir / "subfolder"
    sub_dir.mkdir()
    (sub_dir / "file3.txt").write_text("content3")

    # Non-recursive listing should include immediate children
    contents = DirectoryUtils.list_directory(str(test_dir))
    assert "file1.txt" in contents
    assert "file2.txt" in contents
    assert "subfolder" in contents

    # Recursive listing should return file paths relative to test_dir
    rec_contents = DirectoryUtils.list_directory(str(test_dir), recursive=True)
    assert "file1.txt" in rec_contents
    assert "file2.txt" in rec_contents
    assert os.path.join("subfolder", "file3.txt") in rec_contents


def test_remove_directory(tmp_path):
    test_dir = tmp_path / "remove_dir"
    test_dir.mkdir()
    # Create a file inside the directory
    (test_dir / "file.txt").write_text("to be removed")
    # Remove the directory and verify removal
    assert DirectoryUtils.remove_directory(str(test_dir)) is True
    assert not test_dir.exists()


def test_rename_directory(tmp_path):
    src_dir = tmp_path / "old_name"
    dst_dir = tmp_path / "new_name"
    src_dir.mkdir()
    # Rename the directory
    assert DirectoryUtils.rename_directory(str(src_dir), str(dst_dir)) is True
    assert not src_dir.exists()
    assert dst_dir.exists()


def test_move_directory(tmp_path):
    src_dir = tmp_path / "move_src"
    dst_dir = tmp_path / "move_dst"
    src_dir.mkdir()
    # Create a file in the source directory
    (src_dir / "file.txt").write_text("moving directory")
    # Move the directory
    assert DirectoryUtils.move_directory(str(src_dir), str(dst_dir)) is True
    assert not src_dir.exists()
    assert dst_dir.exists()
    # Verify the moved file exists in the new location
    assert (dst_dir / "file.txt").exists()


def test_copy_directory(tmp_path):
    src_dir = tmp_path / "copy_src"
    dst_dir = tmp_path / "copy_dst"
    src_dir.mkdir()
    # Create files in the source directory
    (src_dir / "file1.txt").write_text("copy file1")
    (src_dir / "file2.txt").write_text("copy file2")
    # Copy the directory
    assert DirectoryUtils.copy_directory(str(src_dir), str(dst_dir)) is True
    # Ensure both source and destination exist
    assert src_dir.exists()
    assert dst_dir.exists()
    # Check that files were copied
    assert (dst_dir / "file1.txt").exists()
    assert (dst_dir / "file2.txt").exists()
