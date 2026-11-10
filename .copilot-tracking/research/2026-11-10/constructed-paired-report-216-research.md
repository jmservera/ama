---
title: Research - constructed paired observations in the regulatory gate report (Refs #216, #208)
description: Prospective research for one initial operator input-to-report integration of the existing paired-trial scorer
ms.date: 2026-11-10
---

## Task identity

* task_id `issue-216-paired-report-1110`, task_slug `constructed-paired-report-216`
* Branch `feat/demo-constructed-paired-report-216-1110`, pinned main `d52f20a5198de7269f39daf794911545aee01ced`, tree `a817c8480a08e319fcd5466d59ba5e6564af360f`
* Refs #216 and #208 only. No whole-issue closure. Research disposition: `executed`.

## Sources read

* Root admission `issue216-report-admission-1110.json`: fresh OPEN body and all three comments (2026-10-27, 2026-10-31, 2026-11-04).
* Root batch note, section 3 (one initial functional integration, no fresh correction pool, historical correction balances UNKNOWN).
* Repository: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md` (index), `docs/reference/memory.md`, `src/README.md` (commands, validation tiers), `src/agents/README.md` (gate and paired-trial sections), `src/agents/pyproject.toml`.
* Code: `src/agents/evals/run_regulatory_gates.py`, `src/agents/src/zava_forward/agents/paired_trial.py`, `src/agents/src/zava_forward/agents/regulatory_gates.py` (`comparison`), `src/agents/tests/regulatory_gate_fixture.py` (`run`), `src/agents/tests/test_paired_trial.py`.
* This is CLI and data only. No web work, so the web guidance is not engaged.

## Lineage check (stop condition)

* The 2026-11-04 comment says "no further non-human slice remains". It lists #355, #506, #632, #684, #834, #890 and #963 and predates the specific source finding below. No comment owns or exhausts an operator input-to-report consumer for the paired scorer.
* `gh pr list --state all --search "216 in:title"`: seven merged PRs (#355, #632, #684, #834, #890, #963, #1119), none open, none about a report consumer. No open PR matches "216".
* Local branches `feat/issue-216` and `feat/issue-216-r3` are ancestors of main (merged, no retained unmerged attempt). No remote 216 branch. Only worktree for 216 is this one.
* Repository search for `constructed-paired`, `paired-observations`, `paired_observations` (all file types, excluding `.git`): no hits.
* `evaluate_paired_trial` callers outside its own tests: none (`grep -rn` over `src` and `tools`; the only non-test hit is the definition at `paired_trial.py:172`).
* Conclusion: no retained attempt and no equivalent exists. Proceed as an initial slice.

## Baseline (prospective, before any source change)

Environment: Python 3.12.3, venv at `/home/azureuser/source/ama-demo-wt/.venv-issue216-1110` (outside the worktree), `pip install -e src/core -e "src/agents[dev]"`, ruff 0.17.1 and mypy 2.4.0 (declared pins in `src/agents/pyproject.toml`), origin `https://github.com/jmservera/ama.git`.

Command (from repository root, `PYTHONPATH="$PWD/src/core/tests:$PWD/src/agents/tests"`), with a prepared six-row constructed input at `/tmp/b216/obs.json` (one participant per role, cards and chat arms):

```text
python3 src/agents/evals/run_regulatory_gates.py --constructed-paired-observations /tmp/b216/obs.json
usage: run_regulatory_gates.py [-h] [--homes HOMES] [--record RECORD]
run_regulatory_gates.py: error: unrecognized arguments: --constructed-paired-observations /tmp/b216/obs.json
exit=2, stdout 0 bytes
```

* The same refusal occurred for the earlier probe name `--paired-observations` (exit 2, 0 bytes). The command has no supported input or output integration for paired observations.
* Default invocation `python3 src/agents/evals/run_regulatory_gates.py` (exit 0, about 9 s): output sha256 `8f97a758c61fbc82a149c4644d5ae0072ab1c0fd598ff6c59b2677a0ea973f7c`, byte-identical to the committed `src/agents/evals/regulatory_gates_results.json`.
* Its only paired content is `comparison`, from `regulatory_gates.comparison(paired)`: `status: not_evaluated`, all `measurements` None, `ship_recommendation: cards_only`, Unknown economics. It never calls `evaluate_paired_trial`.
* Source hashes at baseline: `paired_trial.py` `85450ae64373dcfb60fb1cdca22ab9e7083d1b72daaa140758687c2e9ddd7736`, `run_regulatory_gates.py` `f8fef61cd18bbc60102bc5e1c15d66c0fa3a49c947c6116be43f4937f0eea1a9`, `regulatory_gates.py` `722b26f3a99afa2dab272e2129d928d8d66019972afbd1733446ed4e8ebbb35a`.

## Scorer contract (unchanged, read-only)

* `evaluate_paired_trial(observations, *, thresholds=None, cost_inputs=None, now)` returns `check`, `status` (`measured` or `not_evaluated`), `pairs`, `per_role`, `invalid_observations`, `unpaired`, `hazard_misses` (critical), `threshold` (gaps), `economics`, `ship_recommendation`, `reasons`, `approval`.
* Observation fields: `participant`, `task` (non-empty strings), `role` in repairs, housing, grants, `arm` in cards, chat, booleans `completed`, `comprehension_correct`, `accepted`, `hazard_missed`, finite non-negative `elapsed_seconds`, `review_seconds` (booleans rejected as numbers).
* The scorer silently excludes invalid rows into `invalid_observations`; for an operator input that would be a success-shaped fallback, so the command must validate and refuse before calling it.
* With `thresholds=None` the result is always `unset_pending_owner_agreement` and `cards_only`. With `cost_inputs=None` economics is `Unknown` with the five named inputs plus `price_source.*`, `usage.*` and "no human-accepted chat checks to divide by" when applicable. `now` is only used by the authority check, which cannot run without cost inputs.

## Conventions found

* Operator commands signal bad configuration with `raise SystemExit("explicit message")` (for example `src/api/.../auth.py`, `src/core/.../mssqlstore.py`): message on stderr, nonzero exit. Argparse errors exit 2.
* Existing bounded-JSON limit pattern: `regulatory_usage.MAX_BYTES = 256 * 1024`.
* Report keys are sorted JSON; the report `version` is `regulatory-evaluation-gates-v1`; exit status is process execution, not a verdict.
* Test fixtures: constructed rows as in `test_paired_trial.row/trial`; command tests need `PYTHONPATH` of core and agents test directories.
* `mypy` config covers `src` and `tests` only; `evals/` is covered by `ruff check .` but not by configured mypy.

## Findings and decisions for planning

* Input option: `--constructed-paired-observations PATH`. Envelope `constructed-paired-observations-v1` with exactly two keys `schema` and `observations`. The schema name is the caller-declared constructed provenance.
* Output: one new distinct top-level section `constructed_paired_observations` only when opted in, holding schema, input sha256, byte and observation counts, an explicit unverified-participation qualification and the unchanged scorer result.
* Existing `comparison`, `answers`, `deterministic_baseline` and `not_evaluated.staff_comprehension` remain unchanged and are not merged with the supplied data.
* No threshold, price, budget, authority or approval input. Scorer called with `thresholds=None, cost_inputs=None`.

## Risks and unknowns

* A constructed file with `accepted: true` is not human acceptance; the scorer reports it as `chat_accepted` and `accepted_checks`. The section qualification names this and the plan adds a test for the wording.
* `--record` writes whatever the report contains. With opt-in, a user could point it at the canonical results file. Existing `--record` semantics are kept; the README warns, and tests use temporary destinations only.
* Unknown: historical correction balances (not assumed); actual staff trial, owner thresholds, graded set and live run remain human or owner work.

## Planning Readiness

`Ready`. Evidence is adequate, no retained attempt, no blocker. Applicable Research gates (lineage, baseline, contract, conventions) pass.
