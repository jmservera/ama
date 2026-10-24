---
title: Details for Entra-authoritative access plan
ms.date: 2026-10-24
---

## Phase 1

* `auth.py`: remove `store.staff` reads in `TrustedProxyProvider`; parse oid with a GUID regex; build `{"code": "E-"+sha256(f"{tid}:{oid}")[:12], "oid", "tid", "name", "email", "role", "roles", "app_admin", "identity_source": "entra", "auth_provider"}`.
* Role resolution: staff roles = mapped claims excluding capability roles; `len > 1` denies; `0` with `ApplicationAdmin` resolves to `Retrofit Programme Manager`; `0` without admin denies. Capability roles `RuleAuthor`, `RegulatoryChat` apply to the validated principal; `RuleOwner` and `AIRestart` apply likewise but keep their downstream named-person and distinct-authority checks.
* Drop `ZF_AUTH_EMAIL_FALLBACK` for trusted-proxy.

## Phase 2

* `Store.actor_record(user)`: DB staff row if `identity_source` is not `entra` and the email matches; for `entra` return the user dict validated by key (`oid`, `tid`, `code`) against recomputed code.
* Replace in bulk_edits, procurement, finance, forms, change_provenance, resident_decisions, workflows, coordinator, chat_privacy, chat_isolation. Compare identity keys exactly as before.

## Phase 3

* Manifest `capabilityRoles` gets `ApplicationAdmin`. `setup-entra.py` already merges. New script `infra/scripts/grant-application-admin.py` with `--tenant`, `--client-id`, `--principal-upn`, `--dry-run` default; applies a single appRoleAssignment when absent.

## Tests

* `src/api/tests/test_auth.py` extended; new `test_entra_authoritative.py`; `infra/tests/test_grant_application_admin.py`.


## Correction cycle 1 of 2 details (appended)

* identity.py: `matches`, `bind`, registry (`people`, `person`, `register`).
* auth.py: admin-only role "Application Administrator", staff-role retention, pending Contractor.
* projection.py/server.py: admin-only allowed set is GET `me`; `_user` binds after authenticate.
* workbench.py: navigation `access` flag only for admins.
* change_provenance.py: `_actor` OID re-resolution.
* grant-application-admin.py: `--expected-oid`.
* Tests: `test_entra_authoritative` (admin data denial, composition, continuity, scoped authority, registry), `test_auth`, `test_rule_alerts`, `test_private_cutover_proof`, `test_grant_application_admin`.

## Correction cycle 2 of 2 details (appended)

* identity.py: `matches(store, tid, oid)`, `legacy_tenant`, `link`, `canonical`, `person`, `people`.
* rulecards.py: `_who` resolver for author/approver/named owner; server.py wires it and links strictly.
* server.py: `_user` links after bind; `/api/me` staff includes recipients.
* Tests: `test_auth.RuleHttpTests` alias independence; `test_entra_authoritative` tenant provenance, alias, concurrency, recipient projection.

## Extra narrow cycle details

* identity.py `distinct`; rulecards.py `distinct` hook in `approve`; server.py wiring; tests in test_auth (RuleHttpTests) and test_entra_authoritative (DistinctTests).
