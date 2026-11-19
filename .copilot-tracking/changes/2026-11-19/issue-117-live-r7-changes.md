---
title: Issue 117 changes, pass 7
ms.date: 2026-11-19
---

No source change. Tier FOCUSED (documentation only). Files: docs/reference/research/issue-117-live-r7-2026-11-19.md, docs/reference/README.md, docs/reference/log.md.

Validation: api `tests.test_document_controls` 19 OK; core `tests.test_document_rescan` 40 OK (20 skipped, no SQL Server). mypy, ruff and rpi-checks not applicable (no src or infra edit). Hosted CI not observed (nothing pushed).

| Criterion | Status |
| --- | --- |
| Uploads are scanned before availability | Local scanner and order of operations proven; Defender end to end and live EICAR unproven (needs ZF_SCANNER=defender on the demo API, outside authorisation) |
| Retention listing, owner approval, legal hold | Proven (ticked) |
