# Research: #216 paired-report field-count Low finding

Disposition: executed. Planning Readiness: Ready.

* PR #1379 final note: Readiness approved with one nonblocking Low README wording follow-up about the field count and identifier description.
* `src/agents/README.md` (section "Constructed paired observations in the report") says "exactly the nine scorer fields" but lists ten: participant, task, role, arm, completed, comprehension_correct, accepted, hazard_missed, elapsed_seconds, review_seconds.
* Code truth: `OBSERVATION_KEYS = {participant, task, role, arm, *BOOLS, *SECONDS}` in `src/agents/evals/run_regulatory_gates.py`; `ID_PATTERN = [A-Za-z0-9][A-Za-z0-9._-]{0,63}`, so an id must start with a letter or digit.
* README also says ids are "letters, digits, `.`, `_`, `-`, at most 64 characters", omitting the first-character rule.
* Behaviour is correct; the defect is documentation only. No behavioural RED test applies; a test that restates README text is excluded by repo test guidance.
