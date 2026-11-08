---
title: Issue 1262 correction cycle 1 manifest pin plan
ms.date: 2026-11-07
---

Research: [research](../../research/2026-11-07/issue-1262-r2-manifest-pin-research.md). Details: [details](../../details/2026-11-07/issue-1262-r2-manifest-pin-details.md). Written before the edit.

* [x] Phase 1: Update only the `recipe` digest in the scenario manifest to the SHA-256 of the committed checker bytes.
* [x] Phase 2: Run the two exact hosted-failure tests (red before, green after) and the related Core modules: scenario_manifest, needs_inventory, perspective_walkthroughs, journey_acceptance, retrofit scenario consumers.
* [x] Phase 3: Append a log entry; changes record; current author Review; state; commit.
* [ ] Phase 4: From the clean frozen head, run the planned Core modules, then `rpi-checks.py --changed --jobs 2 --lock-timeout 0` against current origin/main with a new external out, verify with `--required-scope partial`.
