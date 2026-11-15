<!-- markdownlint-disable-file -->
# Research: C1 scenario manifest stale SHA (PR #1574 src-core)

* Disposition: executed. Planning Readiness: Ready.
* Failure: job 132223245765, `ValueError: Scenario manifest: stale source hash: src/core/tests/dataset.py` (`scenario_manifest.py:101`), in `test_scenario_manifest.py` and `test_needs_inventory.py`.
* Cause: commit 5078151e6 changed the `src/core/tests/dataset.py` docstring without updating its entry in `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`.
* Evidence: recomputed SHA-256 of all four manifest sources; three match, only `fixture` (`src/core/tests/dataset.py`) differs (manifest a54612aa..., file 1f28f108...).
* Merge: `git merge-tree` of HEAD with origin/main 3033dc9c21 is clean, so no rebase is needed.
