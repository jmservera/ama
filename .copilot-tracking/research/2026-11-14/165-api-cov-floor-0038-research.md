---
title: Issue 165 api and agents branch coverage floor research
ms.date: 2026-11-14
---

## Scope

Issue #165 remaining local engineering slice: audit branch coverage for `src/api` and `src/agents`, and CI per-project test configuration. Base `b64ec641f`, branch `test/demo-165-api-cov-floor-0038`. Research disposition: executed. Planning Readiness: Ready.

## Findings

* No coverage gate or `coverage` configuration exists in `src/*/pyproject.toml` or `.github/workflows/` (`mvp-ci.yml` and `src-ci.yml` run `python -m unittest discover` only). `coverage` is not installed; it was installed to a temporary directory for measurement only.
* The expected interpreter `/home/azureuser/source/ama/.venv/bin/python` does not exist. Editable installs point at the primary checkout, so validation used `python3` with `PYTHONPATH` set to this worktree's `src/*/src`, with `ruff` and `mypy` from `~/.local/bin`. `uv` was not used.
* `src/agents` (branch coverage): total 94% (3015 statements, 990 branches). Lowest modules: `review_effectiveness` 88%, `ai_eval` 89%, `alert_triage` 89%, `cohort_ai_eval` 90%, `queue_azure` 91%. Small uncovered error branches: `alert_triage` (naive or malformed timestamps, invalid alert ids, threshold-shape gaps, minimum-sample reasons), `gate_agreement` (malformed agreement fields), `runtime.beat` OSError, `worker.install_signal_handlers`.
* `src/api`: the full-suite coverage run exceeded its 50 minute budget on the shared host, so a targeted run covered pure-logic modules. `auth.py` was 48% in that subset, with password-cookie and trusted-proxy denial paths untested at unit level. `sensor_handover_verify`, `simulator_admin` and `timecapture` are also low in the subset but depend on SQL or fixtures.
* Pre-existing and unrelated: 8 failures and 5 errors in `src/agents` (`test_paired_report_command`, `test_chat_model`, `test_regulatory_gates`) reproduce on the unmodified base (changes stashed). Cause: a `regulatory_gates.comparison()` signature mismatch and import-path fixtures.

## Selected targets

* `src/agents`: `alert_triage`, `gate_agreement`, `runtime.beat`, `worker.install_signal_handlers`.
* `src/api`: `auth.PasswordProvider`, `auth.TrustedProxyProvider`, `auth.make_provider`.
