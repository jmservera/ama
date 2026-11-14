---
title: Runtime to Bicep signal parity plan
ms.date: 2026-11-14
---

Details: [details](../details/2026-11-14-demo-146-runtime-bicep-signal-parity-0424-details.md). Research: [research](../research/2026-11-14-demo-146-runtime-bicep-signal-parity-0424-research.md). Focused validation tier (non-gate test and runbook text only; no workflow, permission or deployment change).

* [x] Phase 1: Add `infra/tests/test_runtime_bicep_signal_contract.py`.
* [x] Phase 2: Fix runbook reason-code drift for `ai-limit-calls`.
* [x] Phase 3: Run targeted tests and ruff.

Critique: one pass, executed inline; verdict accept. Findings applied: restrict reason extraction to `held`/`reason` sites, treat `budget-currency-*` as a documented family.
