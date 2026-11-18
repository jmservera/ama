---
title: Issue 619 changes
ms.date: 2026-11-17
---

## Status

Implementation started. Baseline before any edit: production-config check PASS at eb51af5c9
(command: `python3 -m checks.production_config_a11y_browser_check --axe <pinned> --out /tmp/a11y619-base`
from `src/api`, PYTHONPATH as in src/api README).

## Files changed

* src/api/checks/production_config_a11y_browser_check.py: `horizontal_overflow`, `reflow` (320x256), `reduced_motion` steps.
* src/api/tests/test_production_config_a11y_check.py: overflow helper regression test.
* docs/reference/research/ux/production-ux-acceptance-protocol.md, src/api/README.md, docs/reference/README.md, docs/reference/log.md.

## Divergence (recorded)

First reduced-motion attempt failed (two border-color transitions on tab buttons, started before emulation);
check-setup error, fixed by reload under the setting. A first mypy error (`FloatRect | None` index) fixed.

## Validation (FOCUSED; PYTHONPATH per src/api README, from src/api)

* `python3 -m unittest tests.test_production_config_a11y_check -q`: 3 tests OK.
* `python3 -m checks.production_config_a11y_browser_check --axe <pinned 4.10.3> --out <dir>`: baseline PASS before edit; 50 PASS, completed=true after. Chromium 156.0.8078.4, Playwright 1.64.1.
* `mypy` on the two changed python files: no issues. `ruff format --isolated --line-length 100 --check` on the test file: clean after format. The checks file was already unformatted at base and is not in src-ci ruff list; left unreformatted to avoid unrelated churn.
* Not run: rpi-checks --all (full gate lock held, not required for FOCUSED), hosted CI, any person-run script. Non-applicable: SQL, security, infra, deploy.
