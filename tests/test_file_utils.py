import builtins
from builtins import open as builtin_open
from unittest.mock import patch

import pytest

from darca_file_utils.file_utils import FileUtils, FileUtilsException


def test_file_exist(tmp_path):
    file = tmp_path / "exists.txt"
    file.write_text("test")
    assert FileUtils.file_exist(str(file)) is True
    assert FileUtils.file_exist(str(tmp_path / "missing.txt")) is False


def test_write_file_and_read(tmp_path):
    file = tmp_path / "write.txt"
    content = "hello"
    assert FileUtils.write_file(str(file), content)
    assert FileUtils.read_file(str(file)) == content


def test_write_file_creates_directory(tmp_path):
    file = tmp_path / "nested" / "file.txt"
    content = "auto-dir"
    assert FileUtils.write_file(str(file), content)
    assert file.exists()


def test_write_file_failure(tmp_path):
    file = tmp_path / "fail.txt"

    def fake_open(*args, **kwargs):
        if args[0] == str(file):
            raise IOError("fail")
        return builtin_open(*args, **kwargs)

    with patch("builtins.open", side_effect=fake_open):
        with pytest.raises(FileUtilsException) as exc:
            FileUtils.write_file(str(file), "data")

    assert "FILE_WRITE_ERROR" in str(exc.value)


def test_read_file_missing(tmp_path):
    file = tmp_path / "not_found.txt"
    with pytest.raises(FileUtilsException) as exc:
        FileUtils.read_file(str(file))
    assert "FILE_NOT_FOUND" in str(exc.value)


def test_read_file_failure(tmp_path):
    file = tmp_path / "fail_read.txt"
    file.write_text("data")

    # Save original open so logger won't break
    real_open = builtins.open

    def open_mock(path, *args, **kwargs):
        if str(path) == str(file):
            raise IOError("fail")
        return real_open(path, *args, **kwargs)

    with patch("builtins.open", side_effect=open_mock):
        with pytest.raises(FileUtilsException) as exc:
            FileUtils.read_file(str(file))
    assert "FILE_READ_ERROR" in str(exc.value)


def test_remove_file_success(tmp_path):
    file = tmp_path / "remove.txt"
    file.write_text("bye")
    assert FileUtils.remove_file(str(file)) is True
    assert not file.exists()


def test_remove_file_missing(tmp_path):
    with pytest.raises(FileUtilsException) as exc:
        FileUtils.remove_file(str(tmp_path / "ghost.txt"))
    assert "FILE_NOT_FOUND" in str(exc.value)


def test_remove_file_failure(monkeypatch, tmp_path):
    file = tmp_path / "locked.txt"
    file.write_text("locked")

    monkeypatch.setattr(
        "os.remove", lambda path: (_ for _ in ()).throw(OSError("fail"))
    )
    with pytest.raises(FileUtilsException) as exc:
        FileUtils.remove_file(str(file))
    assert "FILE_REMOVE_ERROR" in str(exc.value)


def test_rename_file_success(tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("rename me")
    assert FileUtils.rename_file(str(src), str(dst))
    assert dst.exists()


def test_rename_file_errors(tmp_path):
    src = tmp_path / "missing.txt"
    dst = tmp_path / "new.txt"

    with pytest.raises(FileUtilsException) as exc:
        FileUtils.rename_file(str(src), str(dst))
    assert "FILE_NOT_FOUND" in str(exc.value)

    src.write_text("src")
    dst.write_text("dst")

    with pytest.raises(FileUtilsException) as exc:
        FileUtils.rename_file(str(src), str(dst))
    assert "FILE_ALREADY_EXISTS" in str(exc.value)


def test_rename_file_failure(monkeypatch, tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("fail")

    monkeypatch.setattr(
        "os.rename", lambda *a, **k: (_ for _ in ()).throw(OSError("fail"))
    )
    with pytest.raises(FileUtilsException) as exc:
        FileUtils.rename_file(str(src), str(dst))
    assert "FILE_RENAME_ERROR" in str(exc.value)


def test_move_file_success(tmp_path):
    src = tmp_path / "move.txt"
    dst = tmp_path / "moved.txt"
    src.write_text("move")
    assert FileUtils.move_file(str(src), str(dst))
    assert dst.exists()


def test_move_file_error(monkeypatch, tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("fail")

    monkeypatch.setattr(
        "shutil.move", lambda *a, **k: (_ for _ in ()).throw(OSError("fail"))
    )
    with pytest.raises(FileUtilsException) as exc:
        FileUtils.move_file(str(src), str(dst))
    assert "FILE_MOVE_ERROR" in str(exc.value)


def test_move_file_src_does_not_exist(tmp_path):
    src = tmp_path / "non_existent_file.txt"
    dst = tmp_path / "destination.txt"

    with pytest.raises(FileUtilsException) as exc_info:
        FileUtils.move_file(str(src), str(dst))

    assert exc_info.value.error_code == "FILE_NOT_FOUND"
    assert "does not exist" in str(exc_info.value)


def test_copy_file_success(tmp_path):
    src = tmp_path / "copy.txt"
    dst = tmp_path / "copy.bak"
    src.write_text("copied")
    assert FileUtils.copy_file(str(src), str(dst))
    assert dst.read_text() == "copied"


def test_copy_file_missing_or_exists(tmp_path):
    src = tmp_path / "missing.txt"
    dst = tmp_path / "new.txt"

    with pytest.raises(FileUtilsException):
        FileUtils.copy_file(str(src), str(dst))

    src.write_text("exists")
    dst.write_text("conflict")
    with pytest.raises(FileUtilsException):
        FileUtils.copy_file(str(src), str(dst))


def test_copy_file_failure(monkeypatch, tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("fail")

    monkeypatch.setattr(
        "shutil.copy2", lambda *a, **k: (_ for _ in ()).throw(OSError("fail"))
    )
    with pytest.raises(FileUtilsException) as exc:
        FileUtils.copy_file(str(src), str(dst))
    assert "FILE_COPY_ERROR" in str(exc.value)
