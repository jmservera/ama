<!-- markdownlint-disable-file -->
# Review: issue 1294 validation policy correction C3

## Scope and Evidence

* Task ID: issue-1294-validation-policy-correction-c3
* Review date: 2026-11-08
* Review scope: full_task
* Assessed boundary: C3 requirements FR1 (direct acceptance command with PYTHONPATH and three-test zero-skip contract), FR2 (append-only log correction), FR3 (complete behavior loop on the actual candidate wording, proxy labeling, retain-sandbox, preserved evidence), focused tier, no workflow/source/security changes, no push. Pre-commit working-tree state on HEAD bd63b22c0b5405ae00f7cbe4d511db30446ab556.
* Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c3-phase-details.md
* Plan critique: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c3-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-correction-c3-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c3-research.md; .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-4.md; .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-4/ (design, log, review, checks/)

## Opening Review State

* Interpreted review goal: confirm the three C3 findings are corrected and the behavior loop honestly completed.
* Review scope: full_task
* Evidence readiness: all artifacts available; plan markers P01-P02 ticked, P03 closes with this Review and the commit.
* Acceptance basis: C3 request and independent review review-1294-bd63-independent.
* First comparison boundary: git diff of src/README.md and docs/reference/log.md against the plan and the runner source.
* Active read-only boundaries: this record only.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: 2026-11-08, one Review pass, read of the diff, changes record, report 4 and sandbox 4 files; no subagents; nothing re-run beyond the recorded checks.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| P01-T01 | README acceptance command (+7/-1) | Reconciled | None |
| P01-T02 | Log correction appended | Reconciled | None |
| P02-T01 | Discovery probe and focused checks | Reconciled | None |
| P02-T02 | Behavior attempt A1 Pass; A2 not needed | Reconciled | None |
| P03-T01 | Changes record, Review, commit | Reconciled | Commit follows this Review |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| P01-T01 | src/README.md | Acceptance command given the runner's PYTHONPATH and its three-test zero-skip rule | tools/rpi-checks.py EMPLOYEE_ACCEPTANCE_BROWSER_PATHS and expected_count 3; employee_acceptance_check.py testsRun == 3 and no skips | Probe: not discoverable without path, discoverable with it, three IDs load; Passed | Reconciled |
| P01-T02 | docs/reference/log.md | C2 "final wording" claim corrected by append; C3 outcome entry appended | 0 removed lines; ASCII scan 0 | Passed | Reconciled |
| P02-T02 | sandbox 4; report 4 | Full independent design, simulated execution, independent grading on the final wording | test-review.md: 13/13 Pass, 0 confirmed defects | Pass (proxy) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| P02-T02 terminal rule | Applied as planned: A1 Pass so wording frozen, A2 not run | PC-001 | Changes record states A2 not needed | Critique applied before implementation | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: PC-001, PC-002, PC-003 applied directly in the plan and details.
* Material revisions: none after critique.
* Dependent-work pause assessment: no early resumption.
* Justification assessment: supported.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| none | | | |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Behavior evidence is a proxy simulation

* Related scope: P02-T02
* Evidence: report 4 Fidelity and limitations (profile unresolved, model not observable, literal-reading simulation, grader did not re-verify executor containment, test-log is a lead condensation)
* Impact: the Pass supports conformance of the wording only; it is not intended-profile or native evidence.
* Destination: follow_up
* Smallest useful next action: human reviewer accepts the proxy limitation (unchecked box in report 4).

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Process slip, README edit preceded rpi-implement invocation

* Related scope: P01-T01
* Evidence: changes record Process note
* Impact: sequencing deviation only; the edit was in planned scope and is covered by the recorded checks and behavior run.
* Destination: follow_up
* Smallest useful next action: none required; disclosed.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Nonblocking grader observations left unedited

* Related scope: P02-T02
* Evidence: test-review.md (b): coordinator line 478 silent on focused+focused; README line 188 without commands; axe file location unstated
* Impact: ambiguity only; not contract elements.
* Destination: follow_up
* Smallest useful next action: optional later wording polish if the owner wants it.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| RV-001 | follow_up | Human reviewer | Residual proxy limitation |
| RV-002 | follow_up | None | Disclosed sequencing note |
| RV-003 | follow_up | Optional | Nonblocking cosmetic |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Human acceptance of report 4 and independent exact-head assessment; hosted CI observation after publication.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: commit and coordinator exact-head assessment.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| discovery probe from src/api (read-only, PYTHONDONTWRITEBYTECODE=1) | acceptance command PYTHONPATH | Passed | not discoverable without path; discoverable with runner path; 3 IDs load |
| git diff --check | working tree | Passed | exit 0 |
| ASCII and append-only scans | added lines; log diff | Passed | 0 non-ASCII; 0 removed log lines |
| README link scan | src/README.md | Passed | clean |
| stale-phrase grep | three guides | Passed | no matches |
| hve-builder-tester full run 4 | guides and log | Passed (proxy) | 13/13 Pass, 0 confirmed defects |
| browser harness / acceptance command run, hosted CI, full gate | | Unavailable/Not run | wording-only focused change; hosted CI unobserved |

## Outcome

* Outcome: Residual work
* Outcome rationale: F1-F3 of the independent review are corrected and verified; behavior loop completed with a proxy Pass on the final guide wording; only nonblocking residuals remain.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | follow_up | Human acceptance of report 4; coordinator exact-head assessment |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: focused local checks and proxy behavior Pass; no browser, hosted CI or full gate
* Blockers: none
