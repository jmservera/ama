---
title: Nomination test bootstrap isolation, fresh proof on main dcaf271ad3 (#1847)
description: Fresh-process re-run of the six #1847 acceptance criteria on main dcaf271ad3 on 2026-11-22, with proven and unproven items for the synthetic demo
ms.date: 2026-11-22
---
# Nomination test bootstrap isolation, fresh proof (#1847)

Scope: test-only issue; fix on main in 7de4a8110 (#1849), layout contract in `src/core/README.md`. This note repeats the 2026-11-18 proof ([earlier note](./nomination-bootstrap-isolation-proof-1847-2026-11-18.md)) on head dcaf271ad3, 2026-11-22. No Azure resource used, no source or test file changed, no secret read. Raw outputs: [evidence folder](./nomination-bootstrap-isolation-proof-1847-2026-11-22/).

## Method

* Source layout: from `src/core/tests`, `PYTHONPATH=../src:../../agents/src:.`.
* Noneditable: `pip install --no-deps --target <tmp>/site ./core ./agents`, `PYTHONPATH=<tmp>/site:.`.
* Editable: throwaway venv, `pip install --no-deps -e ./core -e ./agents`, `PYTHONPATH=.`; metadata `zava-forward-core 0.1.0` resolved.
* [Probe](./nomination-bootstrap-isolation-proof-1847-2026-11-22/identity-probe.py.txt) imports both test modules in the named order in a fresh process and prints origins and identities. Temporary directories were outside the repository and removed.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Layouts, metadata, rejection documented | Proven | `src/core/README.md` "Nomination test layouts (#1847)"; probes below match it. |
| 2 | Both orders in fresh processes per layout; unsupported rejects without mutation | Proven | Source: bulk-first 55 OK, nomination-first 55 OK ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-22/source-layout-unittest-output.txt)). Editable: both orders imported ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-22/editable-layout-probe-output.txt)). Noneditable: nomination-first imports from `src/`, bulk-first rejected with `unsupported layout` ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-22/noneditable-layout-probe-output.txt)). |
| 3 | Origins and identities observed | Proven | `store_file` under this worktree's `src/core/src`; `conflict_same`, `gate_same`, `store_same`, `patch_target_same` all true in supported runs. That the original purge splits class identity is inferred from the failures, not separately measured. |
| 4 | Regression fails on original, passes with fix | Proven | Original bootstrap (7de4a8110^) temporarily restored: 55 tests failures=1 errors=20; `test_nomination_bootstrap` 3 tests failures=2 ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-22/original-bootstrap-adverse-output.txt)). Fixed: 58 OK. `assertRaises(ConflictError)` kept (`test_bulk_edits.py:114`, `:128`). |
| 5 | No family purge, foreign checks kept | Proven | `sys.modules` appears in `test_nomination_route.py` only as a read-only scan (line 26) and a docstring (line 38). |
| 6 | Complete local gate and external full receipt | Unproven | The brief forbids `rpi-checks.py --all` and no source changed, so FULL tier is not triggered. Owner decides whether it is needed before closing. |

Use `Refs #1847`, not a closing keyword. Full Core/API failures named in the issue were not rerun.
