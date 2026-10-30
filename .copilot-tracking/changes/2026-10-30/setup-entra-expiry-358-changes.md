---
title: Setup Entra expiry issue 358 changes
description: Current-source offline verification and acceptance reassessment
ms.date: 2026-10-30
---

## Metadata

Task ID: 358. Implementation date: 2026-10-30.
Plan: .copilot-tracking/plans/2026-10-30/setup-entra-expiry-358-plan.md.
Details: .copilot-tracking/details/2026-10-30/setup-entra-expiry-358-phase-details.md.

## Execution Status

Full plan declared; P01 and P01-T01 through P01-T03 complete for bounded
offline reassessment. Full issue AC2 remains unmet. The separate postcommit
full gate is pending after the final administrative reconciliation commit.
Write boundary: dated tracking artifacts and `infra/README.md` only.
Existing implementation and regressions are already merged; no speculative
source changes or duplicate tests. No web changes.

## Implementation-Time Plan and Detail Updates

PC-001 from the one critique was directly rejected with evidence: it asserts a
project-only filesystem restriction absent from parent context. Explicit caller
shared lock and developer-provided session files root are retained. The
original Complete / Revise critique is unchanged; no second critique.

## Validation Record

Default Python 3.12.3 reports missing ruff, mypy, aiohttp and installed
zava_forward namespace. Missing dependencies justify run-owned pip environment
setup. Heavy execution retains exact caller lock with 600-second admission.
Individual command outcomes recorded below.

### Completed offline infra checks

P01-T01 partial progress: under the exact shared lock,
`python3 -m unittest discover -s infra/tests -p test_setup_entra.py -q`
passed 124 tests in 3.335s, exit 0. This includes the seven behavioral mutations
and `test_legacy_cli_delegates_public_url_without_reimplementing_setup`.
`python3 -m unittest discover -s infra/tests -p test_initialize_api_auth.py -q`
passed 17 tests in 0.028s, exit 0.
API unittest discovery passed, exit 0: 1370 tests in 487.357s, 318 skipped
(1052 not skipped). Skips remain skips, not execution or browser/SQL acceptance.
The user-supplied PYTHONPATH selector was used verbatim from `src/api`.
Mypy passed, exit 0: no issues in 116 source files.
The first Ruff lint/format invocations both exited 2 before analysis because
the run-owned `RUFF_NO_CACHE=1` environment value is invalid; Ruff accepts
`true`/`false`. This is a validation-command setup error, not a source failure.
Original logs retained. Retry changes only that environment value to `true`
under the same shared lock; lint and format retries both passed, exit 0.
Ruff 0.17.1 reports all checks passed and 60 files already formatted.
Mypy version 2.4.0.

Run-owned external evidence root:
`/home/azureuser/.copilot/session-state/ff88c0b4-017d-4da1-9a9a-a3ea3c2615fd/files/issue-358`.
Install log: `install.log`; validation logs: `infra-setup.log`,
`infra-initialize.log`, `api-unit.log`, `api-ruff.log`, `api-format.log`,
`api-mypy.log`; individual exit statuses: `results.tsv`.
Python 3.12.3, isolated venv, pip-installed existing editable core[sql,blob],
agents and api[dev] distributions. No uv or credential lookup.

## Completed Work

### Current runbook reassessment

`infra/README.md` adds the dated current-source/local coverage result and
explicitly retains unmet originally populated deployed-app/full-setup acceptance.
The historical 2026-10-17 and 2026-10-19 records are unchanged.
No production or test files changed; `git diff --name-only` across infra/scripts,
infra/tests and src is empty against the supplied base.

## Validation Summary

| Check | Result | Evidence |
| --- | --- | --- |
| Infra setup | Pass, 124 tests, no skips reported | infra-setup.log; includes seven mutations |
| Legacy initializer | Pass, 17 tests, no skips reported | infra-initialize.log |
| Required API discovery | Pass, 1370 tests, 318 skips | api-unit.log; exact caller PYTHONPATH |
| Ruff lint | Initial invocation error, corrected retry Pass | api-ruff.log and api-ruff-retry.log |
| Ruff format check | Initial invocation error, corrected retry Pass, 60 files | api-format.log and api-format-retry.log |
| Mypy | Pass, 116 source files | api-mypy.log |
| Whitespace / source preservation | Pass | git diff --check; empty source/test diff |
| Browser/axe | Not applicable to this delta | No web files changed; general-discovery skips are not browser acceptance |
| Full local gate | Pending post-commit attempt | No receipt claimed |

## Acceptance Evidence

| Criterion | Disposition | Evidence |
| --- | --- | --- |
| AC1 expired stored credential regression | Proven locally, already merged | Frozen-clock test plus seven-mutation test executed in 124-test suite |
| AC2 originally populated deployed-app/full setup preservation | Unmet | Caller prohibits Azure/credential access; historical synthetic component proof explicitly excludes this case |
| AC3 keep delegating legacy main after conflict integration | Proven locally, already merged | Existing delegation test executed; #352/#356 merged; current initializer main retained |
| AC4 dated current reassessment and local persistence | Proven locally | Original candidate/evidence committed as 097354d9e6a6738aab1ff5683d477cde59aaee51; 18-line runbook addition |

## Pre-Review Reconciliation

Plan and details mark P01-T01/T02 complete, P01-T03 pending. Their acceptance,
validation state and evidence agree. No code change, test addition/removal,
web edit or original evidence rewrite occurred. Original critique is retained
with explicit parent disposition. Ready for the one independent Review with
AC2 residual, and with no claim of full issue acceptance or publication.

## Blockers

AC2: no live originally populated deployed-app/full-setup preservation
verification allowed under caller limits. No offline substitute.

## Remaining Work

The single independent Review executed: Complete / Residual work. RV-001
routes live AC2 to FU1; RV-002 routes the existing local administrative handoff
to the parent. The original Review is preserved, not repeated or upgraded.
Original candidate/evidence local commit now exists:
`097354d9e6a6738aab1ff5683d477cde59aaee51`. Parent reconciliation completes
P01-T03's Review/local handoff without changing the original Review's snapshot.
Final administrative commit and separate postcommit full-gate attempt follow.
No full publication receipt, push, PR or hosted/human approval claimed.

## Post-Review Administrative Preparation

The three package metadata directories produced by this run's editable pip
install were copied to the external `metadata-archive` with a finite 15-file
SHA-256 inventory (`metadata-sha256.txt`). All copied bytes were verified with
`sha256sum --quiet -c` before relocating the original directories to external
`metadata-relocated`. No file was deleted, no historical tracking evidence was
pruned and no source/test file changed. `git ls-files --others --ignored
--exclude-standard` now reports no ignored candidate inputs.
This only prepares a clean committed candidate for gate preflight.

The final gate command is
`python3 tools/rpi-checks.py --all --base 9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19 --out /home/azureuser/.copilot/session-state/ff88c0b4-017d-4da1-9a9a-a3ea3c2615fd/files/issue-358/final-full-gate`.
The runner itself acquires the exact shared heavy lock (600-second timeout);
an outer flock would deadlock. Output goes to external `final-full-gate.log`
and any receipt stays external. This pre-gate snapshot makes no result claim.
The user supplied the reviewed base; current-main reconciliation, fresh final
receipt verification immediately before push and independent exact-head/
human/hosted approval remain coordinator-owned. No fetch/rebase/push occurs here.

## Follow-Up Items

FU1: separately authorized populated existing-app/full-setup preservation
evidence; coordinator/operator owns. Same item as canonical plan.
