---
title: Issue 1837 standalone nomination forms, live demo re-verification (2026-11-23 r2)
description: Per-criterion record for issue 1837 against main ac58e5c451 and live API revision 0000055
ms.date: 2026-11-23
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Refs #1837. Base `ac58e5c451` (origin/main). Live apps `ca-cutover-test-demo-api` revision `0000055` and `ca-resident-demo` revision `0000027`, both active at 100% traffic. No Azure resource was created or changed and no credential is recorded. Builds on the [2026-11-23 record](issue-1837-live-demo-evidence-2026-11-23.md).

## Result

Main still carries the fix: the standalone route page posts JSON with the CSRF header. No open PR overlaps. No source changed.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three submissions, valid challenge target | Proven (earlier record) | [failing run at 9da3fcd](issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); tests pass on main |
| Valid submissions retain records; JSON callers compatible | Proven locally; live write unproven | [route forms run](issue-1837-live-2026-11-23-r2/axe-nomination_route_forms-result.json) POST 200 x3; a live write would add irreversible records to the shared demo |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven | 66 unit tests OK ([output](issue-1837-live-2026-11-23-r2/unit-tests.txt)); [live probe](issue-1837-live-2026-11-23-r2/live-negative-probe.json): urlencoded 400, no header 403, malformed 400, unknown case 404, mismatch 400, case unchanged |
| Browser journeys with axe, zero unexpected skips | Proven locally, qualified | [route forms](issue-1837-live-2026-11-23-r2/axe-nomination_route_forms-result.json) and [challenge](issue-1837-live-2026-11-23-r2/axe-challenge-result.json) passed first run; [nomination](issue-1837-live-2026-11-23-r2/axe-nomination-result.json) failed twice under host load (loopback client timeout, then a sqlite OperationalError returning HTTP 500 to the harness) and passed on the third run |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven; owner-gated | Dated artifacts exist; independent review and hosted CI need publication, which was not permitted |
| Full tier receipt | Not applicable | No src change; `rpi-checks.py --all` not run by instruction |

## Commands

* `python3 -m unittest tests.test_nomination_api_routes tests.test_accessibility_baseline tests.test_content_standard tests.test_nomination_screen tests.test_challenge_no_retaliation_api_220 -q` from `src/api`: 66 OK
* `python3 -m checks.{nomination_route_forms,challenge,nomination}_browser_check --axe <axe-4.10.3> --out <file>`
* Live probe `probe_negative.py` ([copy](issue-1837-live-2026-11-18/probe_negative.py)) with the API URL read from `az containerapp show`; credentials read at run time, none printed.
