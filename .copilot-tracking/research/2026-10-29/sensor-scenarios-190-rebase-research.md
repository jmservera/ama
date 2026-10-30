<!-- markdownlint-disable-file -->
---
title: Sensor scenarios PR 505 rebase research
description: Focused evidence for reconciling PR 505 with current main
ms.date: 2026-10-29
---

# Task Research: sensor-scenarios-190-rebase

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Research disposition | executed |
| Evidence root | .copilot-tracking/ |

## Research Brief

* Research target: current PR 505 ancestry, relevant upstream changes,
  conflict ownership, scenario provenance and local CI selectors.
* Purpose and audience: provide the coordinator a locally validated, rebased
  candidate without pushing or changing draft/approval status.
* Scope: existing feat/sensor-scenarios-190 branch, source in src/, tests
  outside installed packages, related docs and dated RPI evidence.
* Non-goals: new sensor features, issue closure, live services, private data,
  publication, changing required checks or historical review outcomes.
* Criteria: preserve both sides' behavior, main-owned rubric and scenario
  manifest, correct hashes, Ruff/format/mypy and relevant unittest coverage.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What conflicts exist; which source/manifest and CI contracts must remain valid? |
| Codebase scope | src/core, src/api, scenario manifest, .github/rubric, related docs |
| External scope | Read-only PR 505 metadata and GitHub identity |
| Initial internal areas | Existing 2026-10-27 RPI state; component guides and pyproject files; synthetic source/tests |
| Initial external areas | PR 505 |
| Posture | focused, inferred from bounded caller request |
| Explicit limits | /tmp/mv; no push; no full API suite without successful heavy-lock probe |
| Completion basis | Material task questions answered with current source evidence |
| Source edits during research | None |

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instructions | Repository AMA guidance | Selected: branch safeguards, installed namespace, original evidence retention |
| Skills | rpi / rpi-research | Selected: dated phase evidence and ordered loop |
| Skills | Frontend/design | Skipped: no web changes intended |
| Specialists | RPI Researcher | Skipped: one tightly coupled, bounded trace handled inline |
| Independent agents | Plan critique and final Review | Required in their owning later phases |

## User Participation and Direction Controls

The explicit full-loop request selects this follow-up of the recorded running
automatic parent task. It authorizes rebase/history rewriting on this branch
and a new Conventional Commit, but explicitly prohibits push. No new mode
switch or publication consent is inferred. Non-interactive execution uses the
provided conflict policy; no ordinary decision remains for clarification.
Preserve all original 2026-10-27 adverse findings and downstream limitations.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What is the branch/base and relevant conflict scope? | straightforward | Answered |
| Q2 | Which pinned sources and checks can change on rebase? | depth | Answered |
| Q3 | What can local results establish without a push? | straightforward | Answered |

## Prior Knowledge Gate

Read original/addendum, reference index/memory, sector primer, src/README,
core/API pyprojects and original RPI state. Original Review is Not accepted;
this follow-up does not rewrite it or imply parent issue acceptance.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial branch is clean and matches the open draft PR. Fetch succeeded.
Two branch-only commits add sensor scenarios and original RPI evidence.
PR metadata reports CONFLICTING / DIRTY. Relevant implementation scope is
one new core module and its external test module; source already uses src/.

Reflection: prioritize upstream source/manifest contracts and documentation
over unrelated incoming changes.

#### Wave 2: Deeper

Main is b0364e4b326936715d69ab1d75040c4528282af7. The
09099ecd1a66ee9d37ad993707d1f2eda07cdfd4 merge base precedes extensive
documentation updates. Main has no scenario module/test, but changes the
indoor projection and backfill versions. The readings call signature is still
compatible. Main updates the scenario manifest's workbench/recipe hashes.
The installed /tmp/mv interpreter exists (Python 3.12.3), but importing
zava_forward.core fails: install local distributions before tests.

Reflection: retain main's model changes and verify scenario expectations
against them instead of restoring old model behavior. Primary anticipated
conflicts are the reference index/log and core guide.

#### Wave 3: Contrarian

Challenged the assumption that a clean rebase establishes CI success.
Hosted checks cannot assess unpushed HEAD, original parent acceptance remains
adverse, and a passing manifest hash only proves fixture binding. Main's
physics change may shift scenario deltas, so tests must assert exact 15-check
shape and fixed-truth sensitivity rather than merely CLI success.
The heavy-lock probe succeeded, but does not reserve the resource; avoid full
API discovery and select only relevant modules.

Reflection: narrow validation remains meaningful without taking a long shared
lock. Keep full publication gate, hosted checks and human acceptance distinct.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Rebase and selective documentation reconciliation | C1, W1 | Accepted | Explicit caller direction; preserve unmerged branch work |
| Main-owned rubric/manifest | C4 | Accepted | Newer source pins and caller policy |
| Restore old sensor model | C5 | Rejected | Discards independent upstream behavior |
| Local tests establish hosted green status | C2, W1 | Rejected | No push means no new hosted execution |

#### Cycle Re-entry Evaluation

No further cycle required: focused ancestry, APIs, pin contracts and relevant
validation are identified. Actual conflicts and test failures are implementation
evidence; they do not justify unrelated discovery.

## Evidence Log

| ID | Claim | Location / command | Confidence |
| --- | --- | --- | --- |
| C1 | Original task completed with adverse Review and routed dependencies | .copilot-tracking/rpi-sessions/2026-10-27/sensor-scenarios-190-state.json:1 | High |
| C2 | Source/test commands and local gate distinguish local from hosted acceptance | src/README.md:48 | High |
| C3 | Core/API define project Ruff/format/mypy scopes | src/core/pyproject.toml:29; src/api/pyproject.toml:34 | High |
| C4 | Manifest validates four allowlisted file hashes | src/core/src/zava_forward/core/synthetic/scenario_manifest.py:35,97 | High |
| C5 | Scenario generator calls backfill readings and overlays synthetic profiles | src/core/src/zava_forward/core/synthetic/sensor_scenarios.py:217,250 | High |
| C6 | Tests assert eleven cases, fifteen checks, fixed-truth confusion/sensitivity and installed CLI | src/core/tests/test_sensor_scenarios.py:36,95,348 | High |
| C7 | Source CI runs component lint/format/mypy plus unit discovery | .github/workflows/src-ci.yml:73 | High |
| W1 | PR remains open/draft and conflicting at intake | https://github.com/jmservera/ama/pull/505 (retrieved 2026-10-29) | High |

## Findings, Alternatives and Decision State

Q1: rebase the two existing commits onto fetched main; reconcile docs manually.
Q2: retain upstream backfill/projection behavior, main-owned manifest and
rubric, and validate actual source hashes and scenario expectations.
Q3: commit a clean descendant with local commands/results; leave hosted CI,
draft readiness and publication to the coordinator. These findings are
high-confidence within the fetched-base boundary (C1-C7, W1).

Selected recommendation: caller-directed rebase with targeted regression and
project-wide static checks. A merge commit is rejected by caller direction.
Blanket conflict resolution is rejected because it can discard either side.
No external technical sources used; GitHub metadata is the only external input.

## Open Questions, Risks and Residual Uncertainty

Hosted CI cannot execute for this new candidate without the prohibited push.
Mergeability here means conflict-free ancestry and local evidence, not a
fresh GitHub mergeability/CI result.

## Planning Readiness

Ready. Research executed; Q1-Q3 answered (C1-C7, W1). No implementation
readiness blocker. Missing installed packages is an actionable setup step,
not evidence of an application defect. Self-check: questions/evidence,
three ordered waves, alternatives, constraints and residual risks recorded.
