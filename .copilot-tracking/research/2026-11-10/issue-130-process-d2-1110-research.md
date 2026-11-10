---
title: Issue 130 process D2 research
description: Research for the source-unchanged process-disposition continuation (D2) of the issue 130 nomination view
ms.date: 2026-11-10
---

## Status

Research opened at the research-open witness boundary of the new chain (session rpi-130-process-d2). Later sections are added after that boundary and are marked as such.

## What was inspected before research-open (self-reported; reading is not observable)

* Branch `feat/demo-nomination-view-130-1110`, head `eb64413236cd0bc0aacc76ac3a89825ba43a9d19`, tree `ca67389bf4441f5ddfd535b7f2b9b5b0ea43fb6e`, `git status --short --untracked-files=all` empty (zero lines).
* Declared target ref `feat/demo-nomination-ui-parent-81-1110` resolves to `4244e84e763e6e01dd6012fcb9b650dae8d58e9d`, the original base. Not main.
* ROOT `demo-130-process-d2-authority-selection-1110.md`: D1 completed, D2 is a metadata-writing continuation admitted by the task message, not source correction.
* New evidence directory `phase130-process-d2-evidence-1110` contained only the coordinator `launch` event (seq 1) at the start of this session.
* Helper `rpi_phase_witness.py`: required artifacts per event are research (research-open), plan, details, critique (plan-done), changes (implement-start and implement-done), review (review-done), review and changes (commit-complete). An artifact counts only if the state file lists it as a non-absolute path under `.copilot-tracking/` and the file is non-empty. Critique and review are guarded: a later change is a verify finding.

## Scope and distinctions

* Original code implementation: done on 2026-11-10 in the original session, witnessed by the original nine-event chain (seven successful required boundaries, two refused calls, plus one unrecorded wrong-`--repo` call). Not repeated here.
* D1: read-only diagnosis (`handoff-130-phase-diagnostic-1110.md`). It wrote no repository file.
* D2 (this chain): new research, plan, details, critique, changes, review and state files only. Its implementation phase is the production of process-disposition documentation. No product, test, checker, configuration or regular documentation file is edited.

## Findings after research-open (recorded 2026-11-10, after seq 2 of the D2 chain)

### Witness state

* D2 chain seq 1 launch (coordinator) and seq 2 research-open (worker) both `ok`. No refusal so far.

### Source identity at eb644 (read-only `git diff`, `git rev-parse`)

* Product, test and checker changes of the original candidate against base `4244e84e7`: `src/api/src/zava_forward/api/web/{app.js,panels.js,style.css}` (modified), `src/api/tests/test_nomination_screen.py` and `src/api/checks/nomination_browser_check.py` (added). Seven original `.copilot-tracking/` files were also added.
* Git tree ids at eb644: `src` d1079d2692db, `infra` d94040329d54, `tools` 432a4e8f7d74, `.github` 616b0b6675ec, `docs` 9743990dc916, `src/core` 148b92886486, `src/api/src/zava_forward/api/web` 84c27df96dcb, `src/api/tests` db72ce3fb1a5, `src/api/checks` 44f0fcb3f254. These are the baseline that the D2 candidate must keep byte-identical.

### Original artifacts (blob sha256, identical in the worktree and at HEAD)

* research c0fa038e, plan 77779dc6, critique 96923426, details a64fe74b, changes c82d0b61, review 0d6253a9, state 1d55fd05 (all `issue-130-nomination-view-1110`, prefixes of the full values recorded in the changes record).

### Original external records (sha256 prefixes)

* nine-event chain `events.jsonl` a4490908, original log fda8620d, original handoff 7d7c19ac, original brief 390ce07d.
* D1 handoff c2171abf, D1 brief 6c190622, D1 launch-only chain 58080150 (one coordinator launch, no worker event).
* D2 brief d5ffe356.
* Independent Functional assessment 5bd9ee6e: verdict approve, 0 source findings, 12 files read, stated not to be publication authority or an unqualified process pass.

### What cannot be established

* No D2 event, hash or review makes the original refusals compliant. The original STOP instruction was not followed on seq 2 and seq 8 retries and on one wrong-`--repo` call with no event.
* A new clean chain does not show what was reasoned in the original session, is not tamperproof and is not a retroactive waiver.
* Whether the owner's standing minimum covers this operation is the owner's and Root's statement in the task message. This research does not verify it independently.

### Planning readiness

Ready. The distinctions to carry into the plan are original implementation versus D1 diagnosis versus D2 documentation.
