# Research: 440 checkpoint evidence sync (0252)

Task: `440-checkpoint-evidence-sync-0252`. Branch `docs/demo-440-checkpoint-evidence-sync-0252`. Refs #104, #149, #165, #440. Disposition: executed. Planning Readiness: Ready.

## Pins

* Source commit and `origin/main` at start: `ac70acafac6d215a87f25b68c5d8e14f7658ca30`, tree `b6d86d72e7e0fb2af8fd3d665fc33cb35a26f919`, clean worktree.
* After a later fetch `origin/main` is `034af8d88`; `git diff --stat` shows only `.github/rubric/scores/latest.json`, so no source, test or document input differs.
* Document blobs: BRD `34d88395de86` (draft), PRD `a385d27481f8` (in-review), ADR 0002 `96d6db897809` (Proposed).
* Issues #104, #149, #165, #155, #215 and #440 read OPEN on 2026-11-14.

## Findings

* Prior checkpoint format: `docs/architecture/cutover-evidence-pack.md` sections "Post-wave stabilization checkpoint (2026-11-13 ...)": identity pins, traceability table, commands and exits, skips, recommendation, process limits.
* Epic #104 evidence: `src/agents/tests/test_epic104_bounded_ai_invariants.py`, `test_ai_claim_filter.py`, `test_ai_eval.py`, `test_chat_eval.py`; `src/api/tests/test_ai_boundary.py`, `test_ai_call_site_inventory.py`, `test_ai_tasks.py`, `test_ai_consumption_api.py`, `test_chat_panel.py`; `src/core/tests/test_ai_statement_sources.py`, `test_ai_consumption_safety.py`. Source-class labels are the AI suggestion, Unverified and chat panel labels asserted in `ai_eval.py` and `chat_eval.py`.
* Epic #149 evidence: `src/api/tests/test_accessibility_baseline.py`, `test_design_system.py`, `test_content_standard.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_role_endpoint_inventory.py`, `test_regulatory_ux_check.py`, `test_production_ux_acceptance_protocol.py`; browser checks under `src/api/checks/` need Playwright, which is absent here.
* Epic #165 evidence: `src/core/tests/test_scenario_manifest.py`, `test_needs_inventory.py`, `test_generator_coverage.py`, `test_synthetic_output_audit.py`, `test_synthetic_provenance.py`, `test_synthetic_determinism.py`, `test_generated_dataset.py`, `test_stock_fabric.py`, `test_sensor_stream.py`, `test_historical_backfill.py`, `test_device_provision.py`; `src/api/tests/test_live_simulator.py`, `test_iot_stream.py`. OpenStreetMap anchors appear as `building_form_osm` fixtures and the tile-provider CSP assertions in `src/api/tests/test_auth.py` and `test_ui_support.py`; no test named for OSM anchors in the output audit.
* Environmental: a non-editable install breaks golden-file path resolution; an editable install of core, agents and api fixes it. `tests/test_production_config_a11y_check.py` needs Playwright and fails collection.

## Local observations (this session)

Venv `/tmp/venv-440-0252`, Python 3.12.3, editable core, agents, api.

| Command | Result |
| --- | --- |
| `src/core` pytest, 13 synthetic and AI-statement modules | 134 passed, 1369 subtests, exit 0 |
| `src/agents` pytest, 4 modules, `PYTHONPATH=../core/tests` | 104 passed, 214 subtests, exit 0 |
| `src/api` pytest, 15 modules (excluding Playwright module) | 382 passed, 1 skipped (opt-in Chromium, `test_chat_panel.py:1041`), 1249 subtests, exit 0 |
| `infra/tests/test_bicep_policy.py` | 62 passed, 216 subtests, exit 0 |

Earlier runs against a non-editable install failed on golden-file paths (21 agents failures); recorded as environmental.

## Gaps and blockers

Human AT (#155), staff comprehension (#215), owner needs-inventory sign-off (#165), live Azure residuals and hosted CI are not observable locally.

## Follow-ups

1. Package golden files or fail with a named configuration error (low severity, repeat of prior observation).
2. Next checkpoint: add browser and axe runs where Playwright exists.
