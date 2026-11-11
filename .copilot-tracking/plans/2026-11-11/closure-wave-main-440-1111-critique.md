---
title: Closure-wave integrated-main checkpoint plan critique (Refs #440)
description: One independent critique pass over the research, plan and details before Root admission
ms.date: 2026-11-11
---

## Execution

One read-only `rubber-duck` pass (model `claude-sonnet-5.5`) over the research, plan and details. It ran nothing and edited nothing. Verdict: conformant after four non-blocking findings; no critique is repeated for this task.

## Findings and dispositions

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | medium | `RoleEndpointInventory(Matrix)` runs 24 tests (14 own plus 10 inherited from `Matrix` in `test_role_matrix.py`), not 14 | Applied: research and details N8 now expect 24 with the inheritance stated |
| PC-002 | medium | `flock -n` exit 1 on contention is indistinguishable from a unittest failure exit 1 | Applied: B2 uses `flock -n -E 99`; exit 99 with no `Ran N tests` line is blocked, other nonzero exits are failures |
| PC-003 | low | `NoPlaywright` is a finder inside an embedded script; `CapacityBrowserCheck` holds all 5 methods | Applied: relabelled in research and details N10; total 5 unchanged |
| PC-004 | low | #1425 and #1422 are on the integrated tree but have no selector | Applied: details recording rules state they are outside this selector set and the result says nothing about them |

Checked and found correct by the critique: class, method names and static counts for the other selectors, the self-lock behavior of `capacity_browser_check` and `UnacceptedDownloadBrowser`, the lock-free `HandoffReadGuidanceBrowser`, environment needs (`PYTHONPATH` with `../core/tests`, `node`, `ZF_BROWSER_TESTS=1`), store classification, the document-qualified requirement ids, and the absence of hidden source edits, rerun-to-pass, budget draw or pre-admission outcome claims.
