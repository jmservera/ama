---
title: Issue 135 C2 plan critique
description: Single independent critique of the C2 identity and CLI correction plan, with dispositions
ms.date: 2026-11-09
---

* Executed once, 2026-11-09T22:5x-23:0xZ (actual, approximate), by the read-only `rubber-duck` agent against the C2 research, plan, details, source and the independent Functional findings. Not repeated. The original critique is preserved unchanged.

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | State-derived identity (path, inode, size, mtime) can collide after an in-place rewrite that restores size and mtime | Partly accepted. The hashless identity is state-derived by design, because a fresh token for every oversized file would defeat resubmission dedupe. Accepted limit, stated in the README and handoff, not claimed as content identity. Unreadable files, where no state exists, get a fresh attempt token. |
| 2 | Blocking | `sqlite3.Error` from `close()` could replace the exit code with a traceback | Accepted. `_close` swallows `sqlite3.Error`; test mocks a failing connection and close and asserts exit 2, empty stdout and one error line. |
| 3 | Non-blocking | Fresh token on read failure defeats resubmission dedupe for unreadable files | Accepted as an explicit trade-off: each unreadable attempt is its own record, never merged by name. README states it. Test asserts unlike unreadable paths differ. |
| 4 | Non-blocking | Reading limit plus one byte needs an explicit overflow refusal | Accepted. `_capture` refuses when more than the limit was read; test patches the stat to look small while the file is larger. |
