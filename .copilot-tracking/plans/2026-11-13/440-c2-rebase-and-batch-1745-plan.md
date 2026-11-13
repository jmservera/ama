# 440 C2 rebase and batch plan

* Phase 1: rebase 6 branch commits onto origin/main 3a6362008; resolve log.md and cutover-reference-inventory.tsv keeping both sides.
* Phase 2: cherry-pick 5cb6cf0242 and 7c2cfd6575 (tracking-only).
* Phase 3: regenerate TSV via zava_forward.core.synthetic.cutover_audit; run test_cutover_audit (9), test_bicep_policy (61), test_chat_eval, ruff, mypy, link check, secret scrub.
* Phase 4: independent code-review, clean commit with trailer, no push.
