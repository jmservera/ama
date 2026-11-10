---
title: Issue 135 failed-import producer review
description: Single post-implementation review of commit 0de418e34 and routed findings
ms.date: 2026-11-09
---

* Review executed once, 2026-11-09T22:33Z (actual), by the read-only `code-review` agent on commit `0de418e34b4a39b63bc1556ab5f0de7154bcbe71` (base `a04668ae9`). Outcome: Pass with non-blocking findings. No blocking finding. Not repeated in this task.
* Reviewer ran importer tests (59 OK), ruff and mypy; did not rerun the CLI two-process check.

| Id | Severity | Finding | Routing |
| --- | --- | --- | --- |
| 1 | Non-blocking | README says routing keeps version for refusals; the feed keeps version for rejected batches only | Later work: README wording |
| 2 | Non-blocking | Without a digest the ref falls back to the name; two different unhashable files with one name share a row | Later work: document or add size and mtime to the fallback ref |
| 3 | Non-blocking | `stage` does not catch `sqlite3.Error` (traceback instead of exit 2) | Later work |
| 4 | Non-blocking | Rejected-batch note is human free text and is exempt from the no-row-text rule; README should say so | Later work: README wording |
| 5 | Non-blocking | Claim that the unset-staff CLI path was exercised | Not a defect: `CliTests.test_refusal_survives_process_restart_and_view_is_read_only` runs `exceptions` without `ZF_EXCEPTION_STAFF` and asserts `UNROUTED` and `items=0`; the real run in the changes file shows the same output |

Findings are not corrected in this task; they are routed to a later user-selected change so the reviewed head stays the assessed head.
