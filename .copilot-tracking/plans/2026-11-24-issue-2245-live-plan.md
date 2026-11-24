---
title: Plan and critique for issue 2245 (2026-11-24 live run)
ms.date: 2026-11-24
---

## Plan

* [x] Phase 1: change `continuity.demo_owner_override` to require `ZF_DEPLOYMENT_PROFILE=demo` instead of `ZF_ENV != production`; update `test_demo_owner_override.py` (red before, green after).
* [x] Phase 2: research note with per-criterion table; index row and log entry.
* [x] Phase 3: run core override tests, related continuity tests, ruff, core mypy.

Tier: FULL by rule (src change in a security-relevant AI hold). `rpi-checks.py --all` not run; the coordinator runs gates. No Azure change; no deployment (owner action).

## Critique (executed once)

Verdict: proceed. Risk: the override now applies under `ZF_ENV=production` when the demo profile is set. Mitigations: it needs two explicit variables (the dated owner token and the demo profile), the suspension record stays open, the integrity `gate_hold` still wins in SqlStore, and the demo profile is already the discriminator for chat demo activation. Rejected alternative: removing the ZF_ENV check entirely (loses the profile guard). Accepted: no further user decision needed.
