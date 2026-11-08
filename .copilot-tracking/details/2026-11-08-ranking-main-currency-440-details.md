---
title: Issue 440 ranking main currency details
description: Phase details for the current-main currency continuation
ms.date: 2026-11-08
---

## Details

* Phase 1.1: stage only the three currency records. Commit message docs(440): plan ranking checkpoint main currency, Refs trailer, Copilot co-author.
* Phase 2.1: git merge --no-ff origin/main with a Conventional merge message. Verify with git ls-tree that the rubric blob and mode equal 6741ddd6 and 100644, python json.load passes, git diff of the merge against a80acada changes only that file, and ranking paths are byte-identical to aa8f0d11.
* Phase 2.2: add a subsection "Current-main currency note" at the end of the existing ranking section: fresh main identity, rubric-only change, historical qualification, the distinct refusals, selectors refreshed with exits, remaining gaps. Anchor uniqueness checked first; no removed lines.
* Phase 3.1 selectors (from the component guides, not copied from receipts): core unittest discover -p "test_ranking_publication*.py" from src/core with PYTHONPATH=tests; API discover -p "test_ranking_*.py" from src/api with PYTHONPATH=../core/tests:../agents/tests; agents discover -p "test_cohort_ranking_eval.py" with PYTHONPATH=../core/tests; python -m pytest tools/test_tracking_retention.py. SQLite-backed store qualification is repeated.
* Phase 5: refuse if the gate directory exists; never reuse the old gate directory.
