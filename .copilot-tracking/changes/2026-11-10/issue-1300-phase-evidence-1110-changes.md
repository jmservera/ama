---
title: Issue 1300 changes record
description: Changes for the prospective RPI phase witness
ms.date: 2026-11-10
---

## Implementation opening

Opened at tool clock 2026-11-10T03:05:01.292673531Z, before any source edit. At that point the worktree contained only RPI tracking records (research, plan, details, critique, state). Phases Research and Plan ran before the helper existed, so the helper did not witness them; their order is supported only by the state file writes and tool-clock readings recorded in those artifacts.

## Planned changes

* tools/rpi_phase_witness.py (new)
* tools/test_rpi_phase_witness.py (new)
* .github/agents/ama-backlog-delivery-coordinator.agent.md, step 5 only

## Evidence

### Helper and tests (P3)

* Created tools/rpi_phase_witness.py (stdlib; events launch, research-open, plan-done, implement-start, implement-done, review-done, commit-complete; verify) and tools/test_rpi_phase_witness.py (18 cases: tool clock versus rejected caller time, missing/empty/escaping artifacts refused and retained, out-of-order and dirty-start qualification, commit claim without or unrelated to a commit refused, stale review, torn tail, tampered chain, 8 concurrent processes, backward clock, symlink isolation, no environment capture, step-5 invocation present).
* Edit order honesty: the changes record opened at 03:05:01Z (tool clock), before the first source edit (helper written about 03:05:5xZ). This session's own Research and Plan phases were not witnessed by the helper because it did not yet exist.

### Coordinator step 5 (P4)

* Only step 5 edited: launch record before the tmux command, worker boundary calls in the brief, verify with the tmux pane capture, qualifications carried forward, log sha256 recorded before worktree removal. Two static-review wording fixes and two behavior-run ambiguity fixes applied (meaning of exit 1, state path, checkout root).

### Validation (focused tier, P5)

* python3 -m unittest tools/test_rpi_phase_witness.py: 18 tests OK. ruff check and ruff format clean. No full gate, no rpi-checks.
* HVE classification Major, profile Medium (no High declared), fidelity simulation. Static review (generic subagent, fresh context): Pass, 4 Low, 2 applied. Behavior: hve-artifact-tester had no shell tool, so execution was Blocked/Partial (read-only emulation); my own run of launch, refusal and verify in an owned scratch repo is observed but not independent grading. Behavior gate: Deferred. Exact missing stage: shell-capable independent behavior execution and grading, ideally native tmux. No other mechanical host validation was requested.
* AC3 genuine native exercise: Deferred to the coordinator (see handoff).
