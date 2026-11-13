---
title: Issue 134 demo preflight changes
ms.date: 2026-11-13
---

## Scope

Tracking-only; no `src/` or `docs/` edits. Base `3b05143179f83235c5b4e80e70aad99bdc44d83f`. Seed 20260901, as-of 2026-10-13, fictional test register (`register()` from `test_generated_dataset.py`). Refs #134, #165, #176, #435.

## Environment

* `/tmp/venv-preflight-1045` via `python3 -m venv`; `pip install --no-deps -e` of `src/core`, `src/agents`, `src/api`, `src/importer`: all four exit 0. `PYTHONDONTWRITEBYTECODE=1`, `ZF_DOC_STORE=local`, `ZF_DATA` pointed at an unused temp path (no `~/.zava-forward`, `.env` or private data read); `PYTHONPATH` only `../core/tests:../agents/tests` for api. No cloud, Docker or browser. `test_case_journey` runs node and a loopback server only.
* Module origins (all inside the worktree `src/`): `zava_forward.core.store` at `src/core/src/zava_forward/core/store.py`; agents, importer and api namespace paths under `src/agents|importer|api/src/zava_forward/`.
* Venv and temp seeds removed after the run.

## Unit results (true producer exits from status files)

| Module | Tests | Exit |
| --- | --- | --- |
| core `test_generated_dataset` | 16 OK | 0 |
| core `test_scenario_manifest` | 8 OK | 0 |
| core `test_needs_inventory` | 11 OK | 0 |
| importer `test_document_form_fixtures` | 8 OK | 0 |
| api `test_case_journey` | 31 OK, 0 skipped | 0 |

The seed build wrote 980 cases (443 open), matching the runbook.

## Inspection script

`inspect_five.py` (sha256 `cafd08c6274433090a1ce94292c9c90562c6ed98ff6d7061367ff8a1126e22e4`, exit 0). It imports the test builder and `register()`, builds the seed into a temp dir, opens a `Store` with temp live and audit paths, then for each runbook home reads the case, `store.detail` and `store.home_case_view` as a staff Retrofit Programme Manager, and recursively searches case keys for archetype, damp, sensor, conflict and assistant fields. It is read-only.

## Local-seed facts and gaps for the presenter

* All five ids exist, open, zero hazards, stage as stated (four Quality check, ZF-2026-0892 Funding check). `home_case_view` returns OK for all five with keys building, case_id, changed_since_version, home, links, notice, scheme, version, version_status, versions. `building` is absent and `building_id` and `scheme_id` are None: stand-alone homes, consistent with the runbook rule.
* Exported seed cases carry no archetype or damp-report fields, so the runbook's ARC and damp rule is Not verified from the seed (it comes from the generator simulation, not the export).
* No sensor-like fields were found in the exported seed (key search samples the first three items of each list): sensor presence is not verified and stays a deployed-store preflight item.
* No matches for proposal fields in sampled case keys; `stock_reconciliation` is empty for all five and `stock_epc.conflict_type` is empty, so no stock evidence conflict is seeded for these homes. Each case has gate reasons (resident decision needs confirmation; ZF-2026-0892 also funding not confirmed), so the "conflicting evidence with an owner" story relies on those gates, not a stock conflict.
* Unchanged and Not run: simulator cohort, AI scan scope, direct links, deployed store, `/api/cases/<id>` over HTTP (the seed's `Store.detail` was used instead).

## Review follow-ups

None open at implementation. Independent review is recorded separately.
