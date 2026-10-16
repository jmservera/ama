---
title: Public browser access changes
description: Implementation evidence and limits for issue 344
ms.date: 2026-10-16
---

Task 344, public-browser-access-344. Full plan scope. Implementation executed;
real-user and full deployed parity acceptance remain Blocked.
Canonical plan/details/critique under their 2026-10-16 directories.

## P04: Owner-requested review continuation intake

Supplied independent verdict CHANGES against 3f33ff1 is accepted as input to
later implementation, not a repeat of the historical postimplementation Review.
Clean worktree and matching open PR 352 verified. Fetched main and initiated
the explicitly requested merge. Four conflicts affect additive evidence/log,
compiled tests and the old CLI. Resolve by keeping both documentation/test
workstreams and main's thin delegating main(). setup-entra.py already tests
the additive edge callback, Custom forwarding and idempotence; do not duplicate
its command logic. P04 plan/details now own the remaining bounded changes.

### P04-T01: Main integration and CLI ownership

Merged main 204b434 as merge commit 3b08ace, preserving both documentation/log
sections and the additive compiled tests plus incoming secret-reference checks.
The old CLI main() delegates unchanged to setup-entra.py. Existing setup edge
callback tests passed; added a regression pinning delegated argv/result/path.
No extension of setup's already-sufficient discovery/callback algorithm.
During final preparation main advanced to ae99282; integrate that separately
before publication without rewriting either lineage.

### P04-T02: UUID prerequisite and mutation evidence

The entry point now safely treats missing/null clientId as empty, strips only
hexadecimal UUID characters and requires exact 36-character/five-segment form
with separators at the four canonical positions. A separate minLength guard
parameter describes the setup command. Auth depends on guard and edge on auth.
Compiled tests exercise null/empty/sentinel, uppercase/lowercase synthetic
UUIDs, invalid characters/length/wrapping and every misplaced separator.
Four compiled mutations are rejected: nonempty-only, always-ok, constraint
disabled and auth dependency removed. UUID syntax is not a Graph lookup.
No live deployment was attempted over the blocked placeholder configuration.

### P04-T03: Honest evidence and validation

Infra README, evidence pack/JSON and reference index/log document default
redirect mode's User-Agent-sensitive API behavior and full-resource PUT
preservation limits. Only returned fields/references can survive union; absent,
write-only or redacted references require human verification/authorized repair.
No live credential round-trip is proved. Existing six-row criterion audit
retains real sign-in/API-coexistence/feature blockers, no issue ticks.

Validation in a new session pip venv after editable core/agents/API install:

* Full infra suite with REQUIRE_AZ_BICEP=1 and absolute project fixture
  PYTHONPATH: 186 tests passed, no skips. Includes new mutations/delegation
  and retained setup/public-edge/profile/hardening contracts.
* Compiled-policy tests Ruff check/format and compiled tests/initializer mypy
  passed. Initial missing Ruff/mypy resolved by pip installation of the
  repository-pinned versions. A tuple fixture annotation fixed a new mypy
  inference error; no blanket typing suppression.
* Bicep entry build passed. An initial reduce argument-order compile failure
  was corrected before behavioral validation.
* Initial mutation harness used subTest inside an expected-failure helper,
  which swallowed expected assertion failures. Removed the inner subTest;
  final suite now proves those mutations fail normally.
* Focused API auth suite: 32 tests passed, including real-loopback requests.
  Expected denial/missing-law diagnostics are not positive platform proof.
* Installed local API subprocess with temporary synthetic fixture/state:
  responsiveness verified, health/welcome 200 and anonymous API 401; process
  terminated and temporary files removed. No default/private dataset opened.
* Public curl around 18:30 UTC: health 200, native API 401, browser app 302
  and browser JSON API 302; only redirect hostname login.microsoftonline.com
  retained. Read-only management around 18:32 UTC: SQL Ready/public Disabled;
  environment internal/public Disabled. No Azure/tenant writes.
* Git whitespace and JSON/link checks are included in final publication gate.

Original critique/Review remain historical. The supplied independent CHANGES
verdict is user-authorized later work; full acceptance remains Not accepted.
Remaining P04-T04 owns final main reconciliation, PR/issue metadata and push.

### P04-T04: Integrated source candidate

Implementation commit 74af35f carries UUID guard/tests and honest documentation.
Main advanced to ae99282 during execution; merged it without conflicts as
63e3594, retaining incoming regulatory UX/source/checks. Re-ran the full
installed-venv infra suite on that integrated candidate: 186 passed.
The serving image is unchanged: earlier asset-hash proof is dated image
evidence, not parity with these newly integrated source/UX changes.
Updated README/evidence/index relative link paths resolve; JSON and whitespace
checks pass. All commits use the authenticated account's repository-local
noreply email and required Copilot trailer. Remote publication remains pending.

### P04-T04: Publication completed

Pushed 63e3594 (including 74af35f and both main merges) to the existing branch
without force. Updated PR 352 body with the complete criterion audit, guard and
readback limits, fresh probes and current local validation. GitHub reports
MERGEABLE; hosted checks are running, not claimed passed. Added an explicit
unchecked browser/fetch JSON API 401 coexistence criterion to #350, preserving
all its existing body content. The initial conservative body comparison stopped
on trailing-newline differences; normalized only trailing whitespace for the
second comparison before editing, with no remote content discarded.

All P04 tasks are complete. The final evidence-only publication commit records
this state and the serving-image/source-head distinction; no source behavior
changes follow validation. Full #344 acceptance remains Blocked on #349/#350.
No merge, issue tick, live deployment, credential/tenant write, private-data
read or resource deletion occurred. Manual session remains stopped; named
human approvals and the original review's Not accepted outcome are unchanged.

## P01: Infrastructure and Auth

Added `infra/public-edge-existing.bicep` plus two bounded helper modules.
Existing private environment/API/workspace references feed a fail-closed runtime
guard, auth-preserving update and Premium/WAF/Private Link edge. Environment
tags are inherited. Main's production/default credential contract stays intact.
The existing edge now uses explicit HTTPS `/*`, no cache/rewrite, fixed sole
API origin/Host/certificate and GET `/healthz` rather than unsupported HEAD `/`.

Callback initialization accepts a strict HTTPS `--public-url` origin only with
Custom forwarding with exact Front Door-overwritten X-Forwarded-Host/Proto
for a differing host. It retains previous callbacks,
application roles, credentials and permissions. Regression coverage was added
to existing test files; no src runtime change, API exemption, anonymous bypass,
test file or alternative registration was introduced.

Four critique corrections are incorporated in plan/details. No pre-existing removals,
tenant mutations or private data reads.

Live isolation correction before Review: public health and denial recovered
after propagation, but RFC Forwarded changed the callback host under Standard.
Azure rejected an attempted Forwarded-header deletion rule as reserved. The
failed deployment created only an empty, unused originheaders rule set under
the new profile; precisely that owned trial resource was deleted, not the profile or
any pre-existing resource. Corrected both existing-stack and main edge auth to
Custom with Front Door-overwritten X-Forwarded-Host/Proto, and require that
exact configuration in the initializer. Repeated and final hostile probes proved it.

## P02: Deployment and Audit

Initial what-if: eight Create, zero resource Modify/Delete. Incremental
`public-browser-344`, `public-browser-344-browser` and final tagged
`public-browser-344-final` deployments succeeded. Only new edge resources and
`public-browser-344-trusted-proxy` subsequently succeeded after the rejected
`public-browser-344-headers` trial. Only new edge resources and
the existing API auth child were written. Final readback: environment internal
and public Disabled, SQL Ready/public Disabled/private connection Approved,
browser action RedirectToLoginPage/Custom and seven original exclusions.

Native Private Link approval returned asynchronous HTTP 201. Its operation
was polled to Succeeded and connection read back Approved; earlier exit-zero
CLI/REST writes still Pending were not counted as approval.

Exact retained new resources: profile afd-cutover-test, endpoint ep-cutover-test,
origin group og-api / origin api, route-api, sp-waf, to-log-analytics diagnostics,
wafcutovertest and the environment's managed Private Link connection. Nested ARM
deployment records are metadata. Manual job job-cutover-test-public-audit uses
the unchanged serving API digest and existing identity only for registry pull.
Its asset execution ud03kna Succeeded: all 17 hashes match current src,
including all 16 historical assets. No pre-existing resources were deleted/replaced;
the one owned empty trial rule-set deletion is recorded above.

The same owned job's bounded anonymous HTTP execution zqdjdqp Succeeded:
private origin health 200, /api/me 401, /app 401 for a native client,
/.auth/login/aad 302 to login.microsoftonline.com. No cookies, auth queries,
IDs, authenticated API data, Store, dataset or credentials were captured.
This diagnostic amendment distinguishes a working private origin from the
then-unproven public edge; it is not public or positive-user acceptance.

The full matrix now reconciles 16 historical assets and 26 user-visible
capabilities. #349 files the missing valid registration/credential/staff
prerequisite; #350 files feature/data/configuration/positive-role acceptance
gaps. No real-user session or owner acceptance is invented.

## Validation

* Infra: `REQUIRE_AZ_BICEP=1 <session-venv>/python -m unittest discover -s
  infra/tests -q`: 123 passed after the Custom-forwarding regression.
* API, absolute core/agents test PYTHONPATH: 549 tests, OK, 110 opt-in skips.
  Auth-specific 31 tests include real-loopback HTTP servers and positive/
  negative principal, role and tenant contracts.
* API Ruff, format and mypy passed (44 source files). Changed initializer mypy,
  touched compiled-contract test Ruff/format, Bicep build/lint of entry point
  and modules, and diff whitespace checks passed.
* Cut-over parser: nine tests passed. Initial package failures resolved only
  after pip installing declared source distributions/extras into session venv.
* Optional mypy over older initializer test fixture has pre-existing mixed-dict
  typing failures; not claimed clean and not broadly repaired.
* Public smoke completed at 17:01 UTC: health/welcome/static 200; native
  anonymous API families 401; browser /app 302 to Entra with canonical HTTPS
  edge callback. Forged principal/malformed bearer 401; Host conflict 421;
  individual/combined forwarding spoof retains canonical callback. Three
  repeated sets also showed canonical HTTPS after auth propagation.
* Initial direct/default curl both
  returned Front Door 404 with native resource provisioning Succeeded but
  deploymentStatus NotStarted. Provider is Registered, route/origin/endpoint
  Enabled, exact host/probe/route read back; this is not a health pass.
  Later observed success supersedes this transport failure only.
* Browser User-Agent API requests still receive platform 302 even with JSON
  Accept. Filed under #350; no API exemption or positive-platform acceptance.

Missing tenant application is an acceptance blocker, not evidence of successful
sign-in. Full API suite and package hashes cannot substitute for deployed
positive-user feature checks.

## Amendments and Divergences

Additive entry point uses two tiny helper modules for runtime guard and
preserving auth settings; still one new Bicep entry point and no test files.
The existing main/default secret contract is unchanged. A manual image-only
audit job is added to the precise resource plan in phase details; its commands
enumerate package assets and probe only anonymous HTTP status/redirect host,
never initialize or query a data service. Full deployed feature acceptance
cannot be checked without real staff authorization. Gaps filed as #349/#350.

Generated reference inventory was refreshed from tracked current files;
130 matrix rows have destinations and 1,462 references were reconciled.
The two existing legacy reference rows were retained without opening any legacy
content. No historical source/data was read. Final tracking-only line shifts
will be reconciled before commit.

## P03: Review and Publication

One postimplementation Review executed:
.copilot-tracking/reviews/logs/2026-10-16/public-browser-access-344-review.md.
Execution Complete, outcome Not accepted for full #344 acceptance.
RV-001 routes the tenant prerequisite to #349, RV-002 routes browser API 401
to later implementation under #350 after platform trust proof, and RV-003
routes positive-user feature/configuration evidence under #350. No return to
implementation, repeat Review or claim of finding closure.
Implementation commit `33ac8fe` was authored/committed with the authenticated
account's repository-local privacy-safe address and required Copilot trailer.
Pushed feat/public-browser-access-344 and opened
https://github.com/jmservera/ama/pull/352 against main. This publication is not
owner acceptance or merge; issue criteria remain unchecked. A metadata-only
commit records publication and the stopped manual session with blockers retained.
