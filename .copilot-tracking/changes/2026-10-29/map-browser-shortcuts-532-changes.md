---
title: Map browser shortcuts correction changes
description: Original correction execution and local validation evidence for PR 539
ms.date: 2026-10-29
---

## Context and Scope

Task: 532-map-browser-shortcuts-2026-10-29. Full plan scope.
Plan: .copilot-tracking/plans/2026-10-29/map-browser-shortcuts-532-plan.md.
Details: .copilot-tracking/details/2026-10-29/map-browser-shortcuts-532-phase-details.md.
Baseline: f4a6bed44ff5891c4edd0455dabcff3ea39492bf.
Single critique Revise, PC-001 ordering correction applied directly.
Original 2026-10-28 research/critique/Review remain unchanged.

## P01: Handler and Regression Coverage

P01-T01: added one helper and two invocation sites to the existing check. It
focuses map/home marker in embedded/expanded modes, dispatches all seven map
command keys with Ctrl, Meta, Alt and combined Ctrl+Meta+Alt+Shift, and checks
uncancelled dispatch, unchanged map pane/route/focus and zero map API requests.
Added trusted Shift-plus/equals/minus with exact map API zoom deltas.

Pre-fix regression proof: shared nonblocking lock acquired; constructed real
loopback server confirmed responsive; browser failed as expected on the first
Ctrl+= assertion at embedded map focus. Exit 1, not a tooling failure.
Raw evidence:
/home/azureuser/.copilot/session-state/9c54d1fe-4764-44f7-9851-9ecc7c13b3d5/files/map-shortcuts-red.log.

Then added the early Ctrl/Meta/Alt return before map commands, retaining
defaultPrevented, control exclusions and Shift. P01-T02: README documents key
ownership and regression coverage. No semantic, scope or dependency divergence.

## P02: Validation and Local Delivery

The caller-specified issue-526-journey venv/worktree is absent. Existing
/tmp/ama-532-venv was used with current worktree source precedence; no
installation, shared-worktree recreation or cloud fallback.
Full suites only under flock -n /tmp/ama-rpi-heavy.lock, targeted-only if busy.
Pinned axe: /tmp/ama-532-axe-4.10.3.min.js.

### P02-T01: Completed Local Validation

Nonblocking shared lock admitted both red and green runs immediately, then was
released when each foreground command exited. No contention or unlocked heavy
fallback. Green run used, from src/api:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=../core/src:../agents/src:src:tests:../core/tests:../agents/tests
/tmp/ama-532-venv/bin/python -m unittest discover -s tests -q
/tmp/ama-532-venv/bin/python -m checks.map_fullscreen_browser_check \
  --axe /tmp/ama-532-axe-4.10.3.min.js \
  --out /home/azureuser/.copilot/session-state/9c54d1fe-4764-44f7-9851-9ecc7c13b3d5/files/map-shortcuts-green
```

The compound command was held under `flock -n -E 75 /tmp/ama-rpi-heavy.lock`.
All three imported namespace package paths were separately asserted to lie
inside /home/azureuser/source/ama-wt/issue-532/src, not the substitute venv's
editable source locations. No environment installation or mutation.

| Check | Result | Boundary |
| --- | --- | --- |
| API unittest discovery | OK, 1214 tests in 451.358s, 316 skipped | Existing opt-in SQL/browser and backend-specific skips remain; not SQL acceptance |
| Extended map browser | Passed, Chromium 156.0.8078.4, no JS errors | 112 modified key cases, four focus/mode pairs, no map requests; trusted Shift-plus/equals/minus deltas and 80px pan |
| Pinned axe 4.10.3 | Nine states, zero violations, zero unresolved ARIA references | Every state retains color-contrast incomplete, not full WCAG/human acceptance |
| Node syntax | Passed app.js | `node --check` |
| Ruff check and format | Passed edited browser check | Existing installed tool, no dependency change |
| Mypy | Success, one source file | `--follow-imports=silent checks/map_fullscreen_browser_check.py` from src/api |
| Manifest integrity | Four source SHA-256 pins match | No pinned source edited |
| Git diff whitespace | Passed | `git diff --check` |

Raw green log:
/home/azureuser/.copilot/session-state/9c54d1fe-4764-44f7-9851-9ecc7c13b3d5/files/map-shortcuts-green.log.
Output directory retains axe-results.json, browser.json and five screenshots.
Synthetic event dispatch proves cancellation/application behavior, not browser
chrome zoom or actual history traversal.

### Assessed Source Fingerprints

* app.js SHA-256: 432b54f35c3825040d194ab794ac0b0d803098bf0e741e05e139aa09fe539e8b.
* map_fullscreen_browser_check.py SHA-256: 43b62a09943b3f7338cc4f7bdde1331ad2bf1063f5b1b40e1eeea19fcbb58c39.
* axe SHA-256: 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.

## Amendments and Divergences

* PC-001: pre-fix failure moved inside P01 before guard, not after P01.
* Environment substitution is an immediately relevant current-state correction,
  not an authority or behavior change; exact absence and substitute are disclosed.
* No manifest pin targets edited; no pin update required.

## Pre-Review Reconciliation (Original Handoff)

Source implementation and requested local validation complete. P01/P01-T01/
P01-T02/P02-T01 completion evidence is current; P02-T02 remains the local
commit/independent Review closeout, not unfinished source work. Plan and phase
details match the implemented behavior and disclosed environment deviation.
Ready for one independent post-implementation Review of the local candidate.
No material implementation blocker. Original adverse evidence is preserved.
No push, az, force-push, merge, issue closure or publication is authorized.

## P02-T02: Independent Review and Local-Only Closeout

Implementation and original research/plan/details/critique/changes/state evidence
were committed locally as 345df54de0167e3e5abdf8e132112597a0b4adc2:
`fix(web): preserve browser shortcuts on focused maps`. The commit uses
Refs #532 without a closing keyword, privacy-safe authenticated-account author/
committer and the required Copilot trailer.

Exactly one independent post-implementation Review executed: Complete.
Outcome: Conformant with justified divergence. Assessed boundary:
345df54de0167e3e5abdf8e132112597a0b4adc2 versus
f4a6bed44ff5891c4edd0455dabcff3ea39492bf. Original record:
.copilot-tracking/reviews/logs/2026-10-29/map-browser-shortcuts-532-review.md.
No correction source defects. The justified divergence is the disclosed venv
substitution, not an undisclosed behavior change.

Original Review is preserved unchanged. Its RV-001 (Low) routes human AT,
contrast and staff acceptance separately; RV-002 (Medium) routes authorized
publication gates separately. Neither starts a new implementation or Review.
No source bytes changed after the assessed implementation commit.

The final local documentation commit persists the original Review and reconciles
current plan/details/state/changes. This is administrative lifecycle closeout,
not an exact-final-head publication assessment or reusable gate receipt.

## Final Execution and Return State

* Full-plan execution: Complete; all P01/P02 and four task markers complete.
* Remaining source/validation work: none within the correction boundary.
* Task status: completed. Mode: automatic. Phase: Follow-up.
* Session status: stopped by explicit user direction to stop with local commits.
* Correction blockers: none. Human acceptance and publication remain separately
  unmet and ranked in the state; no child work started.
* No az, push, force-push, PR mutation, merge, issue closure or publication.
* No complete local publication gate/receipt was run or claimed; it is not
  authorized by this no-az/no-push task. Original dated failure evidence remains.
