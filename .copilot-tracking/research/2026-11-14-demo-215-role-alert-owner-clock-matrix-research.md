# Research: #215 criteria 1 and 2 role alert matrix (2026-11-14)

Disposition: executed. Planning readiness: Ready.

* Alert card (`regulatoryAlertsPanel`, chat.js) is one shared template: status with text, plain meaning, what was noticed, safe action, decision owner and route, clock and due, source and status. Held values render explicit text ("Unknown", "Unassigned", "No approved clock held").
* Non-colour cues: `state-*` CSS gives each result a distinct glyph and border style.
* Server audiences (`rule_engine.AUDIENCES`): hazard alerts reach Building Safety Liaison, Resident Liaison Officer and Programme Manager; automated-decision alerts reach Coordinator and Programme Manager. Quality Inspector, Grants and Evidence Officer and Programme Support Officer see no alerts by design; suppliers (Contractor) are refused (PermissionError, no law route).
* Siblings cover role guidance copy (wcag_plain_matrix), glyphs (plain_language_noncolour), doubt route. None asserts the five facts per alert per role at API level.
* Observation for follow-up: no alert audience exists for finance/grants, assessor or data-handler roles, so criterion 1 per-role alert content is evidenced only through shared guidance for them.
* Not evidenced: browser, screen reader, staff comprehension. Refs #215.
