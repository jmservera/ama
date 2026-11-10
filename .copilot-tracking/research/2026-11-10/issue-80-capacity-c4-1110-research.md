---
title: Issue 80 capacity browser check initial 503 stage, research
description: Source research into the line-571 failure of the C3 whole browser run and the C3-R1 defect (C4)
ms.date: 2026-11-10
---

## Scope and disposition

* Task `issue-80-capacity-c4-1110`, parent `issue-80-capacity-c3-diagnosis-1110`. Source pin: clean HEAD `1dfcb0ee` (tree `eadc6b4b`), main `6d4cd624` (contained, not re-fetched). Research disposition `executed` (source reading first; observations appended below after the research-open marker).
* Root admits checker-only work: at most two narrow observations, the C3-R1 fix, and a stage-local correction only if a concrete checker cause is established. No app, role or API change, no second full run, no automatic C5. C1 batched-preflight and C2 early-draft disclosures and the C3 adverse evidence stay unchanged.

## Observed failure (C3 browser run 1, `browser-run1.log`)

* Stage `initial packages 503/retry`, `capacity_browser_check.py:571`: `expect(page.get_by_role("alert")).to_contain_text("We could not load packages. Try again.")` timed out at 60 s with no alert. Final snapshot: status "The service is still starting. Trying again, this can take a few seconds." and "Loading workspace data: working...". In the C2 run the same stage passed on the same app source; that is not baseline proof of anything.

## Source facts

* Stage setup (lines ~560-575): `page.route(paged("packages"), inject)` where `inject` defaults to `status=503`, calls `expected_failures.add(route.request)` and fulfils `503` with body `Unavailable` (non-JSON). So every request matching, including retries, is answered 503 immediately and registered. No hold is involved, unlike the delayed-401 stage.
* App (`app.js` 274-300): `startupFailure` is true for a non-JSON 500/502/503/504; `fetchReadRetrying` retries with delays 500, 1500, 3000 ms, so about 5 s of retries then returns the last response; capacity load then rejects and the view shows the alert "We could not load packages. Try again.".
* Hypotheses (not assumed): H1 a retry request escapes the pattern or handler (for example a different URL shape, or a request issued before the route was registered and left pending); H2 the page was still in a previous navigation or the workspace status path never reaches the terminal state (a timer or abort interaction, for example `options.signal?.throwIfAborted()` from a superseded load); H3 flakiness from state left by the preceding manager-route loop (last route `#/screens`); H4 the timeout is real and the alert renders under another role or text.
* C3-R1 (source-read): in the C3 edit the new branch calls `route.fulfill(503)` without `expected_failures.add(route.request)`; `inject(route, status=503)` is semantically identical (adds the request, same status, same body) and is the preferred fix.

## Planning Readiness

Ready for observation: a stage-local disposable driver, which logs matched requests, statuses and content types, retry timing and DOM state for the initial packages 503 stage, preceded only by sign-in and a visit to `#/screens` (the checker's preceding route).

## Observations (appended after the research-open marker, 2026-11-10)

Both used the disposable driver copies in `phase80-capacity-c4-evidence-1110/` (sha256 files alongside), the nonblocking heavy lock, an owned synthetic store under a fresh temporary directory (`ZF_DATA` asserted absent), loopback only, the checker's own `owned_store` and `generated` helpers imported from `src/api/checks` (origin: worktree `src/api/src/zava_forward/api/server.py`; Playwright 1.64.0), direct Python exits.

* Observation 1 (`obs1.*`, exit 0, head `1dfcb0ee`): sign-in, `#/screens`, then the stage `initial packages 503/retry`. Handler `inject` matched the first request and every retry for `/api/packages?limit=5&offset=0` (4 requests in total at t=4.75, 5.26, 6.77 and 9.78 s, spaced about 0.5, 1.5 and 3.0 s as designed). Each answer was 503 with no content type. The sibling `workorders` read returned 200. The workspace status showed "The service is still starting..." during retries; at 9.85 s the h1 became "Workspace unavailable" with the packages failure text, and a `[role=alert]` element with that text appeared. My first snapshot reported only the first (empty) `[role=alert]`, so `alert_seen:false` in that file is a driver snapshot defect, not a product result; the later snapshot lines show the text. Disclosed, not corrected.
* Observation 2 (`obs2.*`, exit 0): the same stage six times, alternating the preceding route between `#/aftercare` and `#/screens`, with all alerts collected. Every iteration showed the packages failure alert after 5.2 to 5.4 s (6 of 6). No page error.
* Conclusion: the stage works as designed in isolation (7 of 7 observed runs). The C3 whole-run failure at line 571 (no alert for 60 s, status still "starting", loading status "working") is NOT reproduced and its cause is UNKNOWN. A hung read, interference from an earlier stage of the whole run, or load from concurrent work on the host are candidate explanations only; none is evidenced. No checker cause is established for line 571, so no correction for it is admitted or proposed. No app-defect claim. Budget of two observations is spent.
* C3-R1 stands as source-proven: the C3 branch fulfils 503 without registering the request.
