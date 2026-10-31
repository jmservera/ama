---
title: Chromium skip gate research
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Task Research: gate-chromium-skip-572

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher / agent | RPI Agent, rpi-research |
| Status | In progress |
| Artifact path | .copilot-tracking/research/2026-10-31/gate-chromium-skip-572-research.md |

## Research Brief

* Research target: exact Chromium skip recognition, fail-closed skip validation and existing browser execution ownership for #572.
* Purpose and audience: justify a safe bounded gate fix for maintainers.
* Scope: tools/rpi-checks.py, tools/test_rpi_checks.py, browser test decorators, command inventory and pinned CI commands.
* Non-goals: workflow changes, full gate execution, Azure, secrets, publication or issue closure.
* Criteria: recognise the two caller-supplied exact reasons, retain rejection of unknown and integration skips, validate using requested targeted commands.
* Requested outputs: dated research, plan, implementation and independent review evidence; local commit.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which skip boundary is safe, and where do the browser cases execute? |
| Initial internal candidate areas | Gate constants/parser, browser stage, test decorators, CI strict checks |
| External scope | Issue #572 only |
| Research posture / provenance | Focused; bounded caller request |
| Explicit limits | No full gate, workflows, Azure or push; heavy commands use flock |
| Edits allowed during research | Evidence and required state only |
| Resolved evidence root | .copilot-tracking/ |
| Completion basis | All in-scope questions evidence-backed after wider, deeper and contrarian waves |

## Extension Registry and Provenance

| Kind | Candidate | Provenance / authority | Disposition |
| --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Repository-wide; branch, evidence and publication safeguards | Selected; caller explicitly prohibits full gate and publication |
| Skill | rpi-research | RPI phase; read-only three-wave research | Selected |
| Specialist | hve-core-all:rpi-researcher | Registered independent research lanes | Skipped; one tightly coupled bounded trace |

## User Participation and Research Decisions

Caller explicitly requests all four phases and local commit. No interactive checkpoint
is needed or available. Issue acceptance is broader than the authorised bounded fix;
preserve that distinction and use Refs #572 only.

## Direction Controls

* Reuse the clean fix/gate-chromium-skip-572 branch at origin/main 4cb5964f.
* Enumerate exact reasons or safely run opt-in tests; justify choice.
* Do not alter pinned workflows or run the complete gate.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How are expected, unexpected and integration skips distinguished? | Straightforward | Open |
| Q2 | Are both Chromium cases already owned by required browser execution? | Depth | Open |
| Q3 | Which bounded alternative preserves the contract with least risk? | Depth | Open |

## Prior Knowledge Gate

Read issue #572 and repository case-study, knowledge-base index and owner memory.
Verified clean branch, exact requested base and no remote branch or existing PR.
Supplied issue evidence is historical and not a current execution receipt.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial search locates exact skip validation, browser opt-in environment and pinned
strict CI checks. Next examine parser semantics and both browser execution lists.
Inline investigation is proportionate; no worker ran.

#### Wave 2: Deeper

Verified that the merged base already owns exact chat-panel execution with
ZF_BROWSER_TESTS=1 after Chromium installation, in both the required command
inventory and Runner.browser. Existing regressions verify dispatch and receipt
rejection for missing flags/selectors/skips/zero execution. The remaining new
asset test skips only when Playwright reports a missing executable.
Reflection: do not duplicate the already merged chat execution fix.

#### Wave 3: Contrarian

Compared globally enabling opt-in discovery against explicit recognition.
Discovery precedes browser installation; moving installation/flags would change
stage prerequisites and run the chat browser journey twice. Broad recognition
could lose the merged chat test-ID/group safeguard, so retain it explicitly even
when enumerating both exact reasons. Integration mode must still reject both.
The asset browser regression is not a dedicated required browser-stage selector;
recognising its known discovery skip does not prove later execution.

#### Parent Synthesis and Disposition

Accept exact enumeration with preserved chat scoping (C1-C4). Reject changed
discovery scheduling as unnecessary lifecycle churn. Defer actual Chromium and
complete exact-head gate evidence to later authorised publication work.
No additional cycle is needed: the bounded questions are answered.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Existing reasons are exact; chat exception is scoped by group, test ID and non-integration mode | tools/rpi-checks.py:63,1021 | High |
| C2 | Chat selector runs after install, with opt-in and integration=True, in inventory and runner | tools/rpi-checks.py:695,1592 | High |
| C3 | Existing regressions cover exact dispatch, receipt binding and fail-closed chat skips | tools/test_rpi_checks.py:29,89,119 | High |
| C4 | Asset test skips only missing Chromium executable with the new exact reason | src/api/tests/test_browser_asset_urls.py:51 | High |
| C5 | Chat decorator requires ZF_BROWSER_TESTS=1 | src/api/tests/test_chat_panel.py:563 | High |
| C6 | Pinned workflow defines the requested unit/Ruff/mypy commands | .github/workflows/src-ci.yml:243 | High |
| C7 | Existing guide documents strict scoped chat discovery and actual required browser execution | src/README.md:175 | High |

External source: https://github.com/jmservera/ama/issues/572, retrieved 2026-10-31
with gh issue view 572. Historical failure is not a current receipt.
Prior-session lookup found no matching recent research. No external web research.

## Alternatives and Decision State

Select enumeration of both exact reasons while retaining existing chat-specific
group/test identity checks. This addresses the caller's bounded request without
accepting unknown skips, permitting integration skips or altering browser stage
ordering. Update the directly related guide and regressions.

Issue criteria remain partially unmet: no actual Chromium execution or fresh
complete browser/MSSQL gate is authorised in this task. No issue closure claim.

## Planning Readiness

Ready. Research disposition: executed. Q1-Q3 answered by C1-C7.
Self-check: all three waves completed in order; sources are located; alternatives,
caller exclusions and residual acceptance gaps are explicit. No research-phase
source edits. Parent next action: Plan using this evidence.
