---
title: PR 507 integration phase details
ms.date: 2026-10-29
---

## Metadata

Task ID: pr-507-refresh-2026-10-29. Slug: rubric-src-198-refresh.
Plan: .copilot-tracking/plans/2026-10-29/rubric-src-198-refresh-plan.md.
Research: .copilot-tracking/research/2026-10-29/rubric-src-198-refresh-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01 |
| P02 | Complete | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Integrate authoritative main

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase and reconcile documents

Context: one branch commit, three predicted doc conflicts. New untracked
evidence is task-owned and non-colliding; no unrelated dirty input existed.
Intent: execute `git rebase origin/main`, preserving main as ancestor and both
additive sides in docs/architecture/cutover-evidence-pack.md,
docs/reference/README.md and docs/reference/log.md. Use main's complete
.github/rubric tree and scenario-manifest.json even for cleanly applied edits.
Do not silently re-pin hashes or edit historical evidence. Verify original
artifact blobs unchanged, main log exact prefix, both index contributions and
main rubric/manifest identity. No application edits or Azure calls.
Completion: no unresolved entries, ancestry and byte-preservation evidence.
Unresolved: none. Rebase complete at `8cc5000c`; main is an ancestor.
Three conflict resolutions retained both sides. Main-owned inputs restored.

<!-- rpi:phase id=P02 -->
## P02: Validate the integration

Depends on P01. Explicit local source/test roots avoid other worktrees.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run bounded local checks and record exact results

From src/core and src/api, use `/tmp/mv/bin/python -m ruff check .`,
`-m ruff format --check .` and `-m mypy`.
Core unittest selector: test_scenario_manifest, test_dependency_rule.
API unittest selector: test_dependency_rule; add only relevant existing selectors
if scenario provenance reveals a tightly coupled integration defect.
PYTHONPATH starts with each local src:tests then sibling core/agents source
and test roots. Main's existing rubric tests may require system Python pytest
because /tmp/mv lacks pytest; first test availability, then use an existing
runner or record a missing-tool failure before restoring declared dependencies.
Never run full API discovery without the user-specified successful lock probe
and lock ownership throughout execution. No new tests, no coverage dilution.
Completion: exact commands, counts and limitations in changes artifact.
Actual: core/API Ruff, format and mypy pass; core 10 and API 2 focused tests
pass. Main rubric suite: 18 failed, 355 passed, seven unavailable-runtime skips.
Its executable inputs and workflows are byte-identical to main; do not repair
them against the owner's explicit policy. Full API discovery not selected.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile evidence for independent Review and local commit

Preserve old critique/Review as historical. Record rebase conflict dispositions
and all new validation results. Reconcile plan markers and details before the
single independent Review. Review writes only its dated artifact and routes
findings later; no same-task fix/re-review loop. Resolve authenticated account
before committing; set repository-local privacy-safe email, use same author
and committer, Conventional Commit and Copilot coauthor trailer. No push.
Implementation completion: pre-Review reconciliation complete, validation and
follow-ups current, all source work complete. The parent lifecycle owns the
single Review and subsequent local commit; publication/hosted checks remain
separate. No source change is authorized after Review in this task.
