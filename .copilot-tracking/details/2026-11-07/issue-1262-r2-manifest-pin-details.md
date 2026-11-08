---
title: Issue 1262 correction cycle 1 manifest pin details
ms.date: 2026-11-07
---

* Edit `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` line 47 only: `sha256` of `recipe` from `dea58169...6f0` to the digest of `src/api/checks/workbench_browser_check.py` at the committed bytes (`4bd825e9...a320`, re-verified with `sha256sum` and `git hash` before commit). The checker must not change afterward.
* Targeted Core commands, from `src/core` with the own venv and `PYTHONPATH=tests` (helper-only), `PYTHONDONTWRITEBYTECODE=1`, no editable build in the checkout.
* Append-only log entry at the end of `docs/reference/log.md`; no index change.
* Final gate: new external out `/mnt/ama-gates/g1262-r2-1107`, no outer flock, report actual groups and skips; no commits after the gate.
