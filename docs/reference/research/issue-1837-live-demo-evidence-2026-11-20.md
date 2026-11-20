---
title: Issue 1837 standalone nomination forms, live demo evidence (2026-11-20)
description: Per-criterion record for issue 1837 with live no-write browser proof on the redeployed demo and local axe re-runs
ms.date: 2026-11-20
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Refs #1837. Base `7c5aca476`. No Azure resource was created or changed and no credential is recorded. Builds on the [2026-11-18](issue-1837-live-demo-evidence-2026-11-18.md) and [2026-11-19](issue-1837-live-demo-evidence-2026-11-19.md) records.

## Finding

No defect remains and no source changed. Since 2026-11-18 the demo (`ca-cutover-test-demo-api`, revision 0000035) serves `/nomination-routes.js`, which closes the earlier "live image lacks the script" gap. A real browser submit of the live challenge form with empty fields posted `application/json` with `X-ZF-CSRF`, and returned field validation ([screenshot](issue-1837-live-2026-11-20/live-form-submit.png), [probe](issue-1837-live-2026-11-20/probe_form.py)), not the original "Could not read that." The case was unchanged. The earlier local `nomination_browser_check` failure did not reproduce; it now passes.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three submissions, valid challenge target | Proven | [2026-11-18 record](issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt) |
| Valid submissions retain records; JSON callers compatible | Proven locally, live write unproven | [route forms axe run](issue-1837-live-2026-11-20/axe-route-forms-result.json) POST 200,200,200; a live write would add irreversible records to the shared demo, so it was not attempted |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven | 66 unit tests OK; [live probe](issue-1837-live-2026-11-20/live-negative-probe.json) |
| Browser journeys with axe, zero unexpected skips | Proven locally | [route forms](issue-1837-live-2026-11-20/axe-route-forms-result.json), [challenge](issue-1837-live-2026-11-20/axe-challenge-result.json), [nomination](issue-1837-live-2026-11-20/axe-nomination-result.json): zero violations; one route-forms `color-contrast` incomplete needs human review |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven | RPI artifacts dated 2026-11-20; review and CI not available to this worker |
| Full tier receipt | Not applicable here | No src change, so FOCUSED; no full receipt run |

## Commands

* `python3 -m unittest tests.test_nomination_api_routes tests.test_accessibility_baseline tests.test_content_standard tests.test_nomination_screen tests.test_challenge_no_retaliation_api_220 -q` from `src/api`: 66 OK
* `python3 -m checks.{nomination_route_forms,challenge,nomination}_browser_check --axe <axe-4.10.3> --out ...`: passed
* Live probes `probe_negative.py` and `probe_form.py` (credentials read at run time, none printed)
