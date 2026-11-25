---
title: Changes issue 2303 r72
ms.date: 2026-11-25
---

## Changes

* Added src/api/tests/test_image_chat_golden_contract.py (3 tests). Run from src/api with PYTHONPATH=src:tests:../core/src:../agents/src: 3 OK. Mutation: removing the COPY line gave failures=1; removing ZF_CHAT_GOLDEN gave failures=1; Dockerfile restored (git diff clean for it).
* mypy (src/api) success; ruff check and format pass on the new file.
* Added docs/reference/research/issue-2303-live-2026-11-25-r72.md with live evidence on revision 0000072 (live-r0000072.json, live-r0000072.png).
* No Dockerfile or handler change: criterion 2 already holds (lines 30, 34).

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1 Local regression test fails without the golden file or variable | Proven | new api test and core test_cutover_audit; two mutation runs failed |
| 2 Dockerfile copies chat_golden.json and sets ZF_CHAT_GOLDEN | Proven | src/api/Dockerfile lines 30 and 34 |
| 3 After deployment GET /api/ai/report returns 200 and Asset and board view loads | Proven on 0000072 with latency caveat | two 200s (73.5 s API, 93.4 s UI), heading present, no "could not be loaded", no console errors; the UI shows Unknown states with reasons, not the word "Loaded" |
| 4 Full tier: complete local gate and external receipt | Unproven | brief forbids rpi-checks.py --all; coordinator owns the gate; change is test-only |
