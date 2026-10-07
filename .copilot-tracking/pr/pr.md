# feat(proper-warm): add retrofit application PoC and architecture

Built a runnable synthetic Proper Warm workbench and documented its implemented
local architecture separately from the provisional Azure-led hybrid target.
The PoC is deliberately not a production service or full PRD MVP.

## Changes

### Transactional workbench

* Added nine represented workflows, versioned case/evidence views, lifecycle
  gates, separate demo authorities, handoffs and owned exceptions.
* Added SQLite command/audit/replay transactions, exact retry reconciliation,
  scoped portfolio metrics, JSON export and persistent restart behaviour.
* Added an offline cited-draft simulator with explicit failure/manual fallback.

### Reproducible runtime and documentation

* Added a pinned, non-root, read-only Docker container with persistent named
  volume and loopback-only port 3410.
* Added architecture alternatives, authority/threat/failure/scale/cost
  boundaries, all-criterion rubric gaps, runbook and actual resource ledger.
* Added scoped CI, 39 passing local tests, five passing simulator fixtures,
  runtime/browser/restart evidence and a 28.55ms localhost GET p95 sample.
* Verified the owner's existing synthetic generator in dry-run mode: 980
  candidates, 13 tables and 23,528 rows, zero validation errors. Existing pack
  and private answer keys were unchanged; analytical records were not silently
  converted into operational approvals.

## Related Issues

None.

## Notes

The container was left available locally at http://127.0.0.1:3410.
No Azure or M365 resources were created. Demo roles are local impersonation,
not authentication; reads are not field-private; the assistant is a simulator,
not evaluated model autonomy. Safety, resident contact, payments and grant
submissions have no external effect. Hosted CI/rubric checks remain pending.
The original/addendum, memory, regulatory snapshots and prior prototype were
preserved. Base updates were merged without rewriting history.

## Follow-up Tasks

* Ratify real identity/authority and managed persistence before any cloud ingress.
* Implement reviewed import/quarantine for the generated analytical pack.
* Evaluate a real bounded model against approved evidence and release gates.
