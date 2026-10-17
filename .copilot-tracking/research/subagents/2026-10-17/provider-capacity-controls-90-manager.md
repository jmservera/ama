# #90 — procurement manager domain review, cycle 1

Date: 2026-10-17. Reviewed repository HEAD:
`adedf1f232e567d3a22a623d9c871513fa6b7cdc`.
Research-only independent domain lane; no operational approval, application
change, permission change, supplier contact or external research. No agents run.
All paths below are repository-relative; citations use `path:line`.

## Evidence and exact requirement boundary

- **Case-study fact:** 60,000 homes, spreadsheet-led coordination by a small
  team, contractor procurement and resident consent are in the original
  challenge; the original does not establish actual contracts or delegations
  (`docs/case_study_48_original.md:15-25`).
- **Case-study fact — exercise authority only:** role agents are research
  instruments, not company approvers; the historical baseline is not legal
  sign-off or live-use approval
  (`docs/case_study_48_addendum.md:68-87`). EXA-007 supplies a fictional
  existing contract/call-off and crew, not verified supplier capacity
  (`docs/case_study_48_addendum.md:121`).
- **Owner-confirmed company fact:** not-for-profit status is confirmed; legal
  form, charitable status and group structure are not. Status cannot establish
  procurement applicability or a person's spending/instruction authority
  (`docs/reference/research/company/company-profile-research.md:23-44`).
- **Case-study fact — documented requirement, not acceptance:** exact current
  PRD **FR-016** requires a *versioned provider-package record* with
  period/scope, contract/call-off, offered/committed evidence, issuer/version
  and provider submission/exception references. FR-008 controls gates,
  FR-009 returns, FR-022 chronology
  (`docs/prds/zava-forward-retrofit-programme-demonstrator.md:843-851`).
  AC-019 requires visible confirmed capacity, authorised issuer, schedule and
  evidence requirements, with drafts marked “not an instruction”; AC-039
  expressly says readiness is not instruction, booking, commitment, acceptance
  or payment. Both are recorded **Not run**
  (`docs/prds/zava-forward-retrofit-programme-demonstrator.md:1465`,
  `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1485`).
- **Case-study fact — documented business controls:** **RULE-007** requires
  contractual commitment for package, location, volume and period; forecasts
  and supplier self-declarations alone cannot unlock scheduling.
  **RULE-008** reserves instructions, variations, scope changes, commitments,
  suspension and reallocation to a named authorised contract manager, recording
  approver, delegation, contract, version and time; reallocation needs a
  modification check and Legal review where required
  (`docs/brds/agentic-retrofit-programme-brd.md:1436-1440`).

Index routing used: company/sector and requirement routes, plus the indexed
agent challenge/what-if evidence
(`docs/reference/README.md:77-79`, `docs/reference/README.md:99`,
`docs/reference/README.md:123-124`). **Sector-informed hypothesis:** suppliers
can offer capacity by email/spreadsheet; a named manager must accept it before
slot suggestions. An app/API is neither necessary nor contractual authority
(`docs/reference/research/company/agent-what-if-study.md:1204-1217`).

## Existing exercise implementation — not proof of business approval

**Case-study fact — repository observation:** `_need_manager` accepts broad
`MANAGER_ROLES` (Programme Manager **and Programme Support Officer**), while
issuer/history fields record a staff name. This is not a contract-specific
delegation check
(`src/core/src/zava_forward/core/workflows.py:13`,
`src/core/src/zava_forward/core/procurement.py:49-51`,
`src/core/src/zava_forward/core/procurement.py:149-160`).
Capacity is numeric offered/committed with a nonempty plain evidence string;
scope can change independently. Issue checks package end and available counts,
not structured evidence authority, source validity, location or units
(`src/core/src/zava_forward/core/procurement.py:93-144`).
Completed orders remain counted; withdrawal removes them from counted states;
correction can return completed work to Issued
(`src/core/src/zava_forward/core/procurement.py:19-21`,
`src/core/src/zava_forward/core/procurement.py:71-72`,
`src/core/src/zava_forward/core/procurement.py:209-233`).

## Explicit exercise recommendation

All recommendations below are **Sector-informed hypotheses — proposed exercise
contracts, not adopted policy or real contractual/legal approval**.

1. **Named authorised issuer contract.** Require a stable authenticated
   staff ID plus display name, a versioned delegation reference, granting
   authority, named contract/call-off and supplier IDs, permitted action types,
   package/location/scope limits, financial/time limits where applicable,
   effective-from/to, revocation status and decision time. The actor must match
   the named current delegation at the consequential action, not merely have
   a manager role or appear in the staff roster. Missing limits or delegation
   remain unknown and block that action. Recording an offer is distinct from
   accepting commitment or issuing work. Preserve separate technical, Finance,
   resident and independent QA decisions; a contract-manager action cannot
   satisfy those gates. For a positive exercise, propose an explicitly
   fictional named issuer/delegation fixture for owner acceptance; this report
   appoints nobody. Basis: RULE-008 and company decision boundaries
   (`docs/brds/agentic-retrofit-programme-brd.md:1440`;
   `docs/reference/research/company/company-profile-research.md:288-299`).

2. **Acceptable evidence.** A controlled, retrievable version of the fictional
   executed contract/call-off plus a supplier commitment accepted by the
   exercise's named delegated manager; link the resource allocation and
   competence/material/mobilisation/subcontractor/QA/client-side evidence.
   An email or spreadsheet can carry that evidence if the contract permits,
   but “supplier says yes”, a resource plan alone, a URL, uploaded file or
   typed “approved” string is not acceptance. Record source ID, version/hash,
   locator, issuer, issue date, received date, applicable/effective interval,
   review date and accepting person/action/reason. Hashes identify bytes;
   they do not prove signature, competence or contractual enforceability.
   Basis: BRD FR-019 and channel-neutral data schedule
   (`docs/brds/agentic-retrofit-programme-brd.md:1437`,
   `docs/brds/agentic-retrofit-programme-brd.md:1441`).

3. **Meaningful units, dates, location and scope binding.** For the bounded
   count-based exercise, explicitly define one unit as **one home work-order
   allocation for the exact measure/scope version, consumed against a total
   package-period quota**. Do not call it crews, crew-days, simultaneous slots
   or homes/week. Those need duration, skills and time-bucket conversion
   evidence and separate shared-resource controls. Bind each commitment and
   reservation to supplier, contract/call-off version, package/scope version,
   named home/building IDs or a controlled location set/version, quantity/unit
   and delivery interval. A postcode or free-text scope alone is insufficient.
   Check scheduled delivery against both package and evidence validity;
   distinguish future-effective evidence from an invalid future issue/as-of
   date. Keep source issue, recorded, reviewed and delivery dates separate.
   The seven-day capacity freshness trigger is an internal **exercise**
   review trigger, not a legal expiry or proof that a recent document is
   sufficient (`docs/case_study_48_addendum.md:120`).

4. **Fail closed without falsifying losses or lifecycle history.** Missing,
   stale, conflicting, unverifiable or mismatched mandatory evidence means
   **Unknown — commitment not established**, with reason, reviewer and next
   action; zero means a known zero, not a missing value. No confirmed
   scheduling, instruction or award follows. A scope/source/delegation change
   invalidates dependent readiness before issue/reissue/booking/correction.
   Record actual capacity reductions even below existing obligations; show the
   deficit, block additional allocation and require manager-led recovery,
   resident updates and contingency review. Do not reject the loss and leave
   old capacity apparently available. Completion is not QA acceptance or
   replenishment; withdrawal/reopening cannot silently recycle quota.
   Preserve reservations, releases, superseded versions and reasons.
   Basis: RULE-007, BRD FR-020, PRD FR-017/AC-039
   (`docs/brds/agentic-retrofit-programme-brd.md:1436-1438`;
   `docs/prds/zava-forward-retrofit-programme-demonstrator.md:852`,
   `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1485`).

5. **No AI instruction/award; contractors read only their own.** AI may
   extract or draft sourced proposals, always marked “not an instruction”;
   it cannot accept capacity, approve its own draft or send a scope/cost/time/
   allocation-changing message. Preserve own-supplier work-order filtering
   and minimum necessary adjustment instructions, never diagnoses. Do not
   broaden contractor write rights. Verify package/capacity reads as well as
   work-order reads: `list_packages` builds all supplier rows, unlike filtered
   `list_work_orders`; the API exposes both paths. This is a scoped acceptance
   concern, not a claim of an executed cross-contractor access test
   (`src/core/src/zava_forward/core/procurement.py:243-278`;
   `src/api/src/zava_forward/api/server.py:383-386`;
   `docs/case_study_48_addendum.md:119`).

## What MUST remain unknown

**Unknown company detail:** actual contracts/frameworks/call-offs, valid
signatures and permitted channels, expiry/variation clauses, named authorised
issuers and deputies, delegation limits, real capacity/competence/TrustMark
status, competing commitments, geography, resource productivity and
mobilisation dates. Do not derive any from a seeded person, contractor name,
numeric capacity, model output or this role review. The company delivery
model itself remains unconfirmed
(`docs/reference/research/company/company-profile-research.md:251-259`).

**Unknown company detail:** exact legal/group structure, Procurement Act
applicability, current thresholds, route selection and modification rules,
payment-notice and leaseholder-consultation applicability need current
qualified procurement/Legal/Finance review. OD-30 remains the explicit gap;
no new legal currentness claim is made here
(`docs/brds/agentic-retrofit-programme-brd.md:1830`).

**Exercise disposition:** recommend the above bounded specification for owner
consideration, not acceptance of present controls. Positive/negative authority,
evidence-version, unit/location/date mismatch, capacity-loss, lifecycle and
own-contractor tests remain **Not run in this lane**. No operational approval,
real supplier commitment, award, resident booking or passing AC is established.
