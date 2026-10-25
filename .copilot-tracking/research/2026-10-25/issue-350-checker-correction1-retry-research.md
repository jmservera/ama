<!-- markdownlint-disable-file -->
---
title: Issue 350 checker correction 1 retry research
description: Forward-ordered research for the correction 1 process-failure retry; written before any plan, critique or execution
ms.date: 2026-10-25
---

Process failure (kept visible, not relabelled): the earlier `issue-350-checker-correction1-*` artifacts were written after the code and failing tests, and no critique ran before implementation, despite the explicit instruction. The published receipt for head 16e6d12d is functionally valid but is not merge permission. Those artifacts and their timestamps are left unaltered. This retry is the last for this failure.

Order actually followed in this retry (2026-10-25, starting 07:38Z): research (this file), then plan and details, then one independent critique, and only then checks and one independent review. No source edit has been made before this file.

Evidence read now (head 16e6d12d, `origin/main` 36996d70, clean tree, no ignored files; resident gate PID 768864 running and not touched):

* `tools/check-demo-feedback.py:118-121`: `except RecursionError` sits before `except ValueError` in `load_evidence` and returns a BLOCKED `Verdict`, so a deeply nested file gives a blocked report and exit 2. No broad `except Exception`.
* `tools/check-demo-feedback.py:222-263`: `check_me` accepts the exact role `identity.ADMIN_ROLE_NAME` through a separate branch that requires `app_admin` true, empty `counts`, empty `staff` and the current `work_queues` contract. The shared checks still run for the key set (`ME_KEYS` plus `work_queues` for non-contractors), `account`, `map` and `navigation`.
* Runtime source `src/api/src/zava_forward/api/server.py:371-380`: for the admin role the server passes `{}` counts, adds `account`, `map`, `navigation`, and adds `work_queues` for every non-contractor. `projection.me_payload` returns `user`, `counts={}`, `staff=[]` for that role. The checker branch matches this.
* The checker still reports `admin_account` as not-run, overall can never be pass, and acceptance stays not-accepted.

Possible gaps to evaluate in critique (not assumed): the admin `user` object keys are not compared to the full principal key set; `expect_role` with the admin role string; other recursion sources after parsing. Candidate checks: run the existing 80 tests, run the CLI on a 10000-deep file, and run the admin fixture through the checker.

Residual and unrelated: `src/api/README.md` still mentions `ZF_AUTH_EMAIL_FALLBACK` (removed by PR449); routed, not changed here.
