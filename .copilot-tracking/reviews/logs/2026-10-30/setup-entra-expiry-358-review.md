---
title: "Issue 358 setup Entra expiry independent Review"
description: "Single post-implementation Review of the current documentation and RPI evidence boundary."
ms.date: 2026-10-30
---

## Opening Review State

* Interpreted review goal: independently compare the complete supplied issue #358 artifact set and current diff without correcting implementation or evidence.
* Review scope: current 2026-10-30 task set on fix/setup-entra-expiry-358 against 9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19.
* Evidence readiness: named artifacts and state JSON are present; the tracked production delta is 18 added lines in infra/README.md. Detailed reconciliation follows.
* Acceptance basis: issue AC1-AC4, current plan and details, preserved critique dispositions, changes and supplied validation evidence. Actual originally populated deployed-app/token-store/full setup preservation is not established by mocks or synthetic history.
* First comparison boundary: requirements, task markers and critique disposition against current artifacts, source preservation and recorded validation.
* Active read-only boundaries: write only this original Review. No source/artifact corrections, additional agents or reviews, cloud, deployment, sign-in, credentials, gate attempt, commit or publication.
* Initial blockers: AC2 is unmet under the no-Azure boundary; local commit and full postcommit gate remain planned rather than completed.

## Scope and Evidence

* Task ID: 358. Review date: 2026-10-30. This is the single original post-implementation Review, not a correction or replacement of a historical Review.
* Observed branch: fix/setup-entra-expiry-358. Observed HEAD equals supplied base 9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19.
* Full current task set inspected: research, plan, phase details, original plan critique, changes and current state JSON, listed below. Current untracked task artifacts were read directly; a tracked-only Git diff would not include them.
* Production-documentation delta: exactly 18 added lines in infra/README.md, the dated "Offline acceptance reassessment (2026-10-30, Refs #358)" subsection. No tracked delta exists in infra/scripts, infra/tests or src against the supplied base.
* Supporting evidence: directly inspected frozen-clock and mixed-secret regressions, seven behavioral mutation killers, production preservation/expiry helpers, legacy delegating main, historical 2026-10-19 original Review and synthetic-summary exclusions.
* External validation logs and results.tsv were accessible at the caller-authorized session evidence root under files/issue-358. Only named local test/check outputs were read; no environment, credential, private dataset or deployed-resource contents were accessed.
* Related issue/PR lineage (#352, #356, #374 and #417) is supplied parent/research evidence, not newly authenticated or independently re-fetched by this Review.
* No tests, installs, cloud operations, gate, sign-in, credential access, commit, push or PR were performed by this reviewer. No additional agent or review was used.

## Execution Status

* Review execution status: Complete.
* The complete supplied current artifact set, full production diff, relevant unchanged source/tests and accessible raw validation results support a credible bounded verdict.
* Implementation execution status: Partial across the full plan. P01-T01 and P01-T02 are complete; P01 and P01-T03 correctly remain unchecked because this Review, local commit and postcommit gate attempt are administrative handoff dependencies. This record supplies the Review portion, not the remaining actions.
* Neither Complete Review execution nor successful local tests establish full issue acceptance.

## Plan-to-Change Reconciliation

| Current plan scope | Changes summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01, FR1-FR3 | Completed offline checks and validation summary | Reconciled | Direct logs agree with 124 setup, 17 initializer, API 1370/318 skips, Ruff retry success and mypy 116. |
| P01-T02, FR4 | Current runbook reassessment | Reconciled | Full tracked diff is the dated 18-line subsection; existing source, tests and tracked historical evidence have no delta. |
| P01-T03 and P01 | Remaining Review/local commit/gate attempt | Reconciled as pending | Review is the current operation; local commit and full postcommit gate attempt must not be retroactively reported complete. RV-002. |
| AC1 | Expired stored-credential regression | Proven locally | Frozen clock covers both names and expiry boundaries; mutation killers execute in the passed setup suite. |
| AC2 | Originally populated deployed-app/full setup preservation | Unmet, explicitly residual | Neither FakeAzure nor the historical real temporary synthetic roundtrip covers this literal criterion. RV-001. |
| AC3 | Delegating legacy main after merged integration | Proven locally, lineage supplied | Direct source retains runpy delegation and setup-suite evidence covers the delegation regression. No new conflict integration was required. |
| AC4 | Dated reassessment and local persistence | Prepared, not fully complete | Documentation and current evidence exist; local commit remains outstanding. RV-002. |
| Follow-Up Items FU1 | Separately authorized populated-target exercise | Reconciled | Same operator/coordinator-owned item appears in plan and changes; not silently added to active implementation. |
| Current state JSON | Review active, AC2 blocker, next action one Review | Reconciled at review entry | Artifact pointers match. prioritized_follow_ups is null, but AC2 and its resolution are explicitly retained in blockers; canonical FU1 is not lost. Parent owns post-Review state update. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/tests/test_setup_entra.py; infra/tests/test_initialize_api_auth.py; src/api | No code/test delta; freshly execute already-delivered safeguards and requested project checks | External raw logs and per-command exits agree with changes | Passed with API skips and initial Ruff invocation errors preserved | Appropriate evidence-only implementation; no demonstrated need for duplicate source/tests. |
| P01-T02 | infra/README.md | Add current dated acceptance boundary next to prior preservation evidence | Exactly 18 added lines; no deletions | Full diff and whitespace review | Accurately distinguishes local proof, historical synthetic proof and unmet deployed-target criterion. |
| P01-T02 | Current research, plan, details, critique, changes and state | Persist decisions, validation, critique disposition and bounded handoff | Full named set inspected directly | Marker/detail/changes/state comparison | Consistent stage-specific records; research's open question table and pending-validation wording are pre-implementation snapshot text, answered by its synthesis and later execution evidence, not current validation failure. |
| P01-T03 | This Review | Independent one-pass comparison and routing | This original record | Evidence comparison only | Review portion complete; no authority to finish commit/gate or alter predecessor records here. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 and critique disposition | Retain exact parent-authorized shared lock and external environment/log root rather than substitute isolated project-local admission | Caller explicitly requires the shared lock; supplied parent context permits the session directory and rejects PC-001's asserted parent restriction | Plan, details, changes and state all record the same rejection and retained paths | Original critique remains Complete / Revise, Medium PC-001 | Justified context correction, not an unexplained waiver or changed acceptance direction. Reviewer does not create or acquire any lock. |
| P01-T01 validation | Correct RUFF_NO_CACHE from invalid 1 to true and rerun lint/format | Initial commands exited 2 before analysis; raw errors and retry outputs preserved | Details and changes distinguish failures from successful retries | No material scope change; no source correction | Supported command-setup correction; first runs are not labelled passed. |
| P01-T01/T02 completion markers | Mark completed checks and dated runbook work while leaving P01/T03 pending | Actual local results and documentation diff | Checklist, details completion evidence, changes and Review-active state agree | Critiqued bounded offline direction unchanged | Descriptive implementation updates preserve confirmed user intent; no fresh planning or critique needed. |
| P01-T03 postcommit gate | Explicitly retain a full gate attempt after local commit, without an outer double-lock | Repository local-gate requirement and parent handoff | Plan/details/changes agree that no attempt or receipt yet exists | Administrative continuation only | Appropriate prospective requirement, not evidence of gate success. RV-002. |

## Critique and Material Revision Assessment

* Exactly one current critique is present: execution Complete, verdict Revise, one Medium PC-001. Its original finding and verdict remain intact.
* PC-001 asserts a project-only runtime restriction and recommends replacement writable paths/shared-lock coordination. The parent explicitly rejects the premise for its own runtime, citing the caller's exact shared lock and developer-provided external session directory. This Review assesses that supplied parent-context disposition; it does not project this reviewer's narrower filesystem restrictions backwards onto the parent's execution.
* The retained shared lock avoids falsely claiming coordination from an isolated replacement. Actual command admission is reported by the implementation record and parent; the inspected result logs establish command outcomes, not an independent process-level lock audit.
* No material unaccepted scope, architecture or acceptance change is evident. Zero source/test additions, canonical ownership, no-cloud/credential boundary and FU1 remain unchanged. No evidence in the supplied records indicates dependent work resumed before disposition; detailed process chronology is not reconstructed independently.
* The historical 2026-10-19 original Review remains Partial / Residual work. The synthetic summary expressly excludes originally populated deployed-app, full secret_reference/password creation and token-store/auth consumption acceptance. Those limitations are preserved, not upgraded by this Review.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| FU1 | Required actual populated target and full setup observation would exceed explicit no-Azure/no-credential authority | Coordinator/operator obtains separate authorization and scopes the real exercise with original-population and binding evidence | Open; RV-001 routes to this distinct follow-up, not a defect or additional active P01 task. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Literal deployed-target preservation acceptance remains unmet

* Related scope: AC2; FR2 acceptance boundary; FU1.
* Evidence: Current plan AC2, changes Acceptance Evidence, state blocker and infra/README.md explicitly retain UNMET status. The historical synthetic-summary exclusions and original Review corroborate the missing original populated-app/full-setup case. Current local tests use FakeAzure.
* Impact: Full issue acceptance and closure are unsupported. Passing metadata/mutation checks and a real but synthetic component roundtrip cannot prove originally populated deployed-app/token-store/full setup preservation.
* Classification: Known residual acceptance work, not a newly introduced implementation defect or an invalid current plan assumption.
* Destination: Distinct follow-up FU1, coordinator/operator-owned separately authorized live work.
* Smallest useful next action: Keep AC2 unmet and #358 referenced only; outside this run, obtain explicit authority and define the genuine populated-target/full-setup evidence and preservation safeguards before any operation. This Review authorizes none.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Local persistence and postcommit validation remain administrative handoff work

* Related scope: P01-T03, P01 and AC4.
* Evidence: Current HEAD still equals base; candidate documentation and task artifacts are uncommitted. Plan/details/changes explicitly leave local commit and full postcommit gate attempt pending. No receipt is present or claimed.
* Impact: Prepared artifacts do not yet satisfy AC4's local persistence requirement, and check summaries are not a full candidate gate or publication approval.
* Classification: Expected remaining administrative handoff, not premature completion or a source defect.
* Destination: Existing P01-T03 parent/coordinator continuation, distinct from FU1 and from later defect implementation.
* Smallest useful next action: After receiving this original Review, parent performs only the authorized local identity/commit handoff using Refs #358 and the required coauthor trailer, then attempts the planned full postcommit gate and records its actual result. Do not push, open a PR or turn an unavailable/failed gate into a passing receipt. This reviewer does not perform those actions.

## Defects

* No demonstrated production, regression-test or current runbook defect within the reviewed delta.
* Neither residual finding requires rpi-implement, rpi-plan or rpi-research in this bounded run. A second Review is not required by these routes.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001, Medium | Distinct FU1 | Coordinator/operator, separately authorized actual populated-target exercise | Explicit known residual criterion; not safely executable here. |
| RV-002, Low | Existing P01-T03 handoff | Parent/coordinator, authorized local commit then gate attempt | Planned administrative continuation; not a new implementation task or acceptance claim. |

## Residual Work

* FU1 remains outside the permitted run and outside bounded implementation completion. It is the only unresolved plan Follow-Up Item.
* P01-T03 remains the existing local handoff task until parent reconciliation and actual execution; this Review does not change its marker.

## Blockers and Remaining Work

* AC2 is blocked by the explicit no-Azure/no-credentials authority boundary. This does not block completion of this offline Review.
* AC4 local commit and postcommit full gate attempt remain pending; full receipt, current-main verification, hosted checks, human approval and issue acceptance are not established.
* No remote publication, deployment or new live authority is granted. Any later candidate change invalidates prior candidate-specific validation as required by repository policy.

## Validation Evidence

External root read-only evidence: /home/azureuser/.copilot/session-state/ff88c0b4-017d-4da1-9a9a-a3ea3c2615fd/files/issue-358.
Commands below were performed by the implementation parent, not rerun by this Review unless explicitly identified.

| Command or check | Scope | Status | Evidence and limitation |
| --- | --- | --- | --- |
| python3 -m unittest discover -s infra/tests -p test_setup_entra.py -q | Existing setup suite | Passed | infra-setup.log: 124 tests, 3.335s, OK; results.tsv exit 0. Direct source includes both expiry-guard mutation killers among seven, mixed-secret assertions and delegation coverage. |
| python3 -m unittest discover -s infra/tests -p test_initialize_api_auth.py -q | Legacy initializer | Passed | infra-initialize.log: 17 tests, 0.028s, OK; exit 0. Direct main source delegates through runpy. |
| PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q, from src/api | Requested API discovery | Passed with skips | api-unit.log: 1370 tests, 487.357s, OK, 318 skipped; exit 0. Only 1052 were not skipped. Exact command/working directory supplied by implementation records. |
| ruff check . and ruff format --check ., initial | API lint/format invocation | Failed before analysis | Both original logs show invalid --no-cache value 1, accepted true/false; results.tsv exits 2. Not source-check failures and not discarded. |
| ruff check . and ruff format --check ., retries with RUFF_NO_CACHE=true | API lint/format | Passed | api-ruff-retry.log: All checks passed; api-format-retry.log: 60 files already formatted; separate exits 0. |
| mypy, from src/api | Static typing | Passed | api-mypy.log: no issues in 116 source files; exit 0. |
| Shared flock admission | Heavy checks | Recorded, not independently reconstructed | Parent/plan/changes retain exact caller lock with 600-second wait. Result logs do not independently establish acquisition timing. No alternate lock or fresh heavy run performed here. |
| git diff --check against supplied base | Current tracked delta | Passed by reviewer | Exit 0; full diff inspected. |
| git diff --name-only against supplied base, scoped to infra/scripts infra/tests src | Source and test preservation | Passed by reviewer | Empty output. HEAD equals base; only tracked production delta is infra/README.md. Historical tracked source/evidence remain unchanged. |
| Browser/axe, SQL, deployed-resource and live sign-in acceptance | Beyond current documentation delta | Not performed | No web change; API skips are not browser/SQL acceptance. Live operations and credentials prohibited. |
| tools/rpi-checks.py --all --base supplied-base --out external-output | Complete postcommit gate | Pending, not run by reviewer | Planned after local commit; no full receipt or hosted/human approval claimed. |

## Outcome

* Outcome: Residual work.
* Rationale: Completed bounded documentation and fresh local evidence match the accepted plan, with source/test preservation and a justified PC-001 parent-context disposition. AC2 remains substantively unmet and AC4/local handoff is not yet complete. Conformant or issue-accepted would overstate the evidence; Not accepted or Defects found would misclassify the acknowledged outside-authority residual as a new defect.
* Severity summary: Critical 0; High 0; Medium 1; Low 1.
* Review execution: Complete. Full implementation-plan execution: Partial.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No demonstrated defect requiring later rpi-implement. |
| Decision gap or invalid assumption | None unresolved | PC-001 explicitly disposed using supplied parent-context evidence; original critique preserved. |
| Material research gap | None in the bounded offline review | Do not route prohibited live acceptance into another offline research loop. |
| Non-blocking residual acceptance work | FU1, RV-001 | Coordinator/operator separately authorizes and scopes actual populated-target preservation. |
| Planned administrative remainder | P01-T03, RV-002 | Parent local persistence and full postcommit gate attempt; preserve actual outcome and no-publication boundary. |

* Validation coverage: raw local test/static-check outcomes verified against recorded summaries; source/test preservation and production diff directly checked. No independent live acceptance, process-level lock audit or full-gate receipt.
* Blockers: AC2 authority/evidence boundary; AC4 and gate remain administrative pending work, not hidden passes.
* This record is the one original Review. No source/artifact correction or second review is requested or performed.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/setup-entra-expiry-358-research.md](.copilot-tracking/research/2026-10-30/setup-entra-expiry-358-research.md) | Current research and source/lineage evidence |
| [.copilot-tracking/plans/2026-10-30/setup-entra-expiry-358-plan.md](.copilot-tracking/plans/2026-10-30/setup-entra-expiry-358-plan.md) | Current requirements, markers, critique disposition and FU1 |
| [.copilot-tracking/details/2026-10-30/setup-entra-expiry-358-phase-details.md](.copilot-tracking/details/2026-10-30/setup-entra-expiry-358-phase-details.md) | Execution details and completion boundaries |
| [.copilot-tracking/reviews/plans/2026-10-30/setup-entra-expiry-358-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/setup-entra-expiry-358-plan-critique.md) | Preserved original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-30/setup-entra-expiry-358-changes.md](.copilot-tracking/changes/2026-10-30/setup-entra-expiry-358-changes.md) | Validation, acceptance and handoff evidence |
| [.copilot-tracking/rpi-sessions/2026-10-30/setup-entra-expiry-358-state.json](.copilot-tracking/rpi-sessions/2026-10-30/setup-entra-expiry-358-state.json) | Current Review-active state and AC2 blocker |
| [infra/README.md](infra/README.md) | Only production-documentation delta |
| [.copilot-tracking/reviews/logs/2026-10-19/live-keyvault-preservation-358-review.md](.copilot-tracking/reviews/logs/2026-10-19/live-keyvault-preservation-358-review.md) | Historical Partial / Residual work boundary |
| [.copilot-tracking/changes/2026-10-19/live-keyvault-preservation-358-synthetic-summary.json](.copilot-tracking/changes/2026-10-19/live-keyvault-preservation-358-synthetic-summary.json) | Historical synthetic exclusions |
| [.copilot-tracking/reviews/logs/2026-10-30/setup-entra-expiry-358-review.md](.copilot-tracking/reviews/logs/2026-10-30/setup-entra-expiry-358-review.md) | This single independent Review |

## Next Steps

Return this record to the active parent for authorized P01-T03 local handoff only: reconcile Review completion, commit locally with Refs #358 and coauthor trailer, and attempt the planned full postcommit gate without a publication claim. No push or PR. Keep FU1 separately routed and AC2 unmet; do not close #358 or replace literal acceptance with local/synthetic proof. This reviewer stops after writing this record and does not attempt the gate or make fixes.
