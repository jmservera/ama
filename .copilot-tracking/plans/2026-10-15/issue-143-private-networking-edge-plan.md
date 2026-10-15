---
title: Issue 143 private networking and public edge plan
date: 2026-10-15
---

## Plan

* [x] Phase 1: add `infra/modules/edge.bicep` (Front Door Premium, WAF, Private Link origin, custom domain, diagnostics).
* [x] Phase 2: wire `enablePublicEdge`, `edgeCustomDomain`, `edgeWafMode` in `main.bicep`; guard checks; EasyAuth forward-proxy; outputs.
* [x] Phase 3: `infra/tests/test_edge_module.py` coverage and edge tests.
* [x] Phase 4: README coverage table, edge procedure and open items.

Critique (single pass): edge off by default, production-only guard, no invented evidence; compatible, applied. Verdict: proceed.

Validation: `az bicep build`, `az bicep lint`, `python3 -m unittest discover -s infra/tests`.
