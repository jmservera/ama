<!-- markdownlint-disable-file -->
# Plan: authenticated roster transport design and tenant checklist (#360)

Task `demo-transport-plan-360`. Research: `.copilot-tracking/research/2026-10-20/demo-transport-plan-360-research.md`. Details: `.copilot-tracking/details/2026-10-20/demo-transport-plan-360-phase-details.md`.

## Objective

Add a reviewable design, not execution, to the existing infra runbook and cutover evidence pack: a documented authenticated result transport for the private worker-to-controller roster candidates result, a script-oriented implementation plan with fail-closed tests, and a tenant-administrator/operator checklist. Preserve the three failed attempts, original roster and adverse evidence.

## Boundaries (non-goals)

* No parser relaxation, decryption, live retry, cloud allocation/deployment/Graph write/secret read/private dataset/billing run, no tenant object change.
* No edit to issue #126 budget/benefits synthesis, cohort, Finance form or map domains. No source code change (design only); no new RPI-gated executable.
* Never delete RG `ama`; never retire Front Door before verified replacement and explicit authorization. Whole 360c/d/e not ticked.

## Phases

1. [x] Research (executed). Evidence above.
2. [ ] Plan critique once; apply compatible findings directly.
3. [ ] Implement documentation:
   * `infra/README.md`: new `### Authenticated Roster Result Transport Design (2026-10-20, Refs #360)` before `### Public welcome and Microsoft account photos`: preserved evidence, requirements trace, options, recommended T1 plus binding extension, decision-needed list, script-oriented plan, tests, tenant/operator checklist, preconditions and non-claims.
   * `docs/architecture/cutover-evidence-pack.md`: concise dated entry linking the design, state of evidence and acceptance delta.
   * `docs/reference/README.md` index row and append-only `docs/reference/log.md` entry.
4. [ ] Review once (`rpi-review`) with original outcome retained.
5. [ ] Commit, full local gate, receipt verification, frozen local handoff. No push.

## Decision-needed items (recorded in the design, not resolved here)

* DN1 Owner/security reviewer accepts ciphertext-only metadata in resource tags despite the official plaintext warning, or requires T2.
* DN2 Real position count and whether compression is permitted (bounded decompression) when above the 40-frame limit.
* DN3 Which code path the three failed attempts ran (reconcile before any retry).
* DN4 T7 manifest-derived positions acceptable or not.

## Success criteria

* Every requested binding and property (run, query, worker, manifest, image, authorization, confidentiality, integrity, freshness, complete response, fail-closed parsing) has a mapped mechanism, a current gap if any and a test.
* No success claim for unexecuted behavior; sources dated; provider samples not generalized.
* Checklist covers app/roles/credential/vault path/roster/SQL restart/browser role tests, identities, private backing services, direct HTTPS, production profile, with tenant authority distinct from RG authority.
* Index and log updated; full local gate passes.

## Critique Disposition

One original critique executed (verdict Revise): `.copilot-tracking/reviews/2026-10-20/demo-transport-plan-360-plan-critique.md`. Seven findings (C1-C7) applied directly; no conflict with owner decisions; not repeated. Additions to scope: DN1 broadened to a privacy/security gate, new DN5 (independent attestation), option T8, threat table, snapshot/ambiguity rules, relay-specific checklist rows.
