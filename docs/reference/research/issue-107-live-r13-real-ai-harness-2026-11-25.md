---
title: Issue 107 capped real-AI acceptance harness, prepared and not run (Refs #107)
description: A fail-closed dry-run harness and eight tests prepare the owner-capped real-AI batch for the five assistants; no tokens were spent and no Azure resource changed
ms.date: 2026-11-25
---

Scope: synthetic demo, desktop only. Tier FULL (new code under `src/api/checks` and `src/api/tests`); `rpi-checks.py --all` was not run. Builds on the [twelfth pass](./issue-107-live-r12-endpoint-deployment-2026-11-25.md). No provider call, no Azure read or write and no sign-in happened in this pass; the live state is the r12 read-only observation of the same day.

## What was prepared

`src/api/checks/assistant_real_ai_acceptance.py` takes an owner authorization JSON (same contract and limits as `heldout_batch`: named human, expiry, call, token and USD caps) and a saved staff `GET /api/assistants` listing. It plans one synthetic, case-free call per assistant whose release is an object with an `id` and no denial `reason` or `missing` evidence, and blocks the rest. Before each call it reserves worst-case tokens and USD, stops at any cap, and charges a missing or out-of-bound usage record at worst case. The command line is dry-run only: a live batch needs `--execute-live` and an injected provider call, so nothing can be spent by accident, and it cannot be useful until an approved release exists (OQ-017).

## Evidence

* `python3 -m unittest tests/test_assistant_real_ai_acceptance.py` from `src/api`: 8 tests OK. They show zero provider calls for a denied listing, an invalid authorization, a missing live flag or provider, and a cap that the worst case would cross; labelled dry-run output; live accounting for ready assistants only; and a stop on malformed usage.
* `ruff check`, `ruff format --check` and `PYTHONPATH=../core/src:../agents/src python3 -m mypy` in `src/api`: clean.
* Assumption: the shape of an in-force `release` entry in the listing is not observed live (none exists), so the harness treats anything except an object with an `id` and no `reason`/`missing` as denied. Confirm it against the first approved release.

## Per-criterion result

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances | Unproven beyond [r12](./issue-107-live-r12-endpoint-deployment-2026-11-25.md); nothing new here | No real older packaged image run; constructed fixtures and local disposable SQL only |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Unproven. The harness for the capped batch is ready and tested offline; delivered-build evidence is not produced | No approved release exists and none may be invented (OQ-017 approver and residual-risk holder); OQ-018 and OQ-019 are owner and DPO items; the owner brief forbids spending tokens |
