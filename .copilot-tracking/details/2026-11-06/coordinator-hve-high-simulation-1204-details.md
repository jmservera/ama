---
title: Details for a fresh High-profile contained HVE simulation (issue 1204)
ms.date: 2026-11-06
---

## Allocations

* Sandbox: .copilot-tracking/sandbox/2026-11-06-coordinator-behavior-005 (absent at intake; 001 to 004 exist and stay untouched). Retained (retain-sandbox true).
* Durable report: .copilot-tracking/hve-builder/2026-11-06/coordinator-behavior-abd6-1204-behavior-report-006.md (005 exists and stays unchanged).
* Changes: .copilot-tracking/changes/2026-11-06/coordinator-hve-high-simulation-1204-changes.md. Review (later, separate): .copilot-tracking/reviews/2026-11-06/coordinator-hve-high-simulation-1204-review.md. State: .copilot-tracking/rpi-sessions/2026-11-06/coordinator-hve-high-simulation-1204-state.json.

## Run-state fields

Run type full; target blob acefb44a; type agent; profile High (responsibility-based lead inference, uncertainty recorded, not metadata); model first actual High model gpt-5.6-sol, recorded from the real dispatch return; fidelity simulation; containment: executor read-only (no write, shell, Git, GitHub, cloud, schedule or cleanup tool), lead-only sandbox writes, pre/post git status and ignored-inclusive status; purpose and requirement map below; reuse: none (full run, prior 25 cases not eligible).

## Requirement mapping to scenarios (designer chooses concrete scenarios; each must be covered)

* R1 liveness/stop decision after fresh complete classification; unknown or unreviewed is research work, never human-blocked; actual unknown backlog.
* R2 each tick advances a real next action; rotating batch of up to five closure-review items with session SQL cursor; no audit claim from printing a queue; no invented issues.
* R3 two no-progress ticks trigger bounded recovery; tick end versus approved run end; no stop while actionable or unknown work remains; actual held heavy resource despite quiet logs, initial_wait or a free-lock interval; original-session recovery.
* R4 one question at a time without stopping independent lanes; freshly granted and expired approvals persisted and reclassified; never re-request or expand granted authority.
* R5 eight-assignment cap, 20-PR drain to 10-15, parent stacks, batched publication, exact-head review, selected tiers, human boundaries, no gratuitous rebase.
* R6 reconciled schedule/stop/rebase text; correct schedule replacement (create, verify, stop old, read back exactly one delivery and one cleanup recurrence; prompt versions and IDs in evidence).
* R7 briefs from current canonical policy; genuine prospective RPI and frozen local handoff; genuine parent targets; no worker publication before coordinator validation.
* R8 evidence-safe finite cleanup (explicit selection, active receipt/image ownership, no wildcard removal, missing upstream not counted as zero).
* R9 issue closure and human gates (tick only proven criteria; leave human boxes).

## Dispatch wrappers (lead composes; scenario text black-box)

* Designer: generic task subagent (no selected custom agent; agent_type general-purpose only because the interface requires a type), model gpt-5.6-sol, template from references/stage-dispatch.md in full, run-state path, target pointer, issue criteria, canonical criteria; returns content only, no file writes. Scenarios must not name the artifact, path, headings, authoring history, expected answer or test framing. Do not inspect or judge tools frontmatter.
* Executor: hve-core-all:hve-artifact-tester, model gpt-5.6-sol (same as design availability result), wrapper with artifact pointer, sandbox path, profile and every scenario prompt; returns the complete trace; read-only.
* Grader: fresh generic subagent with the complete evidence-grading template and dispatch restrictions from references/stage-dispatch.md in its prompt, model per the same resolved High availability, finalized test log, design log, target, purpose, requirements, catalog and rubric; returns verdict and findings content only.
* If the first design dispatch fails: record the real error verbatim, apply skill rules once.

## Evidence and checks

Persist verbatim returns (design, trace, review) plus dispatch evidence (requested and returned model, status). Focused checks: git diff --check, JSON parse of state, relative link existence, exact source blob and ignored-inclusive status before and after, only new files added (no tracked file modified), no secret patterns (names-only pattern check on new files), human checkbox unchecked.

## Not authorized

Native run, harness, installs, heavy work, source or schedule edits, push or PR, deletion or move of historical evidence, proxy regrading or relabelling.
