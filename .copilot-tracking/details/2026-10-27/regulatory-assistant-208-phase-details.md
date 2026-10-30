<!-- markdownlint-disable-file -->
# RPI Phase Details: Regulatory assistant completion

## Metadata

* Task ID: 208
* Task slug: regulatory-assistant-208
* Related plan: .copilot-tracking/plans/2026-10-27/regulatory-assistant-208-plan.md
* Evidence: .copilot-tracking/research/2026-10-27/regulatory-assistant-208-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Durable conflicts and consumption | Implemented; local regressions passed | P01-T01, P01-T02 |
| P02 | Evaluation and presentation | Implemented; evaluation/browser passed | P02-T01, P02-T02 |
| P03 | Validation and evidence | Implementation evidence complete; ready for one Review | P03-T01 |

Direct dispositions of PC-001 through PC-006 preceded implementation; original
critique Revise remains immutable. P01/P02 engineering completion does not
mark any issue acceptance criterion or human approval complete.

<!-- rpi:phase id=P01 -->
## P01: Durable conflicts and content-free consumption

Existing ask and doubt each own transactions. Extract their shared referral
writer so automatic conflict routing joins the ask transaction without nesting
SQL BEGIN statements. JSON restores chat_threads on failure; SQL rollback also
restores its append-only audit. The JSON file ledger remains separately
committed and must not be described as atomic.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Atomic automatic and manual doubt writer

Context: research C5/C6; #214 conflicting sources shown and escalated.
Resolve the named owner through the existing registered-principal and projected
case checks. Validate before mutation. Within the transaction recheck thread
state/version, append the pair, create the owner inbox and receipt through the
shared helper, audit, commit. Manual referrals keep their existing selected-turn
and idempotency behavior. Return the actual receipt to UI; history retains the
receipt as a separate assistant message. Never transfer source thread access.

Within the transaction, before mutation, re-admit the sender, verify its current
role matches the thread, re-resolve the named owner and verify both case
projections. Trusted ingress role remains the authenticated role, not a wider
database role. This is a local store lock/SQL transaction guarantee, not a
distributed Entra revocation synchronization claim. Tests inject changes after
initial admission but before this final check.

Idempotency is one referral per stored source-thread/assistant-turn identity.
Repeating ask intentionally creates a new pair even for equal question text.
Clients must reload after uncertain/committed responses rather than blind ask
retry. JSON post-save audit failure retains durable pair/inbox/receipt and
raises explicit reload guidance; never restore only memory and claim rollback.
Audit-only usage cannot assert those durable turns all have metering.

Validation: JSON/SQLite conflict success, exact evidence, idempotent subsequent
manual doubt, absent/ambiguous owner, reduced owner role, failed insertion,
audit and commit, restart. Existing ordinary answer/refusal/alerts remain.
Completion evidence: focused core/API outcomes and rollback assertions.
Unresolved: actual company appointment remains absent.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Offline usage and privacy boundaries

Context: tokenomics additions on #214/#217. This path is offline extractive;
the deterministic engine is also model-free. Define one small pure
identifiers/counts/version usage shape for these known tasks. No arbitrary
model-output metadata, prices or financial authority is accepted.

Record outcome/call/token counters and UTC period in existing chat audit
metadata, in the same SQL transaction. Aggregate only own/current-role/day
metadata; never inspect messages or retrieve raw facts for metering. State
historical unmetered records separately; do not reconstruct or invent them.
Read at most 1,000 latest ledger positions. SQL obtains max(seq) then projects
only matching authenticated actor/action detail with CASE over that finite
primary-key range, returning no foreign detail. JSON tails at most 256 KiB
and 1,000 complete lines, discarding a partial first line. Report bounded_partial
when either bound truncates; otherwise recorded_audit_only. No response claims
an exact daily turn total, even for an untruncated ledger, because absent audit
events and historical missing role metadata cannot be reconstructed. Legacy
matching events without usage are counted as unmetered within the window.
Both limits bound engineering read work, not urgent human intake.
Check/alert records carry the same zero-call metadata on creation, preserving
readable historic records. Expose status metadata via the existing regulatory
capability and synthetic/privacy admission. Align usage retention with its
parent records, explicitly unknown until DPO review; no deletion added.

Validation: schema counts exactly zero, no content fields, role/user/day
separation, rollback/restart and metadata-only access. Bounds are zero inference
for every role/day, not a quota on urgent human intake or deterministic checks.

<!-- rpi:phase id=P02 -->
## P02: Evaluation and role-shaped presentation

Retain the existing frozen exact extractive oracle, not self-validating
membership. The report remains a development report with provisional targets.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Explicit cost and no-spend comparator

Add independently authored expected zero-call metadata and mutation assertions.
Report AI cost per accepted check as Unknown: no accepted human denominator,
dated price, billing/allocation or review effort evidence. No model calls are
authorized; calls/tokens/budget cap is zero and paid expiry is absent because
there is no paid authority. Do not expose a fabricated zero total service cost.
Cards_only persists without pre-agreed staff value evidence. Regenerate the
existing 60,000 stateless-home report; preserve the distinction from continuing
stock and actual model/participant evaluation.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Existing alert/chat presentation

Read current fetched guidelines and repository Fluent/content/accessibility
standards before edits. Add usage text and automatic owner-receipt state to
the current panel. Restore receipt state from stored history, not guesses.
Keep manual doubt available for ordinary answers/refusals and preserve native
keyboard buttons, non-colour labels and plain-language mode. Add meaningful
form name/autocomplete where touched. No unrelated style or framework change.

Extend the existing synthetic loopback browser harness for conflict, owner
receipt, usage, missing evidence and ordinary paths. Reuse pinned axe hash.
No actual staff comprehension or full WCAG certification is inferred.

<!-- rpi:phase id=P03 -->
## P03: Validation, documentation and evidence

<!-- rpi:task id=P03-T01 -->
### P03-T01: Local regression and acceptance reconciliation

Use the external session venv installed after actual missing imports. First run
focused core/agents/API tests; escalate to affected-package discoveries for
shared transaction/read-model changes. From src/api run the requested existing
discovery with PYTHONPATH=../core/tests:../agents/tests. Run Ruff/mypy per
affected package and node --check for changed JS. Run the existing browser
harness with pinned axe when available, preserving explicit missing checks.
The evaluation runner exercises constructed data only, no ZF_DATA reads.

The actual SQL transaction COMMIT lives in SqlRepo.txn, not SqlRepo.commit
(a no-op). Inject failure before that statement takes effect and assert COMMIT
was attempted, then reopen and compare pair/inbox/receipt/audit/head preimages.
JSON save failure and post-save audit failure have separate tests. A lost
acknowledgement after successful SQL COMMIT is a committed/uncertain result,
not evidence of rollback. No request-idempotency extension is claimed.

Update existing project READMEs, regulatory synthesis, reference index and
append-only log with facts and unresolved criterion matrix. Do not alter legal
snapshots, memory, original specification, workflows or acceptance checkboxes.
Run one independent post-implementation Review, retain its original verdict
and route findings to future work. Commit implementation and original evidence
with gh-derived privacy email and required trailer. Publication remains
blocked unless the mandatory full-gate conflict is legitimately resolved.
Never invoke --all against the caller's explicit exclusion or claim the
permitted scoped gate replaces mandatory coverage.

### Implementation Completion Evidence (2026-10-27)

P01-P03 implementation markers are reconciled with the changes record's actual
35-row criterion matrix and original adverse outcomes. Core affected suites:
114 OK; agents discovery: 106 OK; API discovery: 1,122 run, 808 passed and
314 skipped; migration guard: 25 OK. Ruff check/format and mypy passed in all
three packages; JS syntax passed; actual browser/axe passed 21 scoped states.
The evaluation remains stateless synthetic development evidence.

P03 completion denotes implementation evidence and handoff, not execution of
the next lifecycle Review. No material scope change, second critique or human
approval occurred. No full/scoped RPI gate ran; publication and operational
acceptance remain blocked as recorded in plan/changes.
