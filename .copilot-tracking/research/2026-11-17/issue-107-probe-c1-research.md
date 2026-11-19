---
title: Issue 107 old-image SQL probe correction research
description: Original dated research for one bounded correction of the execution-readiness findings on the retained old-image SQL probe
ms.date: 2026-11-17
---

## Status

Opening artifact written before research-open and before any substantive source search. Validation of each finding against actual code is appended below after that boundary.

## Scope

* Child branch `test/assistant-old-image-sql-107`, declared target `feat/assistant-107-integration` pinned 1c9ac230be1dad9a4ecc21975f9ffe0845309fc4, opening candidate db7ad278b505e764b627d095e21f88db6fb622a1.
* Diagnostic, focused tests and README only. No application, store, policy, schema, service, public UI or HVE instruction change.
* Inputs: independent preparatory review (seven blockers, one path mitigation) copied at evidence-107-c1/execution-readiness.json and functional-findings.json; original implementer review under issue-107-old-image-sql is preserved unchanged.
* Historical note: the review's statement that 1837 holds the shared heavy lock is no longer reliable; the actual holder must be checked by the coordinator.
* Retained image sha256:ad99bbb99df321f8d874b0df52ead4b3e24f4fb02c21a2245b278ea1a1e2cf78, Git provenance unknown, never inferred from a tag.

## Findings under validation

1. Host networking (probe line 80).
2. Incomplete observations accepted (315-326, identity/task checks, ignored exits).
3. Cross-time SPID uniqueness (279-283).
4. Later step errors erase earlier violations (262-266).
5. Cleanup errors and ambiguous create (744-749).
6. Token ceiling and consumption not compared (361-367).
7. No wall-clock deadline for host SQL (705-713).
8. Lexical output containment (598-603).

## Evidence boundary

This runtime has no Docker socket and no SQL. Only current-source SQLite self-test, unit tests with fakes and static checks can run here; none is actual old-image evidence.

## Validation against actual code (after research-open, seq 2)

Read in full: `src/api/checks/old_image_sql_probe.py` (773 lines), `old_image_worker.py` (258), `tests/test_old_image_sql_probe.py` (331), the README section, `src/core/tests/sqlguard.py` (admission) and `_Conn`/`connection_string` in `src/core/src/zava_forward/core/mssqlstore.py`. No Docker, SQL or image was run.

| # | Finding | Code evidence | Disposition |
| --- | --- | --- | --- |
| 1 | Host network | `worker_create_args` emits `--network=host`; `sqlguard._verify_container` only needs the loopback publish | Accepted with one refinement. An internal-only network cannot publish ports, so the SQL container keeps the default bridge (loopback publish, needed by the independent host connection) and is also connected to the private internal network with an alias. Workers attach only to the private network. |
| 2 | Missing observations accepted | `first(..., {})` defaults; no check of module set, `missing`, return code, task ids or the exact `executed` entry | Accepted. Fixed protocol table plus typed validation; malformed or missing evidence is INSUFFICIENT. |
| 3 | SPID uniqueness | `spids` rule in `judge`; worker samples `@@SPID` in a short transaction that closes | Accepted. The rule is removed; container identity (id plus hostname equal to the short id) and the separate host process remain; the limit is stated. |
| 4 | Later error erases violation | `judge` returns at the first non-ok step; `scenario` and `actual` drop observations on exceptions; the worker `main` replaces partial output with `status=error` | Accepted. Adverse checks run on partial observations first; the worker keeps its partial record on error; `scenario` writes into a caller-owned record and catches every error. |
| 5 | Cleanup | `cleanup` swallows failures and `actual` ignores unremoved ids; the create timeout path does not track a daemon-side container | Accepted. Names are registered before create; reconciliation by exact name plus both run labels; per-resource report; exit never 0 with unresolved cleanup. |
| 6 | Token pool | only `calls` and `used_calls` compared | Accepted. One well-formed four-column row; ceilings and both consumption columns compared against `after_remaining`. |
| 7 | No deadline | `MssqlDb` and the readiness loop call the driver directly; `subprocess.run` captures unbounded output | Accepted with a stated limit: a call blocked inside the native driver cannot be killed, so it runs on a daemon thread, is abandoned at its deadline, the owned SQL container is removed by cleanup, and the process exits with `os._exit` after reporting. |
| 8 | Output path | `new_output` is lexical and creates parents | Accepted. Parent resolved with symlinks, leaf created exclusively with `mkdir`, canonical location re-checked and reported. |

## Planning Readiness

Ready. Research disposition: executed. Fidelity: all corrections are verifiable here only by fake-driven unit tests and the current-source SQLite self-test; actual Docker network, label filters and old-image behaviour remain unobserved.
