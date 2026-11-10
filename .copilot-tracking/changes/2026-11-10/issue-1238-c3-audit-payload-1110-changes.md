---
title: Issue 1238 C3 changes (audit payload provenance)
ms.date: 2026-11-10
---

* Source: `src/core/src/zava_forward/core/resident_decisions.py` adds `_approval_detail` (SHA-256 of canonical JSON over case, request, reservation, attempt, role, bound identity, binding id and digest, and the hash of the evidence reference; no raw evidence text). `_authorization_holds` now requires an audit entry whose detail equals the recomputed value. Legacy generic entries fail closed.
* Tests: three regressions in `src/core/tests/test_resident_decisions.py` (evidence substitution, restamped binding digest, legacy generic audit), inherited by the JSON, SQLite and MSSQL classes.
* Docs: `src/core/README.md` supersession section.
* No store, sqlstore, server, app, schema, roles or Quality file touched; no binding populated.

## Evidence (tests RUN / PASS / SKIP)

| Step (UTC) | Command | Run | Pass | Skip | Exit |
| --- | --- | --- | --- | --- | --- |
| Red 01:00:16 | resident_decisions `-k supersede` | 54 | 29 | 19 (+6 fail) | 1 |
| Green 01:00:36 | same | 54 | 35 | 19 | 0 |
| Module 01:00:52 | test_resident_decisions (JSON, SQLite) | 371 | 239 | 132 | 0 |
| Related | preview 36, journey_store 5, handoff 20, finance 29, priority_order 142 (65 skip) | 232 | 167 | 65 | 0 |
| MSSQL 01:03:13 | `-k supersede -k late_outcome -k forward`, one nonqueued flock, disposable 127.0.0.1 container removed (cleanup exit 0) | 114 | 113 | 1 (SQL replay only, JSON class) | 0 |
| Static | ruff check Core and API clean; ruff format --check on test file; strict mypy Core 283 files, API 211 files | | | | 0 |

Environment: owned venv with core, agents, api editable from this worktree; ruff 0.17.1, mypy 2.4.0. Raw logs in scratch `/tmp/issue1238-c3-1110.VZJlo6`.
