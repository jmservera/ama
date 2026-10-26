---
title: Issue 350 feedback checker correction 5 review
description: One local RPI Review of finite JSON numbers and exact schema typing
ms.date: 2026-10-23
---

## Task and Opening Review State

Task ID: issue-350-demo-feedback-correction5.
Execution: Complete. Outcome: Conformant within the local correction boundary.
Review boundary: the two supplied P2 findings and this bounded local correction,
not publication, deployed acceptance or whole-issue acceptance.
P01/P02 implementation and local checks complete; P03 Review/local commit
pending. No source blocker or unresolved in-scope finding at handoff.
No independent review agent needed: the complete diff and evidence fit one
direct inspection. This is a local self-review, not the later coordinator's
independent exact-head assessment.

## Artifact Set

* Research: .copilot-tracking/research/2026-10-23/issue-350-demo-feedback-correction5-research.md.
* Plan: .copilot-tracking/plans/2026-10-23/issue-350-demo-feedback-correction5-plan.md.
* Details: .copilot-tracking/details/2026-10-23/issue-350-demo-feedback-correction5-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-23/issue-350-demo-feedback-correction5-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-23/issue-350-demo-feedback-correction5-changes.md.
* Source: tools/check-demo-feedback.py and tools/test_check_demo_feedback.py.
* Execution logs: session files/correction5-red.log,
  correction5-green.log and correction5-local-checks.log.

## Review Questions

Does every decoded float use the finite-number guard before evidence checks?
Does schema type exclude bool and float without changing supported int?
Do regressions use actual raw exponent tokens rather than Infinity?
Do finite values preserve field scope and existing offline evidence limits?
Are earlier outcomes retained and publication prerequisites routed honestly?

## Requirements and Plan Reconciliation

| Requirement / task | Evidence and assessment |
| --- | --- |
| FR1 / P01-T01, P01-T02 | json.loads invokes the typed finite callback for every floating numeric token, including nested unchecked data; ValueError is converted by the existing specific invalid-JSON handler into BLOCKED before runtime/check dispatch. Literal NaN/Infinity rejection remains wired. |
| FR2 / P01-T01, P01-T02 | Exact `type(schema_version) is int` rejects both bool values and 1.0 before supported-value comparison. Supported integer 1 and unsupported integer 2 have explicit controls. |
| FR3 / P01-T01 | Raw 1.25, 1e308, 1e-999 and -1.25 remain decoded floats. Rank stays unchecked, nonnegative latency passes, negative latency fails; numeric-looking strings retain their previous field rules. |
| FR4 / P01-T01 | Invalid inputs require all measurable checks BLOCKED with the relevant reason, no runtime invocation, gaps NOT-RUN, offline_only true and acceptance not-accepted. Supported integer fixture preserves SQL/write cap, gaps and overall cap. |
| NFR / P01-T02 | Seven-line typed finite callback, one decoder wiring change and exact integer guard. No new catch, schema framework, dependencies, recursive traversal or component-policy changes. |
| P02-T01 | 77 tests pass after final formatting; isolated cache-free Ruff lint/format and git whitespace pass. Only expected two tool edits and correction5 artifacts, no ignored files. |
| P03-T01 | This single Review assesses corrected source, tests, plan reconciliation, critique and observed local evidence. |
| P03-T02 | Local commit intentionally follows Review; privacy identity and commit are parent closeout work, not already-executed evidence at review time. |

The original P2 exponent issue is closed at decoding, rather than only guarding
latency or adding a rank schema. A nested list/dict extra outside AI also
exercises that boundary. The raw-token replacement checks exactly one sentinel,
so the test cannot pass merely because it accidentally injected a string,
invalid leading-plus number or literal Infinity. Invalid inputs use an
AssertionError sentinel instead of relying on the pre-existing overall cap.
All five added test methods remain within the locked budget; existing tests
are retained and the invalid-input helper is strengthened.

## Critique and Implementation-Time Decisions

One independent planning critique executed before source edits, verdict Revise,
with its original two findings preserved. PC-001 was applied: local completion
requires no unresolved in-scope acceptance defect. This Review finds none.
PC-002 was rejected because its cited /tmp restriction was worker-local and
not present in the primary's applicable instructions. Existing tempfile
behavior and installed interpreter selection were retained, without editing
other worktrees or ignore rules.
No significant design divergence, new user decision or scope change occurred.
One formatter-requested layout adjustment was ordinary local judgment,
followed by a final green suite and lint/format/whitespace checks.
Research, plan, details, changes and source agree on completed P01/P02 and
remaining P03 closeout. Earlier RPI artifacts, outcomes and markers are intact.

## Validation Evidence

| Check | Result | Boundary |
| --- | --- | --- |
| New regressions before source fix | Expected failure | 2 methods, 13 subtest failures: 9 overflow, True and 1.0 reach runtime; False/2 fail explicit integer diagnostic |
| Final focused suite | Passed | 77 tests, 0.238s, installed packages, no bytecode |
| Ruff lint 0.17.1 | Passed | Both tools, isolated E,F,W,B,BLE,I selection with E501 ignored, no cache |
| Ruff format | Passed | Both tools already formatted after one ordinary formatting adjustment |
| Whitespace and input inspection | Passed | git diff --check; only named tools and correction5 artifacts, no ignored inputs |
| Full gate / receipt verification | Not run | Explicit owner local-only stop; new-head evidence belongs to coordinator |
| Coordinator independent exact-head assessment | Not run | Reserved for coordinator after fresh full gate |
| SQL/deployed/actual-AI/human/hosted acceptance | Not run | Excluded; cannot be established by synthetic local checker tests |

Red failure count is not claimed as 13 acceptance bugs: False and unsupported
integer 2 already blocked, but their diagnostic changed to make type explicit.
Prior exact-head receipt SHA-256
1b01ea5d797af7d12981bdf6f0122e6dfabd765940982f8d5ba579b64c85f1cc
belongs to the supplied initial head/base; it does not validate this correction.

## Findings and Routing

No in-scope implementation defect, unaccepted decision or missing research
evidence identified. Severity for in-scope defects: none.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Coordinator publication evidence remains outside this task

* Evidence: explicit owner stop after local tests/Review/local commit, and
  plan Follow-Up Items. Changed source invalidates the earlier receipt for
  the new head; independent coordinator assessment has not run here.
* Impact: local correctness evidence is not permission to publish or accept
  any deployed, SQL, AI or original issue criterion.
* Classification: existing out-of-scope residual prerequisite, not a source
  defect or incomplete local acceptance requirement.
* Destination: distinct coordinator follow-up after the local commit.
* Next action: coordinator runs fresh complete exact-head gate and official
  receipt verification against its current main base, then independent
  exact-head assessment before considering publication. Preserve draft PR
  and open issue/all original criteria unticked.

## Outcome and Closeout

Execution: Complete, exactly one postimplementation RPI Review.
Outcome: Conformant only for this bounded local correction.
No unresolved in-scope finding blocks local commit. Publication remains
unassessed and unauthorized, and broader acceptance remains unmet.

| Finding class | Destination |
| --- | --- |
| Implementation defects | None found; no repeat implementation or Review |
| Significant decision gaps | None |
| Material research gaps | None |
| Out-of-scope residual | RV-001 to coordinator after local commit |

The parent may synchronize Review/local closeout markers and state, resolve
privacy-safe commit identity and perform the authorized new local commit.
No second Review, source edits, gate invocation, push or PR/issue update is
part of this record's continuation.
