---
title: Issue 440 finance-parent verification research
description: Prospective research for a finite local observation of the recovered finance candidate, before any test was executed
ms.date: 2026-11-10
---

## Scope and disposition

* Research disposition: `executed` (new, bounded). Coordinator report `demo-finance-checkpoint-ready-1110.md` was read in full. Its correction stands: the post-#1233 documentation checkpoint was consumed through #1234 on 2026-11-06 (#440 comment `6679709806`). This task does not duplicate it, reopen the approved synthetic full-history or Invalid-and-regenerate decisions, or repeat static reading as runtime proof.
* This is local verification of an existing candidate. It is not a new feature, not main integration, not a FULL receipt and not closure of #93, #96 or #440.

## Identities (read from local Git objects, before execution)

| Item | Exact identity |
| --- | --- |
| Finance source branch | `feat/finance-integration-93` |
| Finance head (this worktree HEAD, clean at start) | `4642b55fdbafec564b67803420439b91d7ea8ce1` |
| Finance tree | `e2628422d13ae87df3a6b7ecfdd12f24a4fc1052` |
| Verification branch | `test/demo-finance-parent-440-1110`, worktree `issue-440-finance-parent-1110` |
| Current main pin (independent, read-only objects) | `ddeebd01694ddb46b456451d9ac6390347e51aaa`, tree `b917297ef34bc3e7e7948f9e46ffe6b7e66e6c88` |
| Shared merge base | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` |
| Finance versus main | 2 commits only on finance (#1223 `0472fd5d`, #1233 `4642b55f`); 81 only on main |

The coordinator's older main `3bc20719` is superseded by the supplied pin; the pin includes #1339.

## Contract documents (blob identity, finance versus main)

* BRD `docs/brds/agentic-retrofit-programme-brd.md` blob `34d88395de`, status `draft`, version 0.21.0. Identical at finance and main.
* PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` blob `c788b917ba`, status `in-review`, version 0.21.0. Identical at both.
* ADR 0001 to 0007 blobs identical at both. No contract document drift between finance and main; a draft or in-review status is not approval.

## Source overlap with main (classification only, no merged tree built)

The two finance commits change 7 `src` files: core `form_export.py`, `form_review.py`, `forms.py`, `README.md`, and tests `test_form_dependencies.py`, `test_form_export.py`, `test_form_review.py`.

| Surface | Main change since merge base | Class |
| --- | --- | --- |
| `core/forms.py`, `form_review.py`, `form_export.py`, `form_staging.py` | none | no source conflict |
| `core/tests/test_form_{dependencies,export,review,review_pack,staging}.py` | none | no conflict |
| Core imports of the form modules: `ai_registry`, `identity`, `controls`, `documents`, `change_provenance` | none | unchanged |
| `core/projection.py` (+1/-1), `core/doc_controls.py` (+8/-2) | yes, small | dependency drift, not form logic; unverified on main |
| `core/store.py` (+104/-11) | quality evidence, unresolved-order, retained-stage logging | shared hook; zero form-related changed lines |
| `core/sqlstore.py` (+554/-47), `procurement.py` (+17/-10), `mssqlstore.py` | yes | shared hooks reserved by #132; zero form-related changed lines |
| `api/server.py` (+98/-7) | `/api/form-schemas.csv` list export: `LIST_EXPORTS`, row-source map, `SCHEMA_EXPORT_FIELDS`, `list_rows` branch calling `forms.list_schemas`; other non-form hunks | shared hook; the only form-adjacent change; finance form routes (`_forms`, `form_review.view/action`) unchanged in content |
| `api/tests/test_form_staging_api.py` (+149/-1) | CSV export tests, new `controls`, `projection` imports | differs from the finance blob `f12fb157`; a parent result does not carry over |
| `docs/reference/log.md`, `src/core/README.md` | yes | documentation overlap only; certain textual conflict on integration |

Exact shared-hook overlap before anyone expands implementation: `api/server.py` (list-export constants and `list_rows`, plus the neighbourhood of the `_forms` dispatcher) and `api/tests/test_form_staging_api.py`. `forms.list_schemas` exists at finance (line 391) and is unchanged on main, so the CSV hook should bind, but that is a prediction, not an observation. A main-only finding is not reproduced at the finance head, and a parent-only pass is not main compatibility.

## Environment findings that shape the plan

* The ambient `pip` has editable installs of `zava-forward-{core,api,agents}` that resolve to the primary checkout `/home/azureuser/source/ama/src/...`, not this worktree. Running tests there would silently observe different source. The plan uses a new external virtual environment, with pinned hashed build tools, and `--no-deps` editable installs of this worktree's own projects, then proves their `direct_url`, module `__file__` paths and test file blob hashes.
* Core test names that also exist in `api/tests` (`test_buildings`, `test_chat_panel`, `test_dependency_rule`, `test_version`) are not selected. API tests use the `tests` namespace package from `src/api` while Core helpers (`dataset`, `test_form_staging`) are flat modules from `src/core/tests`; resolved paths are recorded.
* `core` has no runtime dependencies. `api` declares aiohttp, Azure SDKs and `core[sql,blob]`; the server imports only the standard library plus `core`, `agents` and `api`. The API module runs only if imports resolve without acquiring those heavy dependencies; otherwise that is recorded as a prerequisite block, not worked around.
* No project type check is selected: the tree is unchanged, and a single-file surrogate would not be an exact project receipt.

## Boundaries

* No product, test, config or shared-document edit. No schema, rule, calculation, template, eligibility or submission work. No model, provider, Azure, private dataset, credential, SQL Server, browser or full gate. Network use is limited to installing the pinned hashed build tools into the external venv, disclosed in the changes record.
* Pass means only that the tested synthetic JSON/SQLite and loopback paths worked at this head. It cannot discharge #96 C1/C5/C6, #93 closure, an old FULL at a later candidate or named financial, privacy or human acceptance.

## Planning Readiness

Ready. Unknowns before execution: whether the external venv can be built and whether API imports resolve.
