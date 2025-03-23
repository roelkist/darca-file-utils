import os

import pytest

from darca_file_utils.directory_utils import (
    DirectoryUtils,
    DirectoryUtilsException,
)


def test_directory_exist(tmp_path):
    path = tmp_path / "exists"
    path.mkdir()
    assert DirectoryUtils.directory_exist(str(path))
    assert not DirectoryUtils.directory_exist(str(tmp_path / "ghost"))


def test_create_directory(tmp_path):
    path = tmp_path / "create"
    assert DirectoryUtils.create_directory(str(path))
    assert path.exists()


def test_create_directory_already_exists(tmp_path):
    dir_path = tmp_path / "existing"
    dir_path.mkdir()
    assert DirectoryUtils.create_directory(str(dir_path)) is True


def test_create_directory_failure(monkeypatch, tmp_path):
    path = tmp_path / "fail"

    monkeypatch.setattr(
        "os.makedirs", lambda *a, **k: (_ for _ in ()).throw(OSError("fail"))
    )
    with pytest.raises(DirectoryUtilsException) as exc:
        DirectoryUtils.create_directory(str(path))
    assert "DIRECTORY_CREATION_ERROR" in str(exc.value)


def test_list_directory_basic(tmp_path):
    path = tmp_path / "dir"
    path.mkdir()
    (path / "file.txt").write_text("x")
    (path / "sub").mkdir()

    out = DirectoryUtils.list_directory(str(path))
    assert "file.txt" in out
    assert "sub" in out


def test_list_directory_recursive(tmp_path):
    path = tmp_path / "deep"
    sub = path / "nested"
    sub.mkdir(parents=True)
    (sub / "x.txt").write_text("x")

    files = DirectoryUtils.list_directory(str(path), recursive=True)
    assert os.path.join("nested", "x.txt") in files


def test_list_directory_error(monkeypatch, tmp_path):
    path = tmp_path / "boom"
    path.mkdir()

    monkeypatch.setattr(
        "os.listdir", lambda *a, **k: (_ for _ in ()).throw(OSError("fail"))
    )
    with pytest.raises(DirectoryUtilsException) as exc:
        DirectoryUtils.list_directory(str(path))
    assert "DIRECTORY_LISTING_ERROR" in str(exc.value)


def test_list_directory_missing(tmp_path):
    with pytest.raises(DirectoryUtilsException) as exc:
        DirectoryUtils.list_directory(str(tmp_path / "ghost"))
    assert "DIRECTORY_NOT_FOUND" in str(exc.value)


def test_remove_directory_success(tmp_path):
    path = tmp_path / "toremove"
    path.mkdir()
    assert DirectoryUtils.remove_directory(str(path))
    assert not path.exists()


def test_remove_directory_missing(tmp_path):
    with pytest.raises(DirectoryUtilsException):
        DirectoryUtils.remove_directory(str(tmp_path / "ghost"))


def test_remove_directory_failure(monkeypatch, tmp_path):
    path = tmp_path / "locked"
    path.mkdir()
    monkeypatch.setattr(
        "shutil.rmtree", lambda *a, **k: (_ for _ in ()).throw(OSError("fail"))
    )
    with pytest.raises(DirectoryUtilsException) as exc:
        DirectoryUtils.remove_directory(str(path))
    assert "DIRECTORY_REMOVE_ERROR" in str(exc.value)


def test_rename_directory(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    assert DirectoryUtils.rename_directory(str(src), str(dst))
    assert dst.exists()


def test_rename_directory_failures(tmp_path):
    missing = tmp_path / "ghost"
    with pytest.raises(DirectoryUtilsException):
        DirectoryUtils.rename_directory(str(missing), str(tmp_path / "any"))

    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    with pytest.raises(DirectoryUtilsException):
        DirectoryUtils.rename_directory(str(src), str(dst))


def test_rename_directory_error(monkeypatch, tmp_path):
    src = tmp_path / "from"
    dst = tmp_path / "to"
    src.mkdir()
    monkeypatch.setattr(
        "os.rename", lambda *a, **k: (_ for _ in ()).throw(OSError("fail"))
    )
    with pytest.raises(DirectoryUtilsException):
        DirectoryUtils.rename_directory(str(src), str(dst))


def test_move_directory(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    assert DirectoryUtils.move_directory(str(src), str(dst))
    assert dst.exists()


def test_move_directory_missing(tmp_path):
    with pytest.raises(DirectoryUtilsException):
        DirectoryUtils.move_directory(
            str(tmp_path / "ghost"), str(tmp_path / "here")
        )


def test_move_directory_error(monkeypatch, tmp_path):
    src = tmp_path / "dir"
    dst = tmp_path / "dest"
    src.mkdir()
    monkeypatch.setattr(
        "shutil.move", lambda *a, **k: (_ for _ in ()).throw(OSError("fail"))
    )
    with pytest.raises(DirectoryUtilsException):
        DirectoryUtils.move_directory(str(src), str(dst))


def test_copy_directory(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    (src / "file.txt").write_text("hi")
    assert DirectoryUtils.copy_directory(str(src), str(dst))
    assert (dst / "file.txt").exists()


def test_copy_directory_failures(tmp_path):
    with pytest.raises(DirectoryUtilsException):
        DirectoryUtils.copy_directory(
            str(tmp_path / "ghost"), str(tmp_path / "dst")
        )

    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    with pytest.raises(DirectoryUtilsException):
        DirectoryUtils.copy_directory(str(src), str(dst))


def test_copy_directory_error(monkeypatch, tmp_path):
    src = tmp_path / "source"
    dst = tmp_path / "target"
    src.mkdir()
    monkeypatch.setattr(
        "shutil.copytree",
        lambda *a, **k: (_ for _ in ()).throw(OSError("fail")),
    )
    with pytest.raises(DirectoryUtilsException):
        DirectoryUtils.copy_directory(str(src), str(dst))
