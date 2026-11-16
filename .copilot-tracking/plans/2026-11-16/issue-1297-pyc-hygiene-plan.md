---
title: "Issue 1297 gate bytecode hygiene plan"
ms.date: 2026-11-16
---

## Objective

Stop the full gate generating ignored `.pyc` files inside its own checkout when a test spawns a scrubbed-environment child of a gate venv interpreter, without relaxing `clean_identity`, snapshot checks or SQL skip controls. Tier: FULL (gate-tool behavior, SQL-sensitive).

Research: `.copilot-tracking/research/2026-11-16/issue-1297-pyc-hygiene-research.md`. Details: `.copilot-tracking/details/2026-11-16/issue-1297-pyc-hygiene-details.md`.

## Phases

* [ ] Phase 1: regression test in `tools/test_rpi_checks.py` that installs each gate venv via `_install` (patched command, `--without-pip` venv) and shows a scrubbed-environment child importing a source module writes no `__pycache__`. It must fail before the fix for non-api venvs.
* [ ] Phase 2: in `tools/rpi-checks.py`, write the `00-rpi-bytecode.pth` policy into every venv in `_install`; keep the receipt-listed `browser-bytecode-policy.pth` api-only.
* [ ] Phase 3: run targeted tool tests and static checks (ruff format/check, mypy if the gate uses it).
* [ ] Phase 4: review, commit implementation and dated RPI evidence, fetch main, run the FRESH full gate under the heavy lock to a new external directory, verify the receipt at current origin/main.

## Gates

* Do not touch `/tmp/ama-gate-1297-20261116T105339Z` or other retained evidence.
* Any changed head/base/tool invalidates a receipt; a failed or partial run stays as adverse evidence.
