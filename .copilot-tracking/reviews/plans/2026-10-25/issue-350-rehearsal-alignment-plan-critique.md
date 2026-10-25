<!-- markdownlint-disable-file -->
---
title: Issue 350 rehearsal alignment plan critique
description: One independent pre-implementation critique with direct dispositions
ms.date: 2026-10-25
---

Execution: complete, independent read-only `rubber-duck`, before implementation, once. Verdict: Revise.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-101 | Blocking | The mandatory full gate runs `docker pull` and an axe-core download, contradicting "no network test" | Rejected as a conflict with confirmed owner direction: the owner explicitly requires `tools/rpi-checks.py --all`. The "no network test" restriction is read as no probing of the deployed service or Azure/Graph; the runner's own prerequisite fetches are disclosed in the PR body, not skipped |
| PC-102 | Non-blocking | Gate and helper containers could starve owner services (3 GB and 2 GB limits) | Accepted: before each heavy step check free memory and that 8350/8444/8445 and `ama-350-feedback-sql` are healthy; stop the helper if not |
| PC-103 | Non-blocking | Merged MSSQL startup is prospective; needs the full SQL environment contract | Accepted: the Phase 1 outcome is recorded as observed, using the 2026-10-24 `run.sh` contract (`ZF_STORE=mssql`, `ZF_SQL_AUTH=password`, loopback server and port, user, password, `ZF_SQL_TRUST_CERT=1`, `ZF_DATA`, `ZF_STATE`, `ZF_PASSWORD`, loopback bind) |
| S-1 | Suggestion | The retention tool does not constrain new tracking artifacts; the gate needs a clean committed tree | Accepted as stated fact |
