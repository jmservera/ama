---
title: Issue 2243 live plan
---

Tier: focused (no src change). Steps: probe live, run targeted tests, write research note and per-criterion table, index and log, commit locally.

Critique (executed once, verdict: proceed): a code change to derive the ledger expiry from the environment is rejected because #625 made it owner-reviewed row data and the SQL is private. Compatible finding applied: record the gap as owner-gated rather than fix it.
