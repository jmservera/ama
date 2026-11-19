# Research: issue 76, fifth live pass (2026-11-19)

Refs #76. Synthetic desktop demo; owner decisions of 2026-11-18 apply. Research disposition: `reused`.

## Question

Which unticked acceptance criterion can be built or proven for the demo? Only one is unticked: "Hazard and safeguarding items show a clock and named owner".

## Evidence reused

* [docs/reference/research/issue-76-live-r4-2026-11-19.md](../../../docs/reference/research/issue-76-live-r4-2026-11-19.md): live read-only probe of revision 0000033. Safeguarding clock (39 elapsed hours, referral and due times, named owner) and hazard clock element with named owner both render. Hazard time values are Unknown because the synthetic hazard record has no `aware_at`.
* `src/core/src/zava_forward/core/taskqueues.py` `hazard_clock` and `project_safety_clock_and_owner`: already implement clock text, fail-closed missing timestamps and fallback accountable owner. Unknown is deliberate; the code never invents elapsed time.
* Existing tests `test_hazard_safeguarding_clock_owner.py` and `test_hazard_safeguarding_clock_owner_76.py` cover them.

## Local re-run

`cd src/core && PYTHONPATH=src:tests python3 -m unittest test_taskqueues test_hazard_safeguarding_clock_owner -q`: 33 tests, OK (2026-11-19).

## Planning Readiness

Ready for a no-source-change outcome. The only gap (hazard time values) needs a synthetic record with an awareness timestamp, which is a data decision for the issue owner; fabricating a timestamp in code would break the fail-closed rule. No live probe was repeated: r4 is the same day and the demo was not changed.
