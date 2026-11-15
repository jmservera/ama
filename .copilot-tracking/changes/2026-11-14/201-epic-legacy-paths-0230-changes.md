---
title: Issue 201 epic legacy-path changes
ms.date: 2026-11-14
---

* Added `tools/test_epic_legacy_path_retirement.py`.
* Validation: ruff check and format passed; 5 new tests OK; `tools/rename-zava-tests.py` OK (25 tests) in a venv with `tools/rename-zava-requirements.txt`; with system Python 7 pre-existing errors from missing `PIL`/`pptx`, identical on baseline.
* Not run: full local gate, hosted CI (focused tier). Not pushed.
