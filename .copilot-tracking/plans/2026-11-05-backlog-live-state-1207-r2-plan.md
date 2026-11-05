# Plan r2: correct omission-as-negative-evidence (Refs #1207)

* Original plan and its critique stay unchanged; this corrects independent findings F1 (HIGH) and F2 (MEDIUM) on commit fcf59982.
* F1: evidence model is positive (`--active`), explicit negative (`--inactive`) and Unknown (everything else). Unknown In Progress with no open PR is kept and reported. `--active none` and subset-based demotion are removed. Overlap, closed or unknown numbers and malformed lists abort before any write; messages do not echo input.
* F2: add test_backlog_sync to the existing src-ci.yml step (unittest, ruff check, ruff format, mypy for the new test and tool) and to the existing paths filter; no job, check name, permission or protection change. Replace the implementation-shape worktree test with behavioural tests.
* Critique: not repeated for the task (one-pass rule); corrections are compatible with the confirmed issue scope. Focused tier; no app, SQL, infrastructure or deployment change.
