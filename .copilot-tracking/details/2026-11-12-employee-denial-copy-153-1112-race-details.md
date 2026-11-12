---
title: Issue 153 stale-stage refusal plan details
ms.date: 2026-11-12
task_id: 153-blocked-copy-readiness-1112
---

## Phase 1 details

Test location: `src/api/tests/test_mvp.py`, class `ApiTests` (uses `self.call` with a cookie; add the `X-ZF-CSRF` header only if the existing helper requires it, as the existing login-flow test does without it). Fixture: build the ZF-3 package/capacity/work order/appointment exactly as `StoreTests.test_gate_blocks_until_everything_confirmed` does, against the store held by the server; sign in Sam and Pam; Pam advances (200); Sam advances (400).

## Phase 2 details

Single raise site `src/core/src/zava_forward/core/store.py` `Store.advance`. The message is returned by `server.py` through the existing `except ValueError` branch as `{"error": str(e)}`, so the client renders it unchanged in the existing `p.err` and status region. The owner is the case owner field already displayed on the case page.

## Phase 3 details

Commands run from `src/api` with the isolated venv (`pip install -e core -e agents -e api`): `PYTHONPATH=../core/tests python -m unittest ...` (PYTHONPATH only exposes the shared test dataset directory, as the repository guide specifies for src/api tests, not the source packages).
