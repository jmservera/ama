---
title: Setup Entra expiry issue 358 phase details
description: Current-source verification and evidence-only implementation tasks
ms.date: 2026-10-30
---

## Metadata

Task ID: 358. Slug: setup-entra-expiry-358.
Plan: .copilot-tracking/plans/2026-10-30/setup-entra-expiry-358-plan.md.
Research: .copilot-tracking/research/2026-10-30/setup-entra-expiry-358-research.md.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Preserve implementation and refresh acceptance evidence | P01-T01/T02 complete; Review pending | P01-T01 through P01-T03 |

<!-- rpi:phase id=P01 -->
## P01: Preserve implementation and refresh acceptance evidence

Already-merged work satisfies original local coverage requests; remaining live
criterion is not executable under caller limits. No new source or tests,
no removals, no generated targets. Implementation is documentation/evidence
only; no frontend changes or browser/axe requirement is triggered.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Run existing local regression and requested project checks

Use Python 3.12 and pip, run-owned environment under the external session
folder at
`/home/azureuser/.copilot/session-state/ff88c0b4-017d-4da1-9a9a-a3ea3c2615fd/files/issue-358`.
Retain the caller's exact shared lock; PC-001's asserted project-only boundary
does not apply to the parent runtime and is rejected, not silently waived.
Missing ruff/mypy/aiohttp were observed before install. Install existing
core/agents/API distributions with pip and their dev dependencies as needed.
Existing infra setup tests patch subprocess transport with FakeAzure and
temporary synthetic profiles. These are not real credential files or live CLI
invocations. Preserve this distinction in all acceptance statements.

Run under `flock -w 600 /tmp/ama-rpi-heavy.lock`:
`python3 -m unittest discover -s infra/tests -p test_setup_entra.py -q` and
`python3 -m unittest discover -s infra/tests -p test_initialize_api_auth.py -q`.
From `src/api`, run
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`,
`ruff check .`, `ruff format --check .`, and `mypy`.
Record exit status separately, not a chained success that hides later checks.
Stop/retry only missing dependencies or task-caused failures; do not fix
unrelated existing API issues. Completion means actual results documented,
not that a failure or skip counts as passing acceptance.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Document current acceptance and implementation disposition

Add a dated subsection adjacent to the existing preservation explanation in
`infra/README.md`. Preserve all historical counts and outcomes as dated
history; state current source still includes safeguards, no code defect
demonstrated, live original criterion unproven, no Azure performed.
Only runbook and current dated artifacts may change.
Changes record must contain command outcomes and AC matrix.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Independent Review and local handoff

Give one fresh reviewer the plan/details/critique/research/changes pointers,
base SHA and exact candidate diff. Review writes only its canonical artifact.
Require explicit distinction between bounded phase completion and issue
acceptance. Preserve original critique and Review outcomes. Do not repair
Review findings in this task or repeat Review.
Resolve privacy-safe authenticated git identity, commit locally with
`Refs #358` and required coauthor trailer. No push or remote write.
After the commit, attempt `tools/rpi-checks.py --all --base` with the supplied
base and new external output directory. This existing runner itself holds
`/tmp/ama-rpi-heavy.lock` with a 600-second acquisition timeout; do not wrap
it in a second flock that deadlocks its internal acquisition.
Coordinator owns current-main receipt verification/publication and required
human/hosted approval. A gate failure is not passing evidence.

## Completion Evidence

P01-T01: 124 setup tests and 17 initializer tests passed. API discovery passed
1370 tests with 318 skipped; mypy passed 116 source files. Initial Ruff
invocations failed before analysis due to `RUFF_NO_CACHE=1`; retry with
`true` passed lint and format (60 files already formatted).
P01-T02: dated runbook reassessment added; source/tests/history unchanged.
P01-T03: independent Review and local commit remain pending.

## Unresolved Items

AC2 remains blocked by explicit no-Azure/no-credentials direction. Full local
publication receipt and exact-head assessment are not claimed by this plan.
