========================================
Darca File Utilities
========================================

A modular Python utility library for **file and directory operations** 
with support for **YAML file management**. This project includes structured 
logging and follows best practices for Python development.

----------------------------------------
📦 Features
----------------------------------------

- **Directory Operations**
  - Create, list, rename, move, and delete directories.
- **File Operations**
  - Read, write, copy, rename, move, and delete files.
- **YAML Utilities**
  - Read and write YAML files.
- **Structured Logging**
  - Uses `darca-log-facility` for centralized logging.
- **Automated Testing**
  - Uses `pytest` and `pytest-cov` for test coverage.
- **Code Formatting**
  - Uses `black` and `isort` for consistent formatting.

----------------------------------------
🚀 Installation
----------------------------------------

Ensure you have **Python 3.12+** installed.

Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/darca-file-utils.git
cd darca-file-utils
```

### 🛥 **Using Makefile**
To set up everything:
```bash
make install
```

Alternatively, install dependencies manually:
```bash
python3 -m venv /tmp/darca-log-venv
source /tmp/darca-log-venv/bin/activate
poetry install
```

----------------------------------------
🛠 Usage
----------------------------------------

### 📂 **Directory Operations**
```python
from darca_file_utils.directory_utils import DirectoryUtils

# Create a directory
DirectoryUtils.create_directory("my_folder")

# List directory contents
print(DirectoryUtils.list_directory("my_folder"))
```

### 📄 **File Operations**
```python
from darca_file_utils.file_utils import FileUtils

# Write to a file
FileUtils.write_file("example.txt", "Hello, world!")

# Read the file
content = FileUtils.read_file("example.txt")
print(content)
```

### 💑 **YAML Operations**
```python
from darca_file_utils.yaml_utils import YamlUtils

# Save a dictionary to a YAML file
YamlUtils.write_yaml_file("config.yaml", {"key": "value"})

# Load YAML content
config = YamlUtils.load_yaml_file("config.yaml")
print(config)
```

----------------------------------------
🔍 Running Tests
----------------------------------------

To run all tests with **pytest**, including coverage reports:
```bash
make test
```

This will:
- Run all test cases in the `tests/` folder.
- Generate a coverage report in **HTML, JSON, and terminal**.

----------------------------------------
🛠 Development
----------------------------------------

### 🎨 **Formatting Code**
To automatically format the code:
```bash
make format
```

### 🛡 **Pre-Commit Checks**
Run all required checks before committing:
```bash
make check
```

### 📚 **Building Documentation**
To generate documentation using **Sphinx**:
```bash
make docs
```
Documentation will be available in `docs/build/html/`.

----------------------------------------
🤝 Contributing
----------------------------------------

We welcome contributions to improve the project!
- If you find a bug or want to request a feature, create an **issue**.
- To contribute code, create a **pull request** with a clear description of the changes.
- Ensure your code passes all checks by running:
  ```bash
  make check
  ```

----------------------------------------
🛢 Cleaning Up
----------------------------------------

To remove the virtual environment and Poetry cache:
```bash
make clean
```

----------------------------------------
📜 License
----------------------------------------

This project is licensed under the **MIT License**.

