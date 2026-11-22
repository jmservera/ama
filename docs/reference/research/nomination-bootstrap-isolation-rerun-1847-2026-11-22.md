---
title: Nomination test bootstrap isolation, re-run on main 3219004e90 (#1847)
description: Third fresh-process re-run of the #1847 acceptance criteria on main 3219004e90 on 2026-11-22, with proven and unproven items for the synthetic demo
ms.date: 2026-11-22
---
# Nomination test bootstrap isolation, re-run (#1847)

Scope: test-only issue. The fix is on main in 7de4a8110 (#1849) and the layout contract is in `src/core/README.md` ("Nomination test layouts (#1847)"). This note repeats the [earlier 2026-11-22 proof](./nomination-bootstrap-isolation-proof-1847-2026-11-22.md) on head 3219004e90. No Azure resource was used, no source or test file changed (the test file was reverted temporarily for the adverse run, then restored), and no secret was read. Raw outputs: [evidence folder](./nomination-bootstrap-isolation-proof-1847-2026-11-22-rerun/).

## Method

* Source layout: from `src/core/tests`, `PYTHONPATH=../src:../../agents/src:.`.
* Noneditable: `pip install --no-deps --target <tmp>/site` of core and agents, `PYTHONPATH=<tmp>/site:.`.
* Editable: throwaway venv with `pip install --no-deps -e` of core and agents; distribution metadata `zava-forward-core 0.1.0` listed.
* The [probe](./nomination-bootstrap-isolation-proof-1847-2026-11-22-rerun/identity-probe.py.txt) imports both test modules in the named order in a fresh process and prints origins and identities. Temporary directories were outside the repository and removed.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Layouts, metadata, rejection documented | Proven | README section above; probes match it. |
| 2 | Both orders in fresh processes per layout; unsupported rejects without mutation | Proven | Source: bulk-first 55 OK, nomination-first 55 OK ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-22-rerun/source-output.txt)). Editable: both orders imported ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-22-rerun/editable-output.txt)). Noneditable: nomination-first imports from `src/`, bulk-first rejected with `unsupported layout` ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-22-rerun/noneditable-output.txt)). |
| 3 | Origins and identities observed | Proven | `store_file` under this worktree's `src/core/src`; `conflict_same`, `gate_same`, `store_same`, `patch_target_same` all true in supported runs. That the original purge splits class identity remains inferred from the failures. |
| 4 | Regression fails on original, passes with fix | Proven | Original bootstrap (7de4a8110^), noneditable, bulk first: 55 tests, failures=1, errors=20 ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-22-rerun/adverse-output.txt)). Fixed: 58 OK including `test_nomination_bootstrap`. |
| 5 | No family purge, foreign checks kept | Proven | `sys.modules` is only scanned read-only in `test_nomination_route.py`. |
| 6 | Complete local gate and external full receipt | Unproven | `rpi-checks.py --all` is forbidden by the brief and no source changed, so the FULL tier is not triggered. The owner decides whether a receipt is needed before closing. |

Use `Refs #1847`, not a closing keyword. Full Core/API failures named in the issue were not rerun.
