---
title: Issue 135 C2 changes
description: Corrective changes for the three Medium Functional findings
ms.date: 2026-11-09
---

Correction C2 of five total. Original changes record preserved.

* `mapping.py`: added `preview_bytes` (scan, hash, preview of bytes already read); `preview_file` delegates to it with unchanged checks.
* `exceptions.py`: `_capture` reads a source once, bounded, and returns the digest of the bytes read (replaces `_stable_digest`); hashless refusals get an opaque `source:` identity (path, device, inode, size, mtime) or a per-attempt token; `RefusalLedger.record` takes `identity` and rejects a record with neither digest nor identity; `feed_inputs` carries the identity in the feed `source_name` so feed refs stay distinct and `source_sha256` is None; `Routing.structures` keyed by the feed ref.
* `__main__.py`: schema detection via `sqlite_master`; `stage` and `exceptions` connect inside the try, catch `sqlite3.Error`, close only an opened connection with a guarded close, print one stderr line and exit 2 with no stdout.
* `README.md`: hashless identity and its limits, exit code meaning, the rejected-batch note is not sanitized, refusals carry no version.
* Tests: 12 new (9 red first, 3 passed already as regression guards); one superseded assertion updated (`file:big.xlsx` to `source:` prefix) because it encoded finding 1.
* Not changed: core, store, sqlstore, schema, exception_register, API, UI, other worktrees.

## Evidence

* Red `/tmp/issue135-c2-logs/red.log` (71 run, 7 failures, 2 errors), green `green3.log` (71 OK), `lint.log`, real CLI `cli.log`.
