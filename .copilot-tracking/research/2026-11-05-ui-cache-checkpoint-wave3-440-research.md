---
title: UI and cache recovery checkpoint wave 3 research (Refs #440)
description: Current-main qualified research for the due 320px reflow and API bytecode-isolation recovery stabilization checkpoint
ms.date: 2026-11-05
ms.topic: reference
---

* Task: `ui-cache-checkpoint-wave3-440`, owner issue #440 (open; assignee list empty at 2026-11-05 read; existing checkpoint, not a feature). State: `.copilot-tracking/rpi-sessions/2026-11-05/ui-cache-checkpoint-wave3-440-state.json`.
* Research disposition: `executed` (read-only `git show` blob reads, issue reads and run reads on 2026-11-05) reusing the sixth checkpoint record in `docs/architecture/cutover-evidence-pack.md` as the template. Planning Readiness: `Ready` for a documentation-only checkpoint with a bounded focused observation.
* Boundary: local only; no push, PR, merge, issue tick, sign-off, runtime, coordinator, ADR or requirement change. No private data read.

## Source identities (observed 2026-11-05)

| Item | Value | How observed |
| --- | --- | --- |
| Child branch | `docs/parent123-ui-cache-checkpoint-wave3` at `23cdae38b1fe47a47ba5f3f356ed18253aad9c46` (clean at intake) | `git status`, `git rev-parse HEAD` |
| Parent topic | `origin/feat/discovery-assurance-integration-123` = `23cdae38b1fe47a47ba5f3f356ed18253aad9c46`, tree `263475b0e4d01203186b42b5311f4c85c0d4f5dd` | `git fetch`, `git rev-parse` |
| Main at merge of #1219 | `2edba50b7739b83b88ba491648717a9750777a0c` (committed 2026-11-05T14:28:34+01:00) | `git log origin/main` |
| Main after rubric commit | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, bot commit 2026-11-05T13:34:38Z, only `.github/rubric/scores/latest.json` (4 lines) changed from `2edba50b`. Scorer run 42036086584 was still `in_progress` at 13:36Z, so this pin is provisional until completion | `git diff --stat 2edba50b7..origin/main`, `gh run view` |
| Parent versus main | Parent is 3 ahead and 4 behind main at intake (4 behind counted before the rubric commit). Parent is NOT current main and lacks the #1215 and #1219 fixes | `git rev-list --left-right --count` |

The final pinned main commit and tree are recorded in the changes artifact after the scorer run completes, not assumed.

## Document identities (identical at main and parent, verified by blob)

| Document | Status, version | Blob |
| --- | --- | --- |
| BRD-2026-AMA48-001 | draft, 0.21.0 | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD-2026-AMA48-001 | in-review, 0.21.0 | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0003 | Accepted with amendment by the owner (2026-10-15, reconciled 2026-10-18) | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 | Accepted by the owner 2026-10-15 | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Draft and in-review documents are not approvals.

## Root causes and fixes (merged on main)

| Issue | Root cause | Fix | State |
| --- | --- | --- | --- |
| #1215 (closed) | API discovery in a gate-owned source snapshot let the scrubbed harness server child write `__pycache__` under source roots | #1217, merge `180dcf3e2`: `Runner.install_bytecode_policy()` called from `Runner._install("api")`; real-producer regression `tools.test_rpi_checks.GateTests.test_api_install_prevents_scrubbed_server_child_writing_source_bytecode` (main line 2156) | closed |
| #1214 (closed, all 5 ticks) | 320px case-summary header spacing pushed `.case-summary` bottom beyond the unchanged 1600 CSS px bound in `checks.case_journey_browser_check` | #1219, merge `2edba50b7` at 13:28:35Z; 19 reported checks pass, independent published functional and readiness Pass, and current premerge partial receipt verified (reported; not re-observed by this record) | closed |

The earlier #96 full receipt failed and is non-resumable; it is preserved and is not relabelled.

## Requirement and decision traceability (document-qualified)

| Requirement or decision | Source line (main blobs) | Implementing source and tests | Limit |
| --- | --- | --- | --- |
| BRD NFR-008 / AC-064 (accessibility and unfair-exclusion testing, digital and non-digital journeys) | BRD line 1634 | `src/api/checks/case_journey_browser_check.py`: reflow loop over 320, 390 and 1280 at height 800 (about line 1513); no-overflow check `scrollWidth <= innerWidth`; 320x800 summary bound `bottom <= 1600` (line 1526); reduced motion and forced colours; missing-enhancement stacked fallback | Synthetic data and engineering checks; not live-contact or user-research acceptance |
| BRD NFR-009 / AC-071 (journey ownership, tested manual or non-digital alternative) | BRD line 1646 | Same check: manual-route constructed fixture (`manual="Manual route."`), keyboard Enter/Home/End/Space tab and step operation, Escape handling | Service-time thresholds are set by owners under OD-09/OD-25; none approved here |
| PRD NFR-001/NFR-018 and AC-134, AC-093 (keyboard, focus, reflow at 320/390/1280, human help) | PRD lines 868, 1208, 1568, 2204 | Narrow reflow and keyboard checks above | PRD AC status cells read "Not run"; the six-script resident test, zoom and screen-reader checks are not provided by this record |
| ADR 0003 decision 2 (authority, confirmation and closure enforced in the API, not a view); ADR 0003 has no reflow or keyboard text | ADR lines 95-105 | Journey check exercises views against the real server; it does not move authority into a view | ADR 0003 constrains nothing about 320px layout; the trace is indirect and stated as such |
| ADR 0006 (src layout, cut-over gate; accepted) | ADR lines 9 and 279 | `tools/rpi-checks.py` Runner install path (`_install("api")` then `install_bytecode_policy()`), scrubbed harness server (`design_system_browser_check.main()` launch), `src/README.md` local gate | ADR 0006 does not mention bytecode; the trace is through its gate and layout rules, not a bytecode clause |
| #96 full gate versus #96 feature | Issue #96 open "Assisted form workspace and funding or claim pack assembly" | The gate dependency is the Runner and 320px check now fixed on main; the unmerged #96 feature, schema and Finance acceptance are separate and unaffected | A focused main pass is not a #96 full receipt |

## Planned observation (not yet run at this writing)

1. Focused real-producer regression under an exclusive non-queued `/tmp/ama-rpi-heavy.lock` (file exists, 0 bytes, mtime 2026-11-02; a non-blocking `flock` probe at 13:35Z found it free).
2. `checks.case_journey_browser_check` with pinned Chromium and axe at unchanged thresholds, in a fresh detached exact-main worktree `/tmp/ama-main-440-ui-cache-wave3` (absent at intake) with its own venv, scrubbed environment, external outputs and asserted module identities.
3. If the lock is held or a prerequisite (Chromium, axe, interpreter) is missing: no queue, no retry; record holder, unfinished step and resume point as blocked.

## Gaps and risks

* The scorer commit could still move main; a pin must be taken after run 42036086584 completes.
* Pinned axe and Chromium availability in this environment is unknown until probed; no fabricated browser result is allowed.
* No new defect is known. Any reproduced finding is compared with #1214 and #1215 before any proposal.

## Follow-ups

1. Coordinator independent exact-head assessment of this documentation child (ease: high; value: gate).
2. Parent refresh against main with its own exact-head gate (value: closes the "parent lacks fixes" gap; ease: low; separate lane).
3. #96 full-gate rerun by its owner session once the lock is free (value: high; not this task).
