---
title: Issue 176 recovery phase details
description: Exact inspection, validation and publication boundaries
ms.date: 2026-10-17
---

Task ID 176; synthetic-determinism-176. No change in original task identity.
Initial direction: verify the completed 2026-10-16 plan and critique, then
inspect/test the delivered feature. Fresh Research found no upstream drift,
but historical merges are not universally docs-only and the independent
MERGE receipt is unavailable. These are reporting corrections, not source bugs.

## P01

P01-T01: inspect stock_fabric.py, provenance.py, data_paths.py, the full
stock-fabric tests and the already safety-inspected three companion modules.
Compare original plan requirements and PC-001/002 to actual implementation.
Confirm reads/validation precede output publication and provenance reveals
only logical names/digests. Do not open default data or execute against it.

P01-T02: first try the chosen validation command using system Python. If
the package/tool is missing, create an exclusive mktemp-owned `/tmp` venv
and install `src/core[dev]` editable with pip and normal build isolation.
Use the venv's Python for four named unittest modules with absolute
core/tests PYTHONPATH. Run Ruff check/format for the whole core project
and project mypy, matching src-ci.yml. Capture exact commands, version,
exit codes and outputs in dated tracked evidence. Clean only the exact
owned venv at task completion; never reuse/delete another session's path.
Tests supply fictional sources and TemporaryDirectory output. No separate
fake stock baseline or continuing-stock substitute is created.

## P02

P01 handoff: inspection found no introduced defect. Fresh Python 3.12.3
execution passed 45 tests, no skips, in 10.154s; whole-core Ruff check,
47-file format check and 100-file mypy passed. Actual output is retained
in the 2026-10-17 changes directory. No source or test edits. P02 may proceed.

P02-T01: one new recovery Review after completed inspection/validation.
Reconcile plan, current diff, changes, acceptance, historical versus fresh
evidence and all findings. Preserve RV-001/002. If a genuine blocking bug
appears, do not claim successful delivery while it remains unresolved.
The old Review is historical; this is a user-requested new recovery pass,
not a retroactive claim that an independent MERGE was recovered.

P02-T02: resolve `gh api user` immediately before committing and derive
`{id}+{login}@users.noreply.github.com`; set repository-local email and use
for author/committer. Conventional Commit with Refs #176 and the required
co-author trailer. Push normally to the existing branch. Retain PR title/body
acceptance audit and append recovery evidence if needed; no closing keywords.
Verify remote head, PR identity/body, empty closingIssuesReferences and diff.
Report new-head checks separately from the twelve historical successes.
No merge, force push, primary `.env`/`.vscode` changes or issue mutation.
