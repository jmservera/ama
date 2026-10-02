<!-- markdownlint-disable-file -->

# Review: rubric-gate-calibration-context

* Task ID: 2026-10-02-rubric-gate-calibration-context (child of 2026-10-02-rubric-gate-docs-accuracy)
* Plan: .copilot-tracking/plans/2026-10-02/rubric-gate-calibration-context-plan.md
* Changes: .copilot-tracking/changes/2026-10-02/rubric-gate-calibration-context-changes.md
* Mode: one pass, read-only (inspection; no commands run)
* Outcome: Conformant with findings

## Target Verification

| Target | Status | Evidence |
|--------|--------|----------|
| RD-001 | Resolved (partial coverage, see RC-001, RC-002) | `test_given_force_when_context_written_then_baseline_withheld` asserts `calibration` is `True` and `baseline == {"source": None, "total": None, "sections": None, "criteria": {}}`, matching `write_context` (`baseline = {}` when `state["force"]`, then `.get()` per key). `make_repo` writes a `source="workflow"` baseline, so the fixture is not bootstrap and the empty baseline is caused by force alone. `test_given_pr_when_context_written_then_diff_base_is_merge_base` captures `main` HEAD before branching, deletes `REMOVED` on `feature`, and asserts `diff_base` equals that SHA and `removed_files == [REMOVED]`. `diff_args` returns `["main...HEAD"]` for `pull_request`, so the `merge-base` branch of `write_context` is exercised. Both tests are valid pytest (`tmp_path` fixture, module-level functions, plain `assert`, Arrange/Act/Assert). |
| RD-002 | Resolved | Inputs step 1 ends "the baseline scorecard with rationale (empty in calibration runs)". Live-criteria rule now reads "Without such evidence keep the baseline score; in bootstrap and calibration runs, score them from the written evidence alone and keep them low when nothing demonstrates live delivery." This removes the conflict with the calibration rule. Lock `body_hash` changed with the recompile; README L27 already describes bootstrap and calibration as scoring from scratch. |
| Model change | Consistent | `claude-sonnet-5` in `engine.model` (rubric-score.md L26) and gate `--model` (L195). Lock: metadata `agent_model`, `GH_AW_INFO_MODEL`, `COPILOT_MODEL` (two jobs), gate `--model`, `GH_AW_ENGINE_MODEL` all `claude-sonnet-5`. No `claude-sonnet-4.6` or `sonnet-4` under `.github/` (workflow, lock, README, scripts, scores). README L74 states the two pin points without naming a model, so it cannot go stale. `latest.json` `model` is `null` (manual seed), so no recorded score depends on the old model. |

## Findings

### RC-001 Low: PR test does not distinguish merge base from base tip

* Location: `.github/rubric/scripts/test_prepare.py` `test_given_pr_when_context_written_then_diff_base_is_merge_base`
* Evidence: `main` does not advance after `feature` branches, so the merge base equals `main` tip. A regression that set `diff_base` to `git rev-parse <base_ref>` would still pass, yet would read deleted files from the wrong commit once `main` moves on.
* Fix: after the `feature` commit, check out `main`, add and commit an unrelated file, return to `feature`, then compute state. Keep `expected` as the pre-branch SHA.

### RC-002 Low: Non-PR `diff_base` remains untested

* Location: same file; `prepare.py` `write_context` `else: diff_base = first`
* Evidence: RD-001's fix asked for the `push` case ("the scores commit for push"). Plan P01-T02 narrowed scope to the PR case without recording the narrowing. The push branch is simple but still unguarded.
* Fix: add a case on `make_repo`: delete `REMOVED` on `main`, `compute_state(root, "HEAD", "push")`, assert `diff_base` equals the `baseline` commit SHA (`git log -1 --format=%H -- .github/rubric/scores/latest.json`). Or record the deliberate scope cut in the plan.

### RC-003 Info: Model swap has not been exercised

* Location: `.github/workflows/rubric-score.md` `engine.model`; changes log Validation
* Evidence: availability of `claude-sonnet-5` for the `agentic-workflows` integrator is asserted from a list in the changes log, not from a successful run ("Not yet re-run on GitHub"). The workflow comment says a model change should expect a rescore.
* Fix: after the next green run, dispatch a forced calibration run to establish comparability under the new model before relying on PR deltas.

## Carried Residuals

* RS-002 still open: validation used a minimal pytest stub (37 passed, 1 skipped). Run `uv run --with pytest pytest .github/rubric/scripts` on Linux or WSL to confirm the two new tests and skip reporting under real pytest.

## Routing

| ID | Severity | Routing |
|----|----------|---------|
| RC-001 | Low | Follow-up, Implement (strengthen test fixture) |
| RC-002 | Low | Follow-up, Implement (one test) or record scope cut |
| RC-003 | Info | Operational: first GitHub run plus forced calibration |
| RS-002 | Carried | Pair with RC-001/RC-002 real pytest run |
