<!-- markdownlint-disable-file -->

# Changes: rubric-gate-calibration-context

* .github/workflows/rubric-score.md and lock: Inputs step 1 says the baseline is empty in calibration runs; live-criteria rule tells the scorer how to score them in bootstrap and calibration runs (RD-002)
* .github/rubric/scripts/test_prepare.py: `test_given_force_when_context_written_then_baseline_withheld`, `test_given_pr_when_context_written_then_diff_base_is_merge_base` (RD-001)

## Out-of-band fix (owner request)

* Run 37022659125 failed: `400 The requested model is not available for integrator "agentic-workflows"` for `claude-sonnet-4.6`. `engine.model` and the gate `--model` argument switched to `claude-sonnet-5` (listed as available); lock recompiled with no remaining references to the old model.

## Validation

* 37 passed, 1 skipped (symlink), minimal pytest stub.
* `gh aw compile rubric-score`: 0 warnings.
* Not yet re-run on GitHub.
