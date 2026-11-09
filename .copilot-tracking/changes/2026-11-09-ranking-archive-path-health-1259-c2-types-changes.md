---
title: Issue 1259 C2 typing correction changes
description: Changes and validation for the two child-owned strict-mypy diagnostics
ms.date: 2026-11-09
---

## Change

`src/core/tests/test_ranking_archive_blob.py`: added test gets `-> None` (Ruff-format wrapped, an E501 first attempt was corrected) and uses a typed comprehension over `self.fake.calls` instead of the untyped `requests` helper. Equivalent here: SAS auth, no token calls. No source, transport, API, fixture or emulator change; no `Any`, cast or ignore.

## Validation (CI install profile, mypy 2.4.0, ruff 0.17.1, owned venvs outside the repo; logs outside the repo)

| Check | Result | Log sha256 |
| --- | --- | --- |
| core mypy | exit 1, 84 errors; sorted line-stripped diagnostics identical to parent `9b1e2567` | 4f73d9e7... |
| API mypy | exit 1, 9 errors, all inherited core fixture; identical to parent | 88609b17... |
| core ruff check / format --check | exit 0 / exit 0 (225 files) | 82b3e6a6... / f936c74f... |
| API ruff check / format --check | exit 1 (10 errors) / exit 1 (1 file); diagnostics identical to parent, inherited, not cured | 30119145... / 90a99613... |
| core `unittest discover -s tests -p "test_ranking_*.py"` | 136 tests OK | a5bd7457... |
| API `test_ranking_publication_wiring.py` (PYTHONPATH core and agents tests) | 36 tests OK | c8792a4f... |

Note the first attempt (without format) failed Ruff E501 and was fixed in this same cycle. Initial unittest module-name invocations failed on import path and were rerun with the CI `discover -s tests` form. The core test discovery includes the Blob module, publication and runner tests. Not run: full matrix, SQL, scanner, emulator, hosted CI.

Child-owned diagnostics remaining: 0. Inherited remaining: core 84, API 9 mypy, API Ruff 10 plus format 1.
