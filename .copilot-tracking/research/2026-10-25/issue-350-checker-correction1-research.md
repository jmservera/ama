<!-- markdownlint-disable-file -->
---
title: Issue 350 checker correction 1 research
description: Exact contracts behind two blocking complete-PR review defects in tools/check-demo-feedback.py
ms.date: 2026-10-25
---

Process disclosure: the owner asked for prospective artifacts first. Code reading and the failing regressions were done before these artifacts were written, so the research, plan and critique here are retrospective records, not prospective gates. No separate critique was run before implementation; the single independent review covers the finished change.

Evidence (head 68692817, base 36996d70):

* Defect 1: `load_evidence` catches `ValueError` only. `json.loads` on 10000 nested arrays (20056 bytes, below the 1 MiB limit) raises `RecursionError`, so there was no BLOCKED report and no exit 2.
* Defect 2: `check_me` accepted only staff and contractor roles. `server.py` `/api/me` (lines 371-380) returns, for `Application Administrator`, `projection.me_payload` with `counts={}` and `staff=[]`, the full principal user (`app_admin` true), `account`, `map`, `navigation` and `work_queues` (non-contractor). The checker failed this valid response.
* `admin_account` (fixed administrator live acceptance) has no runtime field and stays `not-run`; overall can never be pass.

Historical reviews and the 68692817 alignment evidence are preserved unchanged. Issue #350 stays open with acceptance unchanged.
