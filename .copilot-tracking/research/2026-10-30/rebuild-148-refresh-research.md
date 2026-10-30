---
title: Rebuild 148 branch refresh research
description: Focused integration research for draft PR 511
ms.date: 2026-10-30
---

## Brief

Bring draft PR #511, `feat/rebuild-148`, onto fetched `origin/main`.
Refs #148. Audience: coordinator and independent reviewer. Output:
convergence on a safe local integration, not issue acceptance or deployment.
No push, Azure operations, private data, or legacy executable paths.
Preserve the original 2026-10-27 evidence and open RV-001.

Focused posture follows the explicit bounded task. Repository instructions
and RPI research are selected; web/domain skills and research delegation
are not applicable to this non-UI integration. The full loop is explicitly
requested; no interactive intake is needed.

## Questions and opening state

1. What commits and source projects are affected?
2. Which current-main files must remain authoritative?
3. What validation establishes local integration without claiming hosted CI?

Research disposition: executed. Planning Readiness: Ready.

## Cycle 1

### Wider

`git fetch origin` succeeded on the clean, existing topic branch.
PR #511 is open and draft, targeting main. Two branch commits add the
orchestrator rebuild module, external tests, documentation and original RPI.
Prior hosted project checks pass; rubric conclusion fails and score is
pending. Those statuses describe the old remote head, not this refresh.

### Deeper

Main is `91e890e07af036263316c153cbc7ceff780cdaa2`; original head is
`d18fc2f998b5ebccf021be8cb0b7bac1d5999c67`; merge base is
`f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc`.
Main has no divergent orchestrator files, but updates infra documentation,
rubric scores and scenario-manifest workbench/recipe hashes. Main's manifest
must remain byte-identical and its test must be rerun. Requested /tmp/mv
provides Python 3.12.3 and Ruff 0.17.1.

### Contrarian

The failed rubric conclusion reports `Resource not accessible by integration`,
not an application test failure. Do not patch workflow permissions or discard
main's rubric updates to manufacture success. Fresh hosted execution cannot
occur without the coordinator's push; report that boundary explicitly.
Original RV-001 is outside this refresh and must not be relabelled accepted.

## Evidence

* C1: `src/README.md:64`: local gate and focused-test contracts, exact-head
  receipt constraints and separate hosted/human approval.
* C2: `src/README.md:14`: tests belong outside packages, executable source
  remains under src.
* W1: https://github.com/jmservera/ama/pull/511, retrieved 2026-10-30:
  open draft and existing scope/RV-001.
* C3: `src/orchestrator/pyproject.toml:29`: strict configured mypy includes
  source and external tests with sibling core paths.
* C4: `src/core/tests/test_scenario_manifest.py:21`: validates current pinned
  sources against actual repository files.
* W2: https://github.com/jmservera/ama/actions/runs/40585372759,
  retrieved 2026-10-30: failed conclusion reports integration permissions.

## Decisions and readiness

Preserve scope; do not fix unrelated RV-001 as part of a branch refresh.
User explicitly authorizes rebase/history rewriting locally, not pushing.
Full publication gate may be blocked by shared-host prerequisites or heavy
lock; missing evidence must remain explicit rather than becoming a CI claim.
Selected approach: rebase in place, keep both documentation intents if
conflicted, use current-main rubric/manifest copies, validate bounded offline
selectors and commit with provenance. Merge commits are rejected because the
user explicitly requested rebase. No further research cycle is needed:
all three questions have evidence, and remaining hosted permissions are not
locally resolvable. Self-check: three waves, evidence, non-goals and readiness
recorded; no research delegation or source changes.
