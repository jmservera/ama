<!-- markdownlint-disable-file -->
# RPI Changes: Finance review source guards

## Metadata

* Task ID: finance-510-source-guards
* Implementation date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/finance-510-source-guards-plan.md
* Details: .copilot-tracking/details/2026-10-29/finance-510-source-guards-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/finance-510-source-guards-plan-critique.md, Complete / Pass, no findings
* Baseline HEAD: 7fed0b6b7b70f3a793132aaaf2690ea0fa9f1881

## Execution Status

* Status: Complete; reviewed implementation and original RPI evidence committed locally.
* Declared scope: full plan.
* Completed markers: P01, P01-T01/T02/T03, P02, P02-T01/T02.
* Remaining markers: none.
* First execution boundary: retained-source guard, then alternative qualification, external regressions, documentation, validation and independent Review.
* Approved write boundary: form_review.py, existing external test_form_review.py, src/core/README.md and this task's dated tracking artifacts.

## Execution Summary

Both supplied defects are fixed, including report-local byte reuse, explicit
missing/service-error distinction and staged-history preservation. Seven external
regressions cover both stores. Requested checks and related staging tests pass.

## Completed Work

### Retained evidence availability guard

* P01-T01; src/core/src/zava_forward/core/form_review.py.
* Added _digest with document-ID cache, including a None sentinel for missing bytes; only KeyError becomes DocumentUnavailable. Service failures propagate.
* _visible checks current fields, prior/new history, saved diagnostic fields/history and attachment references, independently of schema/currentness.
* Action preflight shares its local cache with its resulting report. Each standalone report starts a new cache.
* Exact version/hash/kind freshness remains tuple-keyed; historical staleness alone does not deny available history.
* Completion evidence: both JSON/SQLite missing-retention, snapshot-only, service-outage and read-count regressions pass.

### Review-eligible conflict alternatives

* P01-T02; src/core/src/zava_forward/core/form_review.py.
* Source-kind policy uses the same _source_document helper for candidate review and diagnostics. Alternative freshness uses the same _current path and per-report tuple cache.
* Exact case/schema/digest and non-human-only field eligibility precede counting alternatives; only DocumentUnavailable is excluded. No staging mutation.
* Completion evidence: ten exclusion conditions, current-conflict controls, per-field policy, byte/missing read reuse, outage propagation and later-request recovery all pass.

### External regressions and documentation

* P01-T03; src/core/tests/test_form_review.py and src/core/README.md.
* Added seven test methods plus one fixture helper, within maximum eight. No existing test removed or weakened; tests remain outside package.
* Snapshot tests isolate fields, new history, prior-only history and attachment references without relying on live history.
* Documentation records independent availability, local read reuse, alternative qualification and missing/service distinction without changing financial-authority claims.
* Baseline demonstration: all seven new methods run against unchanged form_review.py produced 34 assertion failures (7 tests, 2.081s), including disclosed missing-source history and stale alternatives reported as Conflict.
* Raw baseline command output retained externally: /tmp/1793310518369-copilot-tool-output-1353288-8a333b35-2008-4ec4-be8f-c6cdf6ed8391.txt.

### Single independent Review

* P02-T02; .copilot-tracking/reviews/logs/2026-10-29/finance-510-source-guards-review.md.
* Execution Complete; outcome Conformant; no findings, blockers or routed work.
* Assessed the bounded three-file implementation diff against baseline HEAD, all task evidence and AC1-AC6, not the entire PR.
* Independent checks pass: 26 review/pack tests, 17 staging tests, lint, formatting, typing and whitespace.
* Independent baseline replay of the final seven methods produced 36 assertion failures; the original earlier 34-failure run remains distinct historical evidence. No counts were substituted.
* Source fingerprints are recorded in the original Review; only lifecycle/evidence records change afterward.

### Local delivery

* P02-T02 complete. Commit 5ce4bae3 contains the reviewed three-file fix, external tests, README and all seven original dated RPI artifacts.
* Immediately before commit, SHA-256 values for all three reviewed files matched the original Review's fingerprints.
* Author and committer use authenticated account 8036360 / jmservera with repository-local 8036360+jmservera@users.noreply.github.com; Copilot coauthor trailer included.
* This lifecycle-only closeout records the already-existing implementation commit; no code or original critique/Review outcome is changed.
* No push, Azure operation, rubric-score edit or complete-publication-gate claim.

## Implementation-Time Plan and Detail Updates

* No material divergence. User's explicit full-loop request supplies bounded phase progression.
* Ordinary local judgment: missing-byte cache entries use None, so multiple unusable alternatives from one source do not repeat byte reads. Details updated from dict[str, str] to dict[str, str | None]. This implements the existing one-read requirement, not a new requirement or critique cycle.
* Existing manifests installed with pip editable core[dev] and agents into an isolated session environment only after command-not-found failure. No dependency manifest changes.

## Validation Record

| Check | Scope | Status | Evidence or reason |
| --- | --- | --- | --- |
| Initial exact requested commands | src/core | Unavailable | python, ruff and mypy each return command not found (exit 127); isolated setup now permitted |
| New regression baseline | Seven new external test methods | Failed as expected | 7 tests, 34 assertion failures against original implementation |
| First full regression run | test_form_review* | Passed | 26 tests, no skips |
| Requested discovery after final edits/format | PYTHONPATH=src:tests:../agents/src:../agents/tests python -m unittest discover -s tests -p 'test_form_review*' | Passed | 26 tests, 8.109s, no skips |
| Related staging | Same PYTHONPATH; python -m unittest test_form_staging -q | Passed | 17 tests, 4.428s, no skips |
| First static run | ruff check . | Failed, corrected | One E501 in new test context manager; targeted Ruff formatter corrected it |
| Core lint | ruff check . | Passed | All checks passed |
| Core format | ruff format --check . | Passed | 112 files already formatted |
| Core types | mypy | Passed | No issues in 165 source files |
| Diff whitespace | git diff --check | Passed | No errors |

Commands ran from src/core with the isolated environment's bin prepended to PATH.

## Pre-Review Reconciliation

* Plan markers/details reflect completed P01 and P02; implementation, validation, independent Review and local commit have evidence.
* Completed work, scope, validation and handoff are reconciled. No unimplemented source task or open code blocker.
* Follow-ups: none. The single independent Review completed with outcome Conformant and no findings; local implementation/evidence commit delivered.

## Blockers

* None for local implementation/review. Full publication gate, hosted/human approval and financial acceptance are not claimed.

## Remaining Work

* None. Local delivery complete; no push or Azure.

## Follow-Up Items

* None.

## Return-to-Caller State

* Implementation execution: Complete; Review Complete / Conformant.
* Full-plan delivery: Complete, P01/P02 and all task markers; local commit 5ce4bae3, no push authorized.
* Validation coverage: 26 review/pack tests, 17 related staging tests, core lint/format/types.
* Current plan/details reconciled; original critique remains Complete / Pass. No follow-up or design blocker.
* Task completed; bounded manual session stopped. Original evidence and adverse historical validation attempts are preserved.
