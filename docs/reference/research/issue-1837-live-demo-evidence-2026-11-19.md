---
title: Issue 1837 standalone nomination forms, live demo evidence (2026-11-19)
description: Per-criterion record for issue 1837 after the target-size repair on the standalone routes page
ms.date: 2026-11-19
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Refs #1837. Base `399e2c011`. Builds on [the 2026-11-18 record](issue-1837-live-demo-evidence-2026-11-18.md). No Azure resource was created or changed, nothing was deployed and no credential is recorded.

## Finding

The first unmet criterion was criterion 4: the standalone routes page had no stylesheet, so axe reported `target-size` (WCAG 2.5.8) on every control, and the browser check only recorded it. The page now links the existing `/style.css`, and the check asserts zero target-size violations.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three browser submissions, valid challenge target | Proven on source | [2026-11-18 failing-first record](issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); tests present on main |
| Valid submissions retain records; JSON callers compatible | Proven locally, unproven live | `tests.test_nomination_api_routes` 8 OK; live write needs a redeploy (production change) |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven | existing tests plus [2026-11-18 live probe](issue-1837-live-2026-11-18/live-negative-probe.json) |
| Browser journeys with axe, zero unexpected result | Proven locally | [axe-route-forms-result.json](issue-1837-live-2026-11-19/axe-route-forms-result.json): three POSTs 200, zero violations, zero target-size violations, `controls_under_24px` empty; one `color-contrast` incomplete (needs human review, not a violation) |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven | `.copilot-tracking` artifacts dated 2026-11-19; independent review and hosted CI not claimed |
| Full tier receipt | Unproven by instruction | src changed so FULL applies; `rpi-checks.py --all` not run |

## Commands

* `python3 -m unittest tests.test_nomination_api_routes` from `src/api`: 8 OK
* `python3 -m unittest tests.test_accessibility_baseline tests.test_content_standard`: 48 OK
* `python3 -m checks.nomination_route_forms_browser_check --axe <axe-4.10.3.min.js> --out axe-route-forms-result.json`: passed
* `ruff format --isolated --line-length 100 --check` and `ruff check` on the three changed files: clean
* `python3 -m mypy` in `src/api`: 7 errors, all in `src/core/tests/telemetry_support.py` (missing `opentelemetry.sdk` stubs in this environment); none in changed files
