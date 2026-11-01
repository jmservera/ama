---
title: Role-screens copy lint plan
---

* [x] Reword visible copy (hold to pause, provenance to source details) in `role-screens.js`.
* [x] Rename local identifiers `hold`/`holds` to `pause`/`pauses`.
* [x] Add identifier-only allowances `h.hold`, `inv.hold` in the copy audit; BANNED unchanged.
* [x] Validate: node --check, api unittest, ruff, mypy.

Critique (single pass, direct): compatible; no field renames, no weakening of BANNED. Verdict: proceed.
