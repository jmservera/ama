# Changes: Entra-authoritative application access (issue 360, cycle 5 of 5)

Date: 2026-10-24. Plan: `.copilot-tracking/plans/2026-10-24/entra-authoritative-access-360-plan.instructions.md`.
Critique: `.copilot-tracking/reviews/plans/2026-10-24/entra-authoritative-access-360-plan-critique.md` (REVISE, four blockers, dispositions applied).

## Code

* `src/core/.../identity.py` (new): canonical tenant/OID, derived `E-` code and non-routable `e-<12hex>@entra.invalid` email, display sanitiser, `verified`.
* `src/api/.../auth.py`: trusted-proxy authentication is pure claim validation with no store access. More than one staff role denies. `ApplicationAdmin` alone resolves to the manager option set, view-only; with a staff role the staff role applies. Contractor denied; no email fallback.
* `src/api/.../server.py`: view-only principals receive 403 on every POST except logout. Rule-card approver accepts the derived Entra identity.
* Seam short-circuits via `identity.verified` in bulk_edits, forms, change_provenance, resident_decisions, coordinator, chat_isolation, chat_privacy.

## Provisioning

* `infra/entra/app-registration.json`, `create-api-app-registration.sh`: `ApplicationAdmin` role (stable uuid5 id).
* `infra/scripts/grant-application-admin.py` (new): dry-run default, `--apply`, verifies tenant, app, enabled member principal, idempotent, refuses on mismatch.
* `infra/scripts/setup-entra.py`: `imageType` fix carried from `8b153af4`.

## Tests

* New: `test_entra_authoritative.py`, `test_grant_application_admin.py`.
* Rewritten to Entra semantics: `test_auth.py`, `test_rule_alerts.py` (named alert owners fail closed for Entra principals), `test_bulk_edit_api.py` (SQL oid no longer authoritative), `test_operator_suspension.py` (distinct Entra OID), `test_private_cutover_proof.py` (contractor login denied; wrong-role probe not exercisable).
* Results: infra 371 OK; api 972 run, 1 error (`test_version`, distribution metadata not installed in this environment); core 1243 run, 3 environment-related (`test_version` x2, `test_stock_fabric` CLI). The full gate runs installed.

## Docs

BRD v0.20.0, PRD v0.19.0, ADR 0002 amendment, ADR 0001 lineage, infra README, architecture README, KB index row and log.

## Known limits

* `E-` key truncated to 12 hex; full-pair key is a follow-up.
* Entra principals lose legacy roster ownership; named alert, restart-owner and stored-authority re-reads fail closed.
* Contractor login denied pending company binding.
* Ingress trust boundary requires external forged-header, anonymous and direct-origin negative tests before release.
* Not production acceptance; no live mutation performed yet in this cycle.
