---
title: Plan - move API venv bytecode policy before API discovery (#1215)
description: Focused plan with phase details for the gate bytecode correction
ms.date: 2026-11-05
ms.topic: reference
---

## Objective

Prevent project-api discovery children with scrubbed environments from writing source-tree bytecode, by installing the existing API-venv bytecode policy `.pth` at API venv creation instead of after discovery. Details: [details](../details/2026-11-05-api-discovery-bytecode-1215-details.md). Research: [research](../research/2026-11-05-api-discovery-bytecode-1215-research.md).

## Tier

FOCUSED. `python3 tools/rpi-checks.py --changed`, `tools/test_rpi_checks.py`, a before/after Runner-path regression, and the maintained Runner UI smoke where it applies. No complete gate (no SQL, security, infrastructure, deployment or receipt-scope change). Reassess if the change must touch receipt acceptance.

## Phases

* [x] Phase 1: Add a Runner-path regression that fails on unchanged tooling (real `Runner._install("api")`, real venv, real scrubbed-env child).
* [x] Phase 2: Move the existing policy write into `_install` for the api venv; remove the later browser-group duplicate.
* [ ] Phase 3: Run focused checks and the Runner UI smoke path; record evidence.
* [ ] Phase 4: Commit with identity safeguards; one Review.

## Critique (executed once, independent read-only rubber-duck agent, before implementation)

* Verdict: Issues. The relocation itself was judged sound (a venv `.pth` runs at interpreter startup, so it survives the scrubbed child; `_install("api")` runs before the shared API scheduling chain).
* Blocking finding 1: the planned regression used a generic child importing a temporary package and did not drive the real producer. Disposition: accepted and applied directly. Phase 1 now runs the real `Runner._install("api")` and the real `design_system_browser_check.main()` server launch (Playwright import stubbed, loopback server, scratch snapshot copy), asserting no `__pycache__`/`*.pyc` under the exact core/agents/api source roots in that child's `PYTHONPATH`.
* Non-blocking finding: `setup-api` (browser-only selection) and receipt/resume coverage are reasoned, not directly tested. Disposition: accepted as a noted limitation. `setup-api` and project-api both call the same `Runner.install` -> `_install`, which the regression exercises; no receipt-acceptance code changes. A sealed-receipt or resume test is not added (would approach receipt-scope policy; reassess if requested).
* No conflict with a confirmed user decision; no further critique will be run for this task.

## Constraints

* Delete nothing; failed receipt `/tmp/g96-c6-1105a` and snapshots read-only.
* No change to the producer harness, environment scrubbing, dirty-snapshot guard, cleanup, receipt acceptance or scope.
* No push, PR, merge or issue state change.
