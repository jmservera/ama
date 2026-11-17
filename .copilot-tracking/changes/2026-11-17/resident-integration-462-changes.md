---
title: "Changes: resident-integration-462"
description: "Change record for the Issue #462 continuation: non-rewriting merge of pinned main and local readiness evidence"
ms.date: 2026-11-17
---

Plan: [plan](../../plans/2026-11-17/resident-integration-462-plan.md)

## Status

Opened before `implement-start` (HEAD `926b20a8856622515c60948bf9ed890b241fc1fc`, no merge or edit at that time). The result sections below were written after the work.

Outcome: merge integration and documentation complete; light checks recorded; SQL, image, browser, Bicep-compile and all FULL, independent and hosted checks remain missing. FULL RECEIPT / ACTUAL SQL-IMAGE-BROWSER EVIDENCE MISSING, NOT PUBLISHABLE.

Process note: the first `implement-done` attempt (witness seq 5) was refused with `missing persisted artifact evidence: changes` because this file was accidentally truncated by a scripted rewrite while it was being finalised. The refusal is retained in the witness log; this file was recreated and the boundary re-recorded.

## Results

Evidence directory (external): `/mnt/tmp/ama-run-74bd1fe9-462-integration-20261117T0841/evidence-462-integration` (`light/` logs, `venv/`). Commands ran from this worktree with `PYTHONDONTWRITEBYTECODE=1`, a venv holding editable installs of `src/core`, `src/agents` and `src/api` (plus `playwright==1.64.0` after a missing-dependency mypy result), no `PYTHONPATH=mvp`, and `ZF_DATA` under the evidence directory. The editable-install `egg-info` directories created in the worktree were removed (ignored, self-created) so no ignored input remains.

### Implementation steps

| Step | Result |
|------|--------|
| Precondition | HEAD was exactly `926b20a8856622515c60948bf9ed890b241fc1fc`; `implement-start` witnessed at seq 4 before any merge or edit |
| `git merge --no-commit --no-ff 1c9ac230be1dad9a4ecc21975f9ffe0845309fc4` | Exit 0, automatic, no conflicts. Auto-merged `docs/reference/README.md`, `docs/reference/log.md`, `src/api/README.md`. `MERGE_HEAD` equals the pin. Both intents preserved: main's content and the candidate's threat-model index row, log entry and README link are all present |
| New file `docs/reference/research/resident-demo-threat-model-update-2026-11-17.md` | Dated addendum: derived sensor keys, provenance table (historical, original, newly witnessed), unproved list. The 2026-11-16 threat model is unchanged |
| `docs/reference/README.md` and `docs/reference/log.md` | Index row and appended 2026-11-17 log entry |
| `src/api/README.md` | One documentation-only qualification of main's sentence about the sensor status badge and source line (critique PC-007). No source file was edited by hand |
| Original 2026-11-16 artifacts | `git diff 926b20a8 -- <path>` empty for all eight (research, plan, details, critique, changes, review, state, threat model). Nothing deleted or rewritten |
| Source diff against main | `git diff 1c9ac230 --stat` outside `.copilot-tracking` is four documentation files only; the Python, JavaScript, SQL, Bicep, Docker and runner files are byte-identical to main |

### Validation (light, local)

| Check | Command (summary) | Exit | Result |
|-------|-------------------|------|--------|
| Core resident suites | `python -m unittest discover -s tests -p 'test_resident*.py' -v` in `src/core` | 0 | 626 tests, OK, 186 skipped |
| Core case and projection | same with `test_home_case.py` and `test_indoor_projection.py` | 0, 0 | 8 and 10 tests OK, no skips |
| API resident demo | `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_resident_demo*.py' -v` in `src/api` | 0 | 65 tests OK, no skips |
| API resident API | same with `test_resident_api.py` | 0 | 22 tests, OK, 1 skipped (opt-in local browser) |
| Infra resident | `python -m unittest discover -s tests -p 'test_resident_demo*.py' -v` in `infra` | 1 | 27 tests, 2 errors: `FileNotFoundError: 'az'` in `compiled()` (Azure CLI with Bicep is not installed). 25 pass. Not a source defect and not a pass for the Bicep-compile tests |
| Ruff check and format check | `ruff check .` and `ruff format --check .` in `src/core` and `src/api` | 0, 0, 0, 0 | clean |
| mypy core | `mypy` in `src/core` | 0 | no issues, 326 files |
| mypy api | `mypy` in `src/api` | 1, then 0 | First run: 71 errors in 66 files, 65 of them `playwright.sync_api` not found plus consequent `Any` returns (dev extra not installed). After `pip install playwright==1.64.0` (declared in `src/api/pyproject.toml`): no issues, 309 files. Both logs retained |
| `node --check` | on `demo.js` | 0 | syntax OK |

Skipped tests are not passes. The 186 core skips by reason: 156 `opt-in owned loopback SQL Server`, 27 `opt-in loopback SQL Server`, 1 `Explicit isolated synthetic Azure SQL database required`, 1 `JSON file rollback only`, 1 `SQL replay only`. All SQL-dependent resident reader, view and migration tests are therefore unexecuted here.

An earlier core invocation by dotted module name failed with three `ModuleNotFoundError` import errors (the `tests` directory was not on the path for sibling imports). The log `light/core-unittest.log` is retained as an invocation error, not a code result; the discover form above is the repository's documented form.

### Not run (named continuations)

* Actual SQL Server parity (resident view, migration, allowlist tests): no SQL Server and no Docker socket in this confinement.
* Docker non-root image startup (`resident_demo_image_check.py`): no Docker socket.
* Resident browser journeys (`resident_demo_browser_check.py`, `resident_sensors_browser_check.py`, `case_journey_browser_check.py`): each needs a loopback SQL Server, so they were not attempted and the shared heavy lock `/tmp/ama-rpi-heavy.lock` was not taken. Chromium and Playwright 1.64.0 exist, but a non-SQL browser run would not exercise the changed resident view. Pending, not waived, not a pass.
* Bicep compile tests: Azure CLI absent.
* Complete current-base gate (`tools/rpi-checks.py --all`), external receipt verification, independent exact-head assessment and hosted CI: coordinator.
* Live HTTPS login, correct-case and negative authorization behaviour, live SQL view and grants, Azure resources, spend headroom and any deployment: not performed and not claimable.

### Web guidelines review (changed web file)

Fetched `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` successfully before reviewing `src/api/src/zava_forward/api/resident_demo/web/demo.js`, the only web file this merge changed relative to the candidate (8 added lines from main #1826, lines 297 to 304). Findings in the guideline's format:

```text
## src/api/src/zava_forward/api/resident_demo/web/demo.js

demo.js:297-304 - pass: status group uses a native div with role=group and aria-label, textContent via el(), icon from withIcon() carries aria-hidden, missing freshness handled by "Freshness unknown." fallback, empty history returns before the block
demo.js:304 - note: "Source:" line and badge sentences use sentence case; the generic Title Case rule is not adopted because the repository plain-language content standard governs
```

No CSS rule for `sensor-status` or `sensor-source` exists, so default flow applies. This is a static read, not browser, axe or human accessibility acceptance.
