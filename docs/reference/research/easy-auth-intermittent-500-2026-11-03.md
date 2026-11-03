---
title: Easy Auth Intermittent Empty-Body 500s Under Concurrency
description: Read-only investigation of the intermittent empty-body 500s on the cutover test demo API (issue 810), with burst evidence, what was and was not provable, and options awaiting an owner decision
author: AMA programme
ms.date: 2026-11-03
ms.topic: reference
---

## Scope and authority

Owner decision 2026-11-03 authorised a read-only Azure investigation (config
reads, logs) and a small concurrent-request reproduction against the demo apps.
No Azure resource was changed. No secret, token or cookie was read or recorded.
Target: `ca-cutover-test-demo-api` (resource group `ama`, revision
`ca-cutover-test-demo-api--m691-b6242b9`), warmed with `/healthz` first.

## Findings

All figures are observed on 2026-11-03 between 17:05 and 17:12 UTC from one
client using `curl` over HTTP/2, 30 parallel requests per round, 4 rounds.

| Target | Auth | 500 responses (rounds 1 to 4 of 30) | Other |
| --- | --- | --- | --- |
| demo-api `/healthz` | Easy Auth on, path excluded | 3, 2, 1, 2 | rest 200, 2-byte body |
| demo-api `/welcome.html` | Easy Auth on, path excluded | 2, 1, 1, 0 | rest 200 |
| demo-api `/workspace-shell.js` | Easy Auth on, not excluded, unauthenticated | 0, 0, 0, 0 | all 401, empty body (sidecar answers itself) |
| resident-demo `/healthz` | no auth config | 0, 0, 0, 0 | all 200 |

A 40-request burst captured the failing responses. Each is `500` with
`content-length: 0`, an `x-ms-middleware-request-id` header and none of the
application's own headers (no Content-Security-Policy, no content type).
Successful responses carry the application's headers. The application console
log shows no entry for the failing requests (it only logs escaped errors).

Configuration read (unchanged):

* Easy Auth enabled, `RedirectToLoginPage`, forward proxy `NoProxy`,
  `requireHttps` true; excluded paths: `/healthz`, `/readyz`, `/`,
  `/welcome.html`, `/style.css`, `/zava-logo.png`, `/sign-in`. This matches
  `infra/modules/containerapps.bicep`.
* Scale: min 0, max 4, one HTTP rule; one replica was running; 0.5 vCPU, 1 GiB.
* Startup, readiness and liveness probes are configured (PR 764).

## Interpretation

* The 500 is not produced by the application: it lacks the application's
  headers and is not logged by it.
* Excluding a path from authentication does not avoid it. The excluded paths
  still pass through the authentication middleware on their way to the
  application, and they fail at the same rate.
* Requests the middleware answers itself (401) never failed; only requests it
  forwards to the application container failed. This points at the middleware
  to application hop under many simultaneous new connections.
* A comparable app without Easy Auth was clean in the same test (one sample, a
  different environment, so supporting rather than conclusive).
* The listen-backlog change (PR 786) is an ancestor of commit `b6242b900`, the
  commit the revision is named for (image contents not separately verified),
  and the fault persists, which makes an application backlog
  limit a less likely cause without ruling it out.

Cause status: localised to the Easy Auth middleware layer by the evidence
above (Medium confidence). The precise internal fault is not proven: the Log
Analytics workspace `log-cutover-test` rejected the query from the CLI host
with a network security perimeter error, and the environment diagnostic setting
lists no log categories, so platform auth and system logs could not be read.
Changing either is a resource change outside the authorisation.

## Options for the owner

| Option | Effect | Cost and risk |
| --- | --- | --- |
| Accept and document | No change; reads are idempotent and a retry succeeds | Roughly 1 to 3 percent of burst requests fail; demo only |
| Client-side retry of idempotent GETs on empty 500 | Hides the fault for browsers and probes | Code change in the web client; masks a platform defect |
| Raise min replicas to 1 or more | Removes cold-start variance; does not remove the fault seen with one warm replica | Cost; unproven benefit |
| Allow log access (network perimeter rule or diagnostic categories) so auth and system logs can be read, then retest | Would prove the cause | Resource change; needs owner approval |
| Azure support case citing the `x-ms-middleware-request-id` values | Platform-side root cause | Time; request IDs are short-lived in logs |
| Drop Easy Auth for built-in application token validation | Removes the layer | Security-relevant redesign; needs its own plan and review |

Recommendation: log access first (cheapest route to proof), then decide
between accepting and a support case. Nothing here weakens sign-in, resident
consent or human approval boundaries.

## Acceptance status for issue 810

* Cause identified with evidence: partly met. Layer localised; precise fault not proven.
* Fix, mitigation or owner-approved acceptance: unmet. No owner decision recorded.
* Live 4 x 30 burst clean after a change: unmet. No change was made; the baseline above still shows 500s.
