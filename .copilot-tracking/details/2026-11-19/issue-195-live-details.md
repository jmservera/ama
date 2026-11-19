---
title: Issue 195 live details
---

build_info.commit(env) returns the value when it matches ^[0-9a-f]{7,40}$, otherwise "unknown". Validation prevents log injection. Tier: FULL (src change); the full gate is not run here (heavy lock held, --all forbidden), so publication needs the coordinator's full receipt.
