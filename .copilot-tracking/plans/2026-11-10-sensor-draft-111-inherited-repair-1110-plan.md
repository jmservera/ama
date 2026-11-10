---
title: Issue 111 inherited sensor draft correction plan
ms.date: 2026-11-10
task_id: 111-sensor-draft-inherited-repair-1110
---

## Objective

Spend the ONE Root-authorized inherited correction batch to fix two coupled confirmed defects in the unpublished candidate `d5e7ac2ef`: JSON audit failure after a committed save, and the configured Core mypy failure in the two new files. Nothing else. Research: [research](../research/2026-11-10-sensor-draft-111-inherited-repair-1110-research.md). Details: [details](../details/2026-11-10-sensor-draft-111-inherited-repair-1110-details.md). Critique: [critique](critiques/2026-11-10-sensor-draft-111-inherited-repair-1110-plan-critique.md).

## Classification and tier

Owner DEMO override, focused tier: targeted actual JSON regressions, relevant Core and API draft and analysis selectors, configured FULL Core ruff lint, ruff format and mypy including the new module and tests. API-only mypy is not a substitute. No full gate, no `--changed`, no live MSSQL, cloud, model or private data. The MSSQL draft class stays opt-in and is NOT run; the SQL control flow is restructured only to remove the broad catch, so SQLite and the existing 61 draft tests cover it and the MSSQL gap is stated. The change touches no workflow, dependency manifest, Dockerfile, permission, secret, deployment or security control; the single `pyproject.toml` stanza only relaxes `disallow_untyped_calls` for two modules (existing precedent), with its impact classified as typing-config only.

## Phases

* [x] Phase 1: Research and witness `launch` and `research-open`.
* [ ] Phase 2: Plan, details, one critique, applied findings, witness `plan-done`.
* [ ] Phase 3: Implement. Truthful prospective changes record first, witness `implement-start`, then:
  * [ ] 3a: add the JSON audit-after-commit regressions first and confirm they FAIL on the frozen module copy.
  * [ ] 3b: fix `_persist`: `committed` flag with `try/finally`, no `except BaseException`, `DraftAuditError` on JSON audit `OSError` after commit, top-level `CommittedReloadError` import.
  * [ ] 3c: full type annotations across module and tests; no `cast`, `Any`, `type: ignore`, ignore_errors, broad catches or success-shaped fallbacks.
  * [ ] 3d: one narrow `pyproject.toml` mypy override stanza for the two modules.
  * [ ] 3e: run the focused validation, complete the changes record, witness `implement-done`.
* [ ] Phase 4: ONE Review, witness `review-done`; commit locally, witness `commit-complete`, verify.

## Design

`_persist` after `store.lock` and duplicate and limit checks:

* build the record; set `case[CASE_KEY]`; `committed = False`.
* `try`: SQL: `audit` then `save`, `committed = True` (an unknown `CommittedReloadError` sets `committed = True` and re-raises); JSON: `save`, `committed = True`, then `audit`. `finally`: if not committed, restore the list and trim pending audits exactly as before.
* JSON audit `except OSError as error`: `raise DraftAuditError(view) from error`. The draft stays in memory and on disk; the error message says it was saved and its audit record was not written. Any other audit exception propagates unchanged and still leaves the committed draft in memory (the flag guarantees it).
* `DraftAuditError(RuntimeError)` carries `.draft` (the allowlisted view). The served route maps unknown `RuntimeError` through the existing generic error path; no server change.

## Acceptance

* JSON: after an injected audit `OSError` following a successful save, memory and disk both hold exactly one draft, `DraftAuditError` is raised with the draft view; an unrelated save plus fresh reload keeps it; retry of the same key returns `existing` with the first `created_at`, `created_by`, lineage and digest and writes no duplicate draft; a non-`OSError` audit failure also keeps memory and disk. These new tests fail on `d5e7ac2ef` and pass after the fix.
* Pre-commit save failure still restores memory, writes no audit, and a retry creates exactly one (existing test).
* SQLite restart, conflict and pending-audit tests unchanged and green; refusal, stale, missing, weather and consent tests green.
* `ruff check`, `ruff format --check` and `mypy` (project configuration, from `src/core`) clean on the whole Core project, including both new files; API draft tests and `src/api` mypy on its draft test unchanged and green.
* Frozen head lineage preserved; the fix is a new commit, no amend.

## Independence and ordering

Independent of the 135, 132, 133, 1300 and 1360 work: only `sensor_review_draft.py`, `tests/test_sensor_review_draft.py` and `pyproject.toml` (a new stanza) change. Main (`c9e15acb`) is not adopted; if a later ordinary adoption is needed, it is a merge by the Root-selected step, preserving both intents.

## Non-goals

No audit-gap repair on retry, no store, SQL schema, importer, adapter, server, UI, permission, rule-approval, consent, task, queue, model or ranking change. No unrelated Core cleanup.
