# Details: issue 198

* Edit `.github/rubric/artifacts.json` exclude list only.
* Add two parametrized tests to `.github/rubric/scripts/test_prepare.py`.
* Validate: `cd .github/rubric/scripts && python3 -m pytest -q` (pytest installed with `pip install --user --break-system-packages pytest`; `python3 -m unittest` discovers nothing because the suites are pytest-style).
