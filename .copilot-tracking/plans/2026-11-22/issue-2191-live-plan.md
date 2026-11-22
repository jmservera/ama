---
title: Issue 2191 plan, fresh stored readings for half of homes
ms.date: 2026-11-22
---

Refs #2191. Tier: FULL (a small `src/api` receiver change was added after the live proof found receiver throughput binding). No Bicep, ACR stays Disabled, no image rebuild (deployed image has the 500 cap and `failureRate`).

## Phases

* [x] Phase 1: planner in `tools/demo_consent_mix.py`: `select_reading_cohort` (granted at least 50% of all homes plus 10% headroom, 10% declined) and `plan(..., granted=)`; CLI `select-readings` and `--granted N`; focused tests.
* [x] Phase 2: live cohort build via throwaway jobs: read current device secrets at run time, generate missing certificates, register new hub devices and delete dropped ones (temporary Registry Contributor role, removed after), apply consent with `SensorConsumer.configure` through the planner.
* [x] Phase 3: `az containerapp job update`/secret set on `job-live-simulator` (new cert secrets, control.json, replicaTimeout 270, failure rate stays 0.1); receiver `control.json` updated for the new cohort.
* [x] Phase 4: live proof: probe fresh stored homes (15 min window) at several slots, hub metrics, staff app screenshot with Playwright; cleanup (role removal, key shred, no throwaway jobs).
* [x] Phase 5: research note, changes record with per-criterion table, review, commit.

## Rollback

Prior secrets and control are captured in a 0700 directory; reapplying them restores the 222 cohort. Consent can be re-applied from the planner.
