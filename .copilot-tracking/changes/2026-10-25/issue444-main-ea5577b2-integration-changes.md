# Issue 444 round-3 changes

Date: 2026-10-25. Records what was done after the prospective research, plan, details and critique.

## Integration

* Backup branch backup/444-pre-round3-ab07351a created, then the run-owned branch rebased onto origin/main ea5577b2 (coordinator-authorised).
* One conflict, docs/reference/log.md: kept main's #458 entry followed by the #444 entry. src/api/README.md auto-merged with both sides kept.
* Resident source and tests were identical to ab07351a after the rebase; no staff file changed.

## Correction cycle 1 of at most 2 (Review finding 1, Medium)

Planned in plans/2026-10-25/issue444-main-ea5577b2-integration-correction1-plan.md before the edit.

* resident_preview.py: "Survey booked" and "Install booked" stage text now says the survey or installation is being arranged, and points to confirmed arrangements only "if your page shows it".
* test_resident_preview.py: new test_booked_stages_do_not_claim_a_booking.
* Findings 2 and 3 (Low web items) and the dataset-restart limitation are routed, not fixed.

## Evidence

* Pre-correction (rebased head): ruff and mypy clean, browser check 36 PASS 0 FAIL.
* Post-correction: ruff, format and mypy clean; resident core tests 32 OK; browser check 36 PASS 0 FAIL on own free loopback ports.
* Full suites: see state file and final report; the exact-head gate is the authority.

## Limits

No human screen-reader audit, accessibility harness not run, Fluent 2 partial, not live Azure/SQL/AI acceptance. The correction was not re-reviewed by a second independent Review (one Review per task); it is a one-sentence wording fix with a regression test.
