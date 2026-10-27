<!-- markdownlint-disable-file -->
# RPI Plan: Resident live acceptance

## Task Metadata

Task ID: 462-resident-live-2026-10-27. Slug: resident-live-acceptance.
Date: 2026-10-27. Planning status: Ready for scoped implementation after one critique.
Details: .copilot-tracking/details/2026-10-27/resident-live-acceptance-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-27/resident-live-acceptance-plan-critique.md.

## Executive Summary

Deploy a rebuilt resident image through the resident-only Bicep helper, leaving
external HTTPS ingress open and min0/max1 through2026-12-31T23:59:00Z.
One packaged policy supplies the inclusive2026-12-31T23:59:59Z authority cap
to Bicep, runtime and helpers. Preserve existing authentication and SQL data.
Run live anonymous/negative Playwright plus existing fixture harness coverage;
do not call fixtures authenticated live acceptance.

### What You May Not Know

The deployed demo requires the shared password as well as an admitted fake
email. There is no passwordless route or configurable short session expiry.
The no-secret-read requirement prevents this session from completing positive
login, authenticated isolation, gauges/history/assistant/logout or natural
1800-second expiry. This is a material unmet requirement, not a waiver.
Application expiry stops serving but does not delete ARM ingress automatically.
Underlying SQL allowlist windows and secret expiry are independent: December
ingress does not prove December authenticated availability.

### Unresolved Decisions or Blockers

B1: owner-held credential unavailable; positive acceptance remains blocked.
Owner feedback access can still be restored without touching its credential.
No routine approval needed for the explicitly requested restoration and PR.

## Sources

* .copilot-tracking/research/2026-10-27/resident-live-acceptance-research.md: C1-C4/W1-W4.
* PR #478, evidence branch origin/chore/deploy-resident-474: preserve original partial outcome.
* Owner request 2026-10-27: deployment, budget, retention and acceptance constraints.

## User Decisions and Requirements

* Run research, plan, implement, review in order; commit dated original artifacts.
* Main-based chore/resident-live-acceptance, existing prepared isolated worktree.
* Owner10:37Z update supersedes revision-only restoration and October closure.
* Bicep route only, external HTTPS ingress; min0/max1, no closure watchdog.
* Leave available through2026-12-31T23:59:00Z; inclusive cap23:59:59Z.
* USD30 additional inside renewed USD700 cap to 2026-12-31.
* Preserve 1000-mapping guard, employee login, SQL, other apps min0, eight Manual jobs.
* No secret/.env read, extra RBAC/private endpoints or resource-group deletion.
* Prove real authenticated UI/isolation/expiry where possible; tick only proven #462 criteria.
* Heavy work uses /tmp/ama-rpi-heavy.lock, timeout0; use --changed receipt; no uv.
* Open a main-target PR, no closing keywords, include URL, ingress and cost ledger.

## Goals

* G1: restore feedback availability without expanding cloud authority.
* G2: retain a reproducible live result for every requested scenario.
* G3: publish honest evidence with immutable prior-evidence provenance.

## Scope and Non-Goals

In scope: shared expiry policy, targeted expiry tests, immutable resident image,
resident-only Bicep deployment, safe metadata comparisons, browser checks,
dated evidence, runbook, issue evidence and PR.
Excluded: password bypass/rotation, session fabrication, private datasets,
SQL mutation, employee configuration changes, model provisioning and approval claims.

## Functional Requirements

* Public URL serves the existing synthetic sign-in with HTTPS-only ingress.
* Existing password, identity mapping and read-only own-case projection remain intact.
* Real browser outcomes cover negative authorization, login UI and 320px reflow.
* Credential-dependent checks are individually Blocked, never substituted by mocks.

## Non-Functional Requirements

* Existing resource limits and protected workload projections must compare equal.
* Min0/max1, existing0.25vCPU/0.5GiB; configured expiry moves to December.
* Fresh cost admission precedes deployment; USD30 total resident allocation
  inside renewed USD700 cap. No model allocation is spent or provisioned here.
  Continuous max utilization through December can exceed30; estimate light
  feedback use separately, retain monitoring/stop threshold and billing uncertainty.
  Reconcile the renewed USD700 ama ceiling as the continuation of the historical
  monthly ceiling through December, not USD700 of fresh incremental authority.
  Record this interpretation explicitly. Use actual October spend plus official
  remaining October forecast and the single USD30 allocation; separately compare
  November/December official forecasts against USD700. These forecasts are
  uncertain, not prepaid commitments or hard enforcement. Do not claim a
  cumulative October-December forecast below USD700.
* No new long-lived local process, scheduler or Azure job is added. Application
  expiry is the existing fail-closed serving boundary, not ARM ingress shutdown.

## Acceptance Criteria

* A1: tested revision active and exact URL returns application health/sign-in.
* A2: min/max, source/digest, expiry and protected resource comparisons recorded.
* A3: requested live scenarios each have Passed/Failed/Blocked outcomes.
* A4: original one critique and one independent Review retained; no criterion
  asserted complete from partial proof. Full task outcome remains partial if B1 persists.
* A5: clean committed candidate passes scoped receipt verification and independent
  exact-head publication assessment before push. Hosted/human acceptance remains separate.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-27/resident-live-acceptance-research.md.
Changes: .copilot-tracking/changes/2026-10-27/resident-live-acceptance-changes.md.
Review: .copilot-tracking/reviews/logs/2026-10-27/resident-live-acceptance-review.md.
Ready for scoped operational work after critique; full acceptance blocked by B1.

## Test Ownership

No tests removed. Extend existing core config and infra secret/deploy suites
for December, inclusive exact cap, one second above, expired and non-UTC input.
At most one shared JSON policy and two bounded evidence harnesses are added.
Canonical targets: packaged policy/runtime/Bicep parity, actual HTTPS and ARM metadata.
No generated UI assets. Real browser/API negative tests prove semantics of deployed
denials; byte parity proves asset identity only. Blocked positive tests remain
separate. No broad security or accessibility-conformance audit claimed.
Missing system Playwright may be replaced by the already available Playwright
MCP browser. No model or cloud fallback for local gates.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Restore bounded owner access

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Capture admission and protected baseline

Persist fresh cost, exact revision/digest, safe app/job/SQL metadata; verify budget,
expiry and resource limits before mutation.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Activate revision and open HTTPS ingress

Implement single packaged expiry policy; Bicep consumes it with loadJsonContent,
Python imports reuse AUTHORITY_END. Run focused regression/lint and exact-image
checks; build/push only resident image under timeout-zero heavy lock.
Use resident_demo_deploy.py with ingress on and December31 23:59 expiry.
Retain what-if scope checks and existing approved minimum roles only.
Port8089/HTTPS/min0/max1 verified from live readback and real health.
On failure preserve the already healthy October revision if possible,
record failure explicitly; do not close a healthy owner feedback site by default.

<!-- rpi:phase id=P02 -->
### [x] P02: Live acceptance and evidence

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute actual browser checks

Run real anonymous and negative journeys and 320px layout. Attempt no credential
guessing. Individually record B1 for positive login, own-data UI, assistant,
authenticated top-right sign-out, genuine cross-resident isolation and expiry.
Do not perform exhaustive failed-login attempts that lock out the owner.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Record final state, ledger and criterion mapping

Compare protected metadata and record resident ingress/health/limits.
Update existing operational documentation. Tick only fully supported issue
criteria; otherwise add a precise evidence comment leaving checkboxes unchanged.
Deliver December expiry and cold-start instructions to owner @jmservera.
Leave ingress open and new revision active. No scheduler/watchdog is added.
SQL authorization and secret renewal remain separate custody dependencies;
do not silently extend existing rows or mutate credentials.

<!-- rpi:phase id=P03 -->
### [ ] P03: Original Review and publication

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Review and publish exact candidate

Reconcile plan/details/changes; run one independent original Review.
Commit artifacts with privacy-safe identity and required trailer. Fetch main,
run `python3 tools/rpi-checks.py --changed --lock-timeout 0 --base <reviewed-main-sha>
--out <new-external-directory>`; verify using `python3 tools/rpi-checks.py
--verify-receipt <receipt.json> --required-scope partial --base <fresh-origin-main-sha>`
against exact current base immediately before independent exact-head assessment
and push. If main moves, stop publication for explicit reconciliation first:
integrate non-overlapping main changes with a non-destructive merge before
Review/gating, without rebasing, force-push or changing main.
Create PR to main with evidence, costs, ingress URL and blockers. Do not merge.

## Dependencies

P01-T02 depends on P01-T01 and disposed critique. P02 depends on actual health.
P03 depends on reconciled P01/P02 and original Review. Full acceptance also
depends on B1 credential custody and broader original issue gates.

## Critique Disposition

Original critique executed Complete; verdict Revise retained; no repeat.
The owner's10:37Z update postdates this original critique. Its October-only
no-build/closure assumptions are superseded, not retrospectively regraded.
Apply explicit owner changes directly; no second critique for this task.

| Finding | Disposition | Evidence required |
| --- | --- | --- |
| PC-001 High | Applied directly | Correct8089, compare live PORT/Bicep, actual health and traffic readback |
| PC-002 High | Applied directly | Executable gate/verification argv above, partial scope explicit |
| PC-003 Medium | Applied directly with explicit cap interpretation | Actuals and official forecast bucketed monthly, single USD30 allocation, uncertainty retained; monthly renewal derives from original October ceiling, not a cumulative forecast claim |
| PC-004 Medium | Applied directly | Owner-directed PR/final expiry handoff; future closure pending; post-expiry residual costs possible |
| PC-005 Medium | Applied directly | gh api user at commit boundary; derive/configure local noreply for author/committer |

## Follow-Up Items

* Owner credential-bearing positive live acceptance and natural session expiry.
* Owner must reconcile existing SQL allowlist/secret validity before November
  demonstration; December ingress alone does not extend those authorities.
* Real model activation remains separately owned; deterministic fallback accepted here.

## Handoff

P01/P02 execution complete with partial acceptance: new Bicep revision0000003,
29 live checks passed; six authenticated scenario groups owner-run. B1/B2 remain.
P03 next: integrate newly moved docs-only main, original independent Review,
then final commit, scoped gate and publication. No whole-task acceptance.
