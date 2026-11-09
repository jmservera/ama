---
title: "Research, issue 133 assisted aftercare source integration, Stage A (2026-11-09)"
ms.date: 2026-11-09
---
## Scope and disposition

Research disposition: executed (started 2026-11-09T22:28Z, written 2026-11-09T22:31Z). Planning Readiness: Ready for Stage A (dedicated modules and isolated synthetic contracts). Not ready: connected integration, which needs shared hooks not admitted to this slice.

Inputs read: the ready issue file for #133 (acceptance criteria C1 to C6 and the 2026-10-31 and 2026-11-05 closure audits, treated as requirements data), the shared demo capacity guidance, the repository and Markdown instructions, the core README aftercare section, `aftercare.py`, `test_aftercare.py`, the #193 production-consumer test, `sensor_scenarios.retrofit_comparison`, `projection.STAFF_ROLES`, `controls.RESIDENT_ROLES`, `workflows.MANAGER_ROLES`, `chat_privacy.redact`, the existing server `/api/exceptions` hook, `store.py`/`sqlstore.py` persistence patterns and the `simulator-control.js` and exception-register screen test patterns. Both case studies, the knowledge-base index and memory were opened for context; no regulatory claim is made by this slice.

## Findings

* F1, delivered core: `AftercareRegister` already provides raise (digital or staff-recorded with channel, representative basis required), owner-only investigation, human-basis outcome, evidence-gated remedy, separate closure records, `unresolved`, `overdue`, household `view` without sensor context, sensor context as context only, `evaluator_view` with denominators and Unknowns, `intake_form`/`intake_errors`, `to_state`/`from_state` (refuses weakened snapshots), optional unreviewed pack. These are not recreated. Evidence: `aftercare.py`, 26 passing tests in a fresh scratch environment (21 aftercare, 5 consumer) at base `a04668ae9`.
* F2, gap: nothing turns these helpers into a staff-assisted service. Missing: existing-staff role checks, a durable receipt, idempotent submit, a persistence contract with restart, plain error/denial results, and a per-concern staff display that joins owner, investigation, remedy and closure.
* F3, gap: `evaluator_view` takes only home-id lists. It has no baseline or outcome measure and no per-home join. `sensor_scenarios.retrofit_comparison` supplies synthetic baseline, early and late means with an INSUFFICIENT status; the #193 consumer test proves non-dismissal only with constructed values. A joined view is not delivered.
* F4, hazard found: `_own` compares a free string, so an owner stored as "Unknown" would let any caller who passes "Unknown" act as owner. The adapter must refuse owner actions on a missing true owner and bind owner actions to the acting staff role.
* F5, owner model: no approved evaluator role, DPO or lawful-basis decision exists (open on the issue). Existing roles are `projection.STAFF_ROLES`. Synthetic scenario owners must be labelled as such, and a missing true owner shown as Unknown.
* F6, persistence pattern: the JSON store keeps a dict in `self.data` and the SQL store keeps JSON text in `meta`; `continuity` is the precedent. A single JSON state document (`AftercareRegister.to_state()` plus receipts and actions) fits both and needs no schema. Shared store edits are not admitted now, so Stage A defines a two-method state-store protocol with a file-backed test implementation.
* F7, hook pattern: server hooks are a short `if url.path == ...` block that calls a store method and maps `PermissionError` to 403 (`/api/exceptions`). A pure `handle(method, path, user, body)` returning `(status, payload)` lets the later hook be a thin delegation.
* F8, UI pattern: dedicated screen modules (`simulator-control.js`) share `h`, `api`, `show` and `me` with `app.js`; their tests run the script under node with stubs. A new unwired `aftercare.js` follows that pattern without touching `role-screens.js` or `index.html`.
* F9, privacy: a household statement is free text. This slice is synthetic only, so the service refuses text that `chat_privacy.redact` flags (email, phone, NI number, postcode, special category) and says why, so no actual household data enters a demonstration.
* F10, environment: the machine-wide editable install of `zava-forward-core` points at the primary checkout, not this worktree. All checks use a fresh issue-qualified venv at `/tmp/issue133-1109/venv` with this worktree's core installed (`pip install -e src/core`), never `PYTHONPATH`.

## Boundaries carried into planning

* Assisted channel provenance (`recorded_by`, `channel`), representative basis and the original statement are preserved unchanged. Handover and financial closure never alter a concern or remedy. A sensor reading never dismisses a concern.
* No resident portal, no new permission, no evaluator role, no pack generation, no model or cloud call, no private data.
* Criteria C1 to C6 remain unmet by Stage A: no connected, served, browser or user evidence exists.

## Follow-ups (current)

1. Hook continuation after sibling 132 merges: server routes, store persistence, navigation, endpoint inventory and browser journeys.
2. Evaluator role and DPO position on outcome data (human decisions, gate live acceptance only).
3. Connected pack registration and human-review journey (C6), later and optional.
