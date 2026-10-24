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


## Correction cycle 1 of 2 (coordinator exact-head REVISE against c96dae0c)

The earlier "Known limitations" entries on lost roster ownership, stored-authority
re-reads and Contractor denial are superseded by the corrections below (original
text retained above). Commits 885dc5fc and c96dae0c are preserved; corrections are
new commits.

* F1 (HIGH): `auth.py`, `projection.py`, `server.py`, `workbench.py`. ApplicationAdmin alone is the non-staff role "Application Administrator": no Programme Manager coercion, only GET of the caller's own `/api/me`, empty counts and staff. With a staff role the role, data and actions are that role's, all ten options are listed and flagged `access`.
* F2 (HIGH): `identity.bind` after authentication gives a verified OID matching exactly one enabled roster row its legacy code/email/name (never email match, role from claims only); a registry of acting Entra staff supplies selectable handoff recipients via `workflows._staff_person` and store suggestions. Rule-alert owner acknowledgement positive test restored.
* F3 (HIGH): `change_provenance._actor` re-resolves the bound row by OID at the protected operation (code and email must match `bound`) and overlays `financial_authority` and `contract_authorities`; expiry, revocation, scope, independence checks unchanged; no DB read on the auth path.
* F4 (MEDIUM): `grant-application-admin.py` requires `--expected-oid`; the UPN must resolve to it in dry run and apply, and the read-back verifies resource, role and principal.
* F5 (MEDIUM): a Contractor authenticates to a pending principal with no DB read; `identity.bind` requires exactly one enabled Contractor row with that OID and a company, else 401; contractor positive and wrong-role 403 coverage restored (including `test_private_cutover_proof`).
* Docs realigned: BRD FR-053 AC-106/107, PRD DD-009/FR-062/AC-113/changelog, ADR 0002 subsection, infra README.
* Tests: api focused 83 OK, infra proof/grant 24 OK; full suites and the exact-head gate are recorded separately.
* Known limits: derived `E-` key is a 12-hex digest; registry roles are last-seen; some seams (hazard subject, capacity accepted_by) may still fail closed for unbound principals; the web UI does not yet render the `access` flag; ingress forged-claim, wrong-audience and direct-origin probes on the serving revision remain a pre-deployment gate. Not production acceptance.
