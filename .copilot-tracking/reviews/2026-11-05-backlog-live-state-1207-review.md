# Review: preserve confirmed active delivery in backlog sync (Refs #1207)

* Execution: one self-review of the full diff before commit (not independent; the coordinator assesses the exact final head). Outcome: no material findings.
* Checked: validation precedes every write; active open issue wins over merged-PR history; closed, open-PR, Done-open and review-needed behaviour unchanged; `none` is the only way to assert nothing is active; mocks never reach live gh.
* Residual follow-ups: wire tools/test_backlog_sync.py into src-ci.yml and ci-affected selection; #1204 coordinator wording (see changes artifact); live-board acceptance and the open criterion on the recurring prompt remain unmet. Criteria 1-4 are covered by offline tests only; criterion 5 needs #1204 and exact-head review.
* Trade-off recorded: without `--active`, a genuinely finished In Progress issue with no open PR stays In Progress until the coordinator supplies activity.
