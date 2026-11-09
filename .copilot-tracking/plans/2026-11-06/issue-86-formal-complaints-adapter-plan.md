---
title: Issue 86 formal-complaints adapter plan (2026-11-06)
ms.date: 2026-11-06
---

Scope: issue86 only. Research: `.copilot-tracking/research/2026-11-06/issue-86-formal-complaints-adapter-research.md`. Details: `.copilot-tracking/details/2026-11-06/issue-86-formal-complaints-adapter-details.md`. Branch `feat/formal-complaints-adapter-86`; declared target `feat/controlled-lifecycle-integration-81`; parent pinned `af891a5c`; current-main observation `bb3a3b03` (not a retarget).

Validation tier: FULL, selected because receipt persistence and access boundaries change. Rationale recorded; the complete receipt gate is NOT run here (issue1231r9 owns heavy execution). Only narrow constructed no-service tests run now. The full gate, independent exact-head review, hosted CI and human approvals remain a coordinator handoff.

* [ ] Phase 1: RED tests in `test_resident_decisions.py` (JSON and SQLite via shared class).
* [ ] Phase 2: `complaints_route.py` adapter boundary and `service_forward` action in `resident_decisions.py`.
* [ ] Phase 3: component README note, local checks, Changes, author Review, local commits.

## Design

* New module `zava_forward/core/complaints_route.py`: `UnconfiguredReceiver` default, `receiver_from_env(env)` reading `ZF_COMPLAINTS_ROUTE` (unset or `unconfigured` only; anything else raises `ValueError`), `build_envelope`, `parse_acknowledgement`.
* Store gets `complaints_receiver` (injectable; default from env at first use). Tests inject a synthetic receiver. No network code exists.
* New explicit action `service_forward` (in `RESIDENT_ACTIONS` and `FOLLOWUP_ACTIONS`, so it runs via `_operation`). Body: `id`, `expected_version`, `resident_request_ref` (staff-supplied reference showing the resident asked for this to be sent; required, never inferred), optional `note`.
* Eligible routes: Complaint and Independent review only. Closed requests refused. A request already Acknowledged is refused (no duplicate send).
* Authority: current redress owner or a resident-workflow manager (`_owner_rights`); for Independent review only the named reviewer, and `_require_independent_reviewer` is re-asserted against `reviewed_identity` so an Unknown or same-person reviewer cannot forward.
* Outcomes appended to `req["formal_route"]` as `attempts` (append-only): `attempt`, `status` in Unconfigured, Failed, Acknowledged, `idempotency_key`, `request_id`, `request_version`, `actor`, `at`, `receipt_ref` and `received_at` (Acknowledged only), `reason` (fixed text, never raw exception text). The request fields, status and `version` are not changed; `history` gets no fake response event. Local recording and receiver receipt stay separate fields.
* Envelope minimised: `idempotency_key`, `case_ref`, `request_id`, `route`, `summary`, `desired_outcome`, `accessibility`, `review_reference`. No representative reference, owner identities or safe-contact data.
* During SQL `validate_sql` replay (`context["validating"]`), the handler performs no receiver call and writes nothing durable.
* Resident access under holds is unaffected: the action does not consult disclosure/consent holds, and a test asserts it still works under an unclear-authority hold.
* `followup_view` exposes `formal_route` defaults (`attempts=[]`, `status="Not sent"`) for legacy requests.

## Tests (RED before change)

1. Default unconfigured: attempt recorded Unconfigured, no receipt, request fields identical, nothing sent.
2. Failing receiver (raises) and malformed acknowledgement: Failed attempt persists with request/idempotency identity, no receipt, original request unchanged, later retry allowed.
3. Acknowledged: receipt ref stored separately; envelope exactly the minimised keys; second forward refused.
4. Denied: contractor role, non-owner non-manager, service-owner on an Independent review, same-person or Unknown reviewer; ineligible route (Repair); missing `resident_request_ref`; stale version. No attempt recorded.
5. Hold: forward works under unclear representative authority and a tenure hold.
6. Env factory: unset and `unconfigured` give unconfigured; other values raise.
7. SQL variant: receiver called exactly once (validation replay does not resend).

## Non-implemented

Real receiver, destination, appointment, resident-facing UI, automatic send, delivery SLA, and the operational no-detriment proof.
