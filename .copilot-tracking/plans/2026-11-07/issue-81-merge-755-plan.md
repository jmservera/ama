---
title: Issue 81 fresh-main normal merge plan
description: Prospective plan to merge pinned origin/main 7551e50e into the parent by normal merge and run light no-service checks
ms.date: 2026-11-07
task_slug: issue-81-merge-755
status: prospective
research: ../../research/2026-11-07/issue-81-merge-755-research.md
details: ../../details/2026-11-07/issue-81-merge-755-details.md
critique: issue-81-merge-755-critique.md
---

Choice: NORMAL MERGE (`git merge --no-ff 7551e50e`), not rebase, preserving the three-child history, the capacity correction commits and their SHAs. Stop on drift (origin/main or parent HEAD changes), conflict, or a non-empty source delta beyond the four main files.

Phases: P0 preflight and backup ref (done); P1 prospective records and critique committed; P2 merge; P3 proof: merge parents, `git diff 3e245e14 HEAD` equals main's delta only, blobs of child-owned files identical; P4 light checks; P5 changes, author Review, freeze.

Light commands: scratch `/mnt/ama-gates/g81-755-preparation-1107`; `env -i`, `PYTHONDONTWRITEBYTECODE=1`; pip-install ruff 0.17.1, mypy 2.4.0, core and agents `--no-deps` from a snapshot; prove import origin; unittest the four modules from `src/core/tests`; ruff check, format check, mypy. No queue benchmark, services, uv, private data.

Exclusions: no child merge or mutation, no push, PR, full gate, ticks or approvals.

## Amendment 1 (from the executed critique, verdict Revise; all accepted)

1. Sequence: commit these four records first as PRE (HEAD becomes the records commit); the pre-merge baseline for all proofs is that PRE commit, whose delta from `3e245e14` is exactly these four files. Details step 1 is read accordingly.
2. Proof: assert `HEAD^1` equals PRE and `HEAD^2` equals `7551e50e`; compare `git diff --raw PRE HEAD` with `git diff --raw 0f420dc9 7551e50e` (merge base to main), which must be identical, including modes; the later changes/Review commit must touch only `.copilot-tracking/`.
3. Tests: modules `test_quality_procurement test_gates test_hazard_referral test_resident_preview` run from `src/core/tests` against a `git archive` snapshot of the merged HEAD; exit 0 required, skips listed and explained. The incoming `case_journey_browser_check.py` change is not browser-tested on the merged head (unverified).
