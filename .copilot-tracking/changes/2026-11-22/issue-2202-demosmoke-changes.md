---
title: Issue 2202 demo smoke changes (2026-11-22)
---

Planned changes (documentation and evidence only, no src change, focused tier): docs/reference/research/issue-2202-demosmoke-2026-11-22.md with probes and screenshots, index entry in docs/reference/README.md, log entry in docs/reference/log.md. Issues filed: 2243, 2244, 2245.

## Done

Added the evidence note, probes, results and screenshots, index entry and log entry. Issues filed: 2243 (resident AI expiry hard-coded), 2244 (API start-up write-lock crash-loop), 2245 (employee chat 500 and no generative answer). No source change; tier focused; documentation link review only.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Images rebuilt from main and rolled (API, resident, simulator, receiver) | Unproven: resident image not rebuilt or redeployed; API digest rolled by other work |
| Revisions Running and Healthy; hardening enforced with rollback and agents difference | Partly proven: hardening `enforced` on API and agents, API Healthy at 0000050 after a 13 minute failed-start window; agents difference and rollback not explained |
| Owner demo checks (charts, gauges, consent, routing, half of homes) | Partly proven: earlier evidence for charts, gauges, consent, routing; map readings 59 of 443 (13.3%) below half |
| Live receipt and log entry | Proven |
