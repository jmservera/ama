---
title: Issue 111 API typing C2 details
ms.date: 2026-11-10
task_id: 111-api-type-c2-1110
---

## Edit

Replace `make_handler(App(self.store, PASSWORD))` argument with the same call carrying the exact-call ignore, formatted by ruff to 100 columns (extract `app = App(self.store, PASSWORD)  # type: ignore[no-untyped-call]` on its own line, then `make_handler(app)`; behaviour unchanged). A comment states that the legacy `App` constructor is deliberately untyped and the exemption covers only this call.

## Environment

Venv `/tmp/zf-111-1110/venv`, mypy 2.4.0, ruff 0.17.1 as pinned; `PYTHONDONTWRITEBYTECODE=1`; external mypy cache; raw outputs under `ROOT/checks-111-api-type-c2-1110/`.

## Browser

`PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.quality_sensors_browser_check --out <ext>/results.json` from `src/api`, synthetic fixture and local mock provider only; optional axe file only with its pinned hash check.
