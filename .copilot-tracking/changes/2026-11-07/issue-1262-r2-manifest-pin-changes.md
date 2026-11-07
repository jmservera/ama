---
title: Issue 1262 correction cycle 1 manifest pin changes
ms.date: 2026-11-07
---

* Changed: `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` line 47, `recipe` sha256 `dea58169...6f0` to `4bd825e9b340f3842771e19e8fa4d4770da4004653162cadbf5c93446bdfa320` (committed checker blob, LF). Appended one entry to `docs/reference/log.md`. No index change. Checker, validator, tests and all other manifest content unchanged.
* Red (current head `eb17f9f50`, own venv `/tmp/zf1262/venv`, `PYTHONPATH=tests`, from `src/core`): the two exact hosted tests, exit 1, errors=2, `stale source hash: src/api/checks/workbench_browser_check.py` (`/tmp/zf1262/core_red.log`).
* Green after the digest: the same two tests exit 0 (`core_green2.log`); related modules scenario_manifest, needs_inventory, perspective_walkthroughs, journey_acceptance, retrofit_scenario_consumers, retrofit_scenarios_production_consumers, retrofit_scenarios_retained_store: exit 0, 40 tests OK, no skips reported failing (`core_mods.log`). The fresh planned re-run at the frozen final head is recorded in the final response and state.
* Adverse and historical evidence preserved: the original passed partial receipt `/tmp/zf1262/gate/out/receipt.json` and earlier independent review are historical for `eb17f9f50` and not claimed for the new head; hosted failure run 42414829290 / job 128530646078 and R31 failed ranking receipt untouched.
