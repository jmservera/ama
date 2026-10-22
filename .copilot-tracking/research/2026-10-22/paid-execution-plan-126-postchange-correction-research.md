<!-- markdownlint-disable-file -->

# Task Research: paid-execution-plan-126-postchange-correction

| Field | Value |
|-------|-------|
| Date | 2026-10-22 |
| Researcher / agent | rpi-research skill, inline by the RPI Agent parent (no worker) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-22/paid-execution-plan-126-postchange-correction-research.md |

## Research Brief

* What to research: whether the addendum's 535.33 forecast and S0 baseline can still be called current after the owner-authorized deletion of the cutover-test Front Door Premium profile and WAF policy and the scale-down of the cutover-test demo API app, and what the correct wording is.
* Why it matters: independent review verdict NEEDS CHANGES (addendum lines 364-374 call a pre-change forecast "current").
* Scope: the 2026-10-22 subsection and related wording in docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/log.md; read-only Azure inventory and cost.
* Non-goals: any Azure or tenant mutation, inference, deployment, invented savings, new spend authority, scope expansion.
* Criteria: observed kept; 535.33 and derived limits labelled a conservative PRE-CHANGE scenario; no invented savings or zero residuals; refreshed post-change forecast required before any tranche; outside-RG spend unknown; paid execution blocked.
* Output mode: convergence.

## Research Parameters

| Field | Value |
|-------|-------|
| Research posture | focused (default; bounded correction with named sources) |
| Explicit limits | USD 700 total forecast ceiling; expiry 2026-10-25T16:02Z unchanged |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
|------|-----------|-------------|
| Instruction | AMA repository instructions (applyTo `**`) | selected |
| Skills and specialists | design skills, finance specialist | skipped: documentation-only, figures are Azure facts |

## User Participation and Research Decisions

No interaction (non-interactive run). Active controls: owner decisions of 2026-10-22 unchanged; the coordinator reports deletion and scale-down completed and independently verified at 14:16Z (taken as caller-supplied evidence, corroborated by W1).

## Evidence Log

### Codebase evidence (C#)

* C1: docs/case_study_48_addendum.md, subsection "Finite Costed Execution Plan Options ..." lines 364-374 (the evidence table and "S0 (no change) is the only current baseline" sentence) and the envelope paragraph after it; the "no change" wording, "Current evidence" label, B1 admissible-U list and the history block.
* C2: docs/reference/README.md index row for the subsection and the 2026-10-22 entry in docs/reference/log.md both describe 535.33 as the forecast with no change.
* C3: prior artifacts .copilot-tracking/*/2026-10-22/paid-execution-plan-126-demo-budget-700-* are preserved unchanged as history.

### Live evidence (W#), 2026-10-22 about 14:53Z, read-only

* W1: inventory of resource group `ama`: 91 resources (94 at 13:57Z); no Front Door profile or Front Door WAF policy remain; the cutover-test demo API app has minimum replicas 0 and 0 running replicas; 61 resource names still contain "cutover-test" (other cutover-test resources, such as environments, jobs and endpoints, remain and may still accrue charges).
* W2: Cost Management actual cost, resource group `ama`, daily: identical to the 14:00Z read (242.36 accrued 11-22 Oct; 22 Oct partial 9.43; 17-21 Oct daily 29.69, 30.26, 30.22, 30.22, 30.25). Cost data lags, so no post-change meter evidence exists yet.
* W3: subscription scope still unreadable (authorization denial at 14:00Z; not retried to avoid throttling).

## Waves

* Wider: possible effects of deletion (Front Door base fee, WAF policy, managed private link, app replicas) and of other remaining cutover-test resources; alternatives for the forecast (pre-change, rate-reduced, measured).
* Deeper: the earlier research attributed about 10.64 per day to the Front Door Premium base fee, but that was the fee for the then-existing profile and it is not established that it was the same deleted profile, nor what the app's replica meters contributed; so any saving is unmeasured. Deleted resources can leave residual charges (billing lag, soft-delete, private endpoint or link remnants), so zero residual is not assumed.
* Contrarian: using the 10.64 per day would invent a saving; assuming full removal of all cutover-test cost is unsupported (61 related names remain); keeping 535.33 as "current" misleads because the state it forecasts no longer exists; yet dropping it would hide the worst case. Resolution: keep 535.33 as an explicitly labelled conservative pre-change scenario, which is an upper-bound style figure only if no new cost was added, and require a refreshed forecast.

## Parent Synthesis

Accepted: observed 242.36 remains observed accrued; 535.33, 164.67 headroom and U limits (89.67, 84.67, 74.67, 66.67) become the PRE-CHANGE scenario; no post-change forecast is stated; a refreshed post-change forecast from measured complete post-change days (and a fresh inventory) is required before any tranche activation; reserve, thresholds and 655 cap are unchanged rules. Rejected: inventing a saving or a zero residual. Deferred: measuring actual savings (needs at least one complete post-change day of cost data). No further cycle: remaining gaps need time and access.

## Disposition and Readiness

* Research disposition: executed.
* Planning Readiness: Ready for documentation-only plan; blocked for any paid execution.

## Next Steps

Active parent runs rpi-plan.
