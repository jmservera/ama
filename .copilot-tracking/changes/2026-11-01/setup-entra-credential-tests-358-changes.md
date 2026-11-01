---
title: Changes 358 setup-entra credential tests
ms.date: 2026-11-01
---

* No source changes; AC1 and AC3 already on main via #583.
* Added dated RPI evidence only.
* Validation: `python3 -m unittest tests.test_setup_entra` from `infra/`: 124 OK. `ruff check` and `ruff format --check` report pre-existing findings in the untouched infra scripts/tests; mypy not applicable (no touched project).
