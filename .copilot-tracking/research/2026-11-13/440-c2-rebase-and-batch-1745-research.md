# 440 C2 rebase and batch research

* Task: rebase branch (6 commits, base ca7803e85) onto origin/main 3a6362008, cherry-pick 5cb6cf0242 (#202 audit) and 7c2cfd6575 (#157/#104 audit); both are tracking-only, not in main.
* Expected conflicts: docs/reference/log.md, docs/architecture/cutover-reference-inventory.tsv (append-only; keep both, regenerate TSV).
* Checks: test_cutover_audit (9), test_bicep_policy (61), src/agents test_chat_eval, ruff, mypy, link check, secret scrub.
* Planning Readiness: Ready. Disposition: executed.
