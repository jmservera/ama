<!-- markdownlint-disable-file -->

# Task Research: paid-execution-plan-126-demo-budget-700

| Field | Value |
|-------|-------|
| Date | 2026-10-22 |
| Researcher / agent | rpi-research skill, run inline by the RPI Agent parent (no worker dispatched) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-22/paid-execution-plan-126-demo-budget-700-research.md |

## Research Brief

* What to research: current read-only Azure cost and inventory evidence for the October demo budget, and the smallest finite private-Blob demo options under the owner's revised ceiling.
* Why it matters: the owner decision of 2026-10-22 ("spend approved", then "limit to $700 forecast") replaces the earlier USD 500 total. The costed execution-plan synthesis must carry the new ceiling without letting the old figure pass as current.
* Audience or intended use: the planning phase of this loop and the independent reviewer.
* Scope: the costed-plan subsection of `docs/case_study_48_addendum.md`, the `docs/reference/README.md` index row, `docs/reference/log.md`, existing #126 artifacts, and read-only Azure Cost Management and inventory using the existing signed-in session.
* Non-goals: any paid execution, deployment, job start, resource creation or retirement, role or permission change, tags carrying results, real personal data, human pilot capture. Front Door or other resource retirement is not authorized.
* Criteria: aggregate-only non-sensitive evidence; observed distinct from forecast; unknown liabilities not assumed zero; finite incremental estimate, forecast ceiling and stop thresholds; historical USD 500 preserved as dated history.
* Requested outputs: research artifact with planning readiness.
* Output mode: convergence (revised options for owner approval; nothing is approved here).

## Research Parameters

| Field | Value |
|-------|-------|
| Research question(s) | Q1 What is observed and forecast October spend now, and what is unknown? Q2 Which smallest finite private-Blob demo options fit USD 700? Q3 Which gates and stop thresholds apply? |
| Codebase scope | addendum, reference index and log, #126 tracking artifacts |
| External scope | Azure Cost Management query API (read-only), Azure public retail prices API |
| Research posture | focused |
| Posture provenance | default; bounded internal task with named sources |
| Explicit limits / deadline | USD 700 all-in October forecast ceiling; authorization expiry 2026-10-25T16:02Z, no extension |
| Edits allowed during research? | no, research-only (this evidence file is the only write) |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Authority | Disposition |
|------|-----------|----------------------|-----------|-------------|
| Instruction | AMA repository instructions | applyTo `**` | knowledge base, regulatory-evidence and branch rules | selected |
| Skill | web-design and design skills | web guidance | none: documentation-only task | skipped |
| Specialist | Housing Finance and Grants Lead | cost framing | not needed: the figures are Azure facts | skipped |

## User Participation and Research Decisions

No interactive intake: the owner decisions are supplied verbatim in the task and this run is non-interactive. Active controls: USD 700 replaces 500 as the all-in forecast ceiling (not 700 additional); expiry 2026-10-25T16:02Z unchanged; private Blob with managed identity; no tags carrying results; private services stay private; no retirement, resource-group deletion, identity or role change; screen-reader acceptance and signed source/image attestation may be recorded as unverified production follow-ups; no real personal data.

## Evidence Log

### Codebase evidence (C#)

* C1: existing costed subsection, gating rules, tranche table and thresholds (USD 500 basis; 400/450/475; R 30) in `docs/case_study_48_addendum.md`, heading "Finite Costed Execution Plan Options for an Unfinished Azure Demo (2026-10-20, #126)".
* C2: index row for the subsection in `docs/reference/README.md`; log entries dated 2026-10-20 at the end of `docs/reference/log.md`.
* C3: prior state record `.copilot-tracking/rpi-sessions/2026-10-20/paid-execution-plan-126-recovery-state.json` (task Follow-up, completed); preserved unchanged.

### External and live evidence (W#), retrieved 2026-10-22

* W1: Azure Cost Management query, `ActualCost`, USD, daily, scope resource group `ama` only, read-only, about 13:57Z to 14:00Z. Rows exist from 2026-10-11 to 2026-10-22 (12 days).
* W2: same API at subscription scope: `RBACAccessDenied` (after earlier 429 throttling). Subscription-scope and other-resource-group spend remain unreadable.
* W3: Azure public retail prices API, Storage, UK South, Hot LRS, about 14:00Z: block-blob data stored up to 0.0192 per GB-month, write operations 0.059 per 10,000, read and other operations 0.0047 per 10,000, index tags 0.0376 per 10,000 per month. List prices, not agreement prices.
* W4: read-only inventory of resource group `ama`: 94 resources (unchanged from 2026-10-20); one storage account, Standard LRS, public network access disabled, shared-key access disabled, blob public access disabled, minimum TLS 1.2; eight private endpoints including one for blob.

Aggregates from W1 (USD, estimates until invoiced, exclude credits, can lag):

| Item | Value |
|------|-------|
| Observed accrued 11-22 Oct (22 Oct partial to about 14:00Z) | 242.36 |
| Of which 22 Oct partial | 9.43 |
| Complete days 11-21 Oct | 232.93 |
| Daily 17-21 Oct | 29.69, 30.26, 30.22, 30.22, 30.25 |
| Run rate used (18-21 Oct, four complete days) | 30.24 |
| Forecast, no change: 232.93 + 10 days (22-31 Oct) x 30.24 | 535.33 |

Reconciliation: complete days 11-19 Oct sum to 172.46 against 172.47 recorded on 2026-10-20, so the reads overlap and must not be added. The 2026-10-20 figure of 189.94 included a partial 20 October. No spend appears before 11 October in this scope.

## Wave 1: Wider

Cost scopes exist at resource group, subscription and billing level; only resource group is readable (W2). An existing private-link storage account already has a blob private endpoint (W4), so a container needs no new billable resource type. Alternatives for a result store: new storage account, SQL table, Table or Queue storage. Possible out-of-scope costs (unknown): other resource groups, marketplace, support, reservations, tax, credits.

## Wave 2: Deeper

Prioritised: the existing storage account route. A Blob data-plane write needs an existing managed-identity role assignment, which this loop cannot verify further or grant (no role changes authorized). Meters: capacity and operations (W3); private-link data processing has no numeric rate retrieved and is carried in the allowance; retention features (soft delete, versioning) are not read, and retained bytes count against the cap until they expire. 1 GB, 100,000 writes and 1,000,000 other operations cost about 0.02 + 0.59 + 0.47 = 1.08 at list price; with unknown meters an owner-approvable ceiling of USD 5 is proposed.

## Wave 3: Contrarian

* A new storage account adds retention and endpoint liabilities with no benefit; rejected.
* Reading 700 as "700 additional" would let the forecast reach about 1,235; rejected on the owner wording.
* Treating 535 as the whole month would hide U; rejected because subscription scope is unreadable.
* A forecast ceiling is not authority to spend up to it; the reserve and thresholds still apply.
* The run rate is observed, not guaranteed (it moved from about 15 to about 30 in October); the live projection refreshes daily.
* Tags carrying results would leak data through billing and are excluded by owner decision.
* Front Door retirement would save about 10.64 per day but is not authorized, so it is not an option here.

## Parent Synthesis

Accepted: USD 700 as replacement all-in October forecast ceiling; expiry unchanged; private Blob on the existing account as the smallest result store; finite tranches B1 (ceiling 5) plus the earlier T1 (8) and T2 (10) as optional bounded additions; T3 stays not approvable. Thresholds keep the same 80, 90 and 95 percent shape on 700 (560, 630, 665); envelope cap E at most 655 so the starting live projection (E less R) stays at most 625, below the 630 pause line. Rejected: retirement options, a new storage account, tags. Deferred: U, role-assignment verification, private-link data meter, retention settings, agreement prices.

Envelope arithmetic with R = 30 and RG `ama` at no change: U plus approved ceilings must be at most 655 - 535.33 - 30 = 89.67. Maximum admissible U: B1 alone 84.67; B1 + T2 74.67; B1 + T1 + T2 66.67; B1 + T1 + T2 + T3 (15) 51.67 but T3 remains not approvable. These are limits on U, not assumed values.

No further cycle: the bounded question is saturated and the open gaps need owner access, not more research.

## Decisions, Unresolved Items and Risks

* Blocking any paid tranche: U is unknown; Cost Management read access above resource-group scope is missing (`RBACAccessDenied`); the managed-identity Blob role assignment is unverified and cannot be granted here; private-link data and retention meters are unpriced; model quota Unknown; held-out manifest, human, legal and privacy gates; owner approval of any option.
* Unverified production follow-ups, not passed: screen-reader acceptance; independent signed source/image attestation. Demo evidence is not production acceptance.
* Risk: burn of about 30 per day consumes the headroom if unchanged; expiry falls on a Sunday.

## Research Disposition and Planning Readiness

* Research disposition: executed (focused posture, one complete three-wave cycle, inline).
* Planning Readiness: Ready for a documentation-only plan. Blocked for any paid execution.

## Next Steps

Active parent runs rpi-plan.
