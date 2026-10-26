<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-001 fixture provenance changes
description: Changes record for the runtime-produced fixture tests
ms.date: 2026-10-26
---

Actual order: research, plan and details, critique (Revise, PC-501..504, applied), commit 7a366d5f of those artifacts, then source edit, focused tests, one review, this record.

Source change: only `tools/test_check_demo_feedback.py` (+155 lines): `core_helpers` (checkout-bound `sys.path.insert` and a file-location assertion), `RuntimeFixture` (JSON `Store` over `dataset.DATA` in a temp directory, scripted `_chat` at the AI boundary on a `.invalid` endpoint, `release_support.install` offline release) and five `RuntimeProducedEvidence` tests. `tools/check-demo-feedback.py` and all `src` runtime are unchanged. No checker-contract mismatch was found.

Runtime call path: `Store.detail`, `Store.verify_ledger`, `Store.log_call`, reload through a second `Store` over the same `live.json` and `audit.jsonl`, `Store.ai_priority(user, 1)`; these are the methods behind `GET /api/cases/{id}`, `GET /api/audit-check`, `POST /api/cases/{id}/call` and `POST /api/ai/priority`. HTTP routing itself is not exercised.

Tests: `PYTHONDONTWRITEBYTECODE=1 /home/azureuser/rehearsal-350/venv/bin/python -m unittest tools.test_check_demo_feedback` gave 85 OK (80 earlier plus 5). During the first run my own mistakes (wrong check ids, expecting `pass` where the checker keeps durability `blocked`) were fixed in the test, not the checker. RecursionError and Application Administrator regressions still pass.

Limits: the offline test release id `offline-output-test:priority` is not real release admission; no real model, network, Azure, SQL, browser or gate; JSON-store reload is not SQL durability; the default `bundle()` fixtures stay hand-built (review RV-501); the 980 expected open-programme baseline remains a configured value, distinct from live 443 open and 980 total, with no live capture. A later gate must use `--lock-timeout 0`, base `c8d16059c0c0a22c4ffba88c6b65ac068f64accc`; old receipts are historical.
