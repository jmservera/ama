---
title: Research for #176 determinism, seeds, versioning
ms.date: 2026-11-04
---

* Disposition: executed. Planning Readiness: Ready.
* Merged work found (gh pr list): #237, #257, #243 (manifests, stock fabric and EPC), #309, #368 (snapshots, protected refresh, pinned replay inputs), #633, #703 (replay audit incl. public pack and EPC), #843 (fictional stock register generator).
* Criterion 3 (refresh policy) is already ticked. Criteria 1 and 2 remain unticked because the original private stock register generator and pinned OSM inputs are absent (README of retrofit-synthetic-data, determinism sections).
* Residual gap in code: `sensor_stream.descriptor` records seed and version but no `generator_revision`, and the audit (`determinism_audit.py`) does not replay the register-backed sensor stream.
* Installed `zava-forward-core` points at another worktree; tests need `PYTHONPATH=src/core/src` for this worktree.
* Unachievable locally: reproducing the original register bytes; no Azure.
