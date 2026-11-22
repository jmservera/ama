# Changes: issue 619 live re-proof (2026-11-22)

Refs #619. No src change (focused tier). No Azure resource created or changed; nothing to delete.

## Files

* docs/reference/research/issue-619-live-at-consent-evidence-2026-11-22.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/evidence/2026-11-22/issue-619-live/ (drivers, JSON, screenshots)

## Per-criterion table

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Screen reader testing by a person | Unproven (production only) | No screen reader or person; waived for the demo |
| 2 | Keyboard testing by a person | Engineering proof only; person record unproven | Scripted keyboard run on 2026-11-22 passed on case tabs, blocker disclosure, employee chat and resident chat |
| 3 | Zoom testing by a person | Partly proven by proxy | Viewport 683x450 and 320x256 no horizontal scroll; 200 percent root font probe shows chat entry area scrolls inside a 105 px box (limit recorded); no real browser zoom by a person |
| 4 | Consent step with a real resident journey | Proven on synthetic resident only; real journey unproven | Refusal without consent sends no request; tick, ask, untick clears; works-consent statement |
| 5 | #550 consent before data use | Proven for the demo | No /demo/assistant request before ticking; AI now enabled but reported unavailable (usage limit), rules fallback labelled |
| 6 | #552 Fluent 2 and WCAG baselines preserved | Partly proven | axe 0 violations on case view, employee chat, resident panel; Fluent adoption not re-audited |
