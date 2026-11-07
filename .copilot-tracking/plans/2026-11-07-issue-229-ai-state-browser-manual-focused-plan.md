# Plan: issue #229 AI state browser, manual FOCUSED validation selection

Date 2026-11-07. Successor to the original plan and correction1 plan; originals are unchanged. Written and committed before the selected validation below is run against the final head.

## Why this plan exists

The earlier plan to run `python3 tools/rpi-checks.py --changed --base 660716929...` was a mistaken gate admission. The runner refused it before creating any output directory or receipt (`BLOCKED: Reviewed base differs from current origin/main; reconcile before validation`). That refusal is valid and preserved (scratch `gate.log`, recorded in the correction1 changes). It is not a product test failure and no failure is waived. The runner is not changed, origin/main is not altered, no skip flag is added and the command is not retried.

## Scope analysis (read before choosing the tier)

* Child-only diff against the actual declared parent 660716929 is four source files: `src/api/README.md`, `src/api/checks/data_operator_ai_state.py` (new), `src/api/checks/data_operator_browser_check.py`, `src/api/tests/test_data_operator_ai_state.py` (new), plus RPI records. No product UI, API route, schema, SQL, auth, deployment, infrastructure, model, provider, policy, recovery or image change.
* Core `doc_controls.py` denial-message wording is inherited from the parent (the parent differs from main in that file and in 233/153 work). It is not in the child diff, so all safety, retention and legal-hold predicates are unchanged by this loop.
* A conservative main-relative `--changed` would select the inherited consumer/image and atlas work, unrelated to this child. Not used.
* No SQL, security-sensitive, infrastructure, big-feature or release behaviour is found, so the FOCUSED tier stands. FULL is not silently downgraded; there is no contradiction to report.

## Manual FOCUSED selection

Own venv `/tmp/zf229-scratch/venv` (editable install of this worktree's core, agents, api; identity proved by import path and `pip show`). `PYTHONDONTWRITEBYTECODE=1`. Logs under `/tmp/zf229-scratch/final/`.

1. From `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p "test_data_operator*.py"` (includes the new real-Core-to-real-JS regression).
2. From `src/api`: `ruff check`, `ruff format --check` and `mypy` on the changed checker files, per the existing component configuration.
3. Actual `checks/data_operator_browser_check.py` with `ZF_AXE_REQUIRED=1` and the pinned axe 4.10.3 (SHA-256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb, verified before use), under `flock -n /tmp/ama-rpi-heavy.lock` (no queued wait).

All run against the final frozen head. Each literal exit is recorded. No receipt exists or is claimed for this manual selection.

## Limits

Synthetic fixtures do not prove a serving model, employee effectiveness, accessibility acceptance, resident consent or named approval. Independent exact-head assessment, parent publication, hosted checks and whole #229 AT/human acceptance stay pending. `Refs #229` only.
