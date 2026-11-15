---
title: Issue 146 incident suspension and diagnostic redaction changes
date: 2026-11-14
task_slug: 146-incident-suspend-redaction-0038
---

## Changes

* `src/core/src/zava_forward/core/diagnostic_logging.py`: public `SENSITIVE` widened (SAS, API keys, Basic auth, UK phone, postcode, NI number, resident/UPRN/tenant pairs, long hex/base64); traceback and exception-text redaction; placeholder-safe masking.
* `src/core/src/zava_forward/core/monitoring_coverage.py`: reuses `SENSITIVE`, so allowlisted diagnostic fields reject the same values.
* `src/core/tests/test_diagnostic_logging.py`: three tests.
* `src/api/tests/test_operator_suspension.py`: seeded breach to task-scoped owned suspension to no-silent-restart test.

## Divergences and validation

* Plan critique found nothing requiring user decision. No `continuity.py` change was needed.
* Required `/home/azureuser/source/ama/.venv` does not exist; system `python3` with `PYTHONPATH` to this worktree was used; `uv` not used.
* `ruff check`, `ruff format --check`, `mypy`: pass in `src/core`, `src/api`, `src/agents`.
* `src/api` full suite: 3102 tests OK. `test_operator_suspension` 18 OK. Core `test_scenario_manifest`, `test_diagnostic_logging`, `test_monitoring_coverage`: 49 OK.
* `src/core` full suite: 35 failures and 16 errors, all in device-provisioning tests needing the missing `azure.iot.hub` SDK plus one subprocess test that drops `PYTHONPATH`; none touch changed files. Not run on base for comparison.
* `src/agents` full suite: 436 tests, failures only from missing sibling test paths (fixed by adding `core/tests`: `test_chat_model`, `test_regulatory_gates` OK) and `test_paired_report_command` subprocess tests (`comparison() takes 1 positional argument`), an environment path artifact in files this change does not touch. Not compared with base.
* Hosted CI, independent exact-head review and human approvals were not run; no push.
