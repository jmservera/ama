---
title: "#184 C4 research: integrate fresh main into the live simulator parent"
ms.date: 2026-11-08
---

Prospective record, written and committed before the merge and before any source change.

## Start identity

* Worktree /home/azureuser/source/ama-wt/parent-184, branch feat/live-simulator-integration-184, target main.
* HEAD 33a32831ad5a292aaa0fa803ad33bc253b3179ce, tree a42a72875f23db53f3da3daf6b5bba85029b584e, tracked tree clean.
* Ignored src/core/.ruff_cache/ was created by the coordinator and is preserved. The tree is not ignored-inclusive clean.
* Fetched origin/main: fa7ae0c9770e890f82482456bfcb8e97f1e05429. Merge-base with HEAD: ecb28815b2f5dd354ba1d34046cf02784b49bdd2.
* Ancestry: child commits 2dc125f97 (#185) and 9476dc961 (#188) are ancestors of HEAD.

## Findings

* origin/main differs from the merge-base by 141 paths. Outside docs, rubric and tracking there are ten source paths: src/api/README.md, four src/api/checks files (atlas tensions and data operator), five src/api/tests files, and src/core doc_controls.py.
* None of the ten paths is touched by this branch (live_simulator, live_receiver, sensor_sql, sensor_consumer, infra). A dry `git merge-tree --write-tree` projects a clean merge, tree 13bbf02b596db5827606f30ee7fd03ba8b72bfbd.
* Earlier statements that source equals 6354 do not extend to this tree: 33a lacks the ten UX/API/doc-controls paths now on main.
* Heavy-resource lock /tmp/ama-rpi-heavy.lock was free at check time (non-queued probe). Disk 11G free, RAM about 6G available, no docker containers running.
* Environment limitation: installed editable packages resolve to another checkout, so validation needs a new isolated environment with pip-installed copies of src/core, src/agents and src/api built from the integrated tree.

## Open items, unchanged

* Low gap: restricted-grant main-entrypoint and rejected-DQ receiver test.
* Azure sensor schema provisioning owner, receiver grants, routing-ready setting and live activation remain undecided and out of scope.
* Historical limitation: the /tmp/v184 venv used in C2 and C3 was removed after use despite the no-cleanup brief. Raw output of two C2 SQL attempts was overwritten.

## Planning readiness

Ready. Disposition: executed (read-only git inspection).
