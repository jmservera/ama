---
title: Issue 521 live changes (1444Z run)
description: Changes and per-criterion proven or unproven table for #521
ms.date: 2026-11-18
---

## Changes

Docs and evidence only; no `src/`, `infra/`, workflow or Azure change. Tier FOCUSED (basis: no source change; read-only Azure under the 2026-11-18 owner decisions). The evidence files and research note were written during the Research phase; no source file was edited after `implement-start`.

* Added [research note](../../docs/reference/research/resident-demo-authority-live-521-r2-2026-11-18.md).
* Added an index row in `docs/reference/README.md` and an entry in `docs/reference/log.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/` (raw `az` JSON, SQL and registry probe, Playwright JSON and test outputs; the two screenshots were removed and are not retained).

## Validation

* `src/core`: `test_resident_showcase` 42 OK; `test_resident_showcase_sql` 40 OK (27 skipped).
* `infra`: `test_resident_demo_secrets` and `test_resident_demo_deploy` 33 OK.
* Playwright desktop sign-in: signed_in true, sign out works, binding header absent returns 409.
* mypy, ruff and `rpi-checks.py` not applicable (no Python or workflow change; `--all` never run). Link check of new Markdown: relative targets verified to exist.
* Hosted CI, human approval and independent exact-head review not observed.

## Per-criterion table

| Criterion | Status | Evidence or reason |
|-----------|--------|--------------------|
| 1 Authority end consistent (code, SQL, helper, docs, tests) | Proven (ticked, re-run) | Focused tests pass on the 2028-01-01T00:00:00Z boundary |
| 2 Cost estimate and cap, nothing added | Proven (ticked); no new resource this run | USD 440.90 of USD 700 on 2026-11-18 per the #462 note; billing reconciliation not needed for the demo |
| 3 Rotation and renewal documented | Ticked, not re-derived | No Key Vault rotation per owner decision |
| 4 Live change applied after owner confirmation, verified | Partly proven, open | Proven: live `ZF_DEMO_EXPIRES_AT` 2028-01-01T00:00:00Z, healthy revision 0000012, real sign-in. Unproven: live SQL constraint and `allowed_case` windows (public access Disabled, login refused), image-to-commit mapping (registry denied), apply timestamp (activity log silent), expiry at cutoff (not waited out). The owner-only step is a read-only probe from the private network |

## Unmet

Criterion 4 remains unmet in full; #521 stays open (`Refs #521`, never `Closes`).
