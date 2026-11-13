# 521 cutoff verify research (in progress)

Task: verify #521 Criterion 1 at 3b05143: authority end is exclusive 2028-01-01T00:00:00Z everywhere; old cutoffs (2026-11-01, 2027-01-31/02-01) no longer apply. Tracking-only write surface.

Disposition: executed. Planning Readiness: Ready.

## Single source
* src/core/src/zava_forward/core/resident-demo.json:2 maximum_expiry_utc 2028-01-01T00:00:00Z
* src/core/src/zava_forward/core/resident_showcase.py:42 AUTHORITY_END from JSON; :264 `now >= AUTHORITY_END` excludes; :418 session end min(expires, AUTHORITY_END); :628 `expires > AUTHORITY_END` refused

## Consumers
* infra/scripts/resident_demo_secrets.py:46,51 MAX_EXPIRY = AUTHORITY_END
* infra/scripts/resident_showcase_sql.py:24,35 renders {{AUTHORITY_END}}
* infra/sql/resident-showcase.sql:21,37 CHECK valid_to <= '{{AUTHORITY_END}}'
* infra/resident-demo.bicep:36,38 loads same JSON; expiresAt epoch <= maximumExpiry
* src/api/src/zava_forward/api/resident_demo/app.py:130 min(expires_at, AUTHORITY_END)
* src/api/checks/resident_demo_browser_check.py:8,113,127; resident_demo_image_check.py:144; resident_sensors_browser_check.py:45,281,290 use rs.AUTHORITY_END (no literal)
* resident_demo_deploy.py delegates to secrets_helper.parse_expiry; verifier has no date literal

## Tests
* core test_resident_showcase.py:88-103,438-500 (old values refused, 2028-01-01 accepted, +1s/+1ms refused)
* core test_resident_showcase_sql.py:203-207,639-666 (renderer checks always run; DB checks need MSSQL)
* api test_resident_demo_check.py:83-107; test_resident_demo_api.py:417-441,827
* infra test_resident_demo_secrets.py:225-241; test_resident_demo_deploy.py:341-342; test_resident_assistant.py has no cutoff literal

## Docs
* infra/README.md:4267,4298,4397,4439,4519-4545 state 2028-01-01 exclusive; 4559-4575 historical cost comparisons
* infra/README.md:4614-4621 (dated 2026-11-04) says live move Pending; :1590 later records live app expiry changed to 2028 (dated history)
* src/api/README.md:5630,5676 state 2028-01-01
* Remaining 2026-11-01 hits (api README 1835-1983, ai_consumption*) are the independent model tariff cutoff, intentionally separate.
