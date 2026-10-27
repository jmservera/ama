<!-- markdownlint-disable-file -->
# RPI Changes: Resident live acceptance

## Metadata

Date: 2026-10-27. Task ID: 462-resident-live-2026-10-27.
Slug: resident-live-acceptance. Declared scope: full plan.
Plan: .copilot-tracking/plans/2026-10-27/resident-live-acceptance-plan.md.
Details: .copilot-tracking/details/2026-10-27/resident-live-acceptance-phase-details.md.

## Execution Status

Owner10:37Z update supersedes the older execution direction below.
Current implementation: single packaged policy consumed by Bicep/runtime/helpers,
targeted tests, rebuilt immutable resident image, declarative ingress on through
2026-12-31T23:59:00Z. Existing authentication, SQL and model authority unchanged.
Original critique is retained; no repeat. Existing live URL was already200 at
resumption; this execution does not claim that pre-existing ingress mutation.

Implementation P01/P02 executed; P03 original Review/publication remains.
One independent final-candidate critique executed Complete, verdict Revise
preserved. PC001-PC005 disposed directly before cloud mutation. No second critique.

## Historical P01-T01 Admission Before Superseding Direction

Use existing tested revision/source/digest only. Actual live PORT8089 and Bicep
match (PC001). Owner's renewed USD700 cap is interpreted as continuing the
historical monthly ama ceiling through2026-12-31, consistent with #462's original
October ceiling and existing monthly budget metadata. This is explicit, not a
claim that cumulative October-December forecast fits USD700.
Official forecast and actuals will be retained and reconciled monthly before
activation, alongside one USD30 incremental allocation, not fresh authority.

## Current December Deployment Outcome

P01/P02 executed. Bicep helper dry run found4 resident-owned changes; apply
confirmed declaratively through2026-12-31T23:59Z, new ready revision0000003,
image sha256:fab6a85318f65db006bc610f3b3aff8ae799046d1b9a1813662b3b315c1b6fc7.
External ingress true, HTTPS-only8089, latest traffic100%, min0/max1.
URL https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io
returns200 and /healthz is ready. Old revision0000002 retired by Single mode.
No closure/watchdog. Cold starts after idle are expected.

29 post-deployment Playwright checks passed; six credential-dependent groups
are individually Blocked. Registered own-home/cases, gauges/history, assistant,
cross-resident sessions, actual top-right sign-out and natural1800s live expiry
are NOT accepted. Local API fixtures include real server-clock expiry, not a
live session. Final focused59 API selectors passed; an initial wrong import-path
selector failure remains externally retained, then corrected without source edits.

Protected safe projections compare equal for all three other apps, all eight
Manual jobs, SQL Standard/10 DTU and ACR policies. All four app minima0.
The image passed non-root/read-only/network-none packaged-cap/1000-map checks
and Trivy0.76 fixable HIGH/CRITICAL. ACR push temporarily used the previously
approved VM/32 route and restored public-disabled/export-disabled/None bypass
and exact network rules. No Key Vault value reads, SQL mutation or model calls.
The resident identity now has4 assignments: the3 existing template assignments
were created October26, plus an unrelated aoai-resident-469 role created
10:42Z by concurrent work. This task did not create/remove/use the latter.

Cost admission is the renewed ledger entry cost-ledger-renewed.json. The
historical ledger remains unchanged. USD5 feedback/release reservation sits in
the singleUSD30 allocation inside the recorded renewedUSD700 monthly cap;
illustrative66days x1activehour/day compute2.4948, continuous max59.8752 exceeds
the allowance and is NOT admitted. Daily owner monitoring/stop required; no
hard-cap or zero-cost claim.

B2 is material: both existing secrets expireOctober31 23:59Z and SQL admission
cannot outliveNovember1. The app's December cap does not extend either. Owner
must separately renew those authorizations for November; no secret or SQL
changes are inferred from the instruction to preserve them.

Issue462 criterion mapping: criterion8 (identity,URL,evidence,limits,resources,
expiry/stop and preservation) is proven for this partial delivery and may be
ticked after publication. Criteria1-7 remain open: composite engineering,
hosted/human/identity/canary/employee/live-positive gates are not fully proved.
No issue closure or production/accessibility acceptance.

Main moved from885ee05f to49c942b3 via docs-only PR439. Before original Review,
commit this implementation snapshot and integrate main with a history-preserving
merge to satisfy the gate's current-main ancestor contract. No rebasing, force
push or main write. Original critique remains unchanged after owner supersession.

## Current Blockers and Remaining Work

B1 remains: owner-held shared credential is unavailable under no-secret-read
direction. Positive login, authenticated gauges/history/assistant/account,
cross-resident session isolation, logout replay and genuine1800s expiry cannot
be claimed. No auth bypass or credential rotation is authorized.
B2 (underlying October authority), original Review and publication remain.
The December stop plan is an owner handoff, not a future execution claim.

## Validation

Current targeted results: infra32 tests passed; core39 passed; API87 passed
with one existing opt-in browser skip. API fixture tests include genuine
server-clock1800s expiry, logout and own-case denial; these are not live sessions.
Ruff (repository isolated selector) and focused core mypy passed.
An initial JSON placement under ranking policies broke unrelated registry loads;
the fixture suite exposed it. Moved the policy to package root and explicitly
packaged it, then reran successfully. Original failure output retained externally.
Playwright MCP failed twice with ERR_NETWORK_CHANGED. Installed-project local
Playwright/Chromium then ran29 real HTTPS checks successfully against the
already-open October revision; six authenticated scenario groups remain B1.
This is pre-deployment evidence, not December-image acceptance.
Initially the heavy lock was held by another full gate; timeout-zero attempts
refused without running Docker. Later build/scan/push acquired it successfully.
No lock bypass or cloud build fallback.
ARM-only secret attribute readback shows both existing secrets enabled with
expiry epoch1793491140 (2026-10-31T23:59Z). No values read. Data-plane metadata
request failed private-link403; no network policy was weakened.

### Historical early admission snapshot

The following describes the earlier October-only admission, not the current
December deployment or its renewed ledger entry.
P01-T01 complete: persisted apps/jobs/SQL safe baseline and fresh raw cost
actual/forecast JSON before mutation. Actual USD315.535491423131; remaining
forecasts October118.33709617465566/November605.7771015167236/
December616.7678909301758. October actual+remaining forecast+single30 allocation
USD463.87258759778666; even conservatively adding30 to each future monthly
forecast remains below700. No cumulative multi-month cap claim.
Cost ledger reserves5 within the same30, with continuous compute estimate4.158
plus separately uncertain ancillary/request costs and4 contingency.
All protected bounds passed; PORT8089 and exact digest confirmed.
No mutation or live acceptance run yet. No source, images, containers or jobs
created. System Playwright import missing; use available MCP Chromium rather
than install dependencies or alter gate tooling.

## Pre-Review Reconciliation

Plan P01/P02 checked for execution with six clearly blocked scenario groups,
not full authenticated acceptance. Phase details and current changes reconciled.
Original critique unchanged; superseded owner direction explicitly recorded.
Current generated local cache/egg-info/browser-console inputs are selected for
an external SHA256-verified tar archive before removal of only those exact
generated files. No historical tracking evidence is removed. Archive and restore
manifest remain external under this session's resident-live directory.
Implementation snapshot and non-overlapping main merge precede the one original
independent Review; final evidence commit then exact-current-main scoped gate.

## Original Review and Publication Snapshot

The one independent Review executed Complete, outcome Not accepted:
RV001 High retains November dependency readiness, RV002 High retains six
authenticated live evidence groups, RV003 Medium retains stale cost/handoff
phase-detail prose. Route these to distinct later work; no fixes or repeated
Review in this task. The original critique and Review are preserved unchanged.
Lifecycle Review is finished, not service acceptance.

Implementation5cdbc9cb and current-main integration0820d95d preserve all image
source hashes. The subsequent original Review/state commit is the publication
candidate. This committed snapshot precedes the requested --changed receipt,
verification and independent exact-head publication assessment. Those remain
external to avoid receipt self-reference; actual outcomes belong in the PR.
P03 stays unchecked in this pre-publication snapshot. A draft partial-delivery
PR may be published only after those controls pass; hosted/human/full resident
acceptance remains separate. Only issue462 criterion8 may be ticked from the
recorded identity/URL/evidence/limits/expiry proof; the issue remains open.
