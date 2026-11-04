---
title: Details, issue 133 concern pack
ms.date: 2026-11-04
---
* Phase 1: pack fields are the household statement, recorded facts, investigator questions, optional AI summary, source (`template` or `ai`), `approval` `Not reviewed`, `approved` false, manual route and the neutral notice. Sensor context is excluded.
* Phase 2: `src/core/tests/test_aftercare.py` gains 4 tests (template pack without AI, guarded AI summary, owner-only review that leaves the concern unchanged, registered unapproved task).
* Phase 3: `src/core/README.md` and `docs/reference/log.md`.
