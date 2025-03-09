import os

import pytest
from file_utils import FileUtils  # For file reading/writing used by YamlUtils
from yaml_utils import \
    YamlUtils  # Ensure this module is available on PYTHONPATH


def test_write_and_load_yaml_file(tmp_path):
    test_file = tmp_path / "config.yaml"
    data = {"key": "value", "number": 42, "nested": {"a": 1, "b": [1, 2, 3]}}
    # Write YAML file
    assert YamlUtils.write_yaml_file(str(test_file), data) is True
    # Load YAML file and compare
    loaded_data = YamlUtils.load_yaml_file(str(test_file))
    assert loaded_data == data


def test_load_yaml_file_nonexistent(tmp_path):
    non_exist_file = tmp_path / "nonexistent.yaml"
    # Loading a non-existent file should return an empty dict
    loaded_data = YamlUtils.load_yaml_file(str(non_exist_file))
    assert loaded_data == {}


def test_write_yaml_file_empty_data(tmp_path):
    test_file = tmp_path / "empty.yaml"
    data = {}
    # Write empty YAML data
    assert YamlUtils.write_yaml_file(str(test_file), data) is True
    loaded_data = YamlUtils.load_yaml_file(str(test_file))
    assert loaded_data == data
