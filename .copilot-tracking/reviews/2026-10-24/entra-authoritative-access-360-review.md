# Review: Entra-authoritative application access (issue 360, cycle 5)

Date: 2026-10-24. Reviewed commit: `885dc5fc`, base `f1e2d830`. Independent read-only code-review agent; nothing was executed by the reviewer.

Outcome: CONFORMANT WITH FOLLOW-UPS. No Critical or High findings.

## Critique blockers

* Canonical lowercase UUIDs: resolved (`identity.canonical_guid`, used by principal, verified and provider).
* No claim used in an authorization key: resolved (email always derived; name display-only; `verified` rejects altered keys; seams use it).
* Derived non-routable email: resolved (`e-<12hex>@entra.invalid`; rule-card no-self-approval compares it).
* Release-gated external negative tests: partly resolved. Recorded as a release gate in ADR 0002; not yet evidenced by code or probe.

## Other checks

Multi-role composition correct (admin alone view-only; admin plus one staff role keeps that role; two staff roles or Contractor denied). View-only enforced on every POST except logout. Consent, object grants and no-self-approval preserved. Forged-claim handling fails closed. Grant script dry-run default, no secret output, one verified assignment, idempotent.

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Medium | Direct-origin and forged-header denial not enforced or tested by this change | Resolved in docs: ADR 0002 states it is an unmet release gate. External probe still required before release |
| 2 | Medium | View-only admin reads the full Programme Manager projection, exports and staff directory | Disclosed in ADR 0002 as known exposure; restriction is a follow-up |
| 3 | Low | Any well-formed derived approver email is accepted for rule cards | Follow-up; approval still needs `rule_owner` claim |
| 4 | Low | infra/README described Contractor probe as bound | Fixed in README |
| 5 | Low | procurement, workflows `_staff_person`, finance seams fail closed for Entra staff | Follow-up; already listed as limits |
| 6 | Low | Web UI does not use `view_only` | Follow-up |
| 7 | Low | `setup-entra.py` runtime_patch change outside scope | Accepted; required for the imageType fix |
| 8 | Low | Grant script checks app by id and role value only | Accepted; operator supplies the id |

Review is not repeated within this task. Corrections committed after this review are documentation-only.
