<!-- markdownlint-disable-file -->
# Task Research: pr423-merge-rubric

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/pr423-merge-rubric-research.md |

## Research Brief

Resolve PR #423's integration with current main without losing either side's
work, and explain the failed rubric status. Prepare a bounded implementation
plan with honest evidence improvements. Audience: owner and publishing
coordinator. Output mode: convergence.

## Research Parameters

* Focused posture, selected for the supplied failure and named source targets.
* Scope: this worktree only; merge conflicts, related migration surfaces,
  rubric workflow/scorer/capstone definitions and existing local validators.
* External sources: read-only GitHub PR/run evidence for this repository.
* Non-goals: Azure, deployment, sign-in, secrets, warming, pushes, issue closure,
  score inflation, unrelated worktrees and unrelated implementation.
* Resolved evidence root: `.copilot-tracking/`.
* Research edits: evidence and workflow state only.
* Completion basis: material questions answered, all three waves completed.

## Extension Registry and Provenance

| Kind | Candidate | Disposition and authority |
| --- | --- | --- |
| Instruction | Repository instructions | Selected: preserve original evidence, append-only log, src migration and local gate |
| Skill | rpi-research | Selected: three-wave research evidence |
| Skill | rpi-plan / rpi-implement / rpi-review | Deferred to respective user-requested phases |
| Specialist | Research worker | Skipped: integration and rubric evidence fit direct investigation |
| Specialist | Independent critique / Review | Required at later phase gates, bounded artifacts |

## User Participation and Research Decisions

Owner explicitly requests the full ordered RPI loop and local commits only.
No interaction is needed for routine phase advancement. This is a confirmed
automatic task, with no authority to select later follow-up work.

## Direction Controls

* Keep DN1-DN4, existing tests/docs and original adverse outcomes.
* Main's current implementation and src migration take precedence over stale
  proposal-only paths. Preserve decision intent rather than restoring retired mvp.
* Use `Refs #360`, never a closing keyword. Merge rather than rewrite ancestry.
* Never inspect or modify the owner's other worktree.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What conflicts and migration interactions need resolution? | depth | Answered |
| Q2 | What caused the rubric failure, and what is score versus schema failure? | depth | Answered |
| Q3 | What honest in-scope improvements and local validation are appropriate? | depth | Answered |

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. PR #423 is open;
the supplied worktree is clean and on the requested fix branch.
Initial head: `4696866850f230238617c95b0dbd4297f7e8b245`.
Fetched main: `5634f9a077d175a931c15e3400114665d8c071ee`.
Historical PR-body receipts do not validate this new candidate.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial read-only merge preview identifies conflicts in evidence pack, KB
index, append-only log and local gate script. Infra files auto-merge but
still need semantic inspection. PR status is rubric/score FAILURE despite
successful workflow jobs; bot reports invalid D1 detail keys.

Reflection: do not confuse workflow success with scoring success. Prioritize
schema/normalization and migration-aware semantic merge inspection.

#### Wave 2: Deeper

Downloaded immutable run 40556907743 context and fallback safe-output artifacts
to the external session directory. The submitted D1 has an extra `evidence2`
key, not a missing `change_reason`. Strict adapter rejects extra keys even on
closed criteria. Existing prompt preflight already rejects this shape.
Only A1/A3/A5 were open, each already 5. All 20 submitted grades total 77.

Reflection: a documentation change cannot repair a past model tool call.
Preserve strict validation and add the exact D1 regression, rather than
relax the adapter or change scores. Improve scored infra evidence navigation.

#### Wave 3: Contrarian

Replayed the original saved submission through the deterministic gate:
valid false, same exact D1 error, no score. In-memory counterfactual removal
of only `evidence2` gives valid true, passed true, total 77 versus 77,
floors met. This is diagnostic only, never a new assessment or recorded score.
Current main also has 77; B3/B4/B5/C2 = 2 and D1/D2/D3 = 4/3/2.
Prepared notes do not prove delivery, and infra changes cannot raise closed
pitch/thought-leadership criteria.

Reflection: reject the hypothesis that this failure establishes a low
numerical PR score. Reject fabricated rehearsal/publication or claimed live
transport. Main's IoT/release/retirement changes coexist with the Blob branch.

#### Parent Synthesis and Disposition

* Accepted: merge both histories; four textual conflicts are metadata,
  append-only log and a derived workflow fingerprint.
* Accepted: retain Blob implementation, DN1-DN5 and main's current src/IoT/
  release work. The worker already imports `zava_forward.core.mssqlstore`;
  transport helpers still belong in infra, not retired mvp.
* Accepted: add exact extra-key regression at adapter and prompt-preflight
  boundaries; document evidence/rationale/change_reason as provenance, not
  as score instructions.
* Deferred: real private route, position sizes, production data actions,
  signed attestation, human and hosted acceptance.
* Cycle re-entry: no; named questions answered with direct source and run
  evidence. Next sources are redundant for this bounded local repair.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Clean requested branch; four conflict paths | git status, branch and merge-tree against fetched main |
| W1 | Bot reports schema failure; rubric/score fails | https://github.com/jmservera/ama/pull/423#issuecomment-6305760316 (retrieved 2026-10-30) |
| C2 | Adapter requires exactly three fields, rejects extras | .github/rubric/scripts/scorecard_adapter.py:8-46 |
| C3 | Existing prompt requires complete flat inputs and exact detail keys, with jq preflight | .github/workflows/rubric-score.md:517-577; generated rubric-score.lock.yml:604 |
| C4 | Gate validates whole card before carry-forward; incremental pass compares total to baseline | .github/rubric/scripts/gate.py:87-132,170-240 |
| C5 | Infra informs A1/A3/A5 only | .github/rubric/artifacts.json:37-43 |
| C6 | Section D assesses original synthesis, publish readiness and actual dissemination, separately from capstone docs | docs/reference/method/ama-capstone-assessment-guide.md:67-100; docs/capstone/README.md:287-318 |
| C7 | Worker already uses installed src namespace | infra/scripts/staff-azure-worker.py:165 |
| C8 | Existing tests cover retired tag absence, private lifecycle, profile-bound credentials and image context | infra/tests/test_staff_azure.py:1541-1670 |
| C9 | Main local gate retains full tier for infrastructure and external exact-head receipts | src/README.md: Local RPI gate (origin/main 5634f9a0) |
| C10 | Four conflicts and auto-merge retain IoT roles plus Blob role; combined workflow needs newly computed hash | git merge-tree tree cdb205605c4ecd7c0439aa987c159dfc7e5af2ba |
| W2 | Actual D1 extra evidence2; grades unchanged, only infrastructure open | https://github.com/jmservera/ama/actions/runs/40556907743 (retrieved 2026-10-30), fallback safeoutputs.jsonl SHA256 e05bddba88c51c5145121cba95115f7b0cffeadf1efd20d3afa1cf3c5bbcec55; context SHA256 091208663dc178548ee896790e3dd0fa81c517b4d1abea913a68b425a117f50c |

Delegation: inline; the coupled source investigation did not require a separate worker.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence |
| --- | --- | --- |
| Q1 | Four explicit conflicts; semantic auto-merges need preservation checks, not main-only checkout | C1,C7-C10 |
| Q2 | Invalid model-generated details, not a measured score regression | C2-C4,W1-W2 |
| Q3 | Precise regression and evidence navigation are honest; no available numerical upside for already-ceiling open dimensions | C3-C6,W2 |

## Alternatives and Decision State

Merge is preferred to rebase: user permits either and merge preserves existing
ancestry and original evidence without rewriting commits.

## Open Questions, Risks, and Residual Uncertainty

Historical live results remain unverified. Hosted model compliance cannot be
guaranteed by a local regression. Full local gate may be blocked by missing
prerequisites and must not be reported passing unless it succeeds. No remote
publication is authorized. Original receipts and adverse RPI outcomes remain.

## Planning Readiness

Ready. Research disposition: executed. Sources and claims reconciled;
three waves and self-check complete. All Q1-Q3 answered. Parent advances to
Plan under the explicit full-loop request; no additional research needed.
