---
title: Easy Auth Intermittent Empty-Body 500s Under Concurrency
description: Investigation of the intermittent empty-body 500s on the cutover test demo API (issue 810): burst evidence, the ingress transport cause found on 2026-11-04, the owner-approved live change and its verification
author: AMA programme
ms.date: 2026-11-04
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
* Superseded by the 2026-11-04 follow-up below: the cause is the ingress
  transport setting, not the authentication middleware itself.

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

## Follow-up 2026-11-04: cause found and mitigated

Owner approval 2026-11-04 allowed live changes to `ca-cutover-test-demo-api`
(resource group `ama`) for this issue only. The app was warmed with `/healthz`
first (it had scaled to zero). No resource group, secret or credential file was
touched. Same client, `curl` over HTTP/2 to the ingress, 30 parallel requests
per round.

| Step | Setting | 500 responses |
| --- | --- | --- |
| Baseline, revision `--0000013` | ingress transport `Auto` | `/healthz` 2, 1, 0, 1 of 30; `/style.css` 3, 1 |
| Concurrency scan, same revision | `Auto` | 1 of 80 at 5 parallel, 4 of 160 at 10, 11 of 320 at 20 |
| In-container burst, 4 x 30 to `127.0.0.1:8088` | bypasses ingress and sidecar | 0 (all 200) |
| Test: app speaks HTTP/1.1 keep-alive (temporary command override, revision `--k810`, since deactivated) | `Auto` | `/healthz` 2, 2, 3, 3; `/style.css` 0, 2, 2, 3; `/welcome.html` 3, 5 |
| Ingress transport `Http` | `Http` | `/healthz` 0, 0, 0, 0 |
| Ingress transport `Http2` | `Http2` | 30 of 30 every round (the app does not speak HTTP/2 cleartext, as expected) |
| Final, revision `--t810` (same image `891-1022`, no command override), after setting `Http` | `Http` | `/healthz`, `/welcome.html`, `/style.css` 4 x 30 each: 0 x 500; `/healthz` over forced HTTP/1.1 4 x 30: 0 x 500; `/workspace-shell.js` unauthenticated 4 x 30: all 401 |

Conclusions:

* The application is not the source: it served 120 of 120 concurrent
  in-container requests, and the HTTP/1.0 close-per-request behaviour was ruled
  out (keeping connections alive did not change the rate).
* The ingress transport setting `Auto` is the controlled variable. With `Auto`
  the same revision returned empty-body 500s in every session (about 1 to 3
  percent); with `Http` there were 0 of 600 across the verification rounds.
  Confidence: High that the setting is the cause on this app; the internal
  mechanism (probably the proxy trying HTTP/2 to the app on some connections)
  is not proven because Log Analytics still rejects the CLI host (network
  perimeter) and the registry also rejects it, so no log evidence or custom
  image could be used. Platform logs were not read.
* The application speaks HTTP/1.1 only, so pinning `Http` is a correct
  description, not a workaround. Sign-in, path exclusions and the resident
  consent and human approval boundaries are unchanged.

Live changes made (all reversible): ingress transport `Auto` to `Http`; a
temporary command override revision (`--k810`) created for the keep-alive test,
then removed by a new revision (`--t810`) with the original template, and
`--k810` deactivated. Rollback: `az containerapp ingress update --transport auto`.
Source change: `infra/modules/containerapps.bicep` pins `transport: 'http'` for
the API, with `infra/tests/test_api_ingress_transport.py`; it has not been
deployed from Bicep. Until it merges, a deployment from the old template
(`auto`) would restore the fault.

## Follow-up 2026-11-04 (second): root cause is the API's HTTP/1.0 close-per-response

Owner approval 2026-11-04 (live changes to `ca-cutover-test-demo-api`, resource
group `ama`; no new roles, network paths or SQL changes). Revision `--0000014`
with ingress `Http` still returned empty-body 500s: 8, 10 and 12 of 160 at 20
parallel (5 to 7 percent) on `/healthz`.

Evidence:

* The Easy Auth sidecar log (`http-auth` container) records, for each 500,
  `Failed to forward request to http://127.0.0.1:8088` with `HttpRequestException`
  after 0.5 to 3 ms and inner `HttpIOException: The response ended prematurely
  (ResponseEnded)`. The application log shows nothing for those requests.
* In-container probe: 1600 of 1600 new-connection requests to the app on
  `127.0.0.1:8088` at 20 threads returned 200. The app is not dropping them.
* Stub backend A/B (command override, same ingress, 20 parallel x 160): a raw
  socket stub answering HTTP/1.1 keep-alive gave 0 x 500 in 640 requests; a stub
  answering HTTP/1.0 and closing after each response gave 14 to 25 of 160 (the
  real app's behaviour).
* Real app with `protocol_version = "HTTP/1.1"` (command override launcher):
  0 x 500 in 640 concurrent requests. Python `BaseHTTPRequestHandler` defaults
  to HTTP/1.0, so the API closed every connection. This supersedes the earlier
  keep-alive negative result, whose override did not give a working keep-alive
  handler.

Hypotheses tested live and reverted, or ruled out:

| Hypothesis | Change | Result |
| --- | --- | --- |
| CPU starvation of the shared replica | 1.0 vCPU, 2 GiB (`--0000015`) | Still 5 to 11 of 160; reverted to 0.5 vCPU, 1 GiB |
| Application server or backlog | stub servers (`--0000017` to `--0000020`) | Fault follows connection close behaviour, not the app code |
| Excluded paths, token store, unauthenticated action | read only | Token store off; `/healthz` excluded; failures occur on excluded paths, so not a policy decision |
| Scale rules, probes | read only | min 0, max 4, one replica in every test; probes pass and are not involved |

Fix: the handler in `src/api/src/zava_forward/api/server.py` sets
`protocol_version = "HTTP/1.1"` and an idle `timeout` of 300 s, and closes the
connection (with `Connection: close`) when a request body was not read. This
applies to every method: any request with a non-zero or invalid `Content-Length`
or any `Transfer-Encoding` closes the connection unless the handler read the
body, so an unread body is never parsed as a pipelined request (desync, review
finding; the app trusts `X-MS-CLIENT-PRINCIPAL`). Test:
`src/api/tests/test_keepalive.py`. The full `src/api` suite after the desync fix ran 1818 tests, OK (335 skipped).

Live state: the demo API runs revision `--0000022`, a temporary command override
that applies the same `protocol_version` change to the existing image (no image
could be built or pushed from the CLI host). Ingress `Http`, 0.5 vCPU, 1 GiB,
min 0 and max 4 replicas are as before. Rollback: update the app with the
original template (no `command` or `args`). Deploying an image built from this
source makes the override unnecessary; remove it then.

Verification on `--0000022` (one client, 2026-11-04): `/healthz`,
`/welcome.html` and `/style.css` 3 x 160 each at 20 parallel, plus 200 at 40
parallel: all 200; `/workspace-shell.js` unauthenticated 3 x 160: all 401; 300
sequential `/healthz`: all 200. That is 0 empty-body 500s in 2,180 requests.
Authenticated requests were not made (no credentials). Not proven: behaviour of
the new image (not deployed) and a sustained service level.

## Acceptance status for issue 810

* Cause identified with evidence: met for the setting (controlled A/B on the
  live app); internal mechanism not proven, platform logs unreadable.
* Fix or mitigation applied: applied live under owner approval 2026-11-04 and
  committed to Bicep; Bicep deployment, independent review and hosted CI are
  pending, so the repository change is not yet proven in a deployment.
* Live 4 x 30 burst clean after the change: met on 2026-11-04 (0 x 500 in 600
  requests across four paths); one client and one session, so it is a point
  observation, not a service level.
* Why `Refs` and not `Closes`: the template deployment and the review gates are
  still outstanding.

## Earlier status (2026-11-03, superseded)

* Cause identified with evidence: partly met. Layer localised; precise fault not proven.
* Fix, mitigation or owner-approved acceptance: unmet. No owner decision recorded.
* Live 4 x 30 burst clean after a change: unmet. No change was made; the baseline above still shows 500s.
