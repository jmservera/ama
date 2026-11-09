---
title: Issue 86 formal-complaints adapter boundary research (2026-11-06)
ms.date: 2026-11-06
---

Scope: issue86 only (jmservera/ama#86), branch `feat/formal-complaints-adapter-86`, declared target `feat/controlled-lifecycle-integration-81`, pinned parent `af891a5c`. Research disposition: executed. Planning readiness: Ready.

## Question

Issue 86's remaining criterion is that residents can reach independent human review and the formal complaints route without detriment. Today `resident_decisions.py` records `service_requests` locally and `panels.js` says a recording is not sent to a live complaints service. Is there a narrow, existing contract for a configurable formal-route adapter, and what is the smallest truthful slice?

## Evidence

* `src/core/src/zava_forward/core/resident_decisions.py`: `_res_service_open` builds the local request (routes include "Complaint" and "Independent review"; `service_owner`, `redress_owner`, `review_reference`, `reviewed_identity`, `version`, `history`). No receiver, receipt or outbound concept exists.
* `_require_independent_reviewer(reviewer, historical)` and the "Only the named independent reviewer" checks in `_res_service_update` and `_res_service_reopen` are the identity safeguards to preserve.
* `resident_action` sends `FOLLOWUP_ACTIONS` through `_operation`, which snapshots, runs `_res_<action>`, audits, saves, rolls back on failure, and raises `ResidentCommittedError` if the save succeeded but acknowledgement failed. A caught failure inside a handler therefore persists normally.
* SQL stores replay the handler on a detached record in `validate_sql` (`context["validating"]=True`). An outbound call in a handler would run twice unless it is skipped while validating. This is the main design hazard.
* `server.py` dispatches `resident_action` generically over `RESIDENT_ACTIONS`; no API change is needed for a backend action.
* Configuration pattern: `documents.py` and `doc_controls.py` read a `ZF_*` variable with a safe local default and raise `ValueError` on unknown kinds; transports are injected callables in tests ("nothing here has been run against a real ..."). No existing complaints destination, appointment, URL or credential exists in the repository.
* `test_resident_decisions.py`: `JsonResidentDecisions` is subclassed by `SqlResidentDecisions` (`sql = True`), so one test body covers JSON and SQLite. `test_complaint_and_independent_review_stay_open_under_every_hold` is the delivered hold regression (PR904) and is not repeated.
* Issue 86 criteria 1 to 3 are ticked; comment 6652964057 names the configurable adapter as remaining independent engineering. PR1099 records remaining human criteria. Neither is redone.

## Environment finding

`pip list` shows `zava-forward-core` editable-installed from the primary checkout `/home/azureuser/source/ama`, not this worktree. Bare `python3 -m unittest` in `src/core` imports the wrong tree or fails on `dataset`. Documented component commands use `PYTHONPATH=src:tests` from `src/core`; with it `zava_forward.core.resident_decisions.__file__` resolved to this worktree (verified). All validation uses that form plus `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR` in the supplied scratch. No `PYTHONPATH=mvp`, no uv.

## Findings

* The narrow contract is a small `submit(envelope) -> acknowledgement` callable object, injected on the store, with a factory that defaults to unconfigured, mirroring the `ZF_DOC_STORE` pattern.
* Unknown or real receiver kinds must not be invented: no destination, appointment, credential or consent source is evidenced. The factory therefore knows only `unconfigured`; any other value raises a clear error. A real receiver is future work behind named appointment and DPO/Legal decisions.
* Sending must be an explicit human action on one request, never automatic on `service_open`. Resident wish to forward is not inferred; the staff member supplies the reference recording that the resident asked, and the adapter slice does not decide consent.
* Three outcomes must be distinguishable from local recording: Unconfigured (nothing left the system), Failed (receiver error or malformed acknowledgement), Acknowledged (receiver returned a receipt reference). The local request is never mutated except by an append-only attempt record.

## Risks and residual items

* Acknowledged-then-save-failure: the receiver may hold a receipt the local store lost. Mitigation is a deterministic idempotency key (request id plus attempt number) in the envelope so a retry is recognisable; reconcile through `ResidentCommittedError` guidance. Cannot be fully closed without a real receiver contract.
* The call runs under the store lock; receiver timeouts are the receiver's responsibility. Recorded, not solved.
* Not proven: that a resident can in practice reach the route without detriment, and any real delivery, SLA or access-route evidence. Criterion 4 stays unticked.

## Not in scope

#144 permit/worker/consumption, web panel changes, real transport, appointments, policy activation, ticking criteria, retargeting or rebasing the stack.
