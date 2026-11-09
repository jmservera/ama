---
title: Issue 1259 parent 6d793bc propagation changes
description: Changes record for the normal merge of the new 1258 parent and LIGHT proof
ms.date: 2026-11-08
---

## Changes

* One normal merge (--no-ff) of local fix/ranking-archive-ancestor-durability 6d793bc3ad3fd8427f745530a633bb1e553ec0ef (tree b614f008) into the child; prospective plan commit 80c04772 precedes it. The merge commit is e174b2cfa6e58e7e84fc636b1cbcad26ef103044 (parents 80c04772 and 6d793bc3). Correction: the first version of this record had the two IDs swapped. No conflicts; no source edit, rebase, amend, reset or parent write. Production source unchanged by this step; the _names/_require_creatable hunks and original histories are preserved.
* The delta brought only two test files (core test_ranking_publication.py, API test_ranking_publication_wiring.py) and 1258 continuation records.

## Commands and results (scratch /home/azureuser/.local/share/ama/gates/g1259-parent6d-light-1108)

* Fresh venv; non-editable install of a git-archive export of core, agents, api; module origins confirmed under the venv site-packages; synthetic ZF_DATA; external pip cache and TMPDIR.
* core: `python -m unittest discover -s tests -p 'test_ranking_publication*.py'` in src/core: exit 0, Ran 92, OK, no skips reported (core.log).
* API: `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest test_ranking_policy test_ranking_publication_wiring test_ranking_scale` in src/api: exit 0, Ran 54, OK, no skips reported (api.log). A printed "hard links unsupported" line is the expected mocked fault output of an existing test.
* Includes the parent's new tests and the path-health regressions. No failure occurred.

## Residuals

Parent R1 real crash, R4 extra-sync visibility, PC-004 Store overdue-vs-unknown, mocked stat failure and TOCTOU remain. FULL, receipt, independent assessment, hosted checks and approvals unperformed. No acceptance of 1259, 1258, 79 or 1231.
