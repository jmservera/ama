---
title: Issue 176 recovery review
description: Fresh recovery assessment with explicit evidence and acceptance limits
ms.date: 2026-10-17
---

## Task, Scope and Opening State

Task 176; synthetic-determinism-176. PR #368. One recovery Review explicitly
requested after Research, Plan verification and implementation inspection
performed in that order on 2026-10-17. This does not rewrite the prior Review
or claim that its disappeared logs or independent MERGE receipt were recovered.
Reviewed application head: `196972dc0dac256cdfd41f70bc06e7cad5fbebf2`.
Recovery writes so far are new dated tracking files only.

Plan/details/changes are reconciled: P01 inspection and validation complete,
P02 Review/publication pending. Fresh scoped tests and whole-core checks
passed. No application bug/change; original acceptance gaps retained.
Review is inline/read-only because evidence fits the current context.
No delegated review, cloud call, dataset access or independent approver
impersonation. Execution: Complete. Outcome: Residual work.

## Artifact Set

* .copilot-tracking/research/2026-10-17/synthetic-determinism-176-research.md
* .copilot-tracking/plans/2026-10-17/synthetic-determinism-176-plan.md
* .copilot-tracking/details/2026-10-17/synthetic-determinism-176-phase-details.md
* .copilot-tracking/plans/2026-10-16/synthetic-determinism-176-critique.md
* .copilot-tracking/changes/2026-10-17/synthetic-determinism-176-changes.md
* .copilot-tracking/changes/2026-10-17/synthetic-determinism-176-tests.txt
* .copilot-tracking/changes/2026-10-17/synthetic-determinism-176-lint.txt

Historical comparison: 2026-10-16 research, plan, phase details, changes,
Review and state, current issue text and PR acceptance audit; actual feature
diff and source/helpers/tests read during implementation inspection.

## Plan-to-Evidence Reconciliation

| Area | Assessment |
| --- | --- |
| Research | Executed now, wider/deeper/contrarian in order; current issue/PR, ancestry and missing-source claims assessed |
| Plan verification | Executed now against original plan/details and one existing critique; no new implementation candidate or critique loop |
| P01-T01 | Complete source/helper/test inspection, exact diff and documentation comparison; no introduced defect found |
| P01-T02 | Fresh exact output: 45 scoped tests, no skips; whole-project core Ruff check/format and mypy pass |
| Original PC-001 | Finding-disposition gate retained; no unresolved introduced source blocker, all acceptance/reporting gaps explicitly disposed below |
| Original PC-002 | Current code and passing oracles preserve raw-byte/read-once/BOM/CRLF/date/case/refusal behavior |
| Implementation updates | Missing installed package resolved by declared pip install into exclusive venv; no dependencies, source/tests or confirmed intent changed |
| P02-T01 | This single new recovery Review is Complete; not a recovered historical independent MERGE |
| P02-T02 | Publication still pending at review completion; parent owns commit/push/PR update and closeout, not a second Review |

The original Review/changes report historical source delivery and scoped
checks; this recovery reports direct new execution. The independent prior
MERGE decision is caller-reported only. Current formal GitHub reviews and
comments are empty; available session lookup also returned no receipt.
These facts limit provenance but do not negate the caller's report.

## Git and Check Claim Assessment

`origin/main` is `4ca6c7318ee4be35cef8c5ea6eee3425bf1421c4` and is already
an ancestor of reviewed head `196972d`. No `HEAD..origin/main` commits or
`HEAD...origin/main` delta were found at recovery intake or pre-publication
review. There is no new main code to integrate. The twelve check runs
were retrieved via the commit API and all bind to the full reviewed SHA:
test, image, mssql, validate, image-paths, src-namespace, src-no-working-data,
src-core, src-api, src-agents, src-orchestrator, src-importer.
These are historical hosted successes, not checks on the forthcoming
recovery commit.

Historical merged-main changes are not universally docs-only: `196972d^1`
to `196972d` includes #175 privacy source/tests; `1a1d88c^1` to `1a1d88c`
contains climate documentation/tracking, including the core README.
Feature source/test, core pyproject and source CI have no delta from
`f822bb9` through `196972d`; #175 privacy source/tests at `196972d` match main.
Thus no-post-reviewed-head drift is verified; the broader historical
docs-only characterization is rejected. No merge time is invented for an
unavailable independent review receipt.

## Acceptance Audit Against Current Issue

| Issue criterion | Result | Evidence / boundary |
| --- | --- | --- |
| Same seed/as-of gives byte-identical output for each generator including stock register and sensor data | Unmet overall | All available scoped replay tests pass on constructed inputs. Original OSM stock generator/pinned inputs/runtime absent; fictional scale is not continuing-stock reproduction. |
| Manifests record seed, version and generator revision | Partial overall | Available executable receipts and hashes pass; historical manifests untouched, missing original generator cannot emit a new receipt. |
| Refresh policy states cadence, approvals and live seeded-record protection | Met as documentation only | Trigger-only cadence, named owner approval, versioned new paths/reset authority explicit; refusal and fixture-backed SQLite restart pass. No policy adoption, live SQL reset or operational approval performed. |

## Findings and Explicit Dispositions

### RV-001 [Medium]: Original stock reproduction and receipt remain unavailable

Evidence: current issue, research C1/C7, original RV-001 and current source
inventory. Impact: AC1 remains unmet overall and AC2 partial. Disposition:
retained as a disclosed acceptance gap, not replaced or declared fixed.
Destination: distinct owner-supplied source/input/runtime follow-up, then
`rpi-research`. No private access or replacement is authorized.

### RV-002 [Low]: Refresh policy still lacks owner adoption

Evidence: published proposed policy and original RV-002. Impact: a documented
definition is not authority for publication/seeding/reset. Disposition:
retained; no approval invented. Destination: distinct named-human
approval/amendment follow-up, then `rpi-plan` if implementation is needed.

### RV-003 [Low]: Prior independent MERGE provenance is not recovered

Evidence: supplied report versus empty current GitHub reviews/comments,
historical inline Review outcome Residual work and unsuccessful scoped
receipt lookup. Impact: recovery cannot independently attest that specific
past approval, its time or its complete evidence. Disposition: explicit
limitation in recovery research/review and final handoff; do not relabel
this inline recovery Review as an independent MERGE. Destination: coordinator
retains or supplies the original independent receipt if needed for merge.
The related overbroad docs-only merge claim is corrected in this evidence,
with actual git comparisons; no source remediation is required.

## Validation and Safety Assessment

| Check | Result |
| --- | --- |
| Initial system Python scoped test attempt | Failed before test bodies: missing installed zava_forward, four import errors; declared pip install resolved |
| Fresh four-module run | Passed: 45 tests, no skips, 10.154s, exit 0; direct tracked output |
| Core project Ruff check / format | Passed: all checks, 47 formatted files, exit 0 |
| Core project strict mypy | Passed: 100 files, exit 0 |
| Diff whitespace before publication | Passed; parent will include new artifacts in staged diff check |
| Runtime/application/source/tests/docs change during recovery | None; git diff against reviewed head on protected/application/documentation trees is empty |
| Historical twelve exact-head hosted checks | Verified SUCCESS for 196972d, not claimed rerun by this recovery |
| Lost historical `/tmp` execution logs | Unavailable, not reconstructed |
| Standalone 30-home smoke from original changes | Historical only; no claim of fresh separate smoke; current tests execute CLI subprocesses |
| Original stock, private/continuing data, Azure/live SQL/model | Not accessed or run; excluded |
| Human adoption/operational acceptance | Unperformed; not inferred |

Only existing fictional fixtures/temporary outputs were executed. No new
replacement register or generated data is published. The owned pip venv
is temporary, with direct output already durable; parent cleans its exact
path after validation. No unrelated edits, .env/.vscode writes, secrets,
cost-bearing commands, history rewrite or merge.

## Outcome and Routing

Execution Complete; outcome Residual work, not full issue Conformant/MERGE.
No introduced implementation defects identified; no behavior changes needed.
Recovery evidence is suitable for coordinator consideration after normal
publication, without implying final merge authority. RV-001/002 retain their
distinct owners and prerequisites; RV-003 remains a provenance limitation,
not a fabricated approval or a new coding task.

Return to the user-directed parent for commit/push and PR evidence update.
No additional critique, Review, source work or follow-up loop is scheduled.
