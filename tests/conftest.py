import pytest
import shutil

# A simple fixture for a temporary test directory.
# Although pytest’s tmp_path is available, you may define additional common fixtures here if needed.
@pytest.fixture
def temp_test_dir(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    yield test_dir
    # Cleanup after tests
    if test_dir.exists():
        shutil.rmtree(str(test_dir))
