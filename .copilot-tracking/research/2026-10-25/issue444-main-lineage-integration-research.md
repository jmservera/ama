# Issue 444 lineage integration research

Date: 2026-10-25. Task slug: issue444-main-lineage-integration. Parent task: issue-444 (2026-10-24 artifacts preserved unchanged).

## Scope

Continue the pre-existing owner-authorised #444 synthetic read-only resident preview. This is not implementation of the unaccepted #441 proposal. No new resident capability, provider, account, upload, messaging or AI. Refs #444 only; no closing.

## Evidence

* Candidate head a3e527fd5a8bfe73a10826ed4e316b98464a0782, base f1e2d830f17558efd868919de1973ea7244a8841. Original independent Review outcome: Conformant with follow-ups (one Medium finding fixed with regression test). Original gate receipt /tmp/rpi-444-gate-final/receipt.json was produced against the old base and is historical only.
* Current origin/main is 36996d70a3f6dbee9df4d16400afd07c3614e69e. Merge base with the candidate is f1e2d830 (candidate is a direct descendant of the old base).
* Main added: Entra-authoritative staff access (#449), ledger-safe SQL column migrations (#450), grant-application-admin CLI (#453), #442 resident design docs, rubric fixes, tracking retention policy (#438).
* `git merge-tree` dry run: one textual conflict, docs/reference/log.md (both sides append entries). docs/reference/README.md and src/core/README.md auto-merge. No overlap in src/api package, tests or the resident modules.
* Shared modules my code imports or calls: `resident_decisions` (current_context, authority_for, case_measures), `Store.appointment_status`, `data_paths`, `insights.STAGE_ORDER`. Main's diffs to these are staff-identity only: resident_decisions gains `identity.is_entra` branches in staff-recorder and challenge-visibility functions; store.py adds the `identity` import and uses `identity.people` in handover suggestions; projection.py adds Application Administrator staff-option cases. None change case, grant, appointment or measure semantics used by the resident boundary. Residents have no staff user object, so identity changes should not apply.
* Staff server.py, auth.py, projection.py, store.py remain unedited by this branch; no substantive shared auth change is expected. If merged tests show otherwise, stop and report.
* Existing services are snapshot-based and must not be touched: employee 8350, residents 8444/8445 (tmux ama-444-resident), ama-350-feedback-sql, data /tmp/ama-444-preview-data. All three ports returned HTTP 200 before any edit. Gate PID 725714 (#350) owns the heavy lock and is not to be interrupted.
* Tracking retention policy (main): keep original RPI records and adverse reviews; no pruning of this branch's artifacts.
* Original browser-check limitation retained: it ran against the old base before the Review fix; the full gate later covered it. It will be re-run on the merged head with a distinct disposable port and data directory.

## Risks

* Semantic drift in resident_decisions Entra branches (low). Mitigation: full core/api suites and resident tests on the merged tree.
* log.md conflict resolution must keep both sides, no rewrite of earlier entries.
* Gate must use the new base 36996d70 or a later main if it moves; any later commit invalidates the receipt.

## Planning readiness

Ready. Disposition: executed.
