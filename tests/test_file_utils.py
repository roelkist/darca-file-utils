from darca_file_utils.file_utils import FileUtils  # Ensure the project root is on PYTHONPATH


def test_file_exist(tmp_path):
    # Create a temporary file and verify its existence
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello, world!")
    assert FileUtils.file_exist(str(file_path)) is True

    # Check a file that does not exist
    non_exist_path = tmp_path / "nonexist.txt"
    assert FileUtils.file_exist(str(non_exist_path)) is False


def test_write_and_read_file(tmp_path):
    file_path = tmp_path / "hello.txt"
    content = "Hello, testing!"
    # Write file
    assert FileUtils.write_file(str(file_path), content) is True
    # Read file and verify content
    read_content = FileUtils.read_file(str(file_path))
    assert read_content == content


def test_remove_file(tmp_path):
    file_path = tmp_path / "remove_me.txt"
    file_path.write_text("To be removed")
    assert FileUtils.file_exist(str(file_path)) is True

    # Remove the file
    assert FileUtils.remove_file(str(file_path)) is True
    # Confirm removal
    assert FileUtils.file_exist(str(file_path)) is False


def test_rename_file(tmp_path):
    src_file = tmp_path / "original.txt"
    dst_file = tmp_path / "renamed.txt"
    src_file.write_text("rename me")
    # Rename the file
    assert FileUtils.rename_file(str(src_file), str(dst_file)) is True
    assert not FileUtils.file_exist(str(src_file))
    assert FileUtils.file_exist(str(dst_file))


def test_move_file(tmp_path):
    src_file = tmp_path / "move_me.txt"
    dst_dir = tmp_path / "destination"
    dst_dir.mkdir()
    dst_file = dst_dir / "move_me.txt"
    src_file.write_text("move content")
    # Move the file
    assert FileUtils.move_file(str(src_file), str(dst_file)) is True
    assert not FileUtils.file_exist(str(src_file))
    assert FileUtils.file_exist(str(dst_file))


def test_copy_file(tmp_path):
    src_file = tmp_path / "copy_me.txt"
    dst_file = tmp_path / "copy_me_copy.txt"
    src_file.write_text("copy content")
    # Copy the file
    assert FileUtils.copy_file(str(src_file), str(dst_file)) is True
    assert FileUtils.file_exist(str(src_file))
    assert FileUtils.file_exist(str(dst_file))
    # Verify both files have the same content
    assert FileUtils.read_file(str(src_file)) == FileUtils.read_file(
        str(dst_file)
    )
