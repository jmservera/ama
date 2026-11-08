---
title: Issue 530 C1 chat checker lint and ignored-input hygiene research
ms.date: 2026-11-08
---

* Disposition: executed. Base: HEAD 1c771189 (tree fc27b91f), Main 0f05e9aa unchanged. Refs #530 only.

## Findings

* The original gap details required `employee_chat_browser_check` in the browser lint tuple in both the planned (`tools/rpi-checks.py` plan, about line 1125) and executed (`Runner.browser`, about line 2322) contracts. The delivered change omitted it because `ruff check` (E,F,I,B,UP, line 100) reports 17 errors and `ruff format --check` wants a rewrite. The original Review called the result conformant for LIGHT scope; that claim did not disclose this unfulfilled planned item as a limitation. The original records stay unchanged.
* The 17 errors are one I001 (import order), 15 E501 long lines (mostly long string literals) and one B023 (`denied` loop variable captured by `denied_reply`). The B023 closure is called synchronously inside the same loop iteration by `page.route`, so no behaviour changes if the closure binds `denied` through a default argument. If ruff or a reviewer finds that this changes semantics, stop and name it.
* Ruff pinned by the maintained gate is 0.17.1, the same as the external venv.
* Ignored inputs: `.mypy_cache`, `.ruff_cache`, `src/api/.ruff_cache`, `tools/__pycache__`, `__pycache__` folders and three `*.egg-info` directories exist. Their timestamps (07:39-07:40 today) are after the plan commit 285280edb (07:35), and they were produced by this RPI's pip installs, ruff, mypy and unittest runs. The editable installs point at this worktree `src/*/src`, so the egg-info folders are generated package metadata, not source, receipt or resume inputs.
* Future outputs must be external: `PYTHONPYCACHEPREFIX`, `RUFF_CACHE_DIR`, `MYPY_CACHE_DIR`, and `pip install` metadata must not land in the worktree. Editable installs write egg-info into the source tree, so the venv is reinstalled with a non-editable copy, or the metadata is kept external, only if needed for a later check.

## Planning readiness

* Ready. Scope is the checker file format and lint fixes, two lint contracts and one regression, plus provenance-journalled relocation of the generated ignored paths to an external scratch folder.
