---
title: Issue 2243 live plan r2
---

Tier: focused (no src change). Steps: re-probe live, run targeted tests, write research note, index and log, commit locally.

Critique (executed once, verdict: proceed, no src change): deriving the ledger expiry from the environment is rejected because it removes the owner-reviewed row control (#625) and the SQL is private. Compatible finding applied: record the gap as owner-gated.
