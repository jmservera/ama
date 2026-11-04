<!-- markdownlint-disable-file -->
# Research: Resident demo UX redesign implementation (Refs #462)

Task slug: `resident-demo-ux-462`. Branch `feat/resident-demo-ux-redesign`, target `main`.
Research disposition: `reused` (the owner-approved specification is the research; code facts below re-verified 2026-11-04).
Planning Readiness: `Ready`.

## Inputs

* Owner-approved design: [docs/reference/research/ux/resident-demo-redesign-2026-11-04.md](../../../docs/reference/research/ux/resident-demo-redesign-2026-11-04.md)
* Foundations: design-system.md, wcag-conformance-baseline.md, content-standard.md (same folder).
* Web guidance: web-design-guidelines skill (source fetch recorded in the review file), redesign skill constraints (Fluent 2 preserved, no framework swap).

## Verified code facts

| Fact | Evidence |
| --- | --- |
| Web app is static `index.html`, `demo.css`, `demo.js`, `assistant.js`; CSP `default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'` so inline SVG built with DOM APIs is the only icon route. | `resident_demo/app.py`, `web/` |
| Sign-in keeps `#signin` visible while status loads, clears password before the view loads. | `demo.js` submit handler |
| `<summary aria-label="Your account">Account</summary>` | `index.html` |
| `GET /demo/view` is built by `rs.showcase_view(row)` and lacks `stage` and `documents`. `ShowcaseRow` already carries `stage` and `documents` (`DocumentFacts`). | `core/resident_showcase.py` |
| `POST /demo/assistant` accepts `{topic:"status", use_record:true}` and returns `answer`, `sources`, `label`, `notice`, `help`. Labels: `AI suggestion, not approved`, `AI-generated`, `Summary by rules`, `Summary by rules - AI unavailable: <reason>`, `Summary by rules - AI is not enabled`. No new route needed. | `app.py _assistant`, `aoai.py`, `resident_assistant.py` |
| `test_resident_demo_api.py` asserts the exact top-level view key set. | spec test plan |
| `server.py` routes are untouched, so `test_role_endpoint_inventory.py` needs no change. | spec section on boundary |

## Why sensors do not appear in the live demo (root cause analysis)

1. Repo cause (fixable in source): the generated case body stores the stock link as top-level `synthetic_stock_anchor_id` (`build_mvp_dataset.py` line 255; `stock_fabric.link_report` uses it as the stock home id). The `home` object has no `stock_id`. `resident-showcase.sql` reads only `$.home.stock_id`, so `sensor_home_id` is NULL and `sensors_json` is `[]` for every dataset-derived case. Only hand-seeded test cases with `home.stock_id` link. Fix: derive one `stock_id` in the view with `COALESCE($.home.stock_id, $.synthetic_stock_anchor_id)`.
2. Operational cause (not fixable in repo, Azure not touched): `infra/README.md` records that on 2026-10-29 `dbo.sensor_register`/`dbo.sensor_reading` were absent live, and that the view binds them only when the view is re-applied after the tables exist.
3. Data cause: `sensor_backfill` ends 2026-09-30 (start 2024-10-01 + 730 days), so at the 2026-11-04 demo the latest reading is over 24 hours old. The UI must show the stale state and suppress the forecast; it must not invent fresh data.
4. T-SQL is not compiled by any local check (no SQL Server); source tests assert text only.

## Scope decisions (from the task brief, confirmed)

* Phase 1 PR: spec slices 1, 2, 3 (sign-in loading, icon-only Account, hierarchy, sticky nav, rules summary, optional consented AI summary).
* Phase 2 PR: spec slice 4 (sensors below the important content, forecast, stale/fault states, SQL link fix).
* No Azure access, no deploy, no new routes. No external CDN. Human approval and resident consent boundaries unchanged.

## Not verifiable locally

* Screen-reader, named copy review (#153), real resident usability (#155), live SQL view compile and live data.

## Follow-ups (grounded)

1. Apply the corrected view and load sensor tables live (owner-gated Azure step).
2. Regenerate or extend the sensor backfill to cover the demo date so data is not stale.
3. Human review of resident-facing copy (#153).
