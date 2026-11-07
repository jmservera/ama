---
title: Issue 135 employee exception screen details
ms.date: 2026-11-07
---

## Phase 1 and 2: role-screens.js

* Host line: `screen.overview(signal, data.items, c)`.
* `data-operator.overview(signal, rows, c)`: summary when no home selected and rows exist, then `exceptionRegisterView(signal)` when the hash has `exceptions=1`, else a panel with the explicit link and a note that opening it is recorded in the audit log.
* Register panel sections: heading and status banner; read-only note and returned `note`; access (viewer, roles, scope); sources and unrouted lists; queue table with kind, reference, state, owner, summary, reason, manual next step, original source and eligibility; conflict table with both values, source, date, version, owner; AI explanation text.
* Kind label map is display only; unknown kinds shown as returned text.
* AI wording: `failed_ai_run` is "Requested AI help did not deliver a model result" with "Quarantined" when `original_source.status` is `quarantined`, else "Fell back to rules or template". Note: deliberate workflow-only processing is not an exception and is not a model result either.
* Runbook cell is prefixed "Placeholder guidance, not an approved runbook:".
* Errors: 403 => denied panel using returned server text; any other failure or invalid shape => unavailable panel (reason, owner application support, next action). Never renders old rows.

## Phase 3: tests

* New `src/api/tests/test_exception_register_screen.py` runs node with a fake `api` and counts calls and methods, asserting no non-GET and the endpoint path used.
* Existing test file gains a source assertion that no simulator or write controls appear in the new block.

## Phase 4: commands

* `python3 -m unittest` for both test files from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`, existing exception register and role screen tests, ruff check/format, mypy, `node --check`.
