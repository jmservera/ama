---
title: Issue 1837 standalone nomination forms, live demo close-out (2026-11-23)
description: Per-criterion record for issue 1837 against main and live revisions API 0000054 and resident 0000026
ms.date: 2026-11-23
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Refs #1837. Base `342fad401d` (origin/main). Live apps `ca-cutover-test-demo-api` revision `0000054` and `ca-resident-demo` revision `0000026`, both active and 100% traffic at probe time. No Azure resource was created or changed and no credential is recorded. Builds on the [2026-11-22 r2 record](issue-1837-live-demo-evidence-2026-11-22-r2.md).

## Main check

Main already carries the fix: the standalone route page posts JSON with the CSRF header (#2110 and earlier). No open PR overlaps. No source changed, so this is a focused-tier, evidence-only change.

## Live finding

A real browser submit of the live challenge form with empty fields posted `application/json` with the CSRF header and returned `Supply every required route field...` (HTTP 400 field validation), not the original `Could not read that.` The case JSON was unchanged afterwards, so the 2026-11-22 `case_unchanged: false` reading did not recur ([probe](issue-1837-live-2026-11-23/live-form-probe.json), [screenshot](issue-1837-live-2026-11-23/live-form-submit.png)).

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three submissions, valid challenge target | Proven (earlier record) | [failing run at 9da3fcd](issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); tests pass on main |
| Valid submissions retain records; JSON callers compatible | Proven locally; live write unproven | [route forms run](issue-1837-live-2026-11-23/axe-nomination_route_forms-result.json) POST 200 x3; a live write would add irreversible records to the shared demo, so none was attempted |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven | 66 unit tests OK ([output](issue-1837-live-2026-11-23/unit-tests.txt)); [live probe](issue-1837-live-2026-11-23/live-negative-probe.json): urlencoded 400, no header 403, malformed 400, unknown case 404, mismatch 400, case unchanged |
| Browser journeys with axe, zero unexpected skips | Proven locally, qualified | [route forms](issue-1837-live-2026-11-23/axe-nomination_route_forms-result.json), [challenge](issue-1837-live-2026-11-23/axe-challenge-result.json) passed first run; [nomination](issue-1837-live-2026-11-23/axe-nomination-result.json) hit a 5 s loopback client timeout twice at host load average about 10, then passed on the third run; all zero violations |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven; owner-gated | Dated artifacts exist; independent review and hosted CI need the coordinator or owner after any publication |
| Full tier receipt | Not applicable | No src change; `rpi-checks.py --all` not run by instruction |

## Commands

* `python3 -m unittest tests.test_nomination_api_routes tests.test_accessibility_baseline tests.test_content_standard tests.test_nomination_screen tests.test_challenge_no_retaliation_api_220 -q` from `src/api`: 66 OK
* `python3 -m checks.{nomination_route_forms,challenge,nomination}_browser_check --axe <axe-4.10.3> --out <file>`
* Live probes `probe_form.py` ([2026-11-22 copy](issue-1837-live-2026-11-22/probe_form.py)) and `probe_negative.py` ([2026-11-18 copy](issue-1837-live-2026-11-18/probe_negative.py)); credentials read at run time, none printed.
