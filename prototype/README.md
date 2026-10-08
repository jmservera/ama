---
title: Proper Warm prototype slice
description: Small constructed-data code slice that demonstrates deterministic workflow authority, bounded agent proposals and tamper-evident audit
ms.date: 2026-08-26
---

This is a non-production prototype. It uses constructed, non-identifying
data only and holds state in memory. It exists to show, in running code, the
control boundaries described in ADR 0001 and the PRD.

## What it demonstrates

* Deterministic stage order with gated stages that need a different named
  human approver.
* Service roles (agent, orchestrator, importer) that can never transition a
  case.
* Optimistic concurrency by version and idempotency keys.
* Agent proposals limited to allowed tasks, with citations and a summary.
  Accepting a proposal never advances the case.
* A hash-chained audit log that `verify_audit()` can check.
* A stdlib HTTP API that reads the caller identity from the Container Apps
  `X-MS-CLIENT-PRINCIPAL` header.

## Layout

* `properwarm/domain.py`: rules and audit chain.
* `properwarm/server.py`: HTTP API.
* `tests/`: unit and API tests.
* `scripts/evaluate_agent.py`: offline contract evaluation.
* `web/app.js`: minimal staff view client.
* `Dockerfile`: non-root image for the API Container App.

## Run

```bash
PYTHONPATH=prototype python3 -m unittest discover -s prototype/tests
PYTHONPATH=prototype python3 prototype/scripts/evaluate_agent.py --out /tmp/eval.json
```

## Limits

The evaluation is an offline contract check (`execution:
offline-contract-only`). It does not call a model and is not a measure of
model quality. The image has not been deployed to the `warm-test` stack.
