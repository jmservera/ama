<!-- markdownlint-disable-file -->
# Plan C4: intake integrity corrections (#132)

Research: [staff-intake-132-c4-research.md](../../research/2026-11-09/staff-intake-132-c4-research.md). Details: [staff-intake-132-c4-details.md](../../details/2026-11-09/staff-intake-132-c4-details.md). Critique: [staff-intake-132-c4-critique.md](staff-intake-132-c4-critique.md).

Corrective cycle 4 of 5 total (1 to 3 spent, 1 remains after C4). One coherent change fixing all four independent findings.

## Phases

* [ ] C4-P1 Red tests first: focused regressions for findings 1 to 4 fail on the old head.
* [ ] C4-P2 Core: bind resident scope, propagate corrections, require explicit digest in `staff_intake.py`.
* [ ] C4-P3 Web: treat duplicate as reconciliation in `staff-intake.js`, with live status.
* [ ] C4-P4 Validate: impacted intake, quality, procurement, role, content tests; ruff, strict mypy; actual SQLite then MSSQL and served browser plus axe under one nonqueued owned admission.
* [ ] C4-P5 Review once, record outcome, README and changes record, commit, handoff.

## Success criteria

* Independent QA accepts captured evidence with all real prerequisites satisfied by synthetic fixtures; worker, recorder, corrector and acknowledger are each denied by the real accept path; replacement evidence works after acceptance.
* Latest correction is in `rec.items`, keeps `original_notes` and corrections history, survives restart and is what QA sees.
* New capture without a valid explicit digest is refused with no write; stale digest is 409; valid replay stays ahead of stale.
* Same-ref retry after a lost response shows the existing receipt and acknowledgement action with a non-error status and no extra record.

## Non-goals

No change to quality.py, server.py, projection, escalation write, identities, permissions, acceptance authority, publication or parent integration.
