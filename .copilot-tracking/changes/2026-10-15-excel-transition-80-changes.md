---
title: Changes for issue 80
description: Implementation record and validation for the Excel transition library
ms.date: 2026-10-15
---

## Changes

Added `xlsx.py`, `mapping.py`, `quarantine.py`, `export.py`, rewrote `__main__.py` (no args still prints the version), added `tests/test_excel_transition.py` (17 tests), importer README, reference index and log. No code in `mvp/`. No change to `.env`, `.vscode` or `.copilot-tracking/github-issues`.

## Validation (from `src/importer`, venv with `pip install -e ../core -e ".[dev]"`)

| Command | Result |
| --- | --- |
| `python -m unittest discover -s tests` | 26 tests OK (9 existing, 17 new; includes dependency rule) |
| `ruff check .` | All checks passed |
| `ruff format --check .` | clean after `ruff format` |
| `mypy` | Success, 10 files |
| `python -m zava_forward.importer preview /tmp/demo.xlsx` (synthetic) | mapping alias/exact, 1 ready, 1 to fix, rc 0; source unchanged |
| `python -m zava_forward.importer` | prints `zava-forward-import 0.1.0` |
| `docker ps` | permission denied; image build relies on CI |

SQL Server is unavailable locally; portability is checked by a banned-keyword test only.

## Acceptance criteria status

* [ ] Import shows mapping, conflicts and row-level preview, never changes source: library and CLI done and tested; web surface not built.
* [ ] Every list offers Excel or CSV export, Excel one-way: export functions done; per-list wiring blocked until #144.
* [ ] Export retains version, source, approval, supersession independent of AI provider: History sheet done and tested; ticking awaits the list wiring.
* [ ] Owners set staged thresholds: owner decision, not implemented.

Other open items: AI-assisted column suggestion with approval, importer image and limited SQL role, CI evidence.

## PR #303 review fixes (2026-10-15)

* `xlsx.py`: KeyError, ET.ParseError, ValueError, IndexError and zip/zlib errors during parsing now raise `WorkbookError`, so `__main__` prints "Cannot import" and exits 2. Missing `xl/_rels/workbook.xml.rels` and negative shared-string indexes are explicit errors.
* `xlsx.py`: entity guard now requires strict UTF-8 parts and checks DOCTYPE/ENTITY case-insensitively on decoded text; parts are read with a bounded read; added `MAX_TOTAL_BYTES` (50 MiB across parts) and `MAX_SHEETS` (50).
* `quarantine.py`: `UNIQUE (structure, version)`; decide UPDATE is conditional on `status = 'staged'` and rowcount is checked (rollback and clean `ImportError_` on a lost race); approve decides first, then supersedes the previous approved batch; staging uses MAX(version)+1 and retries on a duplicate version, then fails cleanly. SQL stays portable (no upsert, AUTOINCREMENT or PRAGMA).
* Tests: 8 new unhappy-path tests (34 total) in `tests/test_excel_transition.py`.
* Validation from `src/importer` (PYTHONPATH=src:../core/src, pip venv): unittest 34 OK, `ruff check` and `ruff format --check` clean, `mypy` success (10 files).
