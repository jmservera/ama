---
title: Nomination test bootstrap isolation, fourth re-run on head b11b8259bd (#1847)
description: Fresh-process re-run of the #1847 criteria on 2026-11-23 with live revision confirmation, a root-cause statement for the one unproven criterion and no code gap found
ms.date: 2026-11-23
---
# Nomination test bootstrap isolation, fourth re-run (#1847)

Scope: #1847 is a test-harness issue. Product code, the live apps and Azure play no part in its criteria. The fix is on main in 7de4a8110 (#1849) and the layout contract is in `src/core/README.md` ("Nomination test layouts (#1847)"). This note repeats the [2026-11-22 re-run](./nomination-bootstrap-isolation-rerun-1847-2026-11-22.md) on head b11b8259bd. Read-only `az containerapp show` confirmed live revisions `ca-cutover-test-demo-api--0000054` and `ca-resident-demo--0000026`; nothing was changed in Azure and no secret was read. Raw outputs: [evidence folder](./nomination-bootstrap-isolation-proof-1847-2026-11-23/).

## Method

* Source layout: `PYTHONPATH=../src:../../agents/src:.` from `src/core/tests`.
* Editable: throwaway venv, `pip install --no-deps -e` of `src/core` and `src/agents`; metadata `zava-forward-core 0.1.0` and `zava-forward-agents 0.1.0` listed.
* Noneditable: `pip install --no-deps --target <tmp>/site`, `PYTHONPATH=<tmp>/site:.`.
* The [probe](./nomination-bootstrap-isolation-proof-1847-2026-11-23/identity-probe.py.txt) imports both test modules in a named order in a fresh process. Temporary directories lived outside the repository and were removed.

## Results

* Source and editable layouts import in both orders; `store_file` resolves under this worktree's `src/core/src`; `ConflictError`, `GateError`, `Store` and the `bulk_edits` patch target are the same objects in each module ([source](./nomination-bootstrap-isolation-proof-1847-2026-11-23/source.txt), [editable](./nomination-bootstrap-isolation-proof-1847-2026-11-23/editable.txt)).
* Noneditable: nomination-first imports from `src/`; bulk-first is rejected with `unsupported layout` before any `sys.path` or `sys.modules` change ([output](./nomination-bootstrap-isolation-proof-1847-2026-11-23/noneditable.txt)).
* `unittest` runs in [both orders](./nomination-bootstrap-isolation-proof-1847-2026-11-23/unittest-orders.txt): 58 and 55 tests pass on editable and source layouts; the only noneditable bulk-first error is the explicit rejection.
* A first editable probe printed `No module named 'test_bulk_edits'` because the probe sits outside the tests directory; adding `PYTHONPATH=.` fixed it. That was a harness input error, not a product or bootstrap defect.

## Per-criterion status

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Layouts, metadata, rejection documented | Proven | README section; probes match it. |
| 2 | Both orders in fresh processes per layout; unsupported rejects without mutation | Proven | Results above; the mutation-free rejection is asserted by `test_nomination_bootstrap` (58 OK). |
| 3 | Origins and identities observed | Proven | Identity flags true in every supported run. That the original purge split class identity stays inferred from the 1 failure and 20 errors seen on 7de4a8110^ on 2026-11-22. |
| 4 | Regression fails on original, passes on fix | Proven | Ticked; 2026-11-22 adverse run retained. |
| 5 | No family purge, foreign checks retained | Proven | Ticked; `sys.modules` is only scanned read-only. |
| 6 | Complete local gate and verified external full receipt | Unproven, owner-gated | Root cause: no source file changed, so the FULL tier is not triggered, and the brief forbids `rpi-checks.py --all`; the coordinator or owner runs gates. |

No code gap exists, so no source or test change was made. Use `Refs #1847`, not a closing keyword.
