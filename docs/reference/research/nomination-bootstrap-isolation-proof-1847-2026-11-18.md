---
title: Nomination test bootstrap isolation, per-criterion proof (#1847)
description: Fresh-process evidence for the six #1847 acceptance criteria on main 16880f509, with what is and is not proven for the synthetic demo
ms.date: 2026-11-18
---
# Nomination test bootstrap isolation, per-criterion proof (#1847)

Scope: test-only issue. The fix landed on main in commit 7de4a8110 (#1849) and the layout contract in README commit 354017208 (#1909). This note re-proves each unticked criterion on main 16880f509 with commands run on 2026-11-18. No Azure resource was used or created, no source or test file changed, and no secret was read. Raw outputs are in the [evidence folder](./nomination-bootstrap-isolation-proof-1847-2026-11-18/).

## Method

* Source layout: from `src/core/tests`, `PYTHONPATH=../src:../../agents/src:.`.
* Noneditable layout: `pip install --no-deps --target /tmp/p1847/site ./core ./agents` (a copy outside `src/`), then `PYTHONPATH=/tmp/p1847/site:.`.
* Editable layout: a throwaway venv with `pip install --no-deps -e ./core -e ./agents`; `PYTHONPATH=.` only. Distribution metadata `zava-forward-core 0.1.0` resolved.
* Probe: [identity-probe.py.txt](./nomination-bootstrap-isolation-proof-1847-2026-11-18/identity-probe.py.txt) imports the two test modules in the named order in a fresh process and prints origins and object identity. Temporary install directories and the venv were outside the repository and removed afterwards.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Document supported layouts, source-root and metadata requirements, explicit rejection | Proven | `src/core/README.md` section "Nomination test layouts (#1847)" lists editable install (supplies metadata), source roots on `PYTHONPATH`, noneditable copy only if not imported first, and the `unsupported layout` `ImportError`. The probes below match each statement. |
| 2 | Both orders in fresh processes per supported layout; unsupported layouts reject without partial mutation | Proven | Source layout: bulk-first 55 OK, nomination-first 55 OK ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-18/source-layout-unittest-output.txt)). Editable: both orders imported, all identities true ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-18/editable-layout-probe-output.txt)). Noneditable: nomination-first imports from `src/`; bulk-first is rejected with `unsupported layout` ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-18/noneditable-layout-probe-output.txt)). `test_foreign_module_loaded_first_is_rejected_without_purge` asserts the foreign module is kept, `sys.path` unchanged and the nomination module not loaded. |
| 3 | Observe origins and identities of `ConflictError`, `GateError`, `Store`, patch targets; separate measurement from hypothesis | Proven | Probe fields `store_file`, `conflict_same`, `gate_same`, `store_same`, `patch_target_same` all true in supported runs, `store_file` under this worktree's `src/core/src`. Measurement against the original bootstrap: `KeyError: 'zava_forward.core.bulk_edits'` after the second import, so the family purge removed the module the earlier test still references. That the purge splits exception class identity is inferred from that, not separately measured on the original; the original failure count (1 failure, 20 errors) is measured. |
| 4 | Regression fails on original, passes with fix, keeps second-apply conflict assertion and patch behaviour | Proven | Original bootstrap restored temporarily: `test_bulk_edits` then `test_nomination_route` gave 55 tests, failures=1, errors=20; `test_nomination_bootstrap` gave 3 tests, failures=2 ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-18/original-bootstrap-adverse-output.txt)). With main: `test_nomination_bootstrap test_bulk_edits test_nomination_route` 58 OK. `assertRaises(ConflictError)` remains at `test_bulk_edits.py:114` and `:128`. |
| 5 | No whole-family purge; foreign-module checks retained | Proven | `grep sys.modules src/core/tests/test_nomination_route.py` finds only a read-only scan (line 26) and a docstring (line 38); the pre- and post-import `_foreign_zava_modules()` checks remain. Provenance is shown by `store_file`, not by green status alone. |
| 6 | Focused preflight, complete local gate and verified external full receipt against main | Partly proven | Focused preflight recorded here. The full gate and receipt are unproven: the owner brief forbids `rpi-checks.py --all`, and no source file changed, so the FULL tier is not triggered by this candidate. The issue text asks for it conservatively; the coordinator or owner decides whether to require it before closing. |

## Observations to keep

* The bootstrap does not support a noneditable install imported before the nomination module; that is rejected by design, not repaired.
* Pre-existing full Core/API failures named in the issue were not rerun and are not cleared by this note.
* Because criterion 6 is not met, the pull request linking this evidence must use `Refs #1847`, not a closing keyword.
