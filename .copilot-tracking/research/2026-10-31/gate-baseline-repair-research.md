<!-- markdownlint-disable-file -->

# Task Research: gate-baseline-repair

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/gate-baseline-repair-research.md |

## Research Brief

* What to research: reproduce the complete origin/main gate, diagnose its nine browser B023 closures and the exact chat-panel browser case.
* Why it matters: inherited failures block unrelated issue publication.
* Audience or intended use: implementation and independent PR review.
* Scope: gate-owned browser harness, chat-panel test, tightly coupled gate regressions.
* Non-goals: duplicate #572 integration wiring, new skip allowances, workflow/protection changes, runtime redesign, private data or cloud execution.
* Criteria: original adverse evidence, small root-cause repairs, real Chromium and complete exact-head evidence.
* Requested outputs: dated research, plan, critique, changes and Review, then a PR using Refs #572.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which baseline failures reproduce, and what is the smallest safe repair? |
| Codebase scope | tools/rpi-checks.py, tools/test_rpi_checks.py, src/api/checks, src/api/tests/test_chat_panel.py |
| External scope | GitHub issue #572 and branch lifecycle only |
| Initial internal candidate areas | complete local gate and API/browser harness |
| Initial external candidate areas | issue #572 |
| Research posture | focused |
| Posture provenance | bounded caller task with named failures |
| Explicit limits / deadline | pip only; wait for shared lock; publish without force push |
| Posture-specific completion basis | material failure paths and alternative explanations covered |
| Edits allowed during research? | no source edits |
| Resolved evidence root | .copilot-tracking/research/ |
| Known constraints / excluded sources | synthetic data only; receipts and heavy outputs external |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | repository guidance | all project files | branch, evidence, pip and publication gates | selected |
| Skill | rpi-research | explicit full RPI request | read-only three-wave investigation | selected |
| Specialist | RPI Researcher | available | independent lane | skipped: one tightly coupled failure trace |
| Skill | web-design-guidelines | browser harness only, no web source edit planned | web review rules | not selected for Python-only harness repair |

## User Participation and Research Decisions

Caller explicitly requests the whole ordered loop and publication. Non-interactive execution requires no routine phase prompts. Reuse clean fix/gate-baseline-b023, which has no prior PR and starts exactly at origin/main a75bbdffa51ae34b1fcf779250f1f553d566ee93.

## Scope and Success Criteria

Preserve all runtime behavior, skip boundaries, workflow hashes and original adverse evidence. Fix the nine strict gate-owned B023 errors, not every pre-existing exempt browser harness.

## Task Research Requests

Run the full gate first, then strict browser lint and the exact chat-panel Chromium selector. Diagnose other blockers precisely rather than broadening exemptions.

## Direction Controls

| Control type | Direction or boundary | Source | Effect |
| --- | --- | --- | --- |
| exclude | Do not duplicate #572 wiring | caller | current main already owns the exact browser selector |
| narrow | Small defects only | caller | no runtime redesign |
| exclude | No Ruff suppressions or workflow changes | caller | bind closures and preserve inventory |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Which complete-gate groups fail on main? | straightforward | H | answered |
| Q2 | How can closures retain live mutable state safely? | depth | H | answered |
| Q3 | What fails in the exact Chromium case? | depth | H | answered |
| Q4 | Why does static tooling now report unexpected chat skips? | depth | H | answered |

## Prior Knowledge Gate

Read both case studies, knowledge-base index, owner memory, src local gate and retention policy. Owner memory is context, not evidence. Main already contains #572 selector wiring; issue remains open. Historical reported nine closures were verified with isolated Ruff.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline investigation identified strict browser lint, scoped skip parsing and tooling discovery. The literal caller command under flock waits for the lock but fails argparse because --base is required. Valid runs must also supply --out. The runner itself locks the same file; nested outer locking would deadlock. Used the runner's lock timeout, preserving lock-timeout attempts and waiting again rather than stopping.

Reflection: the first valid attempt was blocked by lint-created ignored caches; removed only those six own cache files and empty directories. Two 1,800-second waits timed out; a longer queued attempt acquired the lock and completed an actual failed full baseline.

#### Wave 2: Deeper

All nine gate-owned closures capture iteration-specific lists, a change string or a case snapshot. Lists are mutated, not rebound within an iteration, so default arguments preserve the same live list. Bind typed nested functions and lambda defaults. The chat-panel case passes unchanged in actual Chromium: one test, zero skips, 2.052 seconds in the external pip-installed environment.

Static tooling fails because test_chat_panel_discovery_skip_is_exact_and_integration_fails_closed prints two synthetic unittest skip transcripts through Runner.command. The outer gate parses those as actual static-suite skips. Capture only those intentional fixture command prints inside that regression test; keep real skip rejection and receipt assertions unchanged.

Reflection: no chat-panel runtime defect or missing selector wiring was reproduced. Repair fixture output leakage, not gate policy.

#### Wave 3: Contrarian

Compared default arguments with partial binding and skip parser relaxation. Default arguments preserve mutable list identity while avoiding late binding; no captured gate-owned callback flag is reassigned within its iteration. Partial is unnecessary indirection here. Other exempt browser harnesses have flags intentionally reassigned and must not be mechanically snapshot-bound.

The unchanged exact chat-panel test passes, contradicting an assumed browser runtime defect. Main already wires it into owned execution. Broadening the skip allowlist or ignoring nested skip output in production would weaken fail-closed behavior and duplicate #572 integration work.

Reflection: preserve the production parser and exact selector, capture adversarial fixture stdout instead. No additional research cycle needed: all material questions have source and execution evidence.

#### Parent Synthesis and Disposition

Accepted closure binding and fixture stdout isolation; rejected skip relaxation, unrelated exempt-harness cleanup and runtime changes. Ready for Plan.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Complete runner requires base/out and owns flock | tools/rpi-checks.py:2275 | view | high | outer flock is not safe for valid execution |
| C2 | Nine gate-owned B023 errors | src/api/checks/case_journey_browser_check.py:85 | isolated Ruff and full gate | high | original 0073-browser.log |
| C3 | Browser stage already executes exact chat-panel selector with flag | tools/rpi-checks.py:1595 | view | high | no new wiring needed |
| C4 | Static unittest output contains two nested chat discovery skips | tools/rpi-checks.py:1481 | full gate | high | original 0068-static.log |
| C5 | Two skips are intentional Runner.command fixture prints | tools/test_rpi_checks.py:109 | original static log and view | high | regression still checks rejection in browser integration |
| C6 | Exact unchanged Chromium selector passes | src/api/tests/test_chat_panel.py:564 | actual Chromium unittest | high | /tmp/ama-gate-baseline-chat-repro-a81da11b.log; one executed, zero skips |
| C7 | Captured lists and change/snapshot values are per-iteration | src/api/checks/case_journey_browser_check.py:84 | source inspection | high | preserve list mutation and callback identity |

### External Evidence

No web research required. GitHub #572 read using gh on 2026-10-31.

### Contradictions / Conflicts

The requested outer flock conflicts with the self-locking runner contract. Preserve serialization with the runner lock, not a bypass. Default configured Ruff suppresses B023 in checks; isolated strict lint is the actual requirement.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Implication |
| --- | --- | --- | --- | --- |
| Q1 | Browser lint and static nested skips fail; downstream groups blocked | C2, C4 | high | both root causes need diagnosis |
| Q2 | Defaults bind lists without copying and bind per-iteration scalar values | C7 | high | smallest repair |
| Q3 | Unchanged chat-panel selector executes successfully | C3, C6 | high | no runtime edit or duplicate wiring |
| Q4 | Adversarial fixture stdout leaks into parent suite parsing | C5 | high | isolate output inside the test only |

## Key Discoveries

Original failed receipt: /tmp/ama-gate-baseline-20261031-repro-wait-a81da11b/receipt.json.
Original log: /tmp/ama-gate-baseline-20261031-repro-wait-a81da11b.log.
The full failure is not yet a Chromium-case execution failure: lint stops the browser group before that selector.

## Alternatives and Decision State

Selected: bind nine gate-owned closure references, use the existing Ruff formatter for the already-unformatted strict file, and capture intentional fixture stdout. Reject production skip parser changes, workflow changes, chat-panel runtime edits and unrelated exempt checks.

## Open Questions, Risks, and Residual Uncertainty

Actual exact selector passes. Complete gate may expose further latent baseline failures after the original static and browser blockers are removed; preserve and diagnose any such evidence.

## Planning Readiness

Ready. Research disposition: executed. Caller-confirmed automatic parent advances to Plan.

## Sources

Repository source and original full-gate output; no private datasets.

## Artifact Self-check

All three waves, material alternatives, evidence IDs and readiness recorded. Original failure retained externally and not relabelled. No source edits during Research.
