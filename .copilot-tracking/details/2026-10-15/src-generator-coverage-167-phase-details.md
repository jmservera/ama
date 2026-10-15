---
title: Generator coverage phase details
description: Issue 167 task-level completion boundaries
ms.date: 2026-10-15
---

Task #167, slug `src-generator-coverage-167`. P01-T01/T02 and P02-T01 complete,
with matching changes evidence. P02-T02 is parent-owned publication after the
single Review, not pending source implementation. Critique PC-001 addressed.

<!-- P01 -->
## P01: Metadata coverage gate

<!-- P01-T01 -->
### P01-T01: Validator and report

Create `src/core/src/zava_forward/core/synthetic/coverage.py` and
`src/core/tests/test_generator_coverage.py`. Use standard-library validation
with typed object guards; do not introduce schema packages or silent defaults.
Input is the public inventory JSON, never a dataset. Reject empty/duplicate
IDs, unsupported statuses, blank labels/rationale, invalid issue references,
unexplained deferrals, and delivered partial/missing needs.
Report all rows, coverage totals, declared conventions and open owner items.
Keep declaration validation distinct from actual generator-output conformance.
Test valid metadata, mutations, deterministic report ordering, and CLI
success/nonzero errors with temporary metadata files explicitly rooted under
the ignored `src/core/tests/__pycache__/` directory; clean each temporary child.
Reuse C4/C5 generator tests instead of duplicating their fixtures.

<!-- P01-T02 -->
### P01-T02: Documentation

Add CLI usage and limits to core README and existing pack gap-closure section.
Update index and append log, preserving all earlier log text. Explicitly
retain pending owner mapping, private stock regeneration and missing output
conformity evidence. Do not change inventory coverage or create owner deferrals.

<!-- P02 -->
## P02: Validation and delivery evidence

<!-- P02-T01 -->
### P02-T01: Local validation

Use the ignored `src/core/.venv/` virtual environment if tools are missing;
pip install editable projects and existing dev extras. Run all five existing
src unittest suites with documented PYTHONPATH, ruff checks/format and mypy.
Run report against merged metadata. Start actual API on loopback with the
existing fictional test dataset in `src/core/.venv/tmp/` temporary ZF_DATA storage;
set TMPDIR to that absolute worktree-local parent for existing suites and pip.
Clean the isolated smoke child after shutdown. Verify health,
static serving and guarded assistant surface, then stop the exact process.
No model billing or Azure mutation. Try Docker and report real permissions
outcome; SQL Server/live AI/Azure/human acceptance stay Not run if unavailable.
Record all command groups/results, including failure and correction.

<!-- P02-T02 -->
### P02-T02: Review and publish

Reconcile plan markers/changes before exactly one rpi-review. Keep material
findings open and route later work, never repeat review.
Use authenticated GitHub identity and requested noreply email, Conventional
Commit/trailer, explicit file staging, non-force push and main PR `Refs #167`.
Include commands/results and unchecked criteria. CI and owner merge remain
outside local acceptance. Do not modify issue checkboxes or merge PR.
