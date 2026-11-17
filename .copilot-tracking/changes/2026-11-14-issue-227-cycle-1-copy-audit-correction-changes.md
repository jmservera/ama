# Issue 227 Cycle 1: copy audit correction

* Trigger: CI `src-api` failure on `c66222a8d`, `tests.test_content_standard.CopyAudit.test_no_internal_terms_in_web_copy`.
* Research: the guard in `src/api/tests/test_content_standard.py` bans the words gate, hold, provenance, trace, snapshot and envelope on any line, including anchor ids. The failing hazard lines used the id `"hold"`. Table captions and the keyboard check `EXPECTED_REGIONS` were unaffected, so they stay unchanged.
* Plan: use plain-language headings and a non-banned anchor id.
* Implement (`src/api/src/zava_forward/api/web/role-screens.js`, hazard triage screen):
  * Jump link and panel heading "Retrofit pause and release decision" now read "Retrofit pause and restart decision".
  * Anchor id `"hold"` renamed `"restart"`.
  * Jump link and panel heading "Evidence boundary" now read "Evidence and checks" on this screen only.
* Validation: targeted modules (content standard, safety screens, keyboard WCAG, safety panel UX, role screens, design system, specialist keyboard check, accessibility baseline, dependency rule) 94 tests OK; `ruff check`, `ruff format --check` clean. `unittest discover` deliberately not run.
* Review: independent review by the coordinator before push.
