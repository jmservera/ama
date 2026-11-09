<!-- markdownlint-disable-file -->
# Issue 189 SQL/main integration critique (2026-11-09)

One critique of the final candidate plan (independent rubber-duck agent, read-only). Verdict: Revise, six findings. Not repeated for this task.

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | Blocking | Browser command omitted `--axe`; the runner then prints NOT RUN. | Applied: `--axe <verified asset>` is required; NOT RUN is never a pass. |
| 2 | Blocking | A readable but unparseable control has no Stop form. | Applied as a disclosed boundary, no behaviour change: Stop is offered for every parsed control (`3d8a7a012`); an unparseable file is `invalid` and fail-closed. The existing test is read and recorded in P4b; a changed requirement would be a new defect recorded with scope and cycle count before any fix. |
| 3 | Blocking | Malformed bulk requests append an audit entry before the view-only gate. | Disclosed, not changed: audit-only record of rejected input already on main, not an operational mutation; removing it would silently drop a security audit. Listed as a boundary of default-deny. |
| 4 | Blocking | Inherited `ZF_RESIDENT_AZURE_TEST`/`ZF_RESIDENT_MSSQL` could enable real SQL tests. | Applied: unset inherited SQL/Azure variables for every selected run. |
| 5 | Blocking | Merging a moved main would be unreviewed. | Applied: stop and report if `origin/main` is not `8d6f029ca`. |
| 6 | Non-blocking | Simulator start/stop call `store.audit`, which may use SQL. | Applied: "no SQL path" qualified; actual SQL stays unverified. |

Reviewer confirmed gate ordering, separate web regions and that selected modules exist.
