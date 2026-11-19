# Changes: issue 130 live audit run 5

Docs only; no `src/` change. Tier FOCUSED. Order deviation, recorded honestly: the live probes, offline tests and the research note draft ran before the plan and details files existed; the witness `implement-start` is called after this file but the note edits predate it.

## Files

* `docs/reference/research/issue-130-live-r5-nomination-route-audit-2026-11-18.md` (new)
* `docs/reference/README.md` (index line), `docs/reference/log.md` (entry)
* `.copilot-tracking/evidence/2026-11-18/issue-130-live-r5/` (probe scripts, outputs, digest, tests, route view)
* `.copilot-tracking/{research,plans,details,critiques,changes,reviews}` run 5 files and the state file

## Per-criterion result

| Criterion | Result |
| --- | --- |
| Representative participation and comprehension need authorized human evidence (only unticked) | Unproven; cannot be proven for the demo (needs real representatives; no confirmed authority in demo; person-run testing excluded) |
| Original account, source, channel kept | Proven offline; live write refused 403 (unproven live) |
| Acknowledged route and named owner | Proven offline; live owner list read only |
| Challenge/correction with competing evidence, reviewer, outcome | Proven offline; live write unproven |
| Correction re-reviews dependents only | Proven offline; live unproven |
| Hazard routes to #85 | Proven offline; route text read live |
| Non-response/support never lower priority; unknown not none | Proven offline; null hazard refused live |
| Tests for wrong identity, limited authority, manual route | Proven offline |
| Nothing sent, booked or approved automatically | Proven live (no write succeeded) |
| RAI challenge/explanation/non-digital route criteria | Offline proven; panels read live |

## Validation

* Live: revision `--0000032`, digest unchanged; 6 write attempts all refused; 0 records after; resident app has no nomination route (5 paths).
* `src/core` 3 modules: 66 tests OK (1 skipped). `src/api` 3 modules: 17 tests OK.
* Secret scan of evidence and note for the three credential values: no match. mypy/ruff not applicable (no source change). `rpi-checks.py --all` not run, by instruction.
* Not proven: live write path (403 identity control, FULL tier to change), OD-41/OD-42, staffed acknowledgement delivery, Azure SQL nomination coverage.
