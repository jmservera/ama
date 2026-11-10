---
title: Issue 1292 original-load diagnostic plan critique
ms.date: 2026-11-09
task_id: 1292-original-load-diagnostic-1109
---

## Execution

* One critique pass, executed once before implementation, by one `rubber-duck` agent over the research, plan and details. Verdict: Revise. It is the only critique for this task; it is not repeated. The critique agent is not independent of this lane's authors beyond being a separate pass.

## Findings and dispositions (all applied directly, none conflicts with the brief except PC-003 in part)

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | Provenance recorded all `ZF_*` values, which can include secrets | Applied: names only, plus an explicit non-secret value allowlist (details P2) |
| PC-002 | Blocking | Inherited provider and filesystem configuration (`AI_ENDPOINT`, `ZF_DIGEST_DIR`) | Applied: every test process runs under `env -i` with `PATH`, `HOME`, `LANG` and owned `PYTHONPATH`, bytecode, `TMPDIR`, `ZF_DATA` (plan R4, details scripts). Inherited shell had only `HOME`, `LANG`, `PATH` among relevant names |
| PC-003 | Blocking | Pair 2 after a plain reproduction contradicts stop-on-reproduction; plain cannot give the trace | Partly applied: a reproduction in the OBSERVER pair stops at once; a plain reproduction cannot preserve a trace, so the stop rule (stop after a PRESERVED trace) is not yet met and pair 2 stays the one trace attempt inside the two-pair cap. This reading is disclosed in the plan before any attempt and is flagged for the independent reviewer; no equivalence claim |
| PC-004 | Blocking | `SqlStore` wrappers sit below the `errors.append` seam and may not give the full traceback or tie to the appended object | Applied: primary capture patches the test helper `open_store` (called inside `opener` immediately before `errors.append`), records the exception with chain, stack and error codes, re-raises with bare `raise`, matches `repr` to the failing assert, reports an unmatched record as unmatched; recorder faults go to `harness_errors` and never replace the original |
| PC-005 | Blocking | Requiring every import origin under worktree `src` would reject the intended venv `mssql_python` | Applied: project modules must resolve into worktree `src`; third-party into the owned venv (or system site for profile A) |
| PC-006 | Blocking | Venv created only on probe failure but used unconditionally | Applied: the two branches are defined; `$PY` is exactly one recorded interpreter |
| PC-007 | Blocking | Pair 2 gated on text markers | Applied: structured gate (no cap, `Ran N` with N>0, API exit 0, Core PASS or REPRODUCED, no profile mismatch or driver fault) |
| PC-008 | Blocking | `flock` exit 1 versus driver exit 1 ambiguous; holder-check errors unspecified | Applied: `admitted.txt` and `driver-exit.txt` markers; failed holder check stops UNADMITTED; driver fault is HARNESS-ERROR |

## Result

* Plan and details revised in place before the planning commit; research unchanged. No second critique.
