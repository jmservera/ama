<!-- markdownlint-disable-file -->
# RPI Phase Details: Finite costed execution plan for #126 (recovery run)

## Metadata

* Task ID: 126-paid-plan-recovery
* Task slug: paid-execution-plan-126-recovery
* Related plan: .copilot-tracking/plans/2026-10-20/paid-execution-plan-126-recovery-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-20/paid-execution-plan-126-recovery-research.md; pre-RPI draft details (unverified input) .copilot-tracking/details/2026-10-20/paid-execution-plan-126-phase-details.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Draft the costed-plan subsection | ready | P01, P01-T01, P01-T02, P01-T03 |
| P02 | Index, log, clarification and checks | ready | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Draft the costed-plan subsection

### Context

The addendum holds EXA-012 (earlier 450 USD cap) and the carry-forward subsections; the new subsection follows the 2026-10-13 carry-forward. Research (F1-F6) supplies the figures.

### Intent

One subsection that lets the owner choose, approve fields, and see exact gates.

### Boundaries

* Included: addendum subsection, ms.date.
* Excluded: infra/README.md, schema packs, map docs, cohort pack, new pages.

### Likely Targets

* docs/case_study_48_addendum.md: new subsection after the carry-forward.

### Dependencies

* Recovery research complete.

### Validation Expectations

* Arithmetic reproduces; no IDs; links resolve.

### Completion Evidence

* Changes record lists the subsection and check outputs.

### Unresolved Items

* Reserve size, SQL pause saving and subscription-scope spend are owner-only; stated as unresolved.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Cost position and options

#### Context

Basis (USD, RG `ama`, ActualCost, retrieved 2026-10-20, estimated): accrued 1-20 Oct 189.94; complete days 1-19 172.47; partial 20 Oct 17.47; run rate 30.245/day (18-19 Oct mean; two-day sample). Meters: SQL vCore about 10.66/day, Front Door Premium base about 10.64/day, old-environment private endpoint 2.4, registry 1.67, remainder small. 94 resources inventoried.

Projection formula: P_RG = 172.47 (complete days 1-19) + 12 days from 20 Oct at the run rate in force. U is the owner-supplied bounded MONTH-END FORECAST of charges and liabilities outside RG `ama` (accrued to a timestamp plus forecast to 31 Oct, incl. applicable liabilities and late billing; scope, source, timestamp, currency recorded). It excludes `ama`, so P_RG and U never double count. Accrued-only is not U. Unbounded or unrecorded U blocks every paid tranche; zero is never assumed. (Corrected 2026-10-20 after independent finding; earlier text defined U as accrued-only.)

* S0 no change: 172.47 + 12 x 30.245 = 535.41; headroom -35.41; blocked.
* S1 Front Door retired effective 21 Oct: 172.47 + 30.245 (20 Oct) + 11 x (30.245 - 10.64) = 418.37. Each day of delay beyond 21 Oct adds 10.64, so the owner recomputes from the actual effective date. Rollback or recreation of the edge adds its own cost and is not included.
* S2 S1 plus SQL idled after 25 Oct: the saving is a range of 0 to 10.66/day, with no measurement. A midpoint of 50 percent over 6.3 days gives 384.79; this is an illustration, not a baseline, and S2 is never used for eligibility until a saving is measured.

Two distinct rules use one set of numbers:

* Approval envelope E = P_option + U + sum of approved tranche ceilings + reserve R, and E must be at or below 475. R = 30 is an assumption without evidence of latency; the owner may replace it, and a larger R shrinks the admissible tranches.
* Live monitoring projection L = accrued + remaining days x measured run rate + unspent ceilings + U, with no reserve. Review at L of 400, pause new starts at 450, stop and clean up at 475; the reserve sits between L and the 500 cap.

Maximum admissible U = 475 - P_option - ceilings - R (R = 30): S1+T1,T2 8.63; S1+T1-T3 -6.37 (blocked); S2+T1-T3 27.21 only if the saving is measured at least equal to the illustration; S0 blocked. These are limits, not assumed values. E at or below 475 implies L at most 445 at start, so the 450 pause is consistent. T0 costs nothing.

#### Intent

Make the arithmetic reproducible and the gating rule one formula.

#### Boundaries

* Included: three options, sensitivity, thresholds, eligibility rule.
* Excluded: any claim that subscription-level spend is known.

#### Likely Targets

* docs/case_study_48_addendum.md.

#### Dependencies

* Research F1-F3.

#### Validation Expectations

* Recompute the numbers by script and record in changes.

#### Completion Evidence

* Stated values equal recomputed values.

#### Unresolved Items

* Reserve and SQL saving remain assumptions flagged as such.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Tranches T0 to T4 and T1 approval template

#### Context

* T0 owner prerequisites (zero spend): record subscription-scope charges, credits and billing latency from an owner-run query with timestamp; choose S1 or S2; name Front Door retirement (profile, endpoint, WAF; managed Private Link after inventory; recreate via infra/public-edge-existing.bicep) and SQL idle (suspend the 5-minute orchestrator schedule). Retire only after inventory per infra README rollback guidance; never VNet, SQL, registry, vault, storage or Foundry; never delete RG `ama`; identities preserved.
* T1 first deployment tranche, existing demo API only, no new billable resource types, duration window 4 hours, ceiling 8 USD (incremental logs and compute only). Mutations T1 may need, each needing explicit approval and a rollback: tenant registration and consent (rollback: owner tenant operator removes the registration; no deletion of identities), roster initialization (rollback: authorised operator reverses through the roster path), and replacing the deny-all ingress restriction (rollback: restore the recorded restriction). Local-first stage 0 (free): `ZF_AUTH=password` sqlite synthetic run via `python3 -m zava_forward.api` to rehearse the owner script. Azure-only needs: real sign-in, roles, private SQL and real AI, which local cannot show. Preconditions (all known open): valid managed-identity client sentinel; tenant registration and consent by a tenant operator (`python3 infra/scripts/setup-entra.py --run-in-azure --secret-store keyvault --yes`); private roster and check/apply path (`initialize-workbench-staff.py --check` then `--apply --restart`) by an authorized private-connected executor; change of the deny-all restriction only under approval. Expected checks: browser sign-in as a named synthetic tenant user reaching /app with the real identity shown; roles page shows the expected synthetic role; SQL staff check reports expected synthetic rows; the AI check is conditional: no model deployments exist, so it reports not available (not pass) unless T2 deployments are separately approved. Pass evidence is an authenticated 200 on /app and an authenticated identity response naming the synthetic user; fail rules: 3xx to a login page, 401 and 403 are failures or not-yet-signed-in, never sign-in. Approval fields: approver, approval time, scope (tranche, resource list), cost envelope and ceiling, start and do-not-start times (latest start = 2026-10-25T16:02Z minus duration minus six hours: T1 06:00Z, T2 (6 h) 04:00Z, T3 (8 h) 02:00Z; 25 Oct is a Sunday, so owner availability is not assumed and earlier approval is advised), identity changes (none or listed), rollback, evidence to capture.
* T2 actual-model evaluation: two deployments in UK South, gpt-4.1-mini and gpt-4.1 version 2025-04-14 (Legacy, inference deprecation 2027-04-14), GlobalStandard capacity 10 each, quota Unknown; caps 300 mini and 100 gpt-4.1 calls; per call bound 12,000 input characters and 600 output tokens; worst case 4.61 USD at list price; practice run on existing non-held-out fixtures only; the first capacity or quota error stops T2 with no retry; token cost basis is list price retrieved 2026-10-20 (USD, not agreement price); held-out manifest and human gates unapproved; deployments deleted at end; ceiling 10.
* T3 Azure validation bill of materials: #358 vault preservation (temporary vault, 1, Standard, UK South, lifetime hours, synthetic secrets); #117 retention/scan simulation (temporary storage account, 1, Standard LRS, UK South, synthetic blobs); #122 restore drill (temporary SQL database, 1, serverless smallest, UK South, synthetic data, deleted after); lifetime 8 hours in total with cleanup inside the window; the operations map to the repository's #358 secret-lifecycle script, the #117 rescan job and the #122 continuity/export path, but no exact commands or unit prices are recorded, so T3 is not approvable until the owner names the commands and records dated unit prices; the 15 USD figure is an owner-set cap placeholder, not a priced estimate; retention liabilities (vault soft-delete, immutable storage) outlive deletion and are counted against the cap until they expire. Transport design is referenced generically as the owner-selected private-transport design, with no dependence on unmerged work.
* T4 sizing (#137/#360): analysis from the evidence only, no allocation, 0.
* Monitoring: daily cost query for RG `ama` plus the subscription-scope figure the owner provides; recompute P each day; latency caveat so thresholds apply to projected month end, not just accrued.
* Hard gates: unrecorded U, an unapproved tranche, or a start after the tranche's latest start blocks it; at expiry no new work; cleanup completes before expiry or is listed as a liability.
* Cleanup and recreation: delete only tranche-created temporary resources; recreate with the named scripts and synthetic data; no private data.

#### Intent

A bounded first tranche with approval fields and honest checks.

#### Boundaries

* Included: T0-T4 tables.
* Excluded: executing anything; approving manifests.

#### Likely Targets

* docs/case_study_48_addendum.md.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Commands match existing scripts' documented usage; no IDs.

#### Completion Evidence

* Tranche tables present with all fields.

#### Unresolved Items

* Private bootstrap, tenant, roster, executor, quota, held-out manifest, legal/privacy terms.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Owner-testable now, blockers, cleanup and recreation

#### Context

Owner can test now only with real evidence: local synthetic run; read-only cost and resource views. Not available: Azure sign-in (sentinel invalid, deny-all 403 is by design). Known capacity failures (B2s, B2als_v2, D2as_v5, no ACR agent pools in UK South) are not retried. Existing liabilities: the recurring daily meters of F2 (94 resources, Premium registry, IoT B1, eight private endpoints, Front Door, SQL, two environments, three apps, eight jobs, Foundry account without deployments).

#### Intent

Make the blockers and liabilities explicit.

#### Boundaries

* Included: statements and gates.
* Excluded: issue acceptance.

#### Likely Targets

* docs/case_study_48_addendum.md.

#### Dependencies

* P01-T02.

#### Validation Expectations

* Every blocker traced to research C-IDs.

#### Completion Evidence

* Blocker list present.

#### Unresolved Items

* None beyond owner-only.

<!-- rpi:phase id=P02 -->
## P02: Index, log, clarification and checks

### Context

Knowledge-base conventions require index and append-only log.

### Intent

Complete the knowledge-base record and verify.

### Boundaries

* Included: docs/reference/README.md row, docs/reference/log.md append, the recovery artifacts and state hold the clarification; the four pre-RPI draft files stay unchanged.
* Excluded: rewriting earlier log entries or the draft body.

### Likely Targets

* docs/reference/README.md, docs/reference/log.md.

### Dependencies

* P01.

### Validation Expectations

* git diff scope; link check; ID scan.

### Completion Evidence

* Changes record.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Index, log and ms.date

#### Context

See phase.

#### Intent

KB consistency and honest history.

#### Boundaries

* Included: edits listed above.
* Excluded: deleting, renaming or editing the draft files.

#### Likely Targets

* as above.

#### Dependencies

* P01.

#### Validation Expectations

* Log entry appended at end only.

#### Completion Evidence

* Diff.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Focused checks

#### Context

No documentation build; use link review, diff, ID scan, arithmetic script.

#### Intent

Evidence for the review.

#### Boundaries

* Included: local read-only checks.
* Excluded: the full gate (run after commit).

#### Likely Targets

* changed files.

#### Dependencies

* P02-T01.

#### Validation Expectations

* All checks pass.

#### Completion Evidence

* Outputs in the changes record.

#### Unresolved Items

* None.
