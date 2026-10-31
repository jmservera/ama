<!-- markdownlint-disable-file -->
# Research: AI metering publication remainder

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/ai-metering-432-publication-research.md |

## Research Brief

* Target: finish the explicitly selected publication follow-up of issue #432.
* Purpose/audience: establish an honest, independently reviewed candidate and
  evidence for the owner's main-targeting PR.
* Scope: previous correction evidence, current main, publication runner lock
  ownership, complete local gate, exact-head review and GitHub publication.
* Non-goals: paid inference, Azure, private data, operational economics approval,
  issue-wide closure or rewriting original adverse critique/Review evidence.
* Criteria: non-rewriting main merge; main's rubric score on conflict; queued
  shared-lock admission; full gate and honest baseline exceptions; normal push
  and PR with Refs #432 unless all nine criteria are proven.
* Requested outputs: dated Research/Plan/Implement/Review evidence and PR.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | How can the requested outer flock safely compose with the self-locking gate? What main/review/acceptance evidence remains? |
| Codebase scope | tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md, existing #432 evidence |
| External scope | GitHub issue/branch/PR metadata; local util-linux flock contract |
| Initial internal areas | Prior correction changes/state; runner heavy_lock and full receipt contracts |
| Initial external areas | origin/main and fix/gate-baseline-b023 lifecycle |
| Posture / provenance | focused; bounded caller-selected publication remainder |
| Limits | flock -w 1800; pip only; no force push, secrets or paid calls |
| Completion basis | Answer material lock/publication questions; preserve operational unknowns |
| Research edits | Evidence/state only |
| Evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance / authority | Disposition |
| --- | --- | --- | --- |
| Instructions | Repository instructions | Source/knowledge/branch/gate boundaries | Selected; explicit caller queued-lock direction supersedes earlier nonqueued preference, not evidence integrity |
| Skill | rpi-research | Installed research contract | Selected |
| Specialist | RPI Researcher | Registered independent research lanes | Skipped; one tightly coupled, low-volume trace |
| Web skills | UI design/accessibility | No proposed web edits | Not applicable |

## Participation and Direction Controls

* User explicitly selected the remaining full RPI loop and authorised merge,
  queued gate, push and PR. This continues the recorded automatic session as
  a child task; no new routine approval is needed or available.
* Preserve the parent Review Complete / Defects found and correction evidence.
  This child gets one critique and one Review, not a replacement parent verdict.
* Known main B023/chat failures may be recorded and published under the caller's
  explicit exception, never called a passing full gate.

## Prior Knowledge Gate

Read the caller-named correction changes first, then original/current project
framing, knowledge index/memory/sector primer and parent correction state.
The lock timeout is historical adverse evidence, not a receipt. The working
branch is clean, has no open PR and fetched main remains a75bbdff.

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Remaining acceptance/publication boundary? | straightforward | High | Answered: source-only Refs; missing operational evidence persists |
| Q2 | Outer flock plus runner self-lock composition? | depth | High | Answered: validate and duplicate explicitly inherited fd, then assert exclusive ownership without unlocking it |
| Q3 | Main baseline fix landed? | straightforward | High | Answered at intake: no matching PR; refetch before publication |

## Research Cycle Log

### Cycle 1

#### Wider

Inline evidence: supplied correction changes, original Review, parent state,
current main/issue/open PR queries, full gate README and runner entry point.
Reflection: source work is complete but full integration receipt and publication
are unperformed. All nine operational criteria are not proven.

#### Deeper

Inline trace: runner opens the same lock independently at tools/rpi-checks.py:2275
and holds it through Runner.run and verify. An ordinary outer flock therefore
self-deadlocks. Investigate inherited lock ownership and runner tests before
selecting a safe, minimal composition. Local util-linux 2.39.3 probe on an
isolated task-owned lock confirms fd 3 survives exec and a nonblocking
exclusive flock on that descriptor shares the outer lock.

#### Contrarian

Inline challenge: releasing and reopening introduces an avoidable ownership gap;
environment monkeypatching bypasses the reviewed runner. Neither is acceptable.
An optional explicit borrowed descriptor can preserve continuous exclusion:
compare descriptor/path regular-file inode/device without following symlinks,
duplicate it, assert nonblocking exclusive flock, and retain the caller's
descriptor and lock through run/verification. The default open/wait path remains
unchanged. Invalid/wrong/contended descriptors must fail closed.

#### Parent Synthesis and Disposition

* Accepted C2/C5: narrowly add inherited-descriptor support plus actual outer
  flock subprocess and contention/error tests.
* Rejected C2/C3: unlock/reacquire, skip locking or runtime monkeypatching.
* Deferred W1/C4: operational economics, resident/historical coverage and real
  presentation delivery remain parent follow-ups, not publication changes.
* Re-entry: no; Q1-Q3 are answered within the focused boundary. Test the selected
  contract in Implement, with independent critique before it and Review after it.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | No runner group or receipt from prior 600-second timeout | .copilot-tracking/changes/2026-10-31/ai-metering-432-review-findings-changes.md:95 | High |
| C2 | Runner independently opens flock and verifies while locked | tools/rpi-checks.py:2275; tools/rpi-checks.py:2346 | High |
| C3 | Full receipt must bind clean exact HEAD/current base | src/README.md:208 | High |
| C4 | Parent corrections are implementation observations, original Review adverse | .copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-review-findings-state.json:21 | High |
| C5 | Existing runner lock test redirects os.open to an owned temporary lock; reuse its isolated test pattern | tools/test_rpi_checks.py:491 | High |
| W1 | Issue has nine criteria and missing operational price/billing/batch inputs | https://github.com/jmservera/ama/issues/432; retrieved 2026-10-31 | High |

## Alternatives and Decision State

Selected: optional validated inherited lock FD, explicitly supplied under the
requested outer flock. C2/C3/C5 support the minimal change to runner, its tests
and directly related README. Existing standalone admission and receipt checks
are preserved. Do not release a foreign owner's lock, rewrite parent outcomes
or infer billing. Rejected alternatives and rationale are recorded in Contrarian.

## Open Questions and Risks

* Safe outer-lock composition must preserve lock ownership across all groups.
* Main may advance while queued; fresh merge/gate is required on changed base.
* Known baseline exceptions are explicit adverse evidence, not passing receipts.

## Readiness and Self-check

Research disposition: executed, Complete. Planning Readiness: Ready on
C1-C5/W1; safe lock contract is specified, runtime tests remain implementation
gates, not research observations. Inline-only participation is accurate.
No raw case data, credentials or operational financial numbers were read.

## Findings, Decisions and Continuation

Q1 -> C1/C3/C4/W1: publication is still required and issue-wide acceptance is
unproven. Q2 -> C2/C5: optional inherited lock is necessary for literal queued
flock composition. Q3 -> fetched main a75bbdff: no baseline-fix PR at intake;
refetch if the known failure occurs and immediately before final publication.
All decisions are parent-owned; scope and authorisations are caller-confirmed.
No new business/financial decision is required. Potential next research is
deferred to the existing operational follow-ups when owner evidence is supplied.

Acting owner: confirmed automatic RPI Agent; next action Plan, with one
independent critique. Gates: implementation tests, complete local gate,
independent child Review and current-base verification pending.

## Sources

* W1 - Issue #432 - https://github.com/jmservera/ama/issues/432
  (retrieved 2026-10-31).

## Artifact Self-check

Questions, all three ordered waves/reflections, dispositions, alternatives,
extension provenance, evidence IDs, caller controls, residual risks and
planning/continuation state checked. No delegated lane or operational approval
is implied. No further material in-scope research source is missing.
