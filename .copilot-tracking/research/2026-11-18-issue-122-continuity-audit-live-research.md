# Issue 122 continuity audit, live research (2026-11-18)

Opening note. Scope: the single unticked acceptance criterion of #122, "A witnessed authorized drill exercises suspension, owned communication responsibility and restart". Owner decision 2026-11-18: no drills on live Azure. Evidence is collected below.

## Findings

* One unticked criterion: witnessed authorised drill. Owner decision forbids drills; restart authority (OD-35) is unappointed.
* Constructed drills pass: core `test_operator_suspension_drill` 6 OK; api `test_operator_suspension` 20 OK.
* Live read-only: `/api/continuity` 200 with leftover `SUS-1` (release suspended, no restart), reversed `CHG-1`/`CHG-2`; `/api/continuity/export` 200.
* A prior run of this issue exists (`issue-122-live-*` artifacts, state preserved as `issue-122-live-state-prior-run.json`).

Research disposition: executed and reused. Planning Readiness: Ready.
Note: `docs/reference/research/issue-122-continuity-live-audit-2026-11-18.md`.
