---
title: Issue 1837 standalone nomination forms, live demo evidence (2026-11-22)
description: Per-criterion record for issue 1837 with live no-write browser proof on demo revision 0000045 and local test and axe re-runs
ms.date: 2026-11-22
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Refs #1837. Base `8bc751023`. No Azure resource was created or changed and no credential is recorded. Builds on the [2026-11-20](issue-1837-live-demo-evidence-2026-11-20.md) record.

## Finding

No defect remains and no source changed. The demo (`ca-cutover-test-demo-api`, revision 0000045) serves the route script. A real browser submit of the live challenge form with empty fields posted `application/json` with the CSRF header and returned field validation, not the original "Could not read that." ([screenshot](issue-1837-live-2026-11-22/live-form-submit.png), [probe](issue-1837-live-2026-11-22/live-form-probe.json)). The case was unchanged.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three submissions, valid challenge target | Proven (earlier) | [2026-11-18 failing-first run at 9da3fcd](issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); tests pass on current base |
| Valid submissions retain records; JSON callers compatible | Proven locally, live write unproven | [route forms axe run](issue-1837-live-2026-11-22/axe-route-forms-result.json) POST 200,200,200; a live write would add irreversible records to the shared demo, so none was attempted |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven | 66 unit tests OK; [live probe](issue-1837-live-2026-11-22/live-negative-probe.json): urlencoded 400, no header 403, malformed 400, unknown case 404, mismatch 400, case unchanged |
| Browser journeys with axe, zero unexpected skips | Proven locally | [route forms](issue-1837-live-2026-11-22/axe-route-forms-result.json), [challenge](issue-1837-live-2026-11-22/axe-challenge-result.json), [nomination](issue-1837-live-2026-11-22/axe-nomination-result.json): zero violations, all outcome passed; one route-forms `color-contrast` incomplete needs human review |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven | RPI artifacts dated 2026-11-22; independent review and hosted CI are not available to this worker |
| Full tier receipt | Not applicable here | No src change, so focused tier; `rpi-checks.py --all` not run by instruction |

## Commands

* `python3 -m unittest tests.test_nomination_api_routes tests.test_accessibility_baseline tests.test_content_standard tests.test_nomination_screen tests.test_challenge_no_retaliation_api_220 -q` from `src/api`: 66 OK
* `python3 -m checks.{nomination_route_forms,challenge,nomination}_browser_check --axe <axe-4.10.3>`: passed
* Live probes `probe_negative.py` and `probe_form.py` (credentials read at run time, none printed)
