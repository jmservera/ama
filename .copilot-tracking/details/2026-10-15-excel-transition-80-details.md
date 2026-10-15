---
title: Phase details for issue 80
description: File-level details for the Excel transition plan
ms.date: 2026-10-15
---

* Phase 1: `src/importer/src/zava_forward/importer/xlsx.py`.
* Phase 2: `mapping.py` (`CASE_LIST` structure, `build_preview`, `preview_file`).
* Phase 3: `quarantine.py` (`QuarantineStore`, tables `import_batches`, `import_rows`).
* Phase 4: `export.py`, `__main__.py` (`preview`).
* Phase 5: `tests/test_excel_transition.py`, `src/importer/README.md`, `docs/reference/README.md`, `docs/reference/log.md`, `pyproject.toml` (mypy override for untyped core).
