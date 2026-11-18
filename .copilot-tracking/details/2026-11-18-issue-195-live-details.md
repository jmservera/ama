---
title: Details for issue 195 live plan
ms.date: 2026-11-18
---

Phase 2: add `v0.21.0` to the docstrings of `tools/test_epic_parity_matrix_old_paths.py` and `tools/test_private_mvp_data_exclusion.py`; add `tools/test_epic_legacy_path_retirement.py` to `GUARD_FILES` in `tools/check-legacy-references.py` with a comment; add a `ReferenceTests` case in `tools/test_check_legacy_references.py` that an untagged retired path in such a file still fails and the tagged one passes.
Phase 3: `python3 -m unittest tools.test_check_legacy_references`, `python3 tools/check-legacy-references.py` (expect 19 residual), `ruff format --isolated --line-length 100 --check` and `ruff check` on edited Python, update `docs/reference/README.md` index and append `docs/reference/log.md`.

Review note: the tools edits described above were dropped from the commit as FULL tier; only the documentation phases remain in this candidate.
