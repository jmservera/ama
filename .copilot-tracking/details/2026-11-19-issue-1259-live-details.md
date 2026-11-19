# Issue 1259 live details (2026-11-19)

* Current run: `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests.test_ranking_publication_runner -q`.
* Pre-fix run: `git archive cd687abad^ src/core/src | tar -x -C /tmp/pre1259`, then the same test class with `PYTHONPATH=/tmp/pre1259/src/core/src:tests`.
* Tier: FOCUSED (documentation and tracking only; no src change). Temporary /tmp/pre1259 is removed afterwards.
