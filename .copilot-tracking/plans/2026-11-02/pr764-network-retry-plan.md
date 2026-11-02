---
title: PR 764 third CI failure plan
date: 2026-11-02
---

* [x] Rebase onto origin/main.
* [x] `fetchReadRetrying`: retry only 500/502/503/504 responses without a JSON content type on GET reads; let network errors and aborts propagate immediately.
* [x] Extend `test_first_load_reads_retry_a_cold_start_gateway_failure`: network error rejected on first attempt, JSON-typed failure with charset not retried, gateway 502 still retried.
* [x] Rerun every src-api step locally.

Critique: executed once, inline (single-function change); compatible with owner direction (genuine non-JSON gateway responses on GET reads only). No conflicts.
