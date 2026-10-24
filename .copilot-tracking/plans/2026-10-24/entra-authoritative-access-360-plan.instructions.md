---
applyTo: '.copilot-tracking/changes/2026-10-24/entra-authoritative-access-360-changes.md'
---

# Plan: Entra-authoritative application access (issue 360)

## Phases

* [ ] Phase 1: auth core. `TrustedProxyProvider` validates tenant, one valid oid and roles from claims, builds the principal, and never touches `store`. Add `ZavaForward.ApplicationAdmin` handling and `Store.actor_record`.
* [ ] Phase 2: call-site seam. Replace the actor `store.staff.get(...)` re-validation in core modules with `actor_record`; keep object grants, resident isolation and approval separation.
* [ ] Phase 3: provisioning. Add `ApplicationAdmin` to `capabilityRoles` in the manifest; add an idempotent `grant-application-admin` Graph path with dry run, tenant, app and principal verification, that only adds the one assignment and refuses unrelated or ambiguous cases.
* [ ] Phase 4: tests. Auth, seam, role composition, identity audit fields, provisioning idempotence and refusals.
* [ ] Phase 5: documentation via BRD, PRD and ADR agents (minimum necessary), KB index and log.
* [ ] Phase 6: gate. Focused tests, `tools/rpi-checks.py --all`, receipt verify, original independent Review, candidate handoff to the coordinator. No push before release.
* [ ] Phase 7: deployment and verification under the finite authority after release (image route priced first). Assign the verified admin the role only after tests and review.

## Success criteria

* Assigned user with no staff row authenticates with a store that raises if touched.
* Wrong tenant, missing or duplicate oid, no role, unmapped role, Bearer without aad all deny.
* ApplicationAdmin alone and with ProgrammeManager both authenticate; two staff roles still deny.
* No self-approval, named-approver, AI-restart or resident-consent boundary changes.
* Provisioning rerun makes no change; wrong tenant, app or principal is refused.

## Details pointer

`.copilot-tracking/details/2026-10-24/entra-authoritative-access-360-details.md`

## Implemented decisions and current limitations (appended 2026-10-24 after the ADR and document handoff)

The original critique REVISE outcome and its dispositions above are preserved. Later evidence changed one design choice and recorded limits:

* ApplicationAdmin alone no longer acts as Programme Manager. The principal resolves to the manager option set for visibility but carries `view_only`, and the server refuses every state-changing request except sign-out. With a staff role the staff role alone supplies authority. Reason: the ADR review concern that role coercion would grant business actions. Tests: `test_entra_authoritative.py`.
* Identity keys remain `E-` plus a 12 hex digest of the canonical tenant and OID, re-derived and verified at actor seams. The 12-hex truncation is a recorded collision-risk limitation; a full-pair key is routed as a follow-up.
* Legacy staff codes and case ownership are not migrated or guessed from email. Existing DB-bound staff lose roster-code ownership under Entra identity until an explicit verified crosswalk exists.
* Named workflows unavailable for Entra principals (RuleOwner or AIRestart named-person binding, procurement capacity re-reads, contractor company binding) fail closed and are reported as limitations, not completed.
* Ingress trust: the Python parser trusts platform-injected headers; anonymous and forged-header denial must be verified externally against the serving build (release gate).
* Documents updated from the session proposals: BRD v0.20.0, PRD v0.19.0, ADR 0002 dated subsection with ADR 0001 lineage note, infra and architecture READMEs, KB index and log. Status is owner-directed design, not deployed or accepted.


## Correction cycle 1 of 2 (appended; original plan unchanged)

Trigger: coordinator exact-head assessment REVISE (F1-F5) against c96dae0c. Scope: separate option visibility from business authority; OID-verified roster continuity and selectable Entra recipients; scoped authority resolved at the protected operation; OID-bound grant script; company-bound Contractor path. No documentation-only resolution. Critique is not repeated for the task; corrections are covered by an independent correction review before the clean-head gate.

## Correction cycle 2 of 2 (appended)

Trigger: coordinator reassessment REVISE of 22ca2c2b. Scope: tenant-aware continuity resolver, canonical distinct-person checks over a transactional alias record, recipient projection. No broad redesign; no third unapproved retry (a remaining blocker goes to an explicit technical ledger).

## Extra narrow cycle (owner approved one)

Scope: unresolved historical author identity denies approval; no history rewrite, no email inference. Result recorded in the changes artifact.
