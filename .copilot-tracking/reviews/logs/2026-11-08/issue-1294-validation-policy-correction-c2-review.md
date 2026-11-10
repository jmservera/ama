<!-- markdownlint-disable-file -->
# RPI Review: issue-1294-validation-policy-correction-c2

* Review date: 2026-11-08
* Execution status: Complete
* Outcome: Residual work
* Assessed boundary: C2 plan, details, critique (PC-001 to PC-007 applied), changes record, research, src/README.md and docs/reference/log.md diffs, behavior report 3 and sandbox 3. Static and simulated evidence only; hosted CI, runner and browser not executed.

## Artifacts compared

* .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c2-research.md
* .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c2-plan.md
* .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c2-phase-details.md
* .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c2-plan-critique.md
* .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-correction-c2-changes.md
* .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-3.md
* .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-3

## Acceptance assessment

* Independent review F2 (mixed rule): met. src/README.md no longer says every mixed change is full; line 68, the classification paragraph and two labelled mixed rows read strictest applicable; "doubt takes the full tier" kept verbatim.
* F3 (direct --out): met. Statement limited to source-backed facts (runner-only 58 bytes via TMPDIR=<out>/tmp; scratch under ZF_BROWSER_SCRATCH or <checkout>/.venv; short TMPDIR unmeasured).
* F1 (behavior): executed, not satisfied. A fresh full independently designed, simulated and graded run returned Revise (proxy, profile unresolved). Four wording findings were corrected once after grading and were not re-simulated.
* Scope: focused tier; diff limited to src/README.md and docs/reference/log.md plus tracking evidence; no workflow, tool, source or protection changes. Checks recorded: git diff --check 0, link scan 0, ASCII 0, stale grep none, selection reproduction 0.
* Preservation: prior reports, sandboxes, reviews and ignored tools/__pycache__ untouched.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Behavior verdict is Revise; post-grade edits unsimulated
* Evidence: report 3 Findings and Fidelity sections; test-review.md.
* Destination: distinct follow-up (independent exact-head reviewer and owner decide acceptance; a later user-selected run may re-simulate).
<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Proxy run, models not observable; no intended-profile or native claim
* Evidence: run-state.md; report 3.
* Destination: residual work (host cannot bind subagent models).
<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Coverage misses in design (coordinator mixed sentence, chat plus unresolved workflow case, receipt currency)
* Evidence: test-review.md coverage.
* Destination: distinct follow-up.

## Validation and limitations

Hosted CI not observed; nothing pushed. Human review box in report 3 unchecked.

## Next Steps

No user action in this task; coordinator performs independent exact-head assessment.
