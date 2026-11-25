---
title: Plan issue 2303 r72
ms.date: 2026-11-25
---

* [x] Add src/api/tests/test_image_chat_golden_contract.py (COPY, ZF_CHAT_GOLDEN, dockerignore).
* [x] Prove the test fails on mutation; run mypy and ruff.
* [x] Live proof on 0000072 (probe script, JSON, screenshot); research note.
* [x] Changes record with per-criterion table; review; commit.

Tier: FULL applies by the issue because src changes (test only); the coordinator owns the gate, rpi-checks.py --all not run.
