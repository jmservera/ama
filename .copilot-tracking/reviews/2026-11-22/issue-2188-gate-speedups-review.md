---
title: Review of issue 2188 shard retry
date: 2026-11-22
outcome: Conformant with findings
---

Executed once after implementation.

* RV-001 (Medium): full gate not run; semantics of verify with retries are covered by unit tests only. Route: coordinator full gate.
* RV-002 (Low): retry unit is the shard, not the test class. Route: follow-up.
* RV-003 (Low): image concurrency and before/after wall time remain open on #2188; the commit must use `Refs`, not `Closes`.
* No evidence of weakened coverage: the passing rerun must satisfy the same matrix identity and skip checks; retries only add recorded evidence.
