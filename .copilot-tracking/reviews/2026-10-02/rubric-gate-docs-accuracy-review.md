<!-- markdownlint-disable-file -->

# Review: rubric-gate-docs-accuracy

* Task ID: 2026-10-02-rubric-gate-docs-accuracy
* Plan: .copilot-tracking/plans/2026-10-02/rubric-gate-docs-accuracy-plan.md
* Changes: .copilot-tracking/changes/2026-10-02/rubric-gate-docs-accuracy-changes.md
* Mode: one pass, read-only (inspection; no commands run)
* Outcome: Conformant with findings

## Target Verification

| Target | Status | Evidence |
|--------|--------|----------|
| RG-003 | Resolved | `prepare.py` `write_context` sets `baseline = {}` when `state["force"]`, so `baseline.source`, `total`, `sections` are null and `criteria` is `{}`. `compute_state` still holds the real baseline for the decide step only. Prompt Scoring rules add the calibration rule forbidding `latest.json` and its history. README Day-to-Day Use matches (context removed, prompt instruction, file still in repo implied). |
| RG-004 | Resolved | Workflow group appends `format('-{0}', github.run_id)` when `github.event_name == 'workflow_dispatch'`, else `''`. Valid Actions syntax (`&&`/`||` ternary, `format`). Lock L84-L86 carries the same expression in the workflow-level `concurrency`. README states forced runs do not cancel each other. |
| RG-005 | Resolved | README live-criteria paragraph adds the instrument exception (rubric, registry, prompt or scripts), matching `INSTRUMENT_PATHS` (`rubric.json`, `artifacts.json`, `rubric-score.md`, `prepare.py`, `gate.py`), and keeps "moves still need a cited changed artifact file". |
| RG-006 | Resolved | README now says a regression or an invalid scorecard on `main` opens an issue and an agent failure or timeout only shows as a failed run. Matches the Publish verdict script (issue only when the gate ran, `!calibration`, ref `main`) and `report-failure-as-issue: false`. |
| RG-007 | Resolved | `diff_base` is `git merge-base <base_ref> HEAD` for the PR range `<base_ref>...HEAD` (same base Git uses for the three-dot diff) and the scores commit SHA for non-PR ranges; empty when no range exists. Prompt Inputs step 3 uses `git show <diff_base>:<path>`. |
| RS-001 | Resolved | `hide_by_symlink` returns `False` on `OSError`; the test calls `pytest.skip("symlinks are unavailable on this host")` inside the test body, which is valid and reports as skipped. Prior changes log has an appended, dated correction; the original line is preserved. |

## Findings

### RD-001 Low: New context behaviour has no automated test

* Location: `.github/rubric/scripts/test_prepare.py`; `prepare.py` `write_context`
* Evidence: no test calls `write_context`. Force-mode baseline withholding and `diff_base` for PR and non-PR ranges are covered only by the manual smoke test in the changes log. A regression would silently un-blind calibration or break deleted-file reads.
* Fix: add two cases using `make_repo`: force context has null `baseline.total` and empty `baseline.criteria`; `diff_base` equals `git merge-base main HEAD` for `pull_request` and the scores commit for `push`.

### RD-002 Low: Two prompt rules still assume a baseline during calibration

* Location: `.github/workflows/rubric-score.md` Inputs step 1 ("the baseline scorecard with rationale") and Scoring rules, live criteria ("Without such evidence keep the baseline score")
* Evidence: in calibration the baseline is empty, so the live-criteria fallback has no value to keep. The later calibration rule ("Score every criterion from scratch") resolves it by intent, but the agent receives conflicting guidance for B1 to B5 and C2.
* Fix: append "(empty when `calibration` is true)" to step 1 and "outside calibration" to the live-criteria fallback, or state the calibration default for live criteria. Recompile the lock.

### RD-003 Info: Per-run concurrency applies to every dispatch, not only forced runs

* Location: workflow `concurrency.group`; README Day-to-Day Use ("Each forced run gets its own concurrency slot")
* Evidence: the condition is `event_name == 'workflow_dispatch'`, so non-forced dispatches also stop cancelling each other. Non-PR runs never commit, so there is no write race. The README statement is true but narrower than the behaviour.
* Fix: none required. Optionally say "Each manual run".

### RD-004 Info: `diff_base` falls back to an empty string silently

* Location: `prepare.py` `write_context` (`merge-base` non-zero exit)
* Evidence: if `merge-base` fails, the prompt would produce `git show :path`. With `fetch-depth: 0` and `fetch: ["main"]` this should not occur, and `compute_state` already refuses to score when the diff itself fails outside bootstrap or force.
* Fix: optional `logger.warning` on failure.

## Carried Residuals

* RS-002 remains open: validation still used a minimal pytest stub (35 passed, 1 skipped). A real `uv run --with pytest pytest .github/rubric/scripts` run on Linux or WSL is still needed to confirm skip reporting.

## Routing

| ID | Severity | Routing |
|----|----------|---------|
| RD-001 | Low | Follow-up, Implement (two tests); pair with the RS-002 real pytest run |
| RD-002 | Low | Next workflow edit (wording plus recompile) |
| RD-003 | Info | No action |
| RD-004 | Info | Optional with the next `prepare.py` edit |

RG-003, RG-004, RG-005, RG-006, RG-007 and RS-001: closed.
