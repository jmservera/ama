<!-- markdownlint-disable-file -->

# Task Research: issue126-cost-refresh

| Field | Value |
| --- | --- |
| Date | 2026-10-23 |
| Researcher / agent | RPI Agent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-23/issue126-cost-refresh-research.md |

## Research Brief

* What to research: current October Azure actual/forecast scope, reporting lag,
  USD 700 all-in headroom and smallest finite development demo dependencies.
* Why it matters: support a separately authorized owner-testable demo without
  confusing development spend with issue #126 acceptance.
* Audience: owner and independent delivery coordinator.
* Scope: this worktree, existing cost synthesis/proposal, infra/source guides,
  issue #126 and read-only Azure management/cost APIs.
* Non-goals: Azure mutation, paid inference, private data, pilot/production
  approval, broad application parity and issue closure.
* Criteria: dated sanitized evidence, scope/currency completeness, no invented
  headroom or price and no activation under this brief.
* Requested outputs: research, plan/details, changes, one Review and conditional
  draft publication after the exact-head local gate.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Can the current all-in forecast be compared with USD 700; what is the smallest dependency-ready demo? |
| Codebase scope | docs/, infra/README.md, src/README.md and relevant setup contracts |
| External scope | GitHub issue #126, Azure management/cost APIs, official Microsoft cost documentation |
| Initial internal candidate areas | Existing addendum finite paid proposal, KB index/log, infra runbook |
| Initial external candidate areas | Cost Management Query/Forecast, subscription/resource inventory |
| Research posture | focused |
| Posture provenance | Caller-bounded continuation |
| Explicit limits / deadline | USD 700 replacement October ceiling through 2026-10-25T16:02Z; no paid execution |
| Completion basis | Material questions evidenced or smallest missing permission/source named |
| Edits allowed during research? | Research and required workflow state only |
| Resolved evidence root | .copilot-tracking/research/ |
| Excluded sources | Secret values, personal roster, SQL/data-plane/private datasets |

## Extension Registry and Provenance

| Kind | Candidate | Provenance | Disposition |
| --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Repository-wide guidance supplied at intake | Selected; source placement, privacy and publication gate |
| Skill | rpi-research | Active phase contract | Selected; ordered wider/deeper/contrarian cycle |
| Skill | rpi-plan, rpi-implement, rpi-review | Explicit caller full-loop request | Selected for later phases only |
| Specialist | Research/Finance role agents | Available host agents | Skipped; tightly coupled evidence can be investigated directly |
| Skill | Web design/accessibility | No web code change | Skipped; no UI audit or conformance claim |

## User Participation and Research Decisions

Caller explicitly requests the full ordered loop and bounded publication; this
is automatic task execution, not a new automatic-session offer. Stop after this
task's publication or explicit blocker. No clarification needed at intake.

## Scope and Success Criteria

Verify current costs without assuming resource-group completeness. Preserve
historical USD 500 and pre-deletion figures. Leave OD-51 open and distinguish
public welcome from signed-in feedback.

## Task Research Requests

The user brief is authoritative for read-only boundaries, expiry, spending
ceiling and publication. A missing cost source blocks activation, not a truthful
documentation update.

## Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Only this worktree/branch | Caller | No other checkout or active gate modified |
| No Azure mutation or paid/data-plane calls | Caller | Management/cost reads only |
| No subtraction of deleted Front Door/WAF accrued charges | Caller | Historical actuals remain included |
| No pilot/legal/production acceptance inferred | Caller and #126 | Acceptance criteria remain open |

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Current actual/forecast, lag, currency and subscription completeness? | depth | High | Open |
| Q2 | Responsibly comparable headroom against USD 700? | straightforward | High | Open |
| Q3 | Existing-resource-first finite welcome/sign-in/feedback/one-AI proposal? | depth | High | Open |

## Prior Knowledge Gate

Clean branch docs/demo-cost-headroom-126 starts at
140d8f494482c78e84d15f3d46b9223d3c487af0; no matching open PR.
Issue #126 fetched with gh and remains open with unchecked acceptance.
Original case study and memory read; index identifies the addendum as existing
cost evidence/proposal owner. Prior forecast is explicitly stale.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read the repository instructions, both case studies (original fully, addendum
relevant current and historical budget/build sections), KB index/memory,
housing-association primer, source guide, infra cost/rollback/auth runbooks
and issue body/comments. Existing evidence belongs in the addendum, not a new
cost page. One enabled/default subscription is visible to this CLI session.

Reflection: current management visibility cannot establish financial coverage;
subscription costs and forecast must be tested independently of RG actuals.

#### Wave 2: Deeper

At 10:55:44Z subscription actual query failed; at 10:55:49Z RG actual query
succeeded with 13 USD daily rows and no nextLink. Total 261.81680274594840;
through 22 October 259.70942112332707; partial 23 October 2.10738162262133.
Subscription forecast failed at 10:55:50Z. No retry of either failed cost
scope. Diagnostics were deliberately withheld to avoid identifiers; current
failure subtype/HTTP code is Unknown, not re-labelled as a verified 403.
Historical subscription authorization denial remains historical evidence.

Management inventory at 10:55:52Z: 91 visible resources, all in ama; eight
private endpoints, two environments, three apps, eight jobs, retained SQL,
storage, registry and AI account; no Front Door/WAF type returned. RG service
forecast at 10:56:24Z returns 195.527921874693124 future USD plus the same
2.10738162262133 partial actual. Conditional RG total = 261.81680274594840 +
195.527921874693124 = 457.344724620641524. This is service-model evidence,
not a measured complete-post-change-day run rate or an all-in forecast.

Reflection: actuals increased; prior 535.33 is historical, not current. Partial
23 October cannot satisfy the existing complete-post-change-day gate.
Cost metadata supplies no exact watermark. Official typical latency is
8-24h EA/MCA, up to 72h pay-as-you-go; agreement type is not established.

#### Wave 3: Contrarian

Challenged "all resources in ama means outside spend zero": official cost
guidance explicitly includes stopped/deleted resources and distinguishes ARM
visibility. Current inventory is not historical purchases, deleted resources,
support/tax, another subscription or external AI coverage. Reject U=0.
Challenged treating a service forecast as the required post-change proof:
23 October is still in progress, and modeled daily forecasts rise again on
27 October. No deletion saving or stable zero-rate assumption is justified.
Challenged broad-parity dependency: existing server independently serves
welcome and protected routes; public welcome needs no demonstrated full
workbench parity or photo-token-store provisioning. Signed-in feedback still
needs real tenant/SQL/bootstrap evidence and is not proved by a redirect.

Two app-inventory formatter attempts failed locally on null fields after
successful management reads; no secret/config values were emitted. Corrected
JMESPath projection succeeded: retained API minimum two, demo API minimum zero,
other app minimum zero; no running-replica claim. Initial gh comments command
used incompatible flags; corrected once successfully. Wrong inferred source
directories were corrected using glob before reading. These are tooling
corrections, not denied-cost retries.

Reflection: no further permitted query resolves inaccessible billing scope or
creates a complete post-change day now. Document the smallest export blocker,
keep activation blocked, and finish the bounded documentation loop.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Current RG actual USD 261.82 | W2 | Accepted | Sum unrounded daily values once |
| Conditional RG service total USD 457.34 | W3 | Accepted with limits | Actual/forecast statuses separated; not all-in or certified post-change |
| All-in headroom | W2-W5 | Deferred / Unknown | Subscription actual/forecast inaccessible and other liabilities unbounded |
| Existing-resource-first two-hour demo | C2-C4 | Accepted for planning only | Separate welcome from auth; one bounded AI task rather than broad evaluation |
| Deletion creates immediate savings or U=0 | W4-W5 | Rejected | Inventory and estimates do not establish financial completeness |

#### Cycle Re-entry Evaluation

No second cycle now: focused scope covered; the remaining material evidence
requires an owner export/access resolution or passage of time, not repeated
denied queries. Re-enter only with comparable bounded month-end costs and
complete post-change-day evidence.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | docs/reference/README.md:314 | Existing addendum owns finite cost proposal; 535.33 forecast is pre-change only |
| W1 | https://github.com/jmservera/ama/issues/126, retrieved 2026-10-23 | Pilot/RAI/Tokenomics criteria remain separate and unaccepted |
| C2 | docs/case_study_48_addendum.md:326-595 | Current USD700 proposal, historical USD500, U forecast definition and expiry |
| C3 | infra/README.md:732-765, 2659-2704 | Continuing baseline meters; optional photo provisioning is not welcome prerequisite |
| C4 | src/api/src/zava_forward/api/server.py:214-235; src/api/README.md:2265-2299 | Welcome and sign-in are separate routes; protected workbench needs real role/SQL binding |
| C5 | src/README.md:46-113; tools/rpi-checks.py:160-172 | Exact-head complete local gate required, even for docs; clean inputs and current base |
| W2 | https://management.azure.com/{scope}/providers/Microsoft.CostManagement/query?api-version=2025-03-01, retrieved 2026-10-23T10:55:44Z-10:55:49Z | Subscription failed; RG daily USD actuals succeeded for 1-23 October |
| W3 | https://management.azure.com/{scope}/providers/Microsoft.CostManagement/forecast?api-version=2025-03-01, retrieved 2026-10-23T10:55:50Z and 10:56:24Z | Subscription failed; RG forecast succeeded for 23-31 October with actual/future statuses |
| W4 | Azure CLI account list/show and resource list management reads, 2026-10-23T10:55Z | One enabled/default visible subscription; 91 visible resources all ama; not billing completeness |
| W5 | https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data, retrieved 2026-10-23 | Lag, estimates, deleted-resource charges and exclusions |
| W6 | https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2025-03-01 and https://learn.microsoft.com/en-us/rest/api/cost-management/forecast/usage?view=rest-cost-management-2025-03-01, retrieved 2026-10-23 | Official POST query contracts are read-only cost queries, scoped not universal |

## Alternatives and Decision State

Select a documentation-only refresh with no headroom number and no activation.
Reject restoring USD500, deducting deleted Front Door accrued charges, assuming
zero outside spend, or broad evaluation/new infrastructure as the minimum demo.
Keep one finite synthetic draft task and existing resources first; missing
current incremental effective rates remain Unknown, not covered by an allowance.

## Open Questions, Risks, and Residual Uncertainty

Smallest owner blocker: provide a sanitized USD October all-in actual and
bounded forecast export including outside-ama past/future liabilities, source,
timestamp, coverage and late-billing treatment; alternatively make the existing
principal's necessary cost reads available through the authorized administrator.
No role assignment is requested or performed here. If conversion is needed,
record approved dated conversion rather than guessing. Complete-post-change-day
meters, incremental prices, tenant/private executor and any task manifest
approval remain unmet. Public welcome and signed-in usability are not observed.
OD-51 denominator, quality floor and production economics remain open.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready for the bounded
documentation update and explicitly blocked execution proposal, not activation.
Self-check: all three waves ordered; internal/external sources cited;
uncertainty and negative results preserved; no source edits in Research.
