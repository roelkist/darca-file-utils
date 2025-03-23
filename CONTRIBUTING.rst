===============================
Contributing to darca-file-utils
===============================

First of all, thank you for taking the time to contribute ❤️

We welcome contributions in many forms:

- 🐛 Bug Reports
- ✨ Feature Requests
- 📥 Pull Requests (PRs)

Getting Started
---------------

1. Fork this repository
2. Clone your fork locally
3. Install dependencies and pre-commit hooks:

   .. code-block:: bash

       make install
       make format  # Optional, but encouraged!

4. Create your feature branch:

   .. code-block:: bash

       git checkout -b feature/my-new-feature

Before Committing
-----------------

Always run:

.. code-block:: bash

    make check

This runs all the essential checks: formatting, linting, pre-commit, and full tests.

Submitting a Pull Request
-------------------------

- Ensure tests are passing (`make test`)
- Add new tests for any new features or fixes
- Include updates to the docs if needed (`make docs`)
- Follow existing code style (`black`, `isort`)

Issue Templates & Feature Requests
----------------------------------

We encourage you to use the issue templates when opening bugs or feature suggestions.

GitHub Actions
--------------

Our CI workflow uses:

.. code-block:: bash

    make ci

This is what runs in GitHub Actions and ensures consistent results across platforms.

Thank you again for contributing!
