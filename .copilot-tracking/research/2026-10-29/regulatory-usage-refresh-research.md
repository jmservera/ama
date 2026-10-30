<!-- markdownlint-disable-file -->

# Task Research: regulatory-usage-refresh

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/regulatory-usage-refresh-research.md |

## Research Brief

* Topic: decouple regulatory answer submission from the secondary usage GET.
* Purpose and audience: fix the Copilot finding on PR #506 for maintainers.
* Scope: `src/api/src/zava_forward/api/web/chat.js`, focused existing
  `src/api/tests` conventions, and dated RPI evidence.
* Non-goals: redesign, unrelated findings, regulatory content, cloud operations,
  pushing, other worktrees, rubric score changes.
* Criteria: answer display immediately permits input cleanup/control recovery;
  delayed and failed usage requests cannot block submission or reject unhandled.
* Requested outputs: research, plan, implementation, independent review,
  focused red/green regression, relevant tests, Node syntax, Ruff if Python
  changes, and one local Conventional Commit with the required trailer.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Where is submission blocked? Which helper contains usage errors? How do existing tests execute real JavaScript? |
| Codebase scope | Current reg208 worktree; chat panel and its test helpers |
| External scope | Required current Web Interface Guidelines only |
| Initial internal candidate areas | chat.js; src/api/tests; API guide; applicable tracking instructions |
| Initial external candidate areas | vercel-labs/web-interface-guidelines/main/command.md |
| Research posture | focused |
| Posture provenance | Default for the caller's bounded target and supplied failure |
| Explicit limits | No push, az, other worktrees, or hand-edit of latest.json |
| Completion basis | Material questions answered and in-scope alternatives challenged |
| Edits allowed | Research evidence and workflow state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and scoped authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository guidance | Supplied AMA instructions, all paths | Selected: branch, tests, privacy-safe commit, evidence retention |
| Skill | rpi-research | Activated research contract | Selected: three inline waves and canonical evidence |
| Skill | web-design-guidelines | Web behavior change | Selected: current source fetched before web edit/review |
| Specialist | RPI Researcher | Registered independent research lanes | Skipped: a small continuous trace is best investigated inline |
| Skill | Visual redesign skills | App design/rebranding | Skipped: behavior-only fix, no visual redesign |

## User Participation and Research Decisions

| Checkpoint | Rationale | Result |
| --- | --- | --- |
| Intake | User explicitly requests the full loop and local commit; noninteractive execution | Run all requested phases without routine approval prompts |

## Scope and Success Criteria

Preserve the existing answer, human-review boundaries, dirty-field protection,
usage-error reporting, and lookup-error handling. The focused regression must
fail on the original code and pass on the corrected code. No operational
acceptance or publication approval is implied.

## Task Research Requests

Investigate the named finding and existing Node-from-Python web-test
conventions. No broader audit or redesign.

## Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Narrow fix to secondary usage refresh | User | No unrelated chat or UI changes |
| Local commit only | User | No push or remote mutation; publication gate not exercised |

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What makes usage refresh block the lookup? | straightforward | Answered |
| Q2 | What contains usage failures and preserves editable input? | depth | Answered |
| Q3 | What focused executable regression follows repository conventions? | straightforward | Answered |

## Prior Knowledge Gate

Caller finding is a hypothesis to verify against current source. Branch is
`feat/regulatory-assistant-208`; PR #506 is open against main; worktree is
clean at intake. Original/addendum, knowledge-base index and owner memory were
read for scope; no new regulatory claim or knowledge-base synthesis is needed.

## Research Cycle Log

### Cycle 1

Focused, inline research. Wider locates the lifecycle and test entry points;
Deeper traces error and field-state helpers; Contrarian challenges unguarded
fire-and-forget and tests that accidentally await the secondary GET.

#### Wider

The answer display precedes an awaited usage request (C1). The existing case
journey test executes shipped JavaScript with a minimal DOM and native Node
assertions (C3). No separate research lane is needed for this continuous trace.

Reflection: the delay is client lifecycle coupling, not answer persistence or
an API contract change.

#### Deeper

The usage helper already catches both request and display failures and writes
an explicit independent usage status (C2). Field cleanup compares raw field
state so changed text, including whitespace, survives (C4). The shared action
wrapper also waits for the handler promise (C5).

Reflection: keep the existing helper and cleanup; remove only the secondary
await and place cleanup first. Main-handler completion then settles shared
busy feedback without waiting for metering.

#### Contrarian

Examined whether an unawaited refresh could leak rejection or whether clearing
input unconditionally was acceptable. C2 contains the ordinary request/render
failure; an extra catch would duplicate the same error handling. C4 rejects
unconditional cleanup because it would erase text edited while awaiting the
answer. C3's immediately resolved usage fixture masks the reported delay.
The regression must leave usage pending, assert UI recovery before settlement,
then exercise both rejection and success. Node strict rejection mode must fail
if a rejected refresh escapes. Also preserve pending-answer duplicate prevention,
request failures, and dirty-field semantics.

Reflection: no new helper, retries, timer, dependency or API change is needed.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Clear submitted unchanged input then call refresh without await | C1, C2, C4, C5 | Accepted | Smallest fix preserving existing error and field handling |
| New helper/timeout or duplicated catch | C2 | Rejected | Existing helper already handles the failure at its owner |
| Test only immediately resolved usage | C3 | Rejected | Cannot detect the reported pending-GET lifecycle |
| Broader browser/accessibility acceptance | W1 | Deferred | No visual/semantic changes; not established by Node tests |

#### Cycle Re-entry Evaluation

No additional cycle is needed: all scoped questions are answered; the
contrarian wave exposed and addressed the masking test fixture.

## Evidence Log

### Codebase Evidence

| ID | Finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Answer is appended before awaited refresh; clear and finally follow that await | src/api/src/zava_forward/api/web/chat.js:390 | view | High |
| C2 | Usage request and showUsage are inside a try/catch reporting independent failure | src/api/src/zava_forward/api/web/chat.js:326 | view | High |
| C3 | Existing JS regression uses DOM/shipped_helpers and immediate usage fixture | src/api/tests/test_case_journey.py:964 | view | High |
| C4 | Cleanup preserves raw changed text and dirty state | src/api/src/zava_forward/api/web/chat.js:140; src/api/src/zava_forward/api/web/app.js:994 | view | High |
| C5 | Handler promises own shared busy/duplicate lifecycle | src/api/src/zava_forward/api/web/async-action.js:40 | view | High |
| C6 | API guide owns the audit-only usage UX description | src/api/README.md:3388 | view | High |
| C7 | System Python lacks installed API distribution and Ruff is not on PATH | Local dependency probes on 2026-10-29 | bash | High |

### External Evidence

| ID | Finding | Source | Retrieved | Confidence |
| --- | --- | --- | --- | --- |
| W1 | Async UI feedback should remain accessible and expose failures near controls | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-10-29 | High |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence |
| --- | --- | --- |
| Q1 | Secondary await prolongs the handler and finally cleanup | C1, C5 |
| Q2 | Existing caught refresh can run independently; retain raw-field guard | C2, C4 |
| Q3 | Add deferred usage cases to the existing shipped-JS regression module | C3 |

## Alternatives and Decision State

Selected recommendation: clear unchanged submitted input, then invoke
refreshUsage without await; retain finally for button/focus recovery.
Add a focused Node regression using existing DOM and shipped helper fixtures,
deferred answer and usage responses, strict unhandled rejection behavior,
both usage outcomes and an edited-input case. Update the existing API usage
paragraph (C6), without creating a knowledge-base page for this narrow fix.

## Open Questions, Risks, and Residual Uncertainty

Dependencies must be restored locally after an actual missing-dependency test
failure. No browser, hosted CI, legal, human or production acceptance is claimed.
Overlapping usage reads may finish out of order; this is advisory audit-only
text, not control authority, and request sequencing is outside the named finding.

## Current Decisions

Reuse the clean caller-selected active branch and open PR. Make one local
commit, no push. Publication-only complete local gate and hosted/human approval
remain separate; the user requests relevant focused validation, not publication.

## Potential Next Research

None required to plan the bounded fix.

## Planning Readiness

Ready. Research disposition: executed. All three waves completed inline.
No research blockers. Parent RPI Agent owns transition to Plan.

## Artifact Self-check

Brief, posture, controls, extension provenance, participation, evidence,
alternatives, all waves, decisions and readiness recorded. No production edits
were made during research.
