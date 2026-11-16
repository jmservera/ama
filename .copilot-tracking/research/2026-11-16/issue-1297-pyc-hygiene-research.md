---
title: "Issue 1297 gate-created ignored bytecode research"
ms.date: 2026-11-16
---

## Status

Research disposition: executed. Planning Readiness: Ready. Source head 2e9bd4ab6a84492da704f068ecf5e7fc65ebcd1b, origin/main 18d3de459f20018e91fab3af87ab0d89123661c6 (fetched at launch).
Earlier research, receipts and adverse witness records are preserved and referenced, not reconstructed: `.copilot-tracking/rpi-sessions/2026-11-16/issue-1297-fix-state.json` and its artifacts, and the retained failed receipt `/tmp/ama-gate-1297-20261116T105339Z/receipt.json` with its checkout and logs (read-only use here). The earlier adverse receipt erased by another worker stays lost, as the #1297 comment records.

## Findings

* The failed gate checkout holds exactly six ignored files under `checkout/src/core/src/zava_forward/core/__pycache__/` (all mtime 2026-11-16 14:41:54.93-14:41:54.96 UTC, one process within 30 ms): `__main__`, `version`, `discovery_assistant_boundary`, `discovery_assistant_demo`, `discovery_assistant_drafting`, `discovery_assistant_evaluation`. No other `.pyc` exists outside the venvs and the external `bytecode/` prefix (12,378 files there), so the Runner's `PYTHONDONTWRITEBYTECODE`/`PYTHONPYCACHEPREFIX` (tools/rpi-checks.py, env block near line 1942) worked for everything it governed.
* The timing is during the project-core test run, not the static phase (static logs 0063-0068 end 14:55-14:56). The user brief's "static phase" is a mislabel by timestamp; the failure only surfaces at `clean_identity` after static.
* Cause: `src/core/tests/test_discovery_assistant_demo.py::run_module` launches `sys.executable -m zava_forward.core discovery-demo` with a deliberately scrubbed environment (`PATH`, `HOME`, `ZF_DATA` only, test `test_demo_runs_from_this_worktree_without_inputs`). The child never inherits the Runner's bytecode variables, so it writes `__pycache__` next to the editable-installed core sources inside the checkout.
* Reproduced read-only in a scratch copy (`/tmp/pyc-repro-*`): `env -i ... python3 -m zava_forward.core discovery-demo` emits exactly those six `.pyc` names.
* Prior art (#1215): the Runner already installs a `00-rpi-bytecode.pth` (`import sys; sys.dont_write_bytecode = True`) into the api venv only, because scrubbed browser-harness servers dropped the flags. `_install` calls `install_bytecode_policy()` only when `name == "api"`; the core, agents, orchestrator, importer and namespace venvs have no equivalent, so any scrubbed-environment child of those interpreters can write source bytecode.
* A source-tree change is not warranted: the test's scrubbed environment is intentional (no environment or file access claim) and other tests (95 files use subprocess) may do likewise.

## Candidate approach

Install the interpreter-level no-bytecode policy into every gate venv, keeping the `out/browser-bytecode-policy.pth` receipt file api-only so receipt file expectations do not change. This does not relax `clean_identity`, snapshot checks or SQL skip rules.

## Residuals

* Scratch dir from reproduction left in /tmp (not removed by policy).
* A scrubbed child that uses a different interpreter (not the venv's) is out of scope.
