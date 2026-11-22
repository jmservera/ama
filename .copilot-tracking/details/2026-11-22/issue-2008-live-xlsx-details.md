---
title: Issue 2008 phase details, 2026-11-22
ms.date: 2026-11-22
---

* P1 files: `src/core/src/zava_forward/core/xlsx.py`, `import_preview.py`; `src/importer/src/zava_forward/importer/xlsx.py`, `mapping.py` (aliases). Success: importer suite unchanged and green.
* P2 response shape for xlsx: `kind: "workbook"`, `source_name`, `source_sha256`, `sheet`, `structure`, `columns[{field, header, how}]`, `unmapped_headers`, `conflicts`, `ready`, `to_fix_count`, `rows[{row, values, problems}]` (max 200), `matched_existing`, `message`. Errors 400 with plain text.
* P3 files: `src/api/src/zava_forward/api/web/app.js`.
* P4 files: READMEs, `docs/reference/research/issue-2008-web-xlsx-import-2026-11-22.md`, `docs/reference/README.md`, `docs/reference/log.md`.
