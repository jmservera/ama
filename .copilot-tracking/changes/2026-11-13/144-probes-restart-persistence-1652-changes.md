---
title: "Changes 144 probes and restart persistence"
ms.date: 2026-11-13
---

Status: complete. Tier: Focused.

* `infra/tests/test_container_contract.py`: agents app has no hosted probe (platform limit), keeps Single revision, limits and queue scale; api keeps three `/healthz` probes.
* `src/agents/tests/test_worker.py`: heartbeat cadence and margin tests (provider-call bound only); `ReplicaRestartTests` for crash before post and between post and ack.
* `infra/README.md`: C2 and C5 rows state exact evidence and remaining Unmet items (executable rollback test, hosted restart receipt).

Validation: container contract 9 OK; bicep policy 61 OK (after installing orchestrator in the venv); `az bicep build infra/main.bicep` OK; agents suite 371 run, only 2 pre-existing import errors (core test modules not on PYTHONPATH); ruff findings equal baseline (3, none new); mypy on test_worker OK.

Divergence: no hosted probe added for agents; Container Apps probes are HTTP or TCP only (Microsoft Learn health-probes page lists no exec probe) and the worker has no listener.
