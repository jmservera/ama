<!-- markdownlint-disable-file -->
# Details

## Approach

* Per-file helper (unique names `opsOwned`, `assistantOwned`, `simControlOwned`, `intakeOwned`, `panelOwned`): `(message, owner, next) => /Owner:/.test(message) ? message : \`${message} Owner: ${owner}. Next action: ${next}\``. Used for dynamic server `message` sinks so server-owned text is never duplicated.
* Fixed literals get inline `Owner: X. Next action: Y.` clauses. Preserve substrings: `Use the manual route`, `could not be saved`, `Your review was recorded`, `Refresh and check the history`, `Assistance unavailable: Assistance request timed out`.
* Owners: application support (system faults), the signed-in role's team manager (role refusals), the Retrofit Programme Manager or an operator for simulator control.
* Do not touch `safetyPanel` or `app.js`.

## Test

In `test_content_standard.py` add a test that for each of the five files finds the helper plus every notice literal listed, asserts `Owner:` before `Next action:` in fixed literals, asserts every dynamic sink line wraps its message with the helper, and asserts no banned terms.

## Critique dispositions (rubber-duck, verdict Revise, all applied)

* Inventory includes rendered blocked states, not only error sinks: `ops.js` role refusal and unavailable simulation, `simulator-control.js` state descriptions and read-only or unwritable notes, `staff-intake.js` review blocker and not-ready notice.
* Helpers return the message unchanged only when `Owner:` precedes `Next action:`; otherwise they append both clauses. Tests cover partial, complete and incidental messages.
* Next actions are outcome specific: read failures say refresh; possible committed changes say check history first; refusals name the team manager.
* Helpers are file-level and unique per file; extracted-function harnesses in `test_case_journey.py` are run to confirm they still pass; `We could not load ... Try again.` is preserved in `ops.js`.
