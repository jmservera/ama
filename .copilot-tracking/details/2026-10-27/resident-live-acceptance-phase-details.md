<!-- markdownlint-disable-file -->
# RPI Phase Details: Resident live acceptance

## Metadata

Task ID: 462-resident-live-2026-10-27. Slug: resident-live-acceptance.
Plan: .copilot-tracking/plans/2026-10-27/resident-live-acceptance-plan.md.
Research: .copilot-tracking/research/2026-10-27/resident-live-acceptance-research.md.

## Phase Index

Owner10:37Z supersession: the original choreography below is historical where
it says no build/template rerun or October closure. Current plan P01-T02 owns
one shared packaged expiry policy, targeted tests, rebuilt immutable image and
resident_demo_deploy.py Bicep apply with external ingress and
2026-12-31T23:59:00Z. Preserve SQL, credentials, employee app and eight Manual
jobs. No closure watchdog. Leave new revision active and reachable. Existing
SQL/secret validity may still require owner renewal for November; do not
silently mutate grants/rows/secrets. Original critique stays unchanged.

Current test ownership: modify existing expiry tests only, no removals.
Validate core/API resident suites, compiled Bicep/helpers, Ruff, real live
Chromium denials/320px and fixture harness expiry. Heavy build and scoped
changed-path gate take /tmp/ama-rpi-heavy.lock with timeout0, never nested.

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Executed, December Bicep deployment | P01-T01, P01-T02 |
| P02 | Executed, partial acceptance with B1/B2 | P02-T01, P02-T02 |
| P03 | Next, before publication | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Restore bounded owner access

Superseding direction executed: shared expiry policy and rebuilt resident image,
resident-only Bicep apply; no secret values, SQL mutation or job execution.
Prior PR478 evidence is referenced by immutable commit, not copied.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Admission and baseline

Capture safe app projection (name/image, ingress, scale, command/argument metadata,
environment names only), all job triggers and SQL SKU. Never request listSecrets
or secret environment values. Read only expiry/host/address-mode/PORT values by exact
allowlist. Record actual MTD cost query (USD315.535491423131 at research), delayed
billing, existing baseline and bounded resident compute allocation. Preserve all
three non-resident app projections exactly; all four minima0 and eight Manual jobs.
Stop before mutation if stale expiry, digest mismatch, max>1 or new budget unknown.
The renewed USD700 is interpreted as continuing the original monthly ama ceiling
through December. Record that interpretation, current October actuals, official
remaining forecast by month, existing reservations and the one USD30 allocation.
Require each monthly sum below700; disclose aggregate multi-month forecast is not
below700. Delayed billing and forecast uncertainty are not a hard-cap guarantee.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Declarative deployment, executed

New immutable image fab6a85318f65db006bc610f3b3aff8ae799046d1b9a1813662b3b315c1b6fc7,
new ready revision ca-resident-demo--0000003. Bicep helper what-if4 owned changes,
typed exact confirmation via real PTY, then successful apply. Expiry December31
23:59Z; public HTTPS8089, min0/max1. Actual health200 and29 real browser checks.
Build and Trivy fixable HIGH/CRITICAL scan passed under timeout-zero heavy lock.
Temporary approved VM/32 ACR push route restored exactly; no new roles.
Four role readback includes an unrelated pre-existing concurrent model assignment
created10:42Z, not created or consumed by this task; do not remove it.

<!-- rpi:phase id=P02 -->
## P02: Live acceptance and evidence

No tests may read secrets, mutate SQL or invent successful authentication.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Browser scenarios

Use real Chromium Playwright against
https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io.
Anonymous assertions: synthetic banner, labelled login, hidden resident content,
hidden account, skip-link keyboard focus, no script errors, HTTPS/header behavior.
Negative requests: anonymous protected view/assistant, forged session, missing
CSRF, cross-origin login, explicit case selectors and absent staff routes.
Use one unmistakably invalid non-secret test password at most; no password guessing.
Mobile: viewport320x800, document width<=320, labelled form/button accessible.
Screenshots may contain only anonymous synthetic UI, never credentials/cookies.
Record each positive journey Blocked B1 with no valid session available. Static
account markup is not a top-right rendered sign-out pass; forged expiry is not
natural expiry; absent selectors without a valid session are not cross-resident
isolation. Fixed1800s cannot safely be shortened without new source/image work.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Final evidence and issue

Record UTC times, exact requests/statuses, source asset SHA256 parity and safe
resource comparisons. Capture final external ingress/traffic/revision limits,
application expiry and real health. Create cost-ledger.json with USD5 admission,
USD4.14 approximate maximum continuous compute, requests/ancillary uncertainty
and no new model/build/RBAC. Keep USD1 prior release/USD20 model/USD4 contingency.
Reference PR #478's immutable evidence branch head without importing its documents.
December expiry/stop instructions are owner-run, not a watchdog or scheduled job.
Deliver via PR and final output, with no future closure claimed.
Post-expiry requests can still incur compute/ancillary costs.
No file in docs/reference changes unless necessary;
if changed, update index and append log.
Map all eight #462 composite criteria, tick only proven whole criteria, and
leave unmet criteria visibly open. Use Refs, never closing keywords.

<!-- rpi:phase id=P03 -->
## P03: Original Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Review, gate, publication

One fresh independent reviewer activates rpi-review, compares original owner
request (including unmet positive acceptance) against actual changes and artifacts,
and writes only the canonical Review. Do not repeat Review or rewrite its outcome.
Later findings route to follow-up; no repair/review loop.
Immediately before committing run gh api user, derive
{id}+{login}@users.noreply.github.com, configure only repository-local user.email
and use that email for both author/committer with the required Copilot trailer.
Scoped gate is explicitly owner-requested evidence-tier validation, not full
release or hosted/human approval. Runner owns timeout-zero shared lock; do not
nest an outer flock around a self-locking gate. Execute
`python3 tools/rpi-checks.py --changed --lock-timeout 0 --base <reviewed-main-sha>
--out <new-external-directory>`, then verify with
`python3 tools/rpi-checks.py --verify-receipt <receipt.json> --required-scope partial
--base <fresh-origin-main-sha>`. Keep final receipt external.
Before push verify fresh main, receipt exact HEAD and partial scope; independent
exact-head publication assessment is separate from original RPI Review and may
permit only a draft partial-evidence PR. Never report whole-task completion.

## Current Blockers

B1: shared credential unavailable under no-secret-read rule. Owner must complete
credential-bearing journeys through its existing secure custody route.
B2: both secret metadata expiries October31 and SQL allowlist limit November1
remain independent owner/private renewal dependencies for November demonstration.
Main advanced to49c942b3 with docs-only PR439 while implementation ran. Integrate
that non-overlapping main history with a merge before original Review and gating;
no source/image rebuild is required because no src/infra runtime input changed.
