<!-- markdownlint-disable-file -->
# Employee chat browser check repair: review (2026-11-03)

Task: `employee-chat-browser-check-530`. Review executed once, inline, over the changes listed in [../../changes/2026-11-03/employee-chat-browser-check-530-changes.md](../../changes/2026-11-03/employee-chat-browser-check-530-changes.md). Independent exact-head review and hosted CI remain required before merge.

Outcome: conformant for scope. The CSS change is small and covered by the passing employee browser legs. Check edits only follow owner-approved behaviour (#568, #812) and keep the focus-visible assertions. The overall shared check is not green.

Findings routed to later work:

* Open, medium: resident chat at 320px wide, Send scrolls out of the viewport (composer content about 660px, capped at 55%); fix under #520, then wire the check into the gate.
* Open, low: the resident log is also short at 320px; revisit after the composer fix.
* Open: criterion 8 stays unmet. Live employee-site verification and owner confirmation of the five agents' names, plus local SQL selectors of the complete gate, are not done.

Assessed boundary: the four source and README files above and `.copilot-tracking/*/2026-11-03/`.
