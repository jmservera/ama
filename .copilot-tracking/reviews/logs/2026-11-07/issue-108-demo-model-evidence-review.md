---
title: Issue 108 demo model evidence review
description: Single post-implementation review of the documentation-only configured model evidence delta
ms.date: 2026-11-07
---

## Execution and outcome

Review executed once on candidate commit `d777f7e2f1b1c3e06f43e1a16949383f9ec005c1` (base `0f420dc9514db22081cb48fa733267d9d33a0d24`). Assessed boundary: three docs files plus RPI evidence. Outcome: Conformant for content; residual blocker for the focused local gate (see R-001). Independent exact-head review and hosted CI remain required and are not claimed.

## Checks

* Every figure in the new section traces to `/mnt/ama-gates/live-891-capacity-1107` (before/after deployment, model capacities, usage lists) or the fresh 2026-11-07 readback. Pass.
* Resource location, configured version and capacity are not presented as serving region, attestation, budget, latency or benefit. Pass.
* No quota or capacity is asserted for any other candidate; mini history is undated and not compared. Pass.
* No credential, token, subscription id or private data in the diff (`git diff` reviewed; account and deployment names only). Pass.
* Log is append-only; original case study, memory, architecture, experimental design, code and infra untouched. Pass.
* No #108 criterion ticked or relaxed; completion not asserted. Pass.
* New links and anchors resolve; older broken links in `log.md` and `README.md` are pre-existing and unrelated. Pass.

## Findings

| ID | Finding | Routing |
| --- | --- | --- |
| R-001 | `python3 tools/rpi-checks.py --changed --base 0f420dc9 --lock-timeout 0` selected only `preflight`, `namespace`, `static` (no image, SQL, browser or scanner group) but exited `BLOCKED: Global heavy-resource lock timeout` because the runner takes the shared `/tmp/ama-rpi-heavy.lock` for every selection and another lane holds it. Not queued or bypassed; no receipt exists | Later: re-run when the lock is free, or the coordinator runs it |
| R-002 | The nano model is `Legacy` with inference retirement 2027-04-14; with `NoAutoUpgrade` the deployment stops at retirement | Recorded in the section; owner decision for any later model change |
| R-003 | Actual-serving region and version attestation, a subscription quota total and a real model call remain unevidenced | Remaining #108 gates, recorded in the section |
