<!-- markdownlint-disable-file -->
---
title: Issue 350 main c8d16059 integration phase details
description: Prospective phase details
ms.date: 2026-10-26
---

* Phase 1: one read-only `rubber-duck`; critique file `reviews/plans/2026-10-26/issue-350-main-c8d16059-integration-critique.md`, committed before the merge.
* Phase 2: commit the four prospective artifacts with the noreply identity (`gh api user`, repository-local) and the Copilot trailer, then the merge with the same.
* Phase 3: `git merge-base --is-ancestor` for each of the three SHAs; `git diff --stat 49851214 HEAD`.
* Phase 4: search for an existing venv that already has `zava_forward` importable (for example `pip list` in existing environments, without modification). Run `python -m unittest tools.test_check_demo_feedback` from the repo root, and resident-preview core and api tests by `discover -s tests -p test_resident_preview*.py` only if importable from the merged source. The checker imports installed packages, so a stale editable path is a recorded limit, not evidence for the merged tree.
* Phase 5: review brief lists the merge SHAs, the file delta and the evidence boundaries; reviewer is read-only.
* Phase 6: changes, state and review committed; report head, ancestry, delta, tests, verdict and gate readiness (disk 6.8 GB free; full gate needs several GB, so not started).
