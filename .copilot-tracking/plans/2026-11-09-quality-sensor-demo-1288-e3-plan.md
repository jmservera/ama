---
title: Plan - issue 1288 E3
---

# Plan: issue 1288 E3 (third of five additional cycles; two remain)

Task `issue-1288-e3`, parent `issue-1288-e2`. Refs #1288 only; whole and live criteria stay OPEN. Research: [research](../research/2026-11-09-quality-sensor-demo-1288-e3-research.md). Details: [details](../details/2026-11-09-quality-sensor-demo-1288-e3-details.md).

## Phases

* [x] P1 Fix the E2 untyped-test mypy diagnostics with proper types and helpers (no `ignore`, stub or `cast`), judged at diagnostic level on the same tool and config. Done before planning; commit `ed6f14f1b`; 141 new to 0 new.
* [x] P2 Integrate pinned main `23e944c1f` ordinarily, keeping sensor and SQL schemas, resolving the 184 overlap. Done; merge `4b8d87801`.
* [ ] P3 Decision on the dedicated synthetic-demo route. Planned outcome: FREEZE (no activation), because no non-inferential positive provenance exists and the only sound design is an owner-decided architecture (research Conclusion).
* [ ] P4 Add one regression test that locks the boundary closed against spoofed simulation claims (SYN naming, demo and chat switches, arbitrary `ZF_DATA`, free text) through the production composition with a real `Ai`, TLS peer, counting meter and token counter.
* [ ] P5 Targeted validation: API SQLite sensor and quality modules, core sensor modules, owned-SQL variants under the nonqueued shared lock, browser and axe, ruff and same-tool mypy comparison. No full gate.
* [ ] P6 One review, handoff, clean local commit.

## Constraints kept

* Real/private captured-data path stays OFF; no new switch, store, token, env variable or provenance system.
* Auth, consent, current-capture checks, manual approval, failure, cost and release safeguards unchanged. No source change outside tests.
* No live Azure or model calls, no push, PR, issue or merge actions, no private `ZF_DATA`.
* No web file edited. Current web-design-guidelines fetched (sha256 `d246b026...0234`); the manual, permission and unavailable paths are unchanged and re-run through the browser check. No AT acceptance claimed.

## Acceptance for E3

* 0 new mypy diagnostics and a clean ruff on the touched tests.
* Targeted tests green (SQLite and owned SQL); skips and counts recorded.
* The frozen decision and the exact future admitted step are in the handoff.
