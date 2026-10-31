<!-- markdownlint-disable-file -->

# Task Research: gate-chat-test-572

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md |

## Research Brief

* What to research: issue #572's exact chat-panel Chromium ownership, coverage inventory, skip enforcement and publication receipt.
* Why it matters: a legitimate opt-in case blocks API discovery while lacking owned gate execution.
* Audience or intended use: implementation and independent PR assessment.
* Scope: tools/rpi-checks.py, tools/test_rpi_checks.py, API browser tests and directly related guides.
* Non-goals: runtime/UI changes, cloud deployment, paid inference, main or other worktree changes, secrets, mvp code.
* Criteria: all four issue criteria; real browser execution; fail-closed skip regression; fresh exact-head complete gate and receipt verification.
* Requested outputs: dated full RPI evidence, implementation, local commit and PR using Refs #572.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Where must the case execute, how is coverage proved, and which skips may API discovery admit? |
| Initial internal candidate areas | tools/rpi-checks.py, tools/test_rpi_checks.py, src/api/tests/test_chat_panel.py, src/README.md |
| External scope | GitHub issue #572 only |
| Research posture / provenance | focused / bounded caller request |
| Explicit limits | pip only; no credential files; no main/other-worktree writes |
| Completion basis | Exact case, owner-stage and negative skip evidence covered |
| Edits allowed during research | Evidence/state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance | Scoped authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | Repository and RPI Agent guidance | Current task configuration | Branch, evidence, full gate and human approval boundaries | Selected |
| Skill | rpi-research | Installed plugin | Ordered three-wave investigation | Selected |
| Skill | Web design skills | Task scope | UI changes/reviews only | Skipped: no UI edits intended |
| Specialist | RPI Researcher | Host registration | Independent lane | Skipped: single coupled trace handled inline |

## User Participation and Research Decisions

Caller explicitly requested the complete ordered loop and publication. No interactive
checkpoint is needed or available. This is a directed full-loop execution, not an
inferred manual-to-automatic switch. Stop after the requested PR action; do not
start an unselected follow-up.

## Direction Controls and Scope

Preserve unexpected integration/dependency skip failures. Do not merely allowlist
the chat reason, disable the test, add skip tokens or change workflow protection.
Reuse clean chore/gate-chat-test-572 (no open PR at intake).

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Where does local Chromium own each opt-in API case? | depth | High | Answered |
| Q2 | How do commands, coverage and skips prove exact case execution? | depth | High | Answered |
| Q3 | Can a fresh complete gate and exact-head receipt be produced here? | straightforward | High | Prerequisites available; execution deferred to post-Review |

## Prior Knowledge Gate

Issue body read first with gh issue view 572. Its historical skip/receipt report
is a starting claim, not current execution evidence. Read original case study,
addendum, knowledge-base index, memory and sector primer. No customer requirement
or live authority change is implied.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline investigation found that merged #575 already owns the exact case in both
the trusted command inventory and Runner.browser; #595 adds discovery reasons.
Reflection: do not duplicate those repairs. Prior original Review leaves real
execution and the complete committed gate unresolved.

#### Wave 2: Deeper

Prioritized command/receipt semantics. check_skips records totals/skips, while
verify_commands verifies argv/env and positive aggregate execution. The named
browser case has no exact successful verbose-ID assertion. Both passing receipt
fixtures substitute an unrelated test_x while still satisfying verification.
Reflection: aggregate success is not proof of this exact required case. Extend
the existing parser narrowly for this selector rather than add a second harness.

#### Wave 3: Contrarian

Challenged adding code when ownership is already merged. Rejected duplicating
dispatch, broadening reasons, adding workflow edits or treating fixture success
as real browser evidence. A no-source-change validation-only PR would leave the
demonstrable exact-case evidence weakness. Existing full receipt mutation tests
provide a proportionate place to reject wrong IDs, counts and ambiguous logs.
Reflection: retain all inherited execution and skip contracts; require one exact
successful case only for its dedicated command. No further cycle is needed:
bounded source questions are covered, and runtime execution is planned validation.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| W1 | Historical exact case is missing from owned Chromium execution | https://github.com/jmservera/ama/issues/572, retrieved 2026-10-31 | High for reported problem; current source verification pending |
| W2 | #575 and #595 are merged; acceptance still requires current complete evidence | https://github.com/jmservera/ama/pull/575 and https://github.com/jmservera/ama/pull/595, retrieved 2026-10-31 | High |
| C1 | Exact browser argv/env/suite/integration already owned | tools/rpi-checks.py:704 and :1603 | High |
| C2 | Chat discovery reason is constrained to exact ID, API group and non-integration | tools/rpi-checks.py:1023 | High |
| C3 | Receipt verifies aggregate execution, not named success | tools/rpi-checks.py:894 and :938 | High |
| C4 | Passing browser receipt fixture uses unrelated test_x | tools/test_rpi_checks.py:318 and :657 | High |
| C5 | Workflow project coverage already includes browser; no workflow change needed | tools/rpi-checks.py:1544 | High |
| C6 | Exact real browser case is loopback synthetic and asserts no model calls | src/api/tests/test_chat_panel.py:563 | High |
| C7 | Complete external gate follows original Review and commit | src/README.md:61 | High |
| C8 | Original prior Review preserves unresolved real execution/full-gate evidence | .copilot-tracking/reviews/logs/2026-10-30/chat-panel-test-in-gate-572-review.md:105 | High |

## Findings, Alternatives and Decision State

Selected: reuse inherited owned Chromium dispatch and coverage; strengthen the
shared suite parser with optional exact-case validation applied by execution and
receipt verification only to CHAT_PANEL_BROWSER_SELECTOR. Require a single test,
one exact verbose success, no skips and no other test-result lines. Add semantic
receipt mutations with updated hashes, runtime regression and honest fixtures.
Run actual opted-in Chromium, caller checks and fresh full committed gate.

Rejected: allowlist-only repair (caller exclusion, C2); duplicate dispatch or
workflow edits (C1/C5); aggregate-only evidence (C3/C4). No production UI edits
or dependency-pin changes are needed.

## Open Questions, Risks and Residual Uncertainty

Python 3.12.3, Docker server, Node, Azure CLI, actionlint, ShellCheck, Trivy 0.76.0,
installed Chromium and browser/SQL/YAML imports are available. Availability does
not prove all required groups will pass. Shared lock contention, registry/network
and inherited failures may block publication. No foreign process may be stopped.

## Planning Readiness

Ready for Plan. Research disposition: executed. Q1/Q2 answered by C1-C6; Q3 has
available prerequisites and an explicit later execution obligation (C7/C8).
Self-check: ordered waves complete, evidence IDs resolve, prior findings preserved,
no source changes during Research, no secrets or external runtime used.
