<!-- markdownlint-disable-file -->

# Plan, Changes and Review: rubric-gate-status-correctness

* Task ID: 2026-10-02-rubric-gate-status-correctness (child of 2026-10-02-rubric-gate-rename-encoding)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-gate-hardening-review.md (RH-004 to RH-007)

## Plan and changes (.github/workflows/rubric-score.md and recompiled lock)

* [x] RH-004 `Report initial status` and `Publish verdict` use `(!cancelled())` instead of `always()`, so a cancelled run never posts a status.
* [x] RH-005 context build and upload steps get ids; a failure in either sets `rubric/score` to failure with "Could not prepare the scoring input". Failures later in the agent job are still explained by the conclusion comment.
* [x] RH-006 `Publish verdict` treats `steps.record.outcome == 'failure'` as a failed recording, so a broken `cp`, `commit` or `jq` cannot yield success.
* [x] RH-007 `dismissReview` is wrapped in try/catch with a warning.
* Critique: not dispatched (stated fixes).

## Validation

* `gh aw compile rubric-score`: 0 warnings; lock contains the new conditions and outcome variables.
* Python unchanged (50 passed, 1 skipped from the previous task).

## Review (one pass, inline)

* Outcome: Conformant. RH-004 to RH-007 closed.
* Residual: a cancelled run leaves the earlier `pending` in place until the next run, which is the intended fail-closed state.
* Carry-over: RH-003, RH-008, RH-009; RS-002 real pytest run; first live run.
