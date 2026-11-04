---
title: Plan for #176 slice 1
ms.date: 2026-11-04
---

* Stacked slices: (1) sensor stream revision and audit replay (this PR); (2) none further achievable in code, since the remaining blocker is the absent original register generator and inputs (owner action).
* Phase 1: add `generator_revision` to `sensor_stream.descriptor`; replay `sensor-stream` in the audit with a fictional register and mixed consent.
* Phase 2: tests, README section, log entry.
* Validation tier: focused (no security, infrastructure, SQL or deployment). Gate not run; coordinator runs gates.
* Critique: executed once inline; compatible finding applied: use the full 64 character digest and the composed sources only when a climate is supplied.
* Boundaries: synthetic data only; no resident, consent or approval behaviour changed; no AI feature touched; no web files changed.
* Details: [details](../details/2026-11-04-synthetic-determinism-176-details.md).
