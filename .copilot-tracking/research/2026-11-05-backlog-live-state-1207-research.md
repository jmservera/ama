# Research: preserve confirmed active delivery in backlog sync (Refs #1207)

* Sources read: issue requirements, docs/case_study_48 documents, docs/reference/README.md and memory.md, tools/backlog-sync.py, .github/agents/ama-backlog-delivery-coordinator.agent.md (reconcile paragraph), tools tests (test_check_design_trace.py pattern), src-ci tools steps, prior #608 issue record. Disposition: executed.
* Existing lifecycle: Closed -> Done; open with open-PR reference or a worktree path ending `issue-<N>` -> In Progress; else Todo. No test existed for the tool; the hyphenated filename needs importlib loading.
* Root cause: `live_worktree_issues` regex `issue-(\d+)$` never matches real run worktrees (`issue-79-publisher`, `rpi-80`), and a worktree is not activity anyway. Merged-PR references and a missing upstream do not signal activity or completion either.
* Local discovery of tmux sessions or frozen candidates would be broad process scanning, which the issue excludes. Narrowest correction: an explicit, validated coordinator input.
* Design: `--active N,N|none`. Active open issues -> In Progress. Input absent -> an In Progress issue without an open PR is kept and reported as unverified (never demoted on unknown activity). Input present and omitting it -> Todo (explicit coordinator evidence). Invalid, unknown or closed numbers abort before any write.
* Unknowns: live board behaviour is not testable offline; src-ci does not run tools/test_backlog_sync.py (wiring would touch workflow/ci-affected selection, deferred).
* Planning readiness: Ready.
