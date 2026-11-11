---
title: Issue 144 permit SQL E3 plan correction P1 research
description: Research for the plan correction that resolves the independent prospective report REQUEST_CHANGES (3 High, 4 Medium) before any real-MSSQL execution
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e3-plan-p1-1111
---

## Scope and disposition

* Research disposition: executed (read-only source and metadata only). Planning Readiness: Ready for a corrected plan; execution is not admitted.
* Parent: `issue-144-permit-sql-1111` (frozen plan commit `1a29cfd674b959872548e6dd5a1ad6ddcc3f767d`, tree `950ee178c90d71d12d91c32e5fcee3196df2ee13`, base `e691255ff7aae111ef32d585900cf82c3789a78c`). Its five tracking files are unchanged.
* Input report (read in full, incorporated by reference, not copied or regraded): `independent-144-permit-sql-plan-1111.json` under the Root files directory. Verdict REQUEST_CHANGES, 3 High, 4 Medium, 0 Critical, 0 Low. The findings are validation-plan defects, not demonstrated application defects. The original authored critique (verdict proceed) stays unchanged as adverse history.
* Authority: this is E3 of the Nov 10 five-cycle extension, admitted by Root, counted from the plan correction even if Implement never starts. E1/E2 spent, E3 admitted, two cycles unadmitted. No new five, no automatic E4. A later admitted implementation belongs to this same E3.

## Source facts verified for the corrections (current tree e691255ff)

* `Ai.__init__` (`ai.py` 85-98) copies `AI_ENDPOINT`, `AI_DEPLOYMENT`, `AI_DEPLOYMENT_STRONG` and `AI_MODEL_VERSION` from the environment; an empty endpoint is "live" in `Ai.is_live` (`ai.py` 137-140: nonbillable only for an `http` loopback endpoint). `Ai.configuration` hashes endpoint, deployment, model, temperature, max tokens, so the authority and the request plan must come from the same fixed configuration (R1).
* `ConsumptionApi.setUp` (`test_ai_consumption_api.py` 50-111) patches `tempfile.tempdir` to `Path.cwd()`, builds `Base()`, an `Ai()` with `model_version` and `model_version_strong` `test-model`, `consumption = service.consumption`, then opens a loopback HTTP server only to obtain an endpoint and patches `_token` and `provider.evidence`. The permit and result helpers (`authority`, `permit_setup`, `permit_request`, `reserved`, `kinds`, `lease`, `used_calls`, `records`, `permitted_result`) use only `service`, `provider`, `pm`, `inner`, and `fixture`-seeded data; none touch the HTTP server. `permit_setup` also sets `inner.fast = "test"` and patches `provider.request_plan` and `provider.is_live` from `inner` (R1, R4).
* `Base.setUp` (`test_assistants.py` 80-105) uses `tempfile.mkdtemp` (under `TMPDIR`), constructs the dataset, `self.store = self.open_store()`, `Provider()`, `Assistants(self.store, config())`. `MssqlFixture` is a plain mixin (`test_assistants.py` 1319-1346): its `setUp` requires `ZF_SQL_SERVER` in localhost, 127.0.0.1 or sql, creates `zf_test_assistants` if absent, drops the assistant tables and calls `super().setUp()`; `open_store` returns an `MssqlStore` with `sql_env`. `class SqlBase(MssqlFixture, Base)` is therefore a valid MRO and `SqlBase()` can be built the way `ConsumptionApi` builds `Base()`.
* Mypy config (`src/api/pyproject.toml`): strict, `mypy_path` includes `../core/src`, `../core/tests`; `test_assistants` and `zava_forward.core.*`, `zava_forward.agents.*` are `ignore_errors` with `follow_imports = skip`, so they resolve as `Any`. `test_ai_consumption_api` is checked strictly and is not in that list. The new module is also strict and gets no pyproject edit.
* Tool pins: `src/api/pyproject.toml` dev extras declare `ruff==0.17.1`, `mypy==2.4.0` (and `playwright`, not needed); `src-ci.yml` and `tools/rpi-checks.py` pin `ruff==0.17.1 mypy==2.4.0` unhashed. These are the existing conventions the plan reuses.
* Clock: `issue_permit` (`assistants.py` 1626-1676) reads `now = self.now(db)` after the blocking `UPDATE assistant_tasks SET revision=revision+1`, then `reserve_in` reads `self.port.now(db)` at `ai_consumption.py` 566. `min_window` check is `now >= min(authority.end, price.end) - min_window` (line 604). `PERMIT_LEASE_MARGIN` 38, `PERMIT_WINDOW` 2. `Assistants.now` is a service attribute, so one passthrough wrapper on the `service` instance records both reads (the existing `after_blocking_update` helper already patches `service.now` the same way).
* E2 (`d28fcd356`): `complete_result` binds `meter_id`/`meter_root` from the stored `reserved` record via `_permitted_root`, rejects a conflicting caller `meter_root` or `meter_id` (`result-rejected`, no settlement) and otherwise passes the bound envelope to `complete`. Pre-E2: the conflicting `meter_id` was already rejected; only the `meter_root` comparison and the server-side binding are new. Therefore N2 must discriminate on the root only; the `meter_id` conflict subtest is expected to pass under N2 (R2).
* Settlement record fields (`ai_consumption.py` 755-805): `completed` has `id`, `tokens`, `charge`, `outcome`, `held`, `returned_model`. A provider-unavailable failure gives `tokens` None, `charge` None, `held` True, `outcome` `provider-unavailable`.
* All 15 carry-forward SQLite method names exist exactly once in `ConsumptionApi` (grep count verified for each).
* `.gitignore` line 16 ignores `/src/**/*.egg-info/`: an editable `pip install -e` in the worktree would create ignored egg-info there, so editable installs are bound to an external source snapshot instead (R6, R7).
* Existing docker image (instantaneous read-only metadata from the parent research): `mcr.microsoft.com/mssql/server:2022-latest`, id `cf8f0ab2ebe6`, digest `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`, already local. Not re-probed in this launch (no Docker command is authorised).

## Disposition of the independent findings (full matrix in the plan)

R1 to R7 each map to one report finding (R1=#1, R2=#2, R3=#3, R4=#4, R5=#5, R6=#6, R7=#7); every one is resolved by a concrete recipe in the corrected plan and details. No source defect is claimed or implied.

## Unknowns carried forward

* Whether the DMV wait resource is a `KEY:` lock on the task row (SQL may choose another granularity): an unsupported observation is INVALID, not a source defect.
* Whether the pre-E2 mutant raises instead of failing an assertion in case 5: an exception where a labelled failure is predicted makes the control INCONCLUSIVE; it is reported, never tuned.
* Pip index, wheelhouse and driver availability (needs the conditional admission in the plan).
