# Research: #225 Finance/grants and #226 Asset/board static UX verification

* Task: 225-226-ux-verify-1045; base 3b05143179f83235c5b4e80e70aad99bdc44d83f; Refs #225, #226, #149, #151.
* Research disposition: executed (bounded, 7-minute budget). Planning Readiness: Ready.
* Read: case study original and addendum, docs/reference README and memory (owner context; not evidence), UX design-system, WCAG baseline and content-standard, web-design-guidelines SKILL, role-screens.js asset-board (registerRoleScreen at about line 205) and finance-invoices (about lines 1240-1340), style.css, tests test_asset_board_screen, test_role_screens, test_role_screens_conformance.
* Prior input path demo-finance-asset-readiness-0630 (bfc8ab5c5, 2 files): existence checked only for path; the 2 .copilot-tracking files are copied byte-identically from git object in the implement phase; renderer source and tests there are not read or run.
* Web Development Guidance: the web-design-guidelines source URL is external; fetch is attempted in Implement and unreachability will be recorded honestly. Skills design-taste/redesign are not applied: no visual change is in scope (read-only audit).
* Initial renderer observations (to be recorded with file:line in changes): screenTable wraps wide tables in a focusable labelled region (native table/caption/th scope=col); status text is textual ("Unknown", "Unresolved", "Paused"), not colour-only; .blocked uses a text title plus a decorative glyph; reduced motion handled in style.css; both screens state no approval, payment or decision is made and name the human decider.
* Limits: no browser, no AT, no WCAG AC4 conformance claim; no src/ or docs/ edit.
