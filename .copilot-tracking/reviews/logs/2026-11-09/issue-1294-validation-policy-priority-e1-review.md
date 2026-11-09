<!-- markdownlint-disable-file -->
# Review: issue-1294-validation-policy-priority-e1

## Scope and Evidence

* Task ID: issue-1294-validation-policy-priority-e1 (owner-authorized extra correction E1; parent C4)
* Review date: 2026-11-09
* Review scope: full task P01-P05 plus all current policy target files (`.github/copilot-instructions.md`, coordinator agent, `src/README.md`, tracking-retention policy, rubric README steps, D4 research note, log entries)
* Plan, details, critique, research, changes: .copilot-tracking/plans/2026-11-09/issue-1294-validation-policy-priority-e1-plan.md; .copilot-tracking/details/2026-11-09/issue-1294-validation-policy-priority-e1-phase-details.md; .copilot-tracking/plans/critiques/2026-11-09/issue-1294-validation-policy-priority-e1-plan-critique.md; .copilot-tracking/research/2026-11-09/issue-1294-validation-policy-priority-e1-research.md; .copilot-tracking/changes/2026-11-09/issue-1294-validation-policy-priority-e1-changes.md
* Other evidence: .copilot-tracking/hve-builder/2026-11-09-issue-1294-validation-policy-static-review-e1-log.md; .copilot-tracking/sandbox/2026-11-09-issue-1294-priority-e1/

## Execution Status

* Execution status: Complete, once. Lead review by the RPI agent, not independent of the implementer. Independent static (three passes) and critique were proxy subagent contexts, not canonical host-bound. Independent exact-head assessment by the coordinator remains required.
* Checks on commit ad2160d4e (focused tier): `git diff --check origin/main HEAD` exit 0; ASCII scan of added lines in the seven touched docs: none; link and anchor check of six policy docs: 89 links, 0 problems; stale-wording grep ("Every final RPI candidate", "requires a local gate before publication"): none; selection probe of 12 cases reproduced and matches the guide. The later one-line coordinator edit and this evidence commit were re-checked with diff-check, ASCII and link checks (see handoff). No `--changed`/full gate, browser, SQL or hosted CI was run or claimed.

## Plan-to-Change Reconciliation

| Plan item | Result |
| --- | --- |
| P01 merge main | Reconciled: clean merge, tools equal to main |
| P02 edits (G1, G4, G5, PC-2/3/4) | Reconciled |
| P03 static review all targets | Three proxy passes; all findings fixed or dispositioned; stack-tip receipt finding rejected as pre-existing #470 design |
| P04 behavior | Proxy simulation 12 of 12 sub-areas, one partial by design |
| P05 checks, review, commit | Reconciled with critique PC-1 order |

## Acceptance Criteria Assessment

| AC | Assessment |
| --- | --- |
| AC1 reconcile CI vs local coverage | Evidenced in `src/README.md` coverage section, including sensor suite, harness, chat-panel selector, selection and absent/skipped semantics. Hosted behavior is inferred from files, not observed |
| AC2 targeted tests, no blanket `--changed` for small/docs | Evidenced in instructions, coordinator, README; refresh rule (step 8) no longer implies a blanket run |
| AC3 full tier retained, mixed stricter, review and approvals remain | Evidenced; no safeguard removed |
| AC4 reconcile wording; record and test five cases | Wording reconciled; representative cases (docs, small chat, SQL, Bicep/security, mixed) tested only by labelled proxy simulation |
| AC5 dated RPI plus independent review and applicable checks on final candidate | Dated RPI artifacts exist; independent exact-head review and hosted CI pending (coordinator); final-head local checks recorded |

## Findings

| ID | Severity | Finding | Destination |
| --- | --- | --- | --- |
| RV-001 | Medium | Static and behavior evidence are proxy; no native, intended-profile or qualified-human proof, and the final state (after the one-line pass-3 fix) was not independently re-passed | Coordinator exact-head assessment; owner has accepted a labelled proxy if canonical is unavailable |
| RV-002 | Medium | Hosted CI unobserved; for these paths Source CI is expected to select every project, namespace and mssql | Observe after publication |
| RV-003 | Low | The exact text of the independent C4 review (two High, three Medium, two Low) is missing; only the issue comment summary survives | Missing evidence recorded, not reconstructed |
| RV-004 | Low | Stack tip receipt (pre-existing #470 design), branch-specific rubric example and `/tmp` example paths not changed | Follow-up only, out of scope |

No Defects found within the boundary beyond those routed above.

## Outcome

* Outcome: Residual work (RV-001 to RV-004). Not accepted as independently verified until exact-head independent assessment, hosted CI and human approvals. #1294 should use Refs unless the coordinator proves all acceptance criteria on actual integration.
