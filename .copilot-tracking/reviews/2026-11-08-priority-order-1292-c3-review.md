<!-- markdownlint-disable-file -->
# Review: priority order 1292, correction cycle C3

**Executed**: once, after implementation, by the implementing agent (not independent; the coordinator's independent exact-head review remains required).
**Boundary**: C3 diff over `f8e9ea7da`; light SQLite, in-memory and static evidence only.
**Web guidelines**: source refreshed in full before review; `app.js` change is one semantic `p role="status"` with plain text and a next step. No findings.

## Findings disposition

| Finding | Status | Evidence |
| --- | --- | --- |
| F1 High unaudited or mixed evidence shown as confirmed | Addressed (SQLite) | mixed audited/unaudited and unaudited different-timestamp tests; clock-step test stays confirmed |
| F2 High absence of contradiction treated as proof | Addressed (SQLite) | tied `seq`, orphan creation event, edited older row tests |
| F3 High earlier-candidate migrations skipped | Addressed by simulation | prior-batch plus zero-row test; one `review` batch, no second review on reopen |
| F4 High cross-timestamp inversion | Addressed by simulation | C0 audit-inversion test; ordinals unchanged |
| F5 High server boundary and UI | Addressed | direct accept/edit refused, reject allowed, accepted record `relied_on` false, static `app.js` check |
| F6 Medium anchors revalidated | Addressed (SQLite) | same-head new digest and sealed-year append tests |
| F7 Medium BEGIN failure | Addressed (SQLite) | injected BEGIN failure: no ROLLBACK, record and event dropped, later flush and save clean |
| F8 Medium fixture admission | Addressed for admission logic | fake-inspector negatives and positive; real Docker provisioning unexercised |
| F9 Medium unresolved rewrite | Addressed (SQLite) | per-record rows, bounded writes over repeated batches, old list adopted once; SQL scale unproven |

## Residual risks and observations

1. Conservative by design: unaudited legacy rows always leave the employee's newest record unresolved until the named data owner decides; this may flag many legacy employees. No resolution mechanism exists.
2. `seq` is trusted as an insertion signal only inside one backfill batch and only for unedited rows; an audit event is still taken as written with its record when positions agree with another signal.
3. The review of earlier candidates relies on recorded batch and legacy ranges; a database with no such metadata is treated as native.
4. `docker inspect` metadata proves container identity and configuration, not that the listener at the port is that container. No listener was contacted.
5. The rolling-release boundary (old writers during migration) remains a human decision; the fence is not a substitute for draining older writers.
6. Overlap: #1288 also edits `src/core/README.md` and may touch the priority panel; ordering and conflict resolution are the coordinator's.

## Outcome: Conformant for the light tier, with routed open items (not repeated in this task)

1. SQL Server red/green, the two original selectors, ledger-enabled migration, scale and real Docker admission: pending separate admission.
2. FULL local gate with verified external receipt, independent exact-head review, hosted CI, current-base integration: pending.
3. Human decisions: data-owner resolution of flagged records; rolling-release boundary. None claimed or invented.
