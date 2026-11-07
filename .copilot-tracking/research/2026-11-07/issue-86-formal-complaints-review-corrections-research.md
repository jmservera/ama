---
title: "Issue 86 formal-complaints adapter: review-correction research"
description: Prospective research validating three Medium contract findings from the independent exact-head functional assessment before any source edit
ms.date: 2026-11-07
issue: jmservera/ama#86
rpi_phase: research
task_slug: issue86-formal-complaints-review-corrections
parent_task_slug: issue-86-formal-complaints-adapter
---

Scope: jmservera/ama#86 only, `Refs #86`, never a closing keyword. Prospective, written before any source or test edit. Planning-only admission: no test, gate, service or heavy run was executed to write this record.

## Starting identities

* Worktree `/mnt/ama-gates/restart-worktrees/issue-86-complaints`, branch `feat/formal-complaints-adapter-86`, HEAD `3445238e43b484a7e550aca3cbbe91c3e9f9be90`, tree `99d97e9e95e33c1d286166e07ebfac55e0475a1c`, ignored-inclusive status empty.
* Declared parent `feat/controlled-lifecycle-integration-81` at `7d390e13a450a5ca096501b1a2ccefcd9a517fd4`; main `0f420dc9514db22081cb48fa733267d9d33a0d24`. None is moved by this slice.
* The FULL r5 receipt for the head above (`/mnt/ama-gates/g86-r5-1107/receipt.json`, sha256 `81e46e363876818eef1db42e4d2937e3630bd84ddd064a11ccc71032a8535e39`) and the adverse R4 receipt stay untouched. Any commit from this slice changes the head, so r5 will not cover the corrected candidate.

## Source assessment (preserved faithfully)

Independent exact-head functional assessment, `/home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-86-34452-r5/functional-findings.json`: verdict `approve_with_comments`, 0 critical, 0 high, 3 Medium, for synthetic/unconfigured publication only. It is not a blocking verdict. The coordinator elects to correct the three tightly coupled contract defects before publication (first correction cycle). The report states that the shipped receiver sends nothing, so none of the three is evidence of a live duplicate, misattributed or false delivery today.

## What exists (read from current source)

* `resident_decisions._forward` (lines 540-562): `_operation(... service_forward)` commits a Pending attempt, then a second `with store.lock` block re-finds the request and reads `route["attempts"][-1]["attempt"]`, builds the envelope, releases the lock, calls `_send`, then commits a `service_forward_outcome` operation naming that attempt number.
* `_res_service_forward` (lines 1324-1349) appends `attempt = len(attempts) + 1`. A Pending attempt blocks another reservation unless `retry_unresolved is True`. `Failed` and `Unconfigured` attempts retry without that flag.
* `_res_service_forward_outcome` (1351-1362) accepts an outcome only for an in-range attempt whose status is `Pending`.
* `complaints_route.STATUSES = (Pending, Unconfigured, Failed, Acknowledged)`; `_send` maps `NotConfigured` to `Unconfigured`, any other receiver exception to `Failed` with `FAILURE_REASON` ("It has not been received."), and an unparseable reply to `Failed` with `MALFORMED_REASON`.
* SQL stores run each `_res_*` handler twice for a mutation: once on the live case and once in `validate_sql` against a detached copy of the committed row with the same `context["body"]` (resident_decisions 262-284). `_operation` holds `store.lock` (an `RLock`, store.py:56) across both, so receiver I/O correctly stays outside, after `persisted` is set and the `with` exits.
* Tests that exercise `forward` live in `JsonResidentDecisions`, which `SqlResidentDecisions` inherits (test_resident_decisions.py:84, 3560), so a test added in the JSON class also runs against SQL under the opt-in SQL variants. Existing concurrency tests use `Barrier` with `ThreadPoolExecutor` and a second `open_store()` (around line 4105).

## Finding 1: send is not bound to the attempt it reserved

Validated: real, narrow. Between the reservation commit and the second lock block another caller using `retry_unresolved=True` on the still-Pending attempt can append attempt 2. The first caller then reads `attempts[-1]` as attempt 2, submits and records against 2, leaving attempt 1 Pending; the second caller's outcome then finds attempt 2 non-Pending and is rejected after the receiver was already called (a second send of the same `idempotency_key`).

Design findings from source:

* `_operation` yields nothing and the handler return value is discarded, so the caller cannot receive the attempt number directly.
* A caller-generated reservation identifier placed in the body (hex uuid created in `_forward`) is safe for SQL replay because the replay reuses `context["body"]`; the handler must read it and never mutate the body. It is distinct from `route_key` (stable per request for receiver idempotency) and survives restart.
* The identifier lets the caller find exactly its own attempt after commit, whatever else was appended. The attempt number alone is not an identity, because two Store instances over one SQL database can both compute `len(attempts)+1` from stale views; the SQL rowversion check turns one into a `ConflictError`, which is the existing, accepted behaviour.
* Retention (`resident_retention` deletion) removes `resident_request_ref` and `requested_by` per attempt. A reservation identifier is an opaque random token with no resident content; the plan keeps it but a test asserts retention leaves no resident reference behind. Final decision recorded in the plan.
* Between reservation and submission the request may be closed or its `version` changed (rights, reassignment). The reservation records `request_version`. Rebuilding the envelope from the current request after the lock gap currently has no check. Cheap, in-scope guard: under the same lock, require the request still open and `version == attempt["request_version"]`, otherwise do not call the receiver and record a definite non-send.
* "Live in-flight vs unresolved": `retry_unresolved` exists so a human can reconcile a Pending attempt whose outcome was lost. A Pending attempt currently being sent by this process is indistinguishable. A process-local in-flight registry keyed by (case, request, reservation) refused for `retry_unresolved` is a minimal, honest mitigation; it cannot see other processes, which is stated, and cross-process duplicates remain bounded by the explicit flag plus the receiver's use of `idempotency_key`. Receiver-side dedupe is not implemented here and stays a named gap.

## Finding 2: an exception does not prove non-receipt

Validated: real. A receiver can durably accept and then raise; the record would assert "It has not been received", and `Failed` retries ordinarily. The malformed-reply branch has the same flaw: a reply arrived, so the receiver was reached.

Findings from source and contract:

* The adapter contract is "one envelope in, raw reply out" (`ComplaintsReceiver`). Only `NotConfigured` is typed. There is no way for a receiver to say "definitely not sent".
* Smallest truthful model: keep `Unconfigured` (definite, nothing sent) and `Failed`, but reserve `Failed` for a definite non-send. Introduce a typed `NotSent` exception (receiver declares a definite pre-send refusal) and a new status `Unconfirmed` for every other exception and for a malformed reply: "Acknowledgement was not obtained. Whether the receiver has this request is unknown." The local request and the attempt identity stay unchanged.
* Retry gate: today only `Pending` needs `retry_unresolved`. `Unconfirmed` joins `Pending` as needing the explicit flag, with a message directing the person to check with the receiver, because only the receiver can say whether it holds the key. The flag is a human reconciliation assertion, not proof; the envelope carries the same `idempotency_key` and a new `attempt` number so a real receiver can dedupe. No receiver is activated, no transport is added.
* Status set is validated by `_res_service_forward_outcome` through `complaints_route.STATUSES[1:]`, so adding one status in the one tuple extends validation consistently. No SQL schema column constrains it (attempts live in the case JSON body).
* Compatibility: no real receiver ever existed, so persisted `Failed` rows come only from synthetic tests on an unpublished branch; no migration is proposed. A reviewer should still see this stated. `Failed` rows that already exist keep ordinary retry; nothing rewrites history.
* Callers and docs referring to the old text: `src/core/README.md` formal-route section (~line 316) and tests asserting `Failed` for exception and malformed modes. No web file renders formal-route status (grep of `src/api` web and README found none), so no web change is required; verified by search, not assumed.

## Finding 3: independent-review sender must be the named reviewer's persisted identity

Validated: real. `_res_service_forward` checks `user["email"] == redress_owner_email`, then `_require_independent_reviewer` (independence from the original recorder), then `_owner_rights`, which returns immediately for `MANAGERS`. A different current manager given the named reviewer's email passes, so identity continuity is never compared.

Findings from source:

* `_forward` receives the actor from `_actor` (verified current staff with `code`, `oid`, `email`), and `_operation` already refuses an actor that differs from the staff-list person for that email.
* Persisted `redress_identity` is `_identity(person)` with `email, code, name, role, oid` (resident_decisions 1312). For non-managers `_owner_rights` compares email, code and oid against the identity.
* `_same_person` is any-of (email, code or oid). That is right for "the same person made the decision" (exclusion), but wrong for continuity, where email equality alone must not suffice.
* Smallest correction that reuses established checks: a helper requiring a Known persisted `redress_identity` (code or oid), then every one of code and oid that is present in the persisted identity must equal the actor's value, with at least one compared. Email is then redundant but kept as the existing first guard. Managers get no bypass for this route only; `_owner_rights` for the Complaint route (not Independent review) is unchanged, so unrelated manager rights are preserved.
* Legacy: requests created before identity binding may lack `redress_identity` or have Unknown identity. Fail closed with the existing wording style: resolve the identity before forwarding. `_identity_status` already classifies Unknown. This blocks only independent-review forwarding on such records, never resident reach to the route by other means.
* Held cases: forward must remain available under authority and tenure holds (existing test); the identity check does not touch holds.

## Constraints, contradictions and unknowns

* No design or authority contradiction found. The three corrections stay inside the existing local-record and synthetic-receiver boundary: no destination, appointment, consent source, transport, automatic sending or operational authority is added.
* New status `Unconfirmed` and exception `NotSent` extend a contract the adapter itself introduced; no existing delivered behaviour of other issues changes. No change to #144 permit, worker or consumption code.
* Unknown: whether a future real receiver can offer receiver-side deduplication by `idempotency_key`. That is a named later decision for the receiver's owner; this slice only makes the adapter's records honest and retry explicit.
* The in-flight registry cannot see other processes. A two-process proof is not claimed.
* Process facts: free-text content is still not screened and the operational criterion (residents reach independent human review and the formal route without detriment) stays unproven and unticked.

## Planning readiness

Disposition `executed` (read the full report and current source). Planning Readiness: Ready. Follow-ups, if later routed, are receiver-side dedupe, a real receiver after named human decisions, and a web control.
