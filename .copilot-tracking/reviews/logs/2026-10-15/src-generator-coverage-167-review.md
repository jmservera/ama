<!-- markdownlint-disable-file -->
---
title: Generator coverage acceptance review
description: Single issue 167 review, engineering result and residual routing
ms.date: 2026-10-15
---

## Scope and Evidence

Task #167, `src-generator-coverage-167`, reviewed 2026-10-15.
Assessed boundary: metadata-only validator/report, tests and documentation;
issue-level acceptance remains broader than this bounded engineering slice.

* Research: .copilot-tracking/research/2026-10-15/src-generator-coverage-167-research.md
* Plan: .copilot-tracking/plans/2026-10-15/src-generator-coverage-167-plan.md
* Details: .copilot-tracking/details/2026-10-15/src-generator-coverage-167-phase-details.md
* Critique: .copilot-tracking/reviews/2026-10-15/src-generator-coverage-167-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-15/src-generator-coverage-167-changes.md
* Source: src/core/src/zava_forward/core/synthetic/coverage.py
* Tests: src/core/tests/test_generator_coverage.py

## Opening Review State

Goal: compare the approved metadata contract with implementation, local results,
owner boundaries and retained follow-ups. Evidence set is current and reviewable.
P01-T01/T02 and P02-T01 are complete; P02-T02 publication belongs to the
orchestrating parent after this review. Acceptance basis is issue criteria,
the bounded plan and PC-001 disposition. Read-only comparison; only this
record may change during Review. No blocker prevents engineering assessment.
Missing owner/private/live evidence limits issue acceptance, not this review.

## Execution Status

Complete. Exactly one post-implementation Review, performed inline because the
two new modules and focused documentation fit one direct comparison.
No repeat Review or correction loop.

## Plan-to-Change Reconciliation and Completed Work Assessment

| Marker | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Typed standard-library validator; 7 positive/negative/CLI tests | Reconciled. All 13 rows reported; IDs/routes/rationale/declarations guarded; no partial stdout on invalid input |
| P01-T02 | Core/pack READMEs, reference index, appended log | Reconciled. Links resolve by relative path/heading inspection; existing log prefix retained; no owner acceptance inferred |
| P02-T01 | Changes command ledger; full suites and local subprocess smoke | Reconciled. All five src suites and static checks pass; failures/corrections and skips explicit |
| P02-T02 | Commit/push/PR authorization and intended Refs #167 linkage | Pending parent publication, not unimplemented source; no merge authorized |
| Follow-Up Items | Research C6, pending inventory open_items and unchanged partial rows | Retained outside active implementation, not silently waived |

Code comparison confirms input is an explicit metadata path, report stdout is
deterministic, and invalid input has nonzero contextual diagnostics.
Report sorts rows/issues, preserves pending owner items and separates
routing_validated from output conformity, owner approval and application
acceptance. Core imports only the standard library; dependency-rule suites
pass. No SQL, new dependency, workload import, generator or image change.
No forbidden configuration/issue-export paths or private dataset enter the diff.

## Implementation-Time Plan and Detail Update Assessment

PC-001 was addressed directly with worktree-local ignored scratch parents;
tests explicitly place temporary metadata under tests/__pycache__ and the
smoke/suites use src/core/.venv/tmp. Cleanup and exact-process shutdown are
recorded. Formatter correction and agents discovery-command correction are
ordinary local execution fixes, not material plan changes. Restoring existing
dependency pins followed demonstrated missing-tool failures, using pip only.
No significant/divergent revision or unapproved dependent work occurred.
The sole critique remains historical with its Revise verdict and resolved
disposition; it was not rerun or misleadingly relabelled Pass.

## Findings and Plan Follow-Up Assessment

No in-scope implementation defect found. The following residuals prevent
claiming full issue/application acceptance; they are not new active plan tasks.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Universal per-record synthetic convention is not evidenced

Evidence: research C6 and scale_fixture homes/events source; inventory declares
is_synthetic on every record, while these records rely on manifest labels.
Impact: routing/declaration validation cannot tick full generator conformity.
Destination: distinct #167/#176 follow-up, planning before changing historical
payload/version/hash contracts. Smallest action: reconcile intended per-record
rule with versioned output and existing determinism tests; do not alter old
snapshots silently.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Owner ratification and private regeneration remain unavailable

Evidence: unchanged inventory open_items, W1/W2/W4 and partial SN-01.
Impact: owner mapping/row-owner approval and stock regeneration cannot be
inferred from child issue closure or the metadata gate.
Destination: owner decision under #167/#168, then rpi-plan if scope is approved.
Smallest action: confirm mapping and decide private register generator/source
scope or explicitly record an owner deferral. No private data was accessed.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Scope, full-scale and real-platform acceptance are not produced

Evidence: SN-03/08/09 open decisions; SN-11/12 partial; Docker denial and
97 environment skips in the changes ledger. Smoke does not perform inference.
Impact: local metadata/SQLite checks cannot prove delivered AI/SQL/Azure,
full-volume load, full profiles/workflows, human review or consent.
Destination: existing #103/#144/#172/#109/#176 workstreams and CI; owner scope
decisions first. Smallest action: retain unticked criteria, allow existing CI
to provide image/SQL Server checks, and obtain named scope/evidence separately.

## Defects and Routed Findings

| Class | Destination | Owner or next action |
| --- | --- | --- |
| In-scope implementation defect | None | No source correction identified |
| Output-convention residual, RV-001 | Distinct follow-up, then rpi-plan | Reconcile labels with historical snapshot compatibility |
| Owner decision gap, RV-002 | #167/#168 owner, then rpi-plan | Mapping and private regeneration scope/deferral |
| Scope/evidence residual, RV-003 | Existing workstreams and CI | Scope/volume approvals before data-consuming implementation |

Later work does not require another Review inside this lifecycle.

## Validation Evidence

| Check | Status and result |
| --- | --- |
| Five src suites | Passed: core 305, agents 70, api 472 (97 skipped), orchestrator 17, importer 39 |
| Ruff lint/format and mypy | Passed in all five projects; new files have no exemption |
| New metadata tests | Passed, 7 tests including malformed JSON/encoding/missing file and deterministic CLI |
| Existing generator/inventory/determinism tests | Passed in core, without private register access |
| Migration regressions | Passed, 25, after restoring existing missing pptx/PIL dependencies |
| Actual API subprocess, fictional SQLite/ZF_DATA | Passed health/static/case 200; assistants 401 unauthenticated, 200 authenticated; child stopped |
| Git diff and local links | Passed diff check and focused path/heading review; unchanged inventory/scenario binding |
| Docker | Unavailable: socket permission denied; rely on CI |
| Actual SQL Server/model/Azure and human acceptance | Not produced; local tests do not establish these gates |

## Outcome and Closeout Routing Record

Outcome: Residual work. The bounded engineering deliverable is supported by
local evidence, with no in-scope defect found. Full #167 acceptance remains
open for RV-001/RV-002 and broader evidence must not be represented as complete.
Use Refs #167, not an automatic closing reference.

Execution Complete is separate from issue acceptance. Parent may publish the
reviewed code and evidence, leaving unmet items unticked, then await CI and
owner decisions. No new source implementation is authorized by this review.
