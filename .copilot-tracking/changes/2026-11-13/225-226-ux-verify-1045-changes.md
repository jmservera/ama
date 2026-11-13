# Changes: #225/#226 static UX verification

Status: complete. Write surface: .copilot-tracking only (no src/ or docs/ edit). Base 3b05143179f83235c5b4e80e70aad99bdc44d83f. Refs #225, #226, #149, #151.

## Added
* Two prior files copied byte-identically from bfc8ab5c5 (cmp identical; historical, status and conclusions are the prior session's): .copilot-tracking/research/2026-11-13/issues-225-226-finance-asset-readiness-0630-research.md and .copilot-tracking/rpi-sessions/2026-11-13/issues-225-226-finance-asset-readiness-0630-state.json.
* This session's research, plan, details, critique, state, changes and review files.

## Evidence boundary
This is partial static and unit evidence only. It does not complete criterion 4 (manual assistive-technology review) and is not a WCAG 2.2 conformance claim. Keyboard operation and rendered behaviour were not assessed (no browser). The first research-open witness call was refused because the research file did not yet exist; it was recorded OK after the file was written.

## web-design-guidelines source
Fetched https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md: HTTP 200, 8055 bytes, 2026-11-13. Rules applied from that fetch.

## Static audit (src/api/src/zava_forward/api/web/)
Scope: asset-board (role-screens.js:205), finance-invoices (:1315, with financeInvoicePanel :1283, financeEconomicsPanel :1303), grants/funding screen (:1465-1496), helper screenTable (:26) and style.css. HELD_CHECK_ERRORS excluded (#96 D8).

| # | Location | Rule | Result |
| --- | --- | --- | --- |
| 1 | role-screens.js:26-34 | Native table, caption, th scope=col; scroll region labelled and tabindex=0 | Pass (static); keyboard use not assessed |
| 2 | role-screens.js:26-34 | Empty states | Pass: explicit "does not establish readiness" copy |
| 3 | role-screens.js:1300, style.css:301-302 | Non-colour status | Pass: text states (Unknown, Unresolved, Paused, Not checked yet); blocked block has text title plus glyph; 8px left border |
| 4 | style.css:48, :282 | Visible focus via :focus-visible | Pass; no outline:none seen in grep of audited rules |
| 5 | style.css:23, :30 | Reduced motion | Pass for --motion and spinner; transitions at :292-293 use var(--motion), listed properties only |
| 6 | role-screens.js:221, :1328 | Human approval boundary | Pass: "records no investment approval", "makes no payment, approval or decision", Board or delegated owner / Finance approver named as decider |
| 7 | role-screens.js:1293 | Payment boundary | Pass: "This system never makes or releases a payment" |
| 8 | role-screens.js:1339-1345 (fundingFieldRows) | Plain language | Advisory: raw field ids and JSON.stringify values appear in the draft table |
| 9 | style.css:302 | Decorative glyph | Advisory: U+26D4 emitted by CSS content may be announced by some screen readers; not assessed with AT |
| 10 | style.css:330 | content-visibility:auto on .screen-record | Advisory: find-in-page and anchor behaviour for off-screen panels not assessed in a browser |
| 11 | role-screens.js:158, :186, :195, :1306 | Plain language | Advisory: terms "Total Cost of AI", "TCA", "OD-51", "denominator" appear in staff copy; defined in context but dense |
| 12 | style.css:331, role-screens.js:100 | Typography | Pass: tabular-nums on .screen-evidence td (corrected after review) |
| 13 | all | Forms, images, media, autocomplete | Not applicable: read-only views, no form or media here |

No blocking defects found; advisories are routed to follow-up, no source edit made.

## Unit verification
* Environment: /tmp/venv-225-1045 (pip install -e src/core src/agents src/api, exit 0); package paths verified under this worktree (namespace packages expose __path__, __file__ is None); node v24.21.0; PYTHONPATH unset; no browser, Docker or cloud call.
* Command (from src/api/tests): python -m unittest -v test_asset_board_screen test_role_screens test_role_screens_conformance
* Producer exit code: 0 (saved status file). Ran 37 tests: 16 asset board, 9 role screens, 12 conformance; 0 skipped; OK.
* Venv and temp logs removed.

## Follow-ups (advisory, unselected)
1. Plain-language pass on fundingFieldRows raw ids and AI-cost jargon (rows 8, 11).
2. Manual AT/browser review for rows 3, 9, 10 and criterion 4 (human owner).

## Review corrections
Independent review corrected row 3, 6, 7, 8, 11, 12 line citations and withdrew the false row 12 tabular-nums finding; applied above. Review file: .copilot-tracking/reviews/2026-11-13/225-226-ux-verify-1045-review.md.
