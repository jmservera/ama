---
title: Issue 120 phase details
date: 2026-11-17
---

# Details

* Phase 1: edit only the Proposal block of decision 7. Keep the original proposal bullets, add `Current build (demonstrator)` bullets and a table of approvals that stay with named humans (DPO, Legal, HR, administrator). Use `*` lists, ASCII.
* Phase 2: the test reads the ADR section between `### 7.` and `## Consequences` and asserts it contains `ZF_TIME_NOTICE_APPROVED`, `ZF_TIME_NOTICE_VERSION`, `request-enable`, `acknowledge` and `different role`. It also asserts these names exist in `timecapture.py`/`server.py` sources so a rename breaks both sides.
* Phase 3: validation commands as in the brief; tests use worktree PYTHONPATH.
