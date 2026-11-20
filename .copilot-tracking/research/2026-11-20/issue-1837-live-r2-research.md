---
title: Research issue 1837 live, run 2
ms.date: 2026-11-20
---

## Opening

* Base `7c5aca476`. Earlier same-day run (`issue-1837-live-research.md`) added the negative-boundary test, now on main. Source repair (#1878, JSON post from `nomination-routes.js`) is on main.
* New this run: the deployed demo (`ca-cutover-test-demo-api` revision 0000035) now serves `/nomination-routes.js` (200) and the routes page carries the script tag, so a live browser journey is possible. Open items: live form transport proof, local browser checks and unit tests re-run, `nomination_browser_check` adverse result.

## Findings

* Live (rev 0000035, read at run time, no secrets): `/nomination-routes.js` 200 and routes page carries the script tag. Real browser submit of the live challenge form with empty/unknown fields posted `application/json` with `X-ZF-CSRF` (not urlencoded), got a field-validation 400 (not "Could not read that."), and the case was unchanged. Negative probe: urlencoded 400, JSON without header 403, malformed 400, unknown case 404, body case mismatch 400, case unchanged.
* Local: 66 API tests OK, zero skips. Three browser checks passed with pinned axe 4.10.3 (sha256 verified): route forms (POST 200,200,200, zero violations, zero target-size), challenge, nomination (zero violations each state). The earlier `nomination_browser_check` failure did not reproduce; the "law store not loaded" lines are logged server-side errors in passing runs.
* Live successful write not attempted: it would add irreversible records to the shared synthetic demo.

## Critique (one pass)

Keep this a no-source-change evidence run; FOCUSED tier because nothing under src, workflows or manifests changes. Do not claim a live write; do not claim independent review or hosted CI.
