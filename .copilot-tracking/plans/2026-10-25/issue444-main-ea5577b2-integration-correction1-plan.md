# Issue 444 round-3 correction cycle 1 plan

Date: 2026-10-25. Written after the Review and before the correction edit. Parent plan: issue444-main-ea5577b2-integration-plan.md (rebase done, no source edits until Review finding 1).

## Scope

Fix only Review finding 1 (Medium). Wording change in `STAGE_TEXT` for "Survey booked" and "Install booked" in src/core/.../resident_preview.py, plus one regression test. No web change, no other finding.

* [x] Neutral wording: progress "A survey of your home is being arranged." / "Installation is being arranged."; next step "Any confirmed time is shown under Confirmed arrangements, if your page shows it."
* [x] Regression test asserts neither stage text contains "is booked" or "recorded as booked".
* [ ] Resident tests, ruff, mypy, full suites, browser check, then the gate. At most two correction cycles; this is cycle 1.
