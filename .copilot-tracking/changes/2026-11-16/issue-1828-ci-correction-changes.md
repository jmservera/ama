---
title: Issue 1828 CI correction cycle 2 changes
description: Changes record for the mypy patch target correction
ms.date: 2026-11-16
ms.topic: reference
---

## Status

Planned before edits. Tier FOCUSED. Base head 8e9324bc69a59bc4efbd128fa50d1cf7974649e7, main 18d3de459f20018e91fab3af87ab0d89123661c6.

## Planned changes (before edits)

* `src/api/tests/test_map_viewport_premise.py`: one line, the patch target of the virtual clock becomes the dotted string `checks.map_fullscreen_browser_check.time.monotonic`.
* Not edited: harness, application, authorization, consent, map and keyboard behaviour, workflows, prior artifacts and evidence.
* Disclosure: the baseline `mypy` reproduction (read-only, `mypy-failing-first.log`) ran before the research-open witness; the witness `launch` event was refused (no brief file) and is preserved in the external log; the new state file pointers were updated with `sed` rather than `edit`.

## Implemented

* `src/api/tests/test_map_viewport_premise.py`: the virtual clock is now patched with `patch("checks.map_fullscreen_browser_check.time.monotonic", monotonic)`. Same runtime object, no harness or assertion change.

## Validation (focused tier, `/tmp/1828/venv/bin/python`, 3.12.3, mypy 2.4.0, ruff 0.17.1, project distributions installed editable from this worktree; no install performed; no PYTHONPATH workaround)

| Check | Result |
| --- | --- |
| Bare `mypy` from `src/api` before the edit (`evidence/.../mypy-failing-first.log`) | reproduces the CI error at line 97 |
| Bare `mypy` after the edit (`mypy-post-fix.log`) | Success, 307 source files |
| Unittest: premise, map sensors, role, ui support, browser harness scratch, employee acceptance (`unit-post-fix.log`) | 124 tests OK |
| `ruff check .` and `ruff format --check .` (`ruff-post-fix.log`) | pass |
| Full `checks.map_fullscreen_browser_check` run 1 and 2 on the new head | exit 0 both; 332 PASS, 0 FAIL, 0 SKIP lines, 14 axe zero-violation scans; identical log sha256 `d0d27d6ed6ba3147d5256e4af9a7fec5e375a0fad5e5d24d02d24f54ea33df39` |

Browser inputs and evidence, external: pinned `/tmp/1828/axe.js` sha256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb verified; logs `/tmp/1828/ci-fix-1.log`, `/tmp/1828/ci-fix-2.log`, results `/tmp/1828/ci-fix-1/` and `/tmp/1828/ci-fix-2/`, digests `/tmp/1828/ci-fix-sha.txt`. The heavy lock was confirmed free (`flock -n`, no `fuser` holder) and taken nonblocking per run. Two operator errors are preserved: `ci-fix-1-failed-start.log` (out dir existed, nothing ran) and `ci-fix-2-wrongcwd.log` (wrong working directory, module not found), both before any check executed.

## Limits

* Hosted CI on the new head is unobserved. The earlier browser results and the independent review Pass for 8e9324b are historical for this head; an independent exact-head review, push and PR update remain with the coordinator.
