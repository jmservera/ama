---
title: Details for #162 live break-glass proof
ms.date: 2026-11-18
---

* Phase 1: `az containerapp show` env names only; no values of secrets read.
* Phase 2: sign in with the staff test user through Microsoft sign-in, in-page `fetch` with `X-ZF-CSRF: 1`; compare audit entry count and chain head.
* Phase 3: `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests.test_chat_isolation -q` from `src/api`.
* Delete any thread created by the probes.
