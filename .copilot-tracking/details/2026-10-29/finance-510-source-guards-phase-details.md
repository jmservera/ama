<!-- markdownlint-disable-file -->
# RPI Phase Details: Finance review source guards

## Metadata

* Task ID and slug: finance-510-source-guards
* Date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/finance-510-source-guards-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/finance-510-source-guards-research.md, C1-C6

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Restore source guards and regressions | Complete, regression evidence recorded | P01-T01 through P01-T03 |
| P02 | Validate and independently review | P02-T01 complete; Review/local commit pending | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Restore source guards and regressions

Context: metadata-only preflight and schema/current-field gated freshness leave
retained history unguarded. Alternatives currently inspect only clean document ID.
No evidence/model/financial authority changes belong here.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Guard retained sources with reusable availability reads

* Context: C1/C3/C4/C5. Missing blob is KeyError, not DocumentStoreError.
* Intent: report/action-local dict[str, str | None] maps document ID to actual digest or missing-byte sentinel. Read/hash once per document, including repeated unavailable alternatives; _current accepts this cache optionally and retains exact tuple freshness in _report. Service errors are not cached or suppressed.
* Traverse draft fields and prior/new history, plus stored diagnostic fields/history and attachment source records. Policy checks remain per field, including replaced/rejected history.
* _visible accepts the local cache; action preflight and resulting _report share it, with no store/global state. Standalone _report starts a new cache.
* Validation: clean-metadata missing blobs in stale-schema, rejected/replaced and snapshot-only retention; deny view/review/diagnose without changed records. Recovering bytes restores availability.
* Completion: external regressions pass for JSON and SQLite, including existing one-read tests.
* Actual evidence: _visible traverses all retained surfaces and _digest caches success/missing bytes by document ID. Requested discovery passes; existing cache assertions are unchanged.
* Dependencies: critique. Unresolved items: none.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Qualify alternatives with current source and field policy

* Context: C2/C6. Count current reviewable values only.
* Intent: a source-policy document helper serves both candidate review and retained visibility/alternatives; _current remains source-freshness authority.
* Match batch case/schema ID/version/digest and relevant candidate field first. Skip human-only fields and DocumentUnavailable sources. Apply policy per field outside source-tuple freshness caching.
* Do not suppress DocumentStoreError. Do not edit staged candidates, history, values or diagnostics.
* Validation: current conflict control; document version/hash/kind/bytes drift; allowed policy mismatch even when metadata otherwise matches; missing bytes; pending/deleted/generated metadata; persisted diagnose results and stage retention.
* Dependencies: shared digest/policy helpers in P01-T01.
* Completion: unusable candidates cannot yield Conflict; currently valid distinct values still can.
* Actual evidence: matching case/schema candidates use shared _source_document and _current; ten exclusion cases and per-field policy/read-reuse controls pass on both stores.
* Unresolved items: none.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Add external regressions and update the contract

* Test ownership locked to src/core/tests/test_form_review.py; maximum eight new methods and bounded helpers. Removals: none. Generated targets: none.
* Semantic and regression coverage are specified in the plan's AC1-AC5; preserve existing cache tests rather than weakening them.
* Read-only checks are tested with spies forbidding source mutation/scanning and comparing durable records after denial or exclusion.
* README describes byte availability independently of staleness and preserves unavailable approvals.
* Dependencies: P01-T01/P01-T02.
* Completion: baseline fails new repro assertions; implementation passes without weakening previous assertions.
* Actual evidence: seven new methods and one fixture helper, no removals. Baseline seven-method run fails with 34 assertion failures; final 26-test discovery passes.

<!-- rpi:phase id=P02 -->
## P02: Validate and independently review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run requested and related targeted checks

* Use exact user commands from src/core, via an isolated local environment if executables are missing.
* Also run test_form_staging, since shared source-policy semantics affect staged-review eligibility.
* Record actual stdout, counts, failures, fixes and command outcomes in changes evidence. Do not infer success from proxy checks.
* Dependencies: all P01 tasks.
* Completion: all four requested commands and staging tests pass; no Azure.
* Actual evidence: 26 review/pack tests and 17 staging tests pass; Ruff lint passes, format reports 112 files formatted and mypy reports 165 source files without issues. See changes record for initial failures and corrections.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Execute one independent Review and commit locally

* Fresh reviewer activates rpi-review with canonical plan/details/critique/research/changes pointers, exact implementation diff and validation evidence.
* Allowed reviewer write: dated Review only. No source fixes or repeated Review.
* Original adverse findings must remain, with later work routed separately.
* Commit identity: gh api user -> returned id/login -> repository-local noreply email for both author and committer.
* Commit source, tests, README and original RPI evidence locally; verify clean status and unchanged rubric. No push or live/publication gate.
* Dependencies: P02-T01.
* Completion: durable independent outcome and local commit. No unresolved human/hosted approval is claimed.
