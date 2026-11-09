<!-- markdownlint-disable-file -->
# Review: priority order 1292, correction cycle C4

**Executed**: once, after implementation, by the implementing agent (not independent; the coordinator's independent exact-head review remains required).
**Boundary**: C4 diff over `dd8c71ca0`; light SQLite, fake-adapter and static evidence only.
**Web guidelines**: source refreshed (full 8055-character file) before the edit and again before review. The `app.js` change moves one `p role="status"` (a polite live region, plain text, a next step) so it shows for every status and after reload. No findings.

## Findings disposition

| Finding | Status | Evidence |
| --- | --- | --- |
| F1 orphan events, tied sequences | Addressed (SQLite) | orphan plus edit and tied-seq tests flag; agreeing audit and distinct seq confirm |
| F2 C1 `rec_order_backfills` | Addressed by simulation | reviewed without rewriting ordinals; malformed history wholly suspect |
| F3 continuity exports | Addressed | full and limited, Proposed, Accepted, Edited; confirmed record unchanged |
| F4 partial BEGIN | Addressed with fakes only | no open transaction; failed rollback discards the connection; real SQL Server unproven |
| F5 singleton rollback | Addressed (SQLite) | confirmed after native record; two in one batch stay unresolved; other user clear |
| F6 committed reload | Addressed (SQLite, static server check) | `CommittedReloadError` committed outcome; no HTTP-level test |
| F7 reviewed-record warning | Addressed (static) | note outside the Proposed branch; initial GET paints it |
| F8 fixture admission | Addressed for logic | host-bound listener, remote Docker negatives; real provisioning unexercised |
| F9 `ai_task` quarantine | Addressed (SQLite) | failed BEGIN and post-BEGIN failure; unrelated entry kept |
| F10 repeated repair cost | Addressed (SQLite) | at most 8 history rows read against 60 rows |
| F11 review cost | Addressed (SQLite) | 1500 singleton batches reviewed in under 60 statements |
| F12 digest content | Addressed | unreadable and same-size content change invalidate the cache |
| F13 malformed anchors | Addressed | `{}`, array, string, bad count, head and algorithm unusable; startup survives |

Outcome: Conformant for the light tier, with the routed items below.

## Residual risks and observations

1. The proof model is stricter: a clock is never proof, so any employee with an unaudited or edited legacy row has a flagged newest record until the named data owner decides. This may flag many legacy employees.
2. The cutover boundary assumes every writer commits its zero-ordinal rows before the repair; a pre-fix binary writing during the repair window is a release decision.
3. A previous newest record whose flag was written by an earlier candidate is trusted as recorded.
4. The api-suite discovery run has unrelated import errors and proves nothing about the server change.

## Routed work

* Admitted SQL Server red/green, original selectors, ledger migration, scale and Docker admission.
* FULL gate with external receipt, independent exact-head review, hosted CI, integration with #184 and #1288.
* Named data-owner resolution mechanism and rolling-release boundary (human decisions).
