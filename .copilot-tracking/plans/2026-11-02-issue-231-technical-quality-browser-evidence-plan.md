# Plan: issue #231 browser evidence slice

* [x] Add `technical_quality_data()` synthetic fixture (`src/api/checks/role_screens_fixtures.py`)
* [x] Add stories `231` and `231q` and `check_readonly_accessibility` (`src/api/checks/role_screens_browser_check.py`)
* [x] Document the stories and the `ZF_AXE_JS` option in `src/api/README.md`
* [x] Run the browser stories, focused gate `--changed`

## Critique (one pass, inline)

Verdict: proceed. Findings applied: keep the axe scan optional via an env var and verify the pinned hash, so the check never fetches from the network; do not change production screen code (no defect found); do not claim WCAG conformance. No finding conflicted with a confirmed decision.
