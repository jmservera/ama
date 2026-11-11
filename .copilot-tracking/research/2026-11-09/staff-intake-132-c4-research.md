<!-- markdownlint-disable-file -->
# Research C4: intake integrity defects (#132)

* Disposition: executed 2026-11-09T23:04Z. Planning Readiness: Ready.
* Cycle: corrective C4 of five total. Prior cycles 1 to 3 remain spent and are not reset. One remains after C4.
* Old head `a4bc4507d3192d00144885a55d20b9a5ea0f082b`, base `a04668ae9`. Parent `feat/demo-quality-workflows-89-1109` stays local; current main is not merged or rebased.
* Evidence read: coordinator-root `independent-132-staff-intake-1109/` functional-findings.json (REQUEST_CHANGES: 3 High, 1 Medium), metadata.json, read-ledger.json; the original RPI review (preserved unchanged); web guidelines fetched fresh and read in full (8055 bytes, sha256 `d246b026...0e38234`).

## Findings and source evidence

1. Resident binding missing (High). `staff_intake.capture` calls `submit_quality(...)` with no `context_revision`, so `rec["resident_binding"]` is `None` (`quality.py` submit_quality, binding block). `accept_quality` then calls `require_resident_clear(c, [])`, and `_resident_decision_gate` returns "Resident scope is unknown" for an empty list (`resident_decisions.py` ~708-711). Nobody can accept. Replacement also fails ("Bind replacement evidence..."). The prior self-review test failed at that gate, so it never proved downstream independence.
   * Available source of truth: the current work order version `resident_bindings` (list of `measure`, `context_revision`), the same list the pack's measures come from (`procurement._wo_view`), and `resident_decisions.current_context(c, measure)["revision"]`. `submit_quality` already validates through `require_context`.
   * Existing fixture: ZF-3 carries synthetic scope revision 1 and a synthetic supplied resident acceptance (`dataset.supplied_resident_fixture`), documents and signoffs; work order WO-0001 is issued with `RESIDENT_BINDINGS`. Independent QA user is `quil`. No waiver or real consent is needed.
2. Correction not propagated (High). `correct` appends to `field_receipt.corrections` only; `rec["items"]` (read by `evidence_gaps`, `require_quality_evidence` and the QA workspace) keeps the original note. Items are `dict(label, evidence)`. Fix inside the same `_quality_operation` block, before `store.save()`.
3. Absent digest defaulted (High). `body.get("pack_digest") or pack["pack_digest"]` makes the stale check vacuous. Digest is a sha256 hex (`job_pack._digest`, 64 lowercase hex). The replay comparison keys (`order`, `measure`, `notes_digest`, `confirmed_by`) do not include the pack digest, so replay can be decided before the digest is required.
4. JS duplicate trap (Medium). `staff-intake.js` capture task throws on `outcome === "duplicate"`, so `intakeForm` never reaches `rerender`. The re-render goes through `roleScreensView()` which reloads and repaints, so a notice must be held in module state and rendered in a `role="status"` live region.

## Constraints and decisions confirmed

* Staff-only synthetic slice. Worker confirmation is a synthetic attestation, not consent. No new identities, escalation write authority, permissions, acceptance authority, contract, payment or resident action. AC5 stays an explicit gap.
* Stay inside 132-owned modules and hooks (`staff_intake.py`, `staff-intake.js`, its tests). No quality.py, server.py or shared-file change is expected. 133 stays dedicated-only.
* Order of checks for capture: input validation, duplicate replay by `capture_ref`, explicit valid digest, stale digest (409), pack ready, resident binding (409 when unbound or stale), submit.

## SQL path

No schema change. Correction writes `rec["items"]` and the receipt inside one `_quality_operation` and one save, same optimistic-rowversion case-body UPDATE already exercised on SQLite and MSSQL. Actual SQLite and MSSQL runs are needed for restart readback of the corrected item.

## Resource admission

Heavy gate (`/tmp/ama-rpi-heavy.lock`, browser and MSSQL) only under nonqueued `flock -n` after inspecting the actual holder. 440, 153 or 1238 may hold it; never queue, spin, kill or reuse.

## Risks

* Moving the stale check before the ready check changes which error an old digest on a not-ready pack returns; existing tests will show it.
* Correction note must pass the same 200 character rule so `rec["items"]` never holds a clipped note.
* The cross-process race remains untested (unchanged limit).
