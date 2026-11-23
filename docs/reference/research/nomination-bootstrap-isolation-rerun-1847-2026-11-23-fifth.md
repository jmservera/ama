---
title: Nomination test bootstrap isolation, fifth re-run on head ac58e5c451 (#1847)
description: Fresh-process re-run of the #1847 criteria on 2026-11-23 for both test-module orders in source, editable and noneditable layouts; no code gap found
ms.date: 2026-11-23
---
# Nomination test bootstrap isolation, fifth re-run (#1847)

Scope: #1847 is a test-harness issue; the fix is on main in 7de4a8110 (#1849) and the layout contract is in `src/core/README.md` ("Nomination test layouts (#1847)"). This note repeats the [fourth re-run](./nomination-bootstrap-isolation-rerun-1847-2026-11-23.md) on head ac58e5c451. Read-only `az containerapp show` reported latest ready revisions `ca-cutover-test-demo-api--0000055` and `ca-resident-demo--0000027`; nothing was changed in Azure and no secret was read. Raw outputs: [evidence folder](./nomination-bootstrap-isolation-proof-1847-2026-11-23-fifth/).

## Method

* Source layout: `PYTHONPATH=<worktree>/src/core/src:<worktree>/src/agents/src:.` from `src/core/tests`.
* Editable: throwaway venv, `pip install --no-deps -e` of `src/core` and `src/agents`; both distributions listed at 0.1.0.
* Noneditable: `pip install --no-deps --target <tmp>/site`, `PYTHONPATH=<tmp>/site:.`.
* The [probe](./nomination-bootstrap-isolation-proof-1847-2026-11-23-fifth/identity-probe.py.txt) imports both test modules in a named order in a fresh process. Temporary directories sat outside the repository and were removed.

## Results

* Source and editable: both orders import; `store_file` resolves under this worktree's `src/core/src`; `ConflictError`, `GateError`, `Store` and the `bulk_edits` patch target are identical objects across modules ([source](./nomination-bootstrap-isolation-proof-1847-2026-11-23-fifth/source.txt), [editable](./nomination-bootstrap-isolation-proof-1847-2026-11-23-fifth/editable.txt)).
* Noneditable: nomination-first imports from `src/`; bulk-first is rejected with `unsupported layout` ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-23-fifth/noneditable.txt)).
* `unittest` in [both orders](./nomination-bootstrap-isolation-proof-1847-2026-11-23-fifth/unittest-orders.txt): 55 tests pass on source and editable in each order; noneditable nomination-first passes 55; noneditable bulk-first gives 1 error, the explicit rejection. `test_nomination_bootstrap` passes 3 tests.

## Per-criterion status

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Layouts, metadata, rejection documented | Proven | README section; probes match it. |
| 2 | Both orders in fresh processes per layout; unsupported rejects without mutation | Proven | Results above; mutation-free rejection asserted by `test_nomination_bootstrap`. |
| 3 | Origins and identities observed | Proven | Identity flags true in every supported run. That the original purge split class identity stays inferred from the earlier adverse run on 7de4a8110^ (1 failure, 20 errors). |
| 4 | Regression fails on original, passes on fix | Proven | Ticked in the issue; 2026-11-22 adverse run retained. |
| 5 | No family purge, foreign checks retained | Proven | Ticked; `sys.modules` is only scanned read-only. |
| 6 | Complete local gate and verified external full receipt | Unproven, owner-gated | No source file changed, so FULL tier is not triggered; the brief forbids `rpi-checks.py --all`. The coordinator or owner runs gates. |

No code gap exists, so no source or test change was made. Use `Refs #1847`, not a closing keyword.
