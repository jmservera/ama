---
title: PR 508 current-main rebase research
description: Focused evidence for an unpushed integration refresh
ms.date: 2026-10-29
---

## Research brief

Bring open PR #508, branch `feat/iot-consumer-110`, onto fetched
`origin/main`, preserving IoT behavior and main's concurrent work. Audience:
delivery coordinator. Output mode: convergence. Posture: focused, selected
because the caller specifies the branch, conflict policy and validation.
No push, Azure operations, automatic issue closure or legacy source writes.

## Direction controls and extensions

The explicit full-loop request authorizes all four phases in this invocation;
it does not authorize an ongoing automatic follow-up session. Repository
instructions, source project guides and RPI phase skills apply. Research stays
inline because this is one continuous integration trace. Independent planning
critique and final review remain separate evidence gates. Web, regulatory and
deployment skills are not applicable to this integration-only refresh.
No interaction is needed: scope and conflict decisions are supplied.

## Questions and initial evidence

1. What commits/files diverge and which conflicts need semantic integration?
2. Which current checks demonstrate compatibility without unsafe heavy work?
3. What remains unproven without publishing or Azure access?

## Cycle 1: Wider

Fetched origin on 2026-10-29. Clean worktree, expected branch. PR is OPEN,
currently not draft (despite task wording), targets main and has no reported
hosted checks. Ten branch commits contain bounded IoT source, tests, package
dependencies, documentation and prior immutable RPI evidence.

Reflection: reuse this active workstream; do not recreate or change PR state.

## Cycle 1: Deeper

Main is `5653547507f3056f09a726a18516237728da5e5b`; intake head is
`09bd0a791e58acfcee9ddeb4f1eb05da173c62f5`. New main changes include
sensor-scenario source/tests and core README plus rubric score. Existing
manifest validates pinned public source bytes. `/tmp/mv` is Python 3.12.3;
core/API editable distributions point to this worktree.

Reflection: preserve the new scenario documentation beside the IoT section,
and test scenario behavior and manifest in addition to IoT selectors.

## Cycle 1: Contrarian

Prior correction's static/test success predates main's newest scenario work.
It is not evidence for the rebased tree. No hosted checks are reported, so
local success cannot establish hosted CI. Full API discovery is unnecessary
for this bounded integration unless focused failures justify escalation;
it must never run without nonblocking heavy-lock admission.

Reflection: rerun configured static checks and relevant modules rather than
reuse old success. Honor caller no-push; publication gate and hosted checks
remain coordinator-owned, not fabricated local acceptance.

## Evidence log

* C1: `src/README.md:44` defines outside-package tests and project commands.
* C2: `src/README.md:58` distinguishes focused checks from full publication
  gates; actual full-gate publication policy remains independently applicable.
* C3: `docs/reference/README.md:47` preserves bounded IoT versus live acceptance.
* C4: `docs/reference/memory.md:10` is context, not validation evidence.
* C5: `src/core/tests/test_scenario_manifest.py:21` validates pinned sources.
* C6: `src/api/pyproject.toml:52` defines namespace-aware strict mypy paths.
* C7: `.copilot-tracking/changes/2026-10-29/iot-review-508-changes.md:52`
  provides historical focused selectors, not current validation.

## Decisions and readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Recommend the requested rebase, semantic append preservation, authoritative
main rubric/manifest copies and fresh focused validation. Reject a merge
commit because the caller explicitly requires rebase; reject wholesale
ours/theirs resolution for documentation because it would lose intent.
No further research is justified unless conflicts or validation expose new
material uncertainty. Existing historical artifacts remain intact. No live
acceptance or CI success may be inferred locally.
