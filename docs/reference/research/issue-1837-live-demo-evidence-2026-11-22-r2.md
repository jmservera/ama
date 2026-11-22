---
title: Issue 1837 standalone nomination forms, live demo evidence r2 (2026-11-22)
description: Per-criterion record for issue 1837 with a re-proof on demo revision 0000053 and local test and axe re-runs
ms.date: 2026-11-22
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Refs #1837. Base `2893d5098d` (origin/main). No Azure resource was created or changed and no credential is recorded. Builds on the [earlier 2026-11-22 record](issue-1837-live-demo-evidence-2026-11-22.md).

## Main check

Main already carries the fix: the standalone route page posts JSON with the CSRF header (#2110 and earlier). No open PR overlaps issue 1837. No source changed, so this is a focused-tier evidence-only change.

## Finding

No defect. On revision `ca-cutover-test-demo-api--0000053` a real browser submit of the live challenge form with empty fields posted `application/json` with the CSRF header and returned field validation (`Supply every required route field...`), not the original `Could not read that.` ([screenshot](issue-1837-live-2026-11-22-r2/live-form-submit.png), [probe](issue-1837-live-2026-11-22-r2/live-form-probe.json)).

Qualification: that probe reported `case_unchanged: false`. Two controlled repeats (view only; view plus the rejected submit) each showed zero differences in the case JSON, and a read three seconds apart was identical, so the first difference is attributed to concurrent activity on the shared demo, not to the 400 submission. The cause was not isolated.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three submissions, valid challenge target | Proven (earlier record) | [failing-first run at 9da3fcd](issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); the tests pass on current main (66 OK) |
| Valid submissions retain records; JSON callers compatible | Proven locally; live write unproven | [route forms axe run](issue-1837-live-2026-11-22-r2/axe-nomination_route_forms-result.json) POST 200, 200, 200; a live write would add irreversible records to the shared demo, so none was attempted |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven | 66 unit tests OK ([output](issue-1837-live-2026-11-22-r2/unit-tests.txt)); [live probe](issue-1837-live-2026-11-22-r2/live-negative-probe.json): urlencoded 400, no header 403, malformed 400, unknown case 404, body/URL mismatch 400, case unchanged |
| Browser journeys with axe, zero unexpected skips | Proven locally | [route forms](issue-1837-live-2026-11-22-r2/axe-nomination_route_forms-result.json), [challenge](issue-1837-live-2026-11-22-r2/axe-challenge-result.json), [nomination](issue-1837-live-2026-11-22-r2/axe-nomination-result.json): zero violations, outcome passed; one `color-contrast` incomplete in route forms needs human review |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven | Dated r2 RPI artifacts exist; independent review and hosted CI are not available to this worker |
| Full tier receipt | Not applicable | No src change; focused tier; `rpi-checks.py --all` not run by instruction |

## Commands

* `python3 -m unittest tests.test_nomination_api_routes tests.test_accessibility_baseline tests.test_content_standard tests.test_nomination_screen tests.test_challenge_no_retaliation_api_220 -q` from `src/api`: 66 OK
* `python3 -m checks.{nomination_route_forms,challenge,nomination}_browser_check --axe <axe-4.10.3>`: all passed
* Live probes `probe_form.py` and `probe_negative.py` (credentials read at run time, none printed; copies in the [2026-11-22](issue-1837-live-2026-11-22/probe_form.py) and [2026-11-18](issue-1837-live-2026-11-18/probe_negative.py) folders)
