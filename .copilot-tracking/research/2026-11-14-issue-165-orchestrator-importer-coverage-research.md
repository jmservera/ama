---
title: Issue 165 orchestrator and importer coverage research
ms.date: 2026-11-14
---

* Disposition: executed. Planning Readiness: Ready.
* Baseline (pip venv, editable installs from this worktree, PYTHONPATH=../core/tests:../agents/tests): orchestrator 89% line+branch, importer 84%.
* Gaps: orchestrator `token_store.main/put_secret` failure paths, `document_rescan.main`, `source_monitor.main` and observation validation; importer `__main__` CLI (54%), `xlsx` safety bounds (85%), export and mapping edges.
* Boundary: synthetic data only; assert no secret, cell value or header text reaches stdout, stderr, ledger or exception text.
* Constraint: pip only, no uv; no network or push.
