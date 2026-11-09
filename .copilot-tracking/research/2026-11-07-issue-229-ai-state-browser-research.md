# Research: issue #229, data-operator browser check covers employee AI state distinctions

Disposition: executed (prospective, before any change). Planning Readiness: Ready. Date 2026-11-07. Parent branch test/ux-evidence-149 at 660716929024aefaee420406d0ff9ba060bb613a (tree 041790b85c78a4f71f2bdaeb9b421fb5218f103c); target is the parent, not main.

## Evidence read

* Issue #229 (open): criteria 1 to 3 and 5 ticked; criterion 4 (WCAG 2.2 baseline, textual state meaning, keyboard navigation) stays unticked. Dependencies #152 and #150 present; their human acceptance remains open.
* `src/api/checks/data_operator_browser_check.py` (191 lines): signs in as pam@example.test, opens the Data steward and operator view, checks the page queue and per-home evidence, Tab reach, reflow, no writes. It never opens the exception register, so the AI-state meanings are covered only by Node/VM unit tests (`tests/test_exception_register_screen.py`).
* `src/api/src/zava_forward/api/web/role-screens.js` lines 855 to 950: exception register entry (explicit open link `&exceptions=1`, nothing loaded until opened), `exceptionHappened` (Quarantined vs "Fell back to rules or template" vs "How it failed is Unknown"), `exceptionOwner` ("from configuration, not an appointment"), workflow-only paragraph, placeholder recovery text, unavailable alert "Do not read this as all clear", empty-list "not an all clear".
* `core/exception_register.py` and `exception_feeds.py`: server builds items from `data["recommendations"]` of kind `ai_task`; Quarantined status or mode ai with non-ai source and a fallback reason raise `failed_ai_run`; workflow-only raises nothing. Roles come from `ZF_EXCEPTION_STAFF`. Viewing is audited server-side (not a browser write). Banner is Unknown when no health check.
* Prior art: six earlier #229 slices (`.copilot-tracking/*/2026-11-0[123]-issue-229-*`) and the checker pattern in `design_system_browser_check.main(..., env_overrides=...)`; `test_capacity_browser_check.py` shows a no-Playwright unit pattern.

## Gap

The browser check does not exercise the exception register at all, so keyboard-opened explicit access, distinct state text, unavailable-is-not-all-clear and zero model or write requests are unverified in a real browser.

## Smallest slice

Extend only the checker: synthetic `ai_task` records (Quarantined, fallback, workflow-only), `ZF_EXCEPTION_STAFF` override, a register section (not auto-opened, keyboard open, per-row text, no controls, Tab reach, reflow, no write/model requests) and an intercepted 503 for the unavailable state. Add a no-browser regression test that renders the real `role-screens.js` with the real store contract to prove the expected phrases.

## Limits

Constructed synthetic fixtures; they do not prove a serving model, employee effectiveness, accessibility acceptance, resident consent or named approval. The unreachable "How it failed is Unknown" row (feeds always supply a reason) stays covered by the existing Node test. Real Chromium and axe need coordinator admission to the shared heavy resource; until admitted the browser run is recorded as pending, not passed. web-design-guidelines source fetched but truncated at 3000 characters (partial); no web file is changed. Parent selected-tier, publication, AT and human gates remain pending.
