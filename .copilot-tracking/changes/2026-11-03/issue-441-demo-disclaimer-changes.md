---
title: Issue 441 demo disclaimer changes
date: 2026-11-03
task_slug: issue-441-demo-disclaimer
---

* `src/api/src/zava_forward/api/resident_demo/web/index.html`, `resident_preview/web/index.html`: Legal/DPO outstanding notice in banner.
* `demo.css`, `resident.css`: `.synthetic .review-note` block rule.
* `src/api/tests/test_resident_demo_api.py`, `test_resident_preview_api.py`: one assertion each.
* `src/api/README.md`, `docs/reference/log.md`: note and append-only entry.

Validation run: resident demo API (41), preview API (15), demo check (6) tests OK; ruff clean on edited tests; mypy clean (cache /tmp/mypy-441). Run with PYTHONPATH to the src trees because the installed editable packages point at another worktree.

Not run: rpi-checks gate, browser checks (no screen-reader or WCAG proof), full suites, benchmarks. Independent exact-head review and hosted CI remain required.

Unmet criteria of #441: 5 (requirements-owner FR-044/AC-084 disposition) and 9 (exact-head independent review and publication gates). The disclaimer is not a Legal or DPO approval.
