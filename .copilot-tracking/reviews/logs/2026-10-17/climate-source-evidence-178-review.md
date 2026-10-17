<!-- markdownlint-disable-file -->
# Review: climate-source-evidence-178

## Scope and Evidence

* Task ID 178; date 2026-10-17; one post-implementation Review.
* Boundary: full bounded P01-P03 evidence delivery and all three original
  issue criteria, including explicit residual access/approval/paired-data gaps.
* Plan: .copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md
* Details: .copilot-tracking/details/2026-10-17/climate-source-evidence-178-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/climate-source-evidence-178-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/climate-source-evidence-178-changes.md
* Research: .copilot-tracking/research/2026-10-17/climate-source-evidence-178-research.md
* Other evidence: source diff, helper/tests, actual JSON, validation outputs,
  canonical case-study/index/memory and #178/#367 context.

## Opening Review State

Goal: assess genuine progress without presenting monthly temperature evidence
as paired historical replay bounds or licence metadata as owner approval.
All P01-P03 markers are complete and validation evidence available.
Acceptance basis: caller's source/access/privacy/delivery limits, original
criteria and planner's bounded implementation contract.
First comparison: source identities/statistics/quality against research and
original criteria; then critique dispositions, test coverage and scope.
Read-only boundary: write only this review; no fixes or other phase changes.
Initial blockers: owner reuse approval UNMET; CEDA login blocks humidity;
these block original issue acceptance, not review execution.

## Execution Status

**Complete.** One Review executed inline on 2026-10-17 against the complete
supplied boundary. No review agents needed; no second Review or closure cycle.

## Plan-to-Change Reconciliation

| Scope | Evidence | Reconciliation |
| --- | --- | --- |
| P01/P01-T01 | Local-only helper, synthetic tests, exact actual-file JSON | Complete; input SHA guard, explicit 360-calendar/351-valid distinction, no RH |
| P02/P02-T01 | Existing synthesis/register, index/log/core README diff | Complete; official comparison and exact regional UUID/citation with access/approval limitations |
| P03/P03-T01 | Changes validation table and details completion evidence | Complete; all markers checked with executable/diff evidence, no active implementation remaining |
| Follow-Up Items | Human reuse/access and paired record/method work | Open, correctly outside bounded scope and mirrored in changes |

## Completed Work Assessment

The helper and test module were read in full. Parsing validates schema/units,
month IDs, duplicate months, finite temperatures and input hash. Quality
categories reconcile per variable; midpoints use same-row accepted values.
Empty series explicitly returns unavailable/null, while zero selected rows
errors. Exact report extrema and tied occurrences agree with independently
calculated Decimal results. The report and synthesis consistently identify
monthly aggregates, not physical or replay limits.

The seven source-family comparison is materially different from #367's
all-unknown table. It distinguishes OGL grants, CEDA authentication, CC BY,
CIBSE purchase/user licensing and incomplete exact terms. The HadUK regional
recommendation is exactly W3/W4, not W2's grid citation. Durham is a separate
retrieved temperature-only cross-check, not a replacement paired source.
Current CEDA versus generic Met Office daily-temperature metadata conflict
is surfaced explicitly, not silently resolved into invented daily humidity.

All changed canonical files were read/reviewed against the recorded official
retrieval results and limits. No raw dataset or copied full provider page is
part of the repository change. No private, runtime, generator, infra or
immutable snapshot changes. No live platform acceptance is claimed.

## Implementation-Time Plan and Detail Update Assessment

P02's addition of the directly coupled core README paragraph is justified:
the old no-retrieval statement became stale. Scope/details/current plan were
updated without changing owner intent or expanding code behavior. Explicit
source URL input prevents fixed-Durham provenance for another station.
Both are compatible local updates, not significant/divergent decisions.

## Critique and Material Revision Assessment

PC-001 resolved by readable 92,268-byte local input, exact locator/hash/invocation
and required CLI hash guard. PC-002 resolved by separate calendar/usable counts,
exclusive categories, same-row pairing, empty semantics and synthetic tests.
PC-003 resolved by regional UUID/citation/access lock; 1km alternative remains
distinct. One critique executed; its Revise verdict was not relabelled Pass.
Planner dispositions and implementation agree. No unsupported human decision,
early dependent-work resumption or second critique found.

## Plan Follow-Up Assessment

| Follow-up | Why outside bounded implementation | Owner / route |
| --- | --- | --- |
| Reuse and automated-access review | Agent may document terms, not approve or create accounts | Juan Manuel Servera; distinct human action, RV-002 |
| Paired RH/T records and representative cadence/geography | Actual hurs request login-blocked, station monthly file has no RH | Authorized evidence provision, then later rpi-research, RV-001 |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Paired historical replay bounds remain unevidenced

* Evidence: C178-HUK-ACCESS / W4 returns login HTML; C178-DUR / JSON humidity
  unavailable. 351 monthly T pairs are not three-per-day T/RH observations.
* Impact: original third criterion and paired-source adoption cannot be accepted.
  This is a disclosed material evidence gap, not an implementation defect.
* Destination: later rpi-research, after authorized record packet/access.
* Smallest next action: supply exact product/station/variable/QC/period records
  without inferring account or terms authority, then assess appropriate geography
  and cadence. No synthetic replacement or humidity inference.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Owner reuse/access review is still UNMET

* Evidence: original caller/issue boundary; source register explicitly UNMET.
  CEDA open licence does not remove login; Met Office terms include an
  automated-copy condition. No approval or terms acceptance was recorded.
* Impact: original second criterion does not become owner-approved adoption.
* Destination: distinct human follow-up to Juan Manuel Servera, not an agent
  implementation or legal sign-off.
* Smallest next action: review exact HadUK and Durham terms/access/attribution
  and explicitly record approval, rejection or deferral before adoption.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Exact alternative terms/site coverage remain partial

* Evidence: comparison/register explicitly lacks CIBSE redistribution permission,
  exact selected zone, MIDAS release acknowledgement and station/QC coverage.
* Impact: comparison is substantive but not complete verification of every
  candidate's eventual reuse/representativeness; original first criterion
  must not be silently marked fully met.
* Destination: later rpi-research, limited to owner-retained candidate(s).
* Smallest next action: obtain public/provider terms and representative site
  metadata if still decision-relevant; no purchase/login or broader replacement
  is authorized by this finding.

## Defects

No substantive implementation defect identified in the assessed boundary.
This is not a security audit, legal opinion or blanket correctness guarantee.

## Routed Findings and Residual Work

| Finding | Destination | Owner / smallest action |
| --- | --- | --- |
| RV-001 | rpi-research later | Authorized paired historical packet, cadence/geography/QC assessment |
| RV-002 | Distinct human follow-up | Owner dataset-specific reuse/access decision |
| RV-003 | rpi-research later | Remaining exact alternative terms/site evidence, if relevant |

No active plan tasks reopened. No subsequent child task selected or started.
Delivery commit/push/PR remains with the RPI parent, per explicit caller direction.
Later implementation of routed work does not require repeating this Review.

## Validation Evidence

| Check | Status / scope |
| --- | --- |
| Focused unittest discovery | PASS: eight methods, tiny wholly synthetic fixtures and CLI success/error |
| Actual public file analysis | PASS: hash-guarded 1991-2020 output; 360 months, 351 valid pairs |
| Independent Decimal and occurrence/count checks | PASS: all extrema/months/source lines, nine estimated exclusions |
| Byte-for-byte helper replay / report hash | PASS: f75566fc1bf62608a78cf7f12647779dab12f0d0cddf86f6f1a7083df6f95615 |
| Compileall, git diff --check | PASS |
| Changed local links and immutable/append-only boundaries | PASS: six added targets/anchors; old log prefix preserved |
| Review import/count audit | PASS: no helper network/app imports; count equations and UNMET/unavailable fields agree |
| Initial all-history link scan | FAILED on pre-existing retired mvp anchor; disclosed and excluded from changed-link result, not fixed |
| Ruff/mypy/full app/live-platform | Not run: tooling not present/no tools-wide target, no app runtime change or platform authorization |
| PR/CI checks | Not yet available at review time; no CI pass claim |

## Outcome

* Execution: **Complete**.
* Outcome: **Residual work** for this full task boundary; original #178
  **Not accepted** as complete. No conformant overall issue outcome claimed.
* Bounded contribution is reviewable: comparison, exact conditional source/terms
  and actual temperature statistics are delivered with material limitations.
* Approval, humidity and remaining exact candidate terms/site evidence stay open.

## Closeout Routing Record

| Class | Destination |
| --- | --- |
| Implementation defect | None identified |
| Significant/divergent decision gap | None; existing owner instructions preserved |
| Material evidence gap | RV-001/RV-003 to later rpi-research |
| Human residual action | RV-002 to owner; no inferred approval |

Return this one completed Review to the active RPI parent for authorized
commit/push/PR delivery, then stop. Do not return to Implement or run Review again.
