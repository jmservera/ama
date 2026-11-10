---
title: Issue 1300 prospective RPI phase evidence research
description: Research for a local observational phase witness adopted by coordinator step 5
ms.date: 2026-11-10
---

## Research Opening

* Task: `issue-1300-phase-initial`, slug `issue-1300-phase-evidence-1110`, posture focused, mode automatic.
* Opening state persisted at tool clock `2026-11-10T03:01:57Z` (`.copilot-tracking/rpi-sessions/2026-11-10/issue-1300-phase-evidence-1110-state.json`) after only the brief, `git status` and the clock were read. No research search had happened before it.
* Disposition: Research `executed`. This phase predates the helper, so the helper did not witness it. Only the state file above and tool-clock readings in the changes record support its ordering.
* Source: base `a61bebe6b71e7f33560e2dee74b38834e4f55c0e`, branch `fix/prospective-rpi-phase-1300-1110`, worktree `issue-1300-phase-1110`, clean at start.

## Scope and inputs

Issue #1300 (authenticated body, no comments, no PR in the all-state search): make future coordinator-launched sessions persist genuine RPI state and artifacts when events occur. Out of scope: host or plugin enforcement, correction policy (#1296 is paused and not imported), KB and `.github/copilot-instructions.md`.

## AC1 trace: observed partial order

Classification: R reported (issue body), W independently witnessed now (read from Git in this session), U unknown.

| Item | Class | Finding |
|---|---|---|
| #152 correction 2 head `e4f77fa75` | R | Issue says research, critique, comment edit and review happened, state first visible after review, changes record after the edit, commit task checked early. |
| Same commit | W | `e4f77fa75` (committed `2026-11-09T05:24:22Z`) adds all seven correction-2 records (research, plan, details, critique, changes, review, state) and the two-line `app.js` edit in one commit. Git therefore shows the final set only. |
| Commits before it | W | `85c7a3741` (04:55:44Z) holds the correction-1 records and source; `06954540e` (04:55:48Z) records the correction-1 review four seconds later. Commit time is not phase time. |
| #1298 candidate `fef352e0b` | W | Committed `2026-11-09T03:55:51Z`, adds research, plan, critique, details, changes, review, state and the source change in one commit. |
| Actual write order of state, changes and edit | U | No surviving raw tool event stream, file mtimes or tmux log was located for either run. The chronology of the gaps is unknown beyond the issue report. |
| Later retention | W | Same artifacts later reach main squashed (`bcc99405c`, `1464b4d85`), so original files are retained but carry no per-phase times. |

Hypothesis, not confirmed: the sessions wrote artifacts in batches near the end. Not established: any CLI, plugin or skill defect.

## Ownership of each gap

| Gap | Owning boundary | Basis |
|---|---|---|
| State visible only after review | RPI Agent durable-state contract (pre and post transition writes) | Installed `rpi-agent` and issue text. The contract already exists. |
| Research opening missing | `rpi-research` skill step 5.3: opening state before substantive search | Installed skill, read this session. |
| Changes record after the edit | `rpi-implement` skill steps 2 and 3: changes and plan state before substantive edits | Installed skill, read this session. |
| Commit marker before commit | `rpi-implement` completion-marker rule | Installed skill. |
| Coordinator cannot tell prospective from reconstructed | Coordinator step 5 brief and verification text: asks for phases and artifacts, has no observation step | `.github/agents/ama-backlog-delivery-coordinator.agent.md`, step 5. This is the repository-owned gap. |
| Backend, model and host attestation | Host. Out of scope and unattainable in repository code. | Brief and issue. |

Owner decisions: none needed for the local helper. Host or plugin enforcement would need the upstream owner and is recorded as an external blocker, not attempted.

## Design findings

* Reuse: canonical state JSON `artifact_paths`, research, plan, details, critique, changes and review files. No second state machine; the helper only observes them.
* Existing `tools/test_rpi_checks.py` shows the unittest convention (temp repos, standard library). `tools/rpi-checks.py` hashes identities but does not witness phases; it is not changed.
* Actual adoption point: coordinator step 5 already generates a fresh brief per launch and runs the tmux command. A helper call at brief creation and at verification is the smallest real invocation.
* Limits to state plainly: a local JSONL with a hash chain is writable by any process with file access, so it is not tamperproof, not host or model attestation and not proof of unobserved reasoning. Model and session labels stay assertions.

## Planning Readiness

Ready. Alternatives rejected: a general workflow engine (too large), editing the brief template outside the repository (not adopted), changing installed skills (no evidence of defect).

## Remaining unknowns

* Raw original timelines for #152 and #1298 (not found locally).
* AC3 genuine native exercise: coordinator-run, deferred from this session.
