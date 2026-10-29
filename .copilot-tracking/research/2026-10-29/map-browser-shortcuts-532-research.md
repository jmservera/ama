<!-- markdownlint-disable-file -->

# Task Research: map-browser-shortcuts-532

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/map-browser-shortcuts-532-research.md |

## Research Brief

* What: correct map interception of Ctrl, Meta and Alt shortcuts while retaining Shift-generated plus.
* Why / audience: PR #539 correction, Refs #532; protect employee browser navigation and zoom.
* Scope: existing app.js map handler, map browser check, directly related README and any affected manifest pins.
* Non-goals: redesign, Azure, private data, push, merge, issue closure or publication.
* Criteria: modifier events remain uncancelled and do not pan/zoom from both map and marker focus; ordinary controls still work.
* Outputs / mode: dated full RPI evidence and local commits; convergence.

## Research Parameters

* Posture: focused (bounded named source and supplied review finding).
* Evidence root: .copilot-tracking/research/2026-10-29/.
* Internal candidates: src/api map handler/check/README; prior issue-532 evidence; scenario manifest.
* External candidates: required current Web Interface Guidelines only.
* Limits: nonblocking /tmp/ama-rpi-heavy.lock; if busy, targeted tests only. No az or remote writes.
* Research edits: evidence and workflow state only.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | Repository guidance supplied in conversation | Selected: src layout, local identity, dated evidence, validation and source pins |
| Skill | rpi-research | Selected: focused three-wave investigation |
| Skill | web-design-guidelines | Selected: current source fetched 2026-10-29; keyboard defaults apply |
| Skill | redesign-existing-projects / public-page design skills | Skipped: behavioral correction, no redesign |
| Specialist | RPI Researcher | Skipped: one tightly coupled low-volume trace; inline research |

## User Participation and Research Decisions

Explicit full-loop request authorizes automatic progression for this correction.
No questions needed; caller supplied exact branch, finding and validation boundary.

## Direction Controls

Preserve Shift plus, ignore Ctrl/Meta/Alt without preventDefault, add assertions
to the existing map browser check. Commit locally only with the requested trailer.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Where are map keys consumed and how do marker events reach the map? | straightforward | Answered |
| Q2 | How can the existing browser check prove cancellation and map invariance without navigating away? | depth | Answered |
| Q3 | What validation, dependencies and pin updates are required? | straightforward | Answered with environment deviation |

## Prior Knowledge Gate

Clean worktree, matching open PR #539 and feat/map-fullscreen-532 verified.
Original case study, addendum, reference index and owner memory read for context.
Prior map artifacts are starting evidence, not current validation.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial reads identify a single custom map keydown handler with Leaflet keyboard
disabled and an existing real-app Playwright check with integrity-pinned axe.
Reflection: inspect marker propagation, check completion/reporting and pin scope
before choosing exact assertions.

#### Wave 2: Deeper

Inline inspection: point markers use mapAction, and arrow/zoom keys bubble to
the map element. Its Leaflet keyboard handler is disabled. Browser runner starts
its own real loopback server and explicitly loads this worktree's src packages.
Manifest sources do not include any proposed edited file (C4-C6).
Reflection: one early modifier guard is sufficient, without disabling Shift.

#### Wave 3: Contrarian

Challenge: real Alt+Left would navigate away; real Ctrl/Meta zoom is not portable
in headless Chromium. Use bubbling, cancelable KeyboardEvents on actually focused
map/marker nodes to inspect dispatch cancellation directly; independently assert
no map-pane DOM/transform change or map requests. Retain trusted keyboard checks
for ordinary panning and add real Shift-plus, equals and minus with exact map
API zoom deltas. Reject blanket modifier/Shift rejection because plus requires
Shift on common layouts. Reflection: synthetic tests establish uncancelled
delivery, not actual browser chrome zoom/history behavior.

#### Parent Synthesis and Disposition

* Accepted: early Ctrl/Meta/Alt return before map commands (C1).
* Accepted: focused cancellation and map-invariance matrix in both modes and
  focus targets, plus positive trusted-key tests (C2, C4).
* Rejected: stopPropagation/preventDefault for modified keys, or blocking Shift.
* Deferred: human AT, staff usability and external publication remain separate.
* Re-entry: not needed; bounded behavior and runner contracts are covered.

## Evidence Log

| ID | Location | Finding |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/web/app.js:1592-1603 | Custom handler ignores consumed/control events but not modifiers; cancels recognized pan/zoom keys |
| C2 | src/api/checks/map_fullscreen_browser_check.py:16-29 | Existing check scans embedded/expanded map states with pinned axe |
| C3 | src/api/README.md:114-152 | Map behavior and focused runner are documented |
| C4 | src/api/src/zava_forward/api/web/app.js:1658-1663 | Point markers attach existing shared mapAction and remain descendants of the key handler |
| C5 | src/api/checks/design_system_browser_check.py:227-258 | Constructed loopback runner uses sys.executable and this worktree's src source paths |
| C6 | docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:48-53 | Four pinned source paths do not include app.js, map check or README; no pin update required |
| C7 | .copilot-tracking/rpi-sessions/2026-10-28/map-fullscreen-532-state.json | Original Review Not accepted; RV-001 is this selected correction; retain original evidence |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-29) | Keyboard interaction and native navigation/zoom must remain usable |

## Alternatives and Decision State

Select the early modifier guard and existing-check extension. No new test file,
framework, helper module or production fallback is needed. No source changed
during Research.

## Risks and Residual Uncertainty

The requested /home/azureuser/source/ama-wt/issue-526-journey/.venv does not
exist, nor does its parent worktree (verified with ls). Use the already existing
/tmp/ama-532-venv from original map validation as an explicit environment
deviation, always with this worktree's source packages first on PYTHONPATH.
Do not recreate a removed shared worktree or alter another environment.
Full publication gate remains outside this no-push/no-az correction.

## Self-check

Three waves completed inline; evidence answers Q1-Q3; source pins examined;
prior failure retained; no private data or remote writes; no further material
research gap. External guidelines retrieved completely on 2026-10-29.

## Planning Readiness

Ready; Research disposition: executed. Parent next action: Plan.
