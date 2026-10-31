---
title: Employee review-thread repairs 570 - independent RPI Review
description: One bounded post-implementation review of the uncommitted repair candidate
ms.date: 2026-10-31
---

## Scope and Evidence

* Task ID: 570-review-threads
* Slug: employee-review-threads-570
* PR: #601; existing branch fix/employee-identity-check-570.
* Assessed boundary: git diff HEAD for src/api/checks/employee_acceptance_check.py, src/api/tests/test_employee_acceptance_check.py, .github/workflows/src-ci.yml, tools/rpi-checks.py, src/api/README.md, docs/reference/README.md and docs/reference/log.md. Not the entire inherited PR.
* Starting HEAD: 62290cb850ad8ce6cad224ef4522e8ee6e3210f8.
* Observed origin/main: e64c6e6c9da407682de59b926944424f94f50671.
* Plan: .copilot-tracking/plans/2026-10-31/employee-review-threads-570-plan.md.
* Phase details: .copilot-tracking/details/2026-10-31/employee-review-threads-570-phase-details.md.
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/employee-review-threads-570-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-31/employee-review-threads-570-changes.md.
* Research: .copilot-tracking/research/2026-10-31/employee-review-threads-570-research.md.

## Opening Review State

* Interpreted review goal: independently assess the two repair threads against the caller-approved requirements, implementation, current RPI evidence and qualified validation.
* Review scope: P02-T02; P01 and P02-T01 completed implementation, with P03 publication pending.
* Evidence readiness: all five supplied task artifacts are present in the initial worktree listing; their substantive reconciliation is not yet assessed. Bounded source diff and branch/base identities have been inspected.
* Acceptance basis: cluster-only 1e-9 absolute centroid tolerance demonstrated through the real producer; strict point/geographic checks; post-install source-CI acceptance CLI using documented environment; coupled workflow digest update; missing-browser discovery qualification retained.
* First comparison boundary: reconcile the supplied artifacts with the seven-file uncommitted repair diff, then examine substantive validation and producer behavior.
* Active read-only boundaries: only this Review record may be written. No nested agents, second Review, source/other-artifact mutations, full API discovery or full local gate. Caller explicitly selects CI-only publication gating; no local-gate wait is required by this Review.
* Initial blockers: none identified for the bounded review. Hosted/publication/live acceptance has not been established.

## Execution Status

* Execution status: Complete.
* Review execution evidence: exactly one independent Review on 2026-10-31, with opening state persisted before substantive comparison. All five supplied task artifacts, the complete bounded implementation diff, relevant producer/consumer code, browser qualification/CLI and workflow were assessed directly. No delegation or second Review occurred.
* This execution status describes the Review, not completion of P03, the whole PR or original live #570 acceptance.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Cluster tolerance and regressions | Reconciled | Exactly two added methods, no removals; real producer remains unchanged; absolute 1e-9 containment slack applies only to clusters. |
| P01-T02 | Hosted execution and same-commit pin | Reconciled | Workflow invokes the maintained CLI immediately after install with the documented environment; only the src-ci.yml digest changes. Actual same-commit packaging remains P03 work. |
| P02-T01 | Initial static checks; verified command results | Reconciled | Recorded producer failure, successful focused/component checks and qualified skips are consistent across plan, details and changes. |
| P02-T02 | Pre-Review reconciliation | Reconciled at entry | Plan/details correctly leave Review pending before this worker executes. This record returns the completed result; parent owns marker reconciliation outside this worker's write boundary. |
| P03-T01 | Publication remains pending | Reconciled | No committed candidate, push, thread resolution or hosted success is falsely recorded. |
| Follow-Up Items | Live identity; hosted checks and owner merge | Reconciled | Kept outside synthetic repair completion and acceptance claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/checks/employee_acceptance_check.py; src/api/tests/test_employee_acceptance_check.py | Permit accumulated centroid roundoff without relaxing raw point or geographic validity. | Bounded diff changes only containment and adds two tests importing the real producer. | Reviewer reran three map tests, zero skips, and independently reproduced old rejection/new acceptance. | Conformant. |
| P01-T02 | .github/workflows/src-ci.yml; tools/rpi-checks.py | Enforce browser execution after setup rather than count qualified discovery skips as acceptance. | Two workflow lines plus its matching exact-byte digest; maintained CLI and discovery qualification unchanged. | Reviewer parsed job scope, working directory, order, environment and digest. | Conformant candidate; same-commit publication is pending. |
| P01-T02 | src/api/README.md; docs/reference/README.md; docs/reference/log.md | Document numerical boundary and hosted enforcement without claiming hosted/live success. | Owning guide and knowledge index agree; log entry is append-only. | Direct Markdown/diff review; existing relative API guide links resolve to the owning file/heading. | Directly related documentation is reconciled. |
| P02-T01 | Supplied changes and phase-details evidence | Record requested validation and its limits. | 18 focused tests, maintained CLI positive/negative runs, API discovery/static checks and 39 tool tests recorded. | Component evidence accepted as supplied, not represented as reviewer reruns. | Sufficient for this bounded Review. |

### Substantive logic and requirements assessment

* src/core/src/zava_forward/core/insights.py computes bounds from original coordinate extrema, accumulates each grid cell's latitude/longitude sums, then divides by count. Default MAP_CAP is 500. The new regression passes 501 unique fictional cases at (54.9, -1.6) through that actual producer with no alternate cap or fabricated centroid.
* Reviewer reproduction observed latitude 54.90000000000044 and longitude -1.600000000000014 against bounds [54.9, -1.6, 54.9, -1.6]. The adapter loaded from starting HEAD rejected this same produced payload; the candidate accepted it. The old adapter was compiled in memory only.
* The candidate uses an absolute tolerance of 1e-9 for clusters and zero for points. It expands all four containment edges only. Independent coordinate validity and bound validity execute before containment, so boolean, nonfinite and latitude/longitude outside exact +/-90 and +/-180 remain rejected even inside an expanded containment window. Bounds remain geographically valid and ordered.
* The table-driven regression covers both modes, both axes, both signs, exact containment edges, 5e-10 slack, 2e-9 rejection, exact geographic endpoints and tiny geographic violations. It checks boolean/nonfinite marker and bound coordinates. Existing malformed-bound, count, schema, kind and total/shown regressions remain; no existing tests were removed. Counts and duplicate-link logic are unchanged.
* The workflow job runs from src/${{ matrix.project }}, installs the editable project/dev dependencies, and applies the changed browser step only to API. Discovery remains before installation. The shell command's temporary PYTHONPATH matches the documented import environment and applies to the acceptance CLI immediately after Chromium installation.
* The maintained CLI selects exactly three named Chromium regressions and exits successfully only when unittest succeeds, testsRun equals three and skipped is empty. The unchanged discovery helper qualifies only the missing-executable error; other browser launch errors propagate. Consequently installation failure, failed browser execution, missing imports or qualified skips cannot produce a successful acceptance CLI step.
* The workflow and pin are both in the bounded uncommitted candidate. Their exact bytes match. That proves candidate coupling, not the future commit's contents.
* No producer, live sign-in, secret, application UI or deployment changes are present in the assessed diff. This is not an accessibility/UI audit or complete inherited-PR review.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| Scope; P01-T02 | Name directly related knowledge index/log alongside the API guide. | Repository knowledge-maintenance convention; no new behavior or divergent caller decision. | Current plan scope, details completion evidence and changes summary name these files. | Existing Complete / Pass critique covers owning documentation and bounded intent; no material replanning required. | Justified descriptive clarification. |
| P02-T01 | Preserve configured E501 exemption in isolated adapter checks. | Supplied isolated check found unchanged embedded JavaScript at line 158, 107 characters; caller explicitly requires retaining its exemption. | Current plan/details and changes explain exemption and all-other-selected-rules coverage. | Does not relax a newly introduced violation or change approved behavior; no material critique re-entry required. | Justified validation qualification, not an all-rules-clean claim. |
| P01-T01; P02-T01 | Change test bounds literals to floats after initial mypy failure. | Test-only list[int]/float assignment failure recorded in changes. | Candidate literals are floats; final static-check results recorded. | Ordinary in-scope typing correction; no material decision gap. | Reconciled; original failed attempt retained. |
| P02 completion/handoff | Replace pending validation with actual outcomes while leaving Review/publication pending. | Recorded focused/browser/component results. | Plan markers, detail phase status and changes Pre-Review Reconciliation agree. | Original critique remains a planning Pass, not implementation or hosted proof. | No stale completion claim at Review entry. |

## Critique and Material Revision Assessment

* Latest critique execution Complete / verdict Pass, zero PC findings: no outstanding dispositions exist.
* The implementation preserves the critiqued producer-derived fixture, two-method budget, numerical boundary, unchanged discovery/CLI contracts and paired workflow-pin intent.
* The documented index/log clarification, existing static-check exemption and test-only type correction are immediately relevant nonmaterial adjustments. They are reflected in current plan/details/changes and do not change accepted scope or user intent.
* No significant divergent decision, unsupported assumption or material revision requiring rpi-plan or rpi-research was identified.
* Phase dependency evidence supports research/critique before P01, completed P01 before validation/Review, and pending P03 after this Review. No evidence of premature publication or inherited hosted approval was found.
* Caller-authorized CI-only publication gating is preserved. No contrary full-local-gate prerequisite is introduced here; prior adverse records are neither rewritten nor relabelled.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Original #570 live employee acceptance / independent expected identity | Synthetic producer/Chromium repairs cannot attest a real employee account or deployed chat/map/case behavior. | Authorized original #570 acceptance owner must obtain independent tenant/object attestation before the separately authorized live acceptance process. | Open, distinct original-issue follow-up; not a repair defect, not added to active P01/P02. |
| Hosted CI and owner merge approval | A local uncommitted candidate cannot prove hosted execution or approval. | Publication parent performs P03 and observes the caller-selected hosted CI gate; owner retains merge approval. | Open, distinct hosted/owner actions. P03 is already planned work, not a new defect. |

## Findings

The complete substantive RV-xxx finding set is empty. Severity counts:
Critical 0; High 0; Medium 0; Low 0. No implementation defect, significant
decision gap or material evidence gap was identified within this boundary.
No synthetic finding ID is assigned to ordinary pending P03 work or the
explicitly excluded live acceptance follow-up.

## Defects

* None within the assessed repair candidate.

## Routed Findings

| Finding | Severity | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- | --- |
| None | None | None | No corrective RPI stage required. | Complete substantive finding set is empty. |

Later implementation of any independently discovered issue must not require a
second Review of this task or misrepresent this record's source boundary.

## Residual Work

* Original #570 live identity/employee acceptance remains a distinct follow-up owned by its authorized acceptance owner.
* Hosted CI observation and owner merge approval remain distinct future actions.
* Candidate publication and review-thread replies/resolution remain existing P03-T01 work, not residual implementation defects.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active work: parent reconciles P02-T02 completion and P02 status, then performs P03-T01 packaging, authenticated privacy-safe commit, non-force publication and evidence-based replies/resolution of the two addressed threads.
* Preserve the workflow and matching pin in that same commit. This Review cannot verify a not-yet-created commit, remote SHA or thread disposition.
* Hosted CI has not executed this uncommitted candidate. No full local gate, exact-head publication receipt, hosted approval, live acceptance or issue closure is established by this Review.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Reviewer: external task-owned venv python -B, PYTHONDONTWRITEBYTECODE=1, PYTHONPATH=tests:../core/tests:../agents/tests; three named map tests via unittest loader from src/api | Existing malformed payload test plus both added map methods | Passed | Three tests in 0.007 seconds, zero skips. No full API discovery rerun. |
| Reviewer: real insights.map_view plus git show HEAD adapter compiled in memory | Producer roundoff and candidate regression sensitivity | Passed | Same real 501-home payload rejected by original adapter and accepted by candidate; exact overshoot observed. No source mutation. |
| Reviewer: read-only YAML/AST/hash verification | Workflow order, job API condition, working directory, documented env and WORKFLOW_HASHES | Passed after probe correction | First probe stopped with reviewer-script KeyError on unnamed steps after map checks passed. Corrected probe uses s.get('name'); all assertions passed. This was a verification-script error, not a candidate failure. |
| Supplied acceptance/identity module execution | Synthetic acceptance and identity regressions | Passed, supplied evidence | 18 tests, zero skips, including three Chromium tests. Not independently rerun by reviewer. |
| Supplied documented maintained CLI | Three loopback Chromium regressions | Passed, supplied evidence | Exactly three tests, zero skips, exit 0. |
| Supplied CLI with empty browser path | Missing-browser qualification / fail-on-skip | Expected nonzero, supplied evidence | Three qualified skips, exit 1; not executed acceptance. |
| Supplied full API discovery | API component | Passed with skips, supplied evidence | 1441 tests in 613.621 seconds; OK(skipped=320). Aggregate reasons not enumerated by quiet output; no claim that these are all missing-browser skips. Not rerun per caller. |
| Supplied API Ruff check/format and mypy | API configured static checks | Passed, supplied evidence | Formatting 66 files; mypy 125 files. Initial test-only typing failure and correction retained in changes. |
| Supplied isolated adapter checks | Changed adapter | Passed with stated exemption, supplied evidence | Existing E501 exemption retained for unchanged embedded JavaScript line 158; all other selected isolated rules and isolated format passed. |
| Supplied tools unittest discovery and isolated static checks | Gate-tool tests and two-file static scope | Passed, supplied evidence | 39 tests; isolated Ruff/format and strict mypy pass. Inner negative-fixture failures are not outer suite failure. |
| Full local gate | Publication | Not run | Explicit caller CI-only/no-local-gate-wait direction; not a Review blocker. |
| Hosted CI, exact-head publication/approval and live acceptance | Beyond uncommitted repair Review | Unavailable / not performed | P03/hosted/owner/live follow-ups; no success inferred. |

### Reviewed candidate identity

These SHA-256 values bind the inspected source bytes, not an exact-head
publication assessment or receipt. Starting HEAD and observed origin/main
remain the values in Scope and Evidence; main ancestry was independently
confirmed with git merge-base --is-ancestor origin/main HEAD.

| Workspace-relative file | SHA-256 |
| --- | --- |
| src/api/checks/employee_acceptance_check.py | 862ef6241ef3d95a0326dd033e8c954441d36ecfacb2cfb1ef83527b5d4c9308 |
| src/api/tests/test_employee_acceptance_check.py | f4bf04f48f2b54e6c2eed0d9efc302c07ea25b5dbe414079dddb0ce4b11c1af9 |
| .github/workflows/src-ci.yml | 9964408b3a69e4bbc01955dcab15612e8794280f1170e6b2d67ec75672224262 |
| tools/rpi-checks.py | 8ac0c2cd9d0288e3e8b809febd5835f0f41bc32f4df9903d3879a424aa699113 |
| src/api/README.md | a49abcf212653dcf60e542375013168a9ed5782fd48466bcd299a2c874fc45f5 |
| docs/reference/README.md | 921e79e86a6a7e52041e841f2e2ef6a0987d424595633c4353cbff0f67a14d82 |
| docs/reference/log.md | 447447e52eaa0011cd9adce4f4bb28be40991be035a548192862d5f48367e9f6 |

## Outcome

* Outcome: Conformant.
* Outcome rationale: both caller-selected repairs satisfy their substantive requirements in the bounded uncommitted candidate. Producer-derived sensitivity and strict negative tests were independently verified; workflow/CLI execution semantics and matching digest were assessed directly. Nonmaterial descriptive adjustments are justified and reconciled. Explicitly pending publication/hosted/live work does not turn this bounded implementation Review into whole-task acceptance.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement correction required. |
| Decision gap or invalid assumption | None | No rpi-plan revision required. |
| Material evidence gap | None | No rpi-research re-entry required. |
| Non-blocking residual work | Distinct original #570 live acceptance and hosted/owner follow-ups | Original acceptance owner and publication parent respectively; preserve separate approval boundaries. |

* Execution status: Complete.
* Outcome: Conformant.
* Findings: zero at every severity.
* Validation coverage: independent three-test map rerun, real-producer original/candidate comparison and parsed workflow/digest verification; additional focused/browser/component/static evidence assessed as supplied.
* Blockers: none for Review; P03 and hosted/owner/live actions remain unperformed.
* Write boundary: only this canonical Review record was created/updated; no other source or artifact was edited. Final worktree listing retained the same pre-existing modified/untracked set plus this record.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/employee-review-threads-570-research.md](../../../research/2026-10-31/employee-review-threads-570-research.md) | Bounded producer and hosted-execution research |
| [.copilot-tracking/plans/2026-10-31/employee-review-threads-570-plan.md](../../../plans/2026-10-31/employee-review-threads-570-plan.md) | Current markers, requirements and follow-ups |
| [.copilot-tracking/details/2026-10-31/employee-review-threads-570-phase-details.md](../../../details/2026-10-31/employee-review-threads-570-phase-details.md) | Task boundaries and completion evidence |
| [.copilot-tracking/reviews/plans/2026-10-31/employee-review-threads-570-plan-critique.md](../../plans/2026-10-31/employee-review-threads-570-plan-critique.md) | Complete / Pass critique, zero findings |
| [.copilot-tracking/changes/2026-10-31/employee-review-threads-570-changes.md](../../../changes/2026-10-31/employee-review-threads-570-changes.md) | Implementation, validation and descriptive amendments |
| [.copilot-tracking/reviews/logs/2026-10-31/employee-review-threads-570-review.md](employee-review-threads-570-review.md) | This single completed Review |

## Next Steps

No user action is required for this Review. Return Complete / Conformant,
zero findings to the active parent for P02 marker reconciliation and P03
continuation under the caller-authorized CI-only gate. Preserve same-commit
workflow/hash coupling and qualified hosted/live claims. This worker stops
after this one Review and performs no publication, mutation of other evidence
or second Review.
