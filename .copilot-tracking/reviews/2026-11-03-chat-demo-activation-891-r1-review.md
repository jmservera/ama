---
title: Issue 891 round 1 review
ms.date: 2026-11-03
---

* Review executed once (self-review with security notes); outcome: conformant for slice 1, open work routed to slice 2.
* Security notes: default deny; exact-match string switch plus profile marker; production/pilot profiles denied; the switch cannot be set by a request; registry authorities stay unknown; no secret in code. Residual risk: anyone able to set container env can enable it, which matches the owner decision; `ZF_DEPLOYMENT_PROFILE` is not yet wired in infra.
* Unchanged controls: per-call gate, cost admission, privacy refs, retention, refusals, workflow-only fallback.

## Acceptance criteria

* 1 Activation record and switch: met in code, default denied. Production never honours it: met via profile marker.
* 2 Controls stay in force: met (tests).
* 3 Disclaimer and model-generated label: met in source and string assertions; no browser run.
* 4 Tests: met.
* 5 Docs and registry note: met; no approval claimed.
* 6 Live check after deploy: UNMET (needs infra wiring and owner-authorised deploy).
