---
title: "#144 C1 README heartbeat fix changes"
ms.date: 2026-11-13
---

* infra/README.md: "Worker and job images" row now reflects #1523 (token source, ApiResultSink, build_runtime, standby loop without the route flag; unit-tested locally; pipeline receipt Unmet); heartbeat sentence states the one-call arithmetic accurately; line ~1627 distinguishes standby from configuration error.
* src/agents/tests/test_worker.py: margin test derives the largest accepted timeout from `TaskMessage.from_json`, uses `ERROR_BACKOFF_SECONDS`, `IDLE_SECONDS`, `HEARTBEAT_MAX_AGE_SECONDS`; `replace_worker` capped at 20 iterations and asserts an ack happened.
* docs/architecture/cutover-reference-inventory.tsv: regenerated with `cutover_audit --write`; check passes (130 rows, 1913 locations).

Validation in /tmp/venv-144c1-1745: src/agents 404 tests OK; test_container_contract 9 OK; test_bicep_policy 61 OK; test_cutover_audit 9 OK; mypy clean (52 files); ruff clean on the changed test, `ruff check src/agents infra` shows the same 111 pre-existing findings in infra before and after (baseline, not touched).
