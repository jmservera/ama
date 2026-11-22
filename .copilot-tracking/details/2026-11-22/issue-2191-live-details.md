---
title: Issue 2191 phase details
ms.date: 2026-11-22
---

## Phase 1

* `select_reading_cohort(all_homes, reading_share=0.5, headroom=0.1, declined_share=0.1)` returns `(cohort, granted)`; granted = ceil(total x reading_share / (1 - headroom)); declined = ceil(granted x declined_share); cohort spread evenly via `select_cohort`; refuses above `MAX_COHORT`.
* `plan(home_ids, now, granted=None)`: default stays half; explicit count validated 0 < granted < len (a declined home is always kept).
* Tests: coverage of reading share and a declined minority for 443 homes; plan with explicit granted; refusal of invalid counts; existing tests unchanged.

## Phase 2 and 3 (live)

* Device id is `SYN-` plus `sensor_key(home)`; files `<device>.pem` and `.key`; secrets are per file; control.json lists the cohort homes.
* Hub registration through the data plane REST API with the job identity `id-cutover-test-api`; thumbprint authentication; register only missing devices; delete dropped ones.
* Update with `az containerapp job secret set` plus `az containerapp job update` volume secrets; verify counts by readback; verify execution Succeeded.

## Phase 4

Probe `job-2191-probe` queries distinct homes with a stored reading in 15, 30 and 60 minutes; target at least 222 of 443 within 15 minutes at repeated slots.
