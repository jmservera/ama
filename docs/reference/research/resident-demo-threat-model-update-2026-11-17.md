---
title: Resident Demo Threat Model Update for Main 1c9ac230 (Issue #462)
description: Dated addendum to the 2026-11-16 resident demo threat model after integrating current main, covering the derived sensor freshness keys and the validation provenance of this continuation
ms.date: 2026-11-17
---

## Status and limits

Addendum to the [2026-11-16 threat model](./resident-demo-threat-model-2026-11-16.md), which is preserved unchanged and was written for main `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`. This addendum covers main `1c9ac230be1dad9a4ecc21975f9ffe0845309fc4`, integrated into the candidate by a non-rewriting merge. It has the same limits: a design-time assessment of a synthetic, shared-password demonstration, not a penetration test, security acceptance, production resident identity assessment, accessibility acceptance, or Legal or Data Protection Officer approval. It authorises no deployment or Azure spend. Live Azure resources, role assignments and the live SQL view were not inspected.

Evidence: [continuation research](../../../.copilot-tracking/research/2026-11-17/resident-integration-462-research.md) and [changes record](../../../.copilot-tracking/changes/2026-11-17/resident-integration-462-changes.md).

## What main changed in the resident surface

Between `5e0c7f74` and `1c9ac230`, one change touched the resident projection: #1826 (`fa8329d5`).

* `showcase_view` in `src/core/src/zava_forward/core/resident_showcase.py` now adds three derived keys to the existing `sensors` object: `freshness` (state and plain-language text), `source` (a fixed synthetic and not calibrated note) and `calibrated: false`.
* The keys are computed server-side from the already allowlisted stored readings and the clock. They add no database column, no new SQL statement and no free text from the database. The 17-column reader allowlist in the 2026-11-16 row T7 is unchanged; the output allowlist gains these three derived keys.
* `demo.js` renders a "Reading status" badge and a "Source" line with `textContent`-based helpers. With no stored readings neither is shown; when the history is stale the badge is replaced by a "not recent" caution.
* The wording says the readings are stored and synthetic, not live and not calibrated. It does not make a measurement, safety or compliance claim.

Effect on the 2026-11-16 rows: T6 (cross-case access), T5 (session), T3 and T1 are unaffected, because the case id still comes only from the signed session and no request input reaches the new keys. T7 gains three derived output keys with no new data source. T10 is unchanged: no write, booking, upload, message or AI path was added.

## Provenance of validation evidence

| Evidence | Provenance | What it supports |
|----------|-----------|------------------|
| Resident login, projection and UI implementation on main | Historical, merged before this continuation; not witnessed by it | The code exists; not re-claimed as new |
| 2026-11-16 research, plan, critique, changes, review, state and threat model | Original run on a different host; preserved byte-identical | The original local checks and the recorded full-gate blocker B1 |
| Integration merge, this addendum, light local checks | Newly witnessed by the worktree witness of session `rpi-462-integration` | Local source integration and readiness only |
| Runner repair on main (#1297 lineage and its skip allowlist) | Reviewed on main; consumed, not edited or re-derived here | Explains why blocker B1 is expected to be cleared on main, which only a current-base full gate can show |

The witness records its own clock, Git state and artifact hashes. Actor, session and model values are caller assertions. It is not tamperproof and cannot attest the original run.

## Still unproved after this continuation

* A full gate on the current base with an externally verified receipt, independent exact-head assessment and hosted CI.
* Actual local SQL Server parity, Docker non-root image startup and browser journeys at the current head, which this confinement cannot run (no Docker socket, no SQL Server) or which wait for the shared heavy lock.
* Live HTTPS login, correct-case and negative authorization behaviour, live SQL view and principal grants, Azure resources, spend headroom and any deployment. The owner grant of 2026-11-16 applies only after the full gates and does not revive the dated October spend approval.
* Human accessibility, copy and DPO review.

## Accepted risks

Unchanged from the 2026-11-16 model: the shared credential and stateless sessions are accepted for a time-boxed synthetic demonstration, and any use with real residents, real consent or production identity needs a new assessment and the human approvals recorded elsewhere.
