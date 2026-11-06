---
title: Plan, issue 153 document-control retention and hold refusals
ms.date: 2026-11-06
---

* [ ] Reword the two `approve_retention_deletion` refusals in `doc_controls.py` (message text only).
* [ ] Add a behaviour regression in `src/api/tests/test_document_controls.py` that triggers both refusals and asserts reason, owner, next action, plain terms, and unchanged exception type, document count, audit event and hash chain.
* [ ] Add a lexical check in `src/api/tests/test_content_standard.py` guarding these literals.
* [ ] Update `content-standard.md` (slice 4 note, narrowed unaudited list), the reference log, and the README index entry if its summary changes.
* [ ] Run the focused tests only; record the pending native focused gate.

Tier: FOCUSED (default). Message text, tests and docs only; no control, storage, permission, retention or deployment change. Complete gate not required (not a big feature, release, infrastructure, SQL or security change).

Critique: one prospective independent critique before implementation; dispositions recorded separately. Details file holds exact copy and constraints.

Boundaries: no change to `resident_decisions.py`, `ai_consumption.py` or any web file. Whole issue stays open; no acceptance or human-review box is ticked. Future PR uses `Refs #153`.
