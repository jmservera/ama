<!-- markdownlint-disable-file -->
# RPI Plan: Capacity SQL reopen correction

## Task Metadata

* Task ID: pr-605-capacity-sql-reopen-correction
* Task slug: capacity-sql-reopen-correction
* Planning status: Ready; one critique complete, dispositions resolved
* Plan date: 2026-10-31
* Phase details: .copilot-tracking/details/2026-10-31/capacity-sql-reopen-correction-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/capacity-sql-reopen-correction-plan-critique.md

## Executive Summary

The external SQL HTTP test fixture now reopens persisted capacity without
wiping or reseeding. Production law-store ownership and unknown-law responses
are unchanged. The shared regression passes SQLite, file and real SQL Server;
one independent Review is Complete / Conformant with no substantive findings.

### User Decisions and Requirements Highlights

* Continue PR #605, Refs #523, on fix/capacity-page-523; full dated RPI loop and non-force push.
* Reuse protected SQL resources and treat CI as the publication gate for this correction.

### What You May Not Know

The named run's terminal failure is a SQLite-specific path assertion. Its
missing-law stack traces are nonfatal logged post-commit checks. The SQL test
also wipes its database whenever make_store is called, including for reopen.
Both need correcting; loading law in the case store would not address them.

### Unresolved Decisions or Blockers

None for implementation. Hosted checks and human merge approval are not local evidence.

## User Decisions and Requirements

* Pull requested branch and merge origin/main first; preserve main rubric score and both log histories if conflicted.
* Investigate actual CI log and reproduce on the protected container if available.
* Fix production or fixture root cause without inventing authority.
* Add or adjust focused tests outside the package.
* Run ruff, ruff format --check, mypy and relevant unit tests from src/api with PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
* Pip only; no secrets persisted; never remove protected container/image.
* Commit with required Copilot trailer and git push -u origin HEAD, never force.
* Do not wait for complete local gate; CI is the requested gate.

## Goals

* The same durable legacy capacity regression genuinely reopens all three stores.
* SQL success must establish persistence rather than a recreated seed.
* Capacity reads do not confer legal, contract or appointment authority.

## Scope and Non-Goals

* In scope: src/api/tests/test_procurement_api.py, src/api/tests/test_mssqlstore.py, directly related src/api/README.md note, dated RPI evidence.
* Non-goals: production API/store changes, new law fixtures, UI edits, dependency changes, full local gate, merge/deploy.

## Functional Requirements

* Separate initial SQL setup/wipe from reopening through the existing reopen_store fixture convention.
* Compare the reopened SQL path/state marker with the actual original backend rather than hardcoded SQLite filename.
* Verify same type, distinct SQL connection, seed-independent persistence, unchanged audit/procurement and missing contract_version. Capture detached nonempty audit before reopening; compare immediately, after reads and after denied action.
* Existing legacy appointment refusal remains 403; missing law checks remain explicit 503/unknown with safe human route.

## Non-Functional Requirements

* No production semantic changes or broader silent exception toleration.
* Existing external test ownership and lint exemptions remain unchanged.
* Real SQL tests use only the session-created isolated database on the protected running container.
* Exactly one independent final-candidate critique and one post-implementation Review.

## Acceptance Criteria

* AC1: Exact named SQL test reproduced before correction; SQLite/file baseline recorded.
* AC2: Shared regression passes all three backends after correction, with seed removed and persisted capacity/audit unchanged.
* AC3: Non-destructive reopening preserves original actual backend/state marker and distinct SQL connection.
* AC4: Repeated legacy reads keep contract_version null and appointment status Unknown; forbidden appointment action cannot mutate procurement.
* AC5: Explicit missing-law HTTP checks return 503/unknown and human safe route; no legal success inferred.
* AC6: Requested API-wide lint/format/mypy and relevant procurement/law unit suites pass.
* AC7: Original critique and Review preserved, correction committed and branch pushed; hosted/human approval left pending.

## Implementation Context Record

| Context | Record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-31/capacity-sql-reopen-correction-research.md; C1-C6/W1 |
| Plan | .copilot-tracking/plans/2026-10-31/capacity-sql-reopen-correction-plan.md |
| Details | .copilot-tracking/details/2026-10-31/capacity-sql-reopen-correction-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-31/capacity-sql-reopen-correction-plan-critique.md; executed, original Revise, findings disposed |
| Changes | .copilot-tracking/changes/2026-10-31/capacity-sql-reopen-correction-changes.md; implementation-owned |
| Readiness | Implementation and one independent Review complete; evidence publication remains authorized parent action |
| Continuation | Automatic parent publishes unchanged assessed source, then awaits CI and human merge approval |

## Sources

* Research C1-C6/W1: exact failure, lifecycle and existing reopen pattern.
* src/api/pyproject.toml and .github/workflows/src-ci.yml: tool configuration and existing CI gate.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct fixture and verify

* Intent: establish genuine reopening and preserved unknown authority.
* Dependencies: completed research and final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Correct and strengthen external reopen regression

* Add common reopen_store helper and non-wiping SQL override.
* Extend existing named test; capture detached nonempty audit before reopen, remove only the current temporary seed, compare actual backend path, verify distinct SQL connection, compare original capacity/audit immediately and after reads/refused action, and assert missing-law response.
* Record directly related API guide clarification.
* Completion evidence: three-source-file coherent diff; seed-independent regression passes in the 40-test SQLite/file/law run and 13-test real SQL HTTP run.
* Details: P01-T01 in the phase-details artifact.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Run requested checks and independent Review

* Run API-wide lint/format/mypy and focused SQLite/file/real-SQL procurement suites plus missing-law tests.
* Preserve all results, update plan/details/changes, then run one independent Review.
* Validation complete: API ruff check/format and mypy pass, 40 SQLite/file/law tests pass, 13 real SQL HTTP tests pass. Independent Review Complete / Conformant, zero substantive findings, at implementation HEAD 183c4ca3df7e39d6f7c83b617ca680883bd049e7.
* Details: P01-T02 in the phase-details artifact.

## Test Ownership and Change Budget

* Canonical tests: external src/api/tests/test_procurement_api.py and SQL subclass src/api/tests/test_mssqlstore.py.
* Exact removals: none of the existing tests; replace only the SQLite-specific assertion.
* Maximum additions: two fixture methods and focused assertions in the existing named test; no new test files.
* Generated targets: none.
* Semantic coverage: unknown contract/law and denied appointment mutation.
* Regression coverage: same backend/path, distinct connection, no seed and unchanged persisted data/audit.
* Validation evidence: existing real SQL baseline failure and SQLite/file baseline success in research; post-change tool and suite results in changes.

## Dependencies

* Protected SQL container is running; dedicated session test database exists.
* Existing /tmp/mv/bin/python environment has ruff, mypy and mssql-python; no install needed absent a missing-dependency failure.

## Critique Disposition

| Finding | Disposition | Response |
| --- | --- | --- |
| PC-001 | Accepted, direct correction | Functional requirements and P01-T01 now require detached nonempty pre-reopen audit baseline and comparisons at reopen/read/refusal boundaries |
| PC-002 | Rejected, not applicable to parent | The critique cites a worker execution boundary banning /tmp which is absent from this parent's supplied instructions. Existing /tmp/mv interpreter and standard temporary fixtures are permitted here; repository API guide itself uses that interpreter. No environment relocation or scratch policy change is justified. Original critique remains unchanged. |

* Critique executed once; original verdict Revise preserved. No unresolved implementation-readiness findings.

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-31/capacity-sql-reopen-correction-changes.md
* All P01 tasks complete. Review: .copilot-tracking/reviews/logs/2026-10-31/capacity-sql-reopen-correction-review.md.
* Implementation committed at 183c4ca3df7e39d6f7c83b617ca680883bd049e7; final evidence-only commit and non-force push remain authorized parent actions.
* No ordinary user decision or additional source work needed; await CI and human merge approval, retain Refs #523.
