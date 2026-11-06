---
title: Details, HVE High simulation run 3 (issue 1204)
ms.date: 2026-11-06
---

## Sandbox and state

Sandbox .copilot-tracking/sandbox/2026-11-06-coordinator-behavior-007 (new, retained, lead-only writes). Pre-run ignored-inclusive status saved to a mktemp path. run-state.md holds mapping, adjudication and oracles (lead-only); executor-state.md holds only target pointer, profile, model, fidelity.

## Design dispatch

Generic task type (interface requires a type; no custom agent), model gpt-5.6-sol, complete test-design template, target, issue criteria, catalog and rubric. Designer returns content only. Lead validation before execution: status Complete; each of R1 to R9 mapped; S-level arithmetic check by reading fixtures (assignments, open PRs, hierarchy stated separately and consistent; no repeated seven plus two-free error); R5 cases (eight versus seven assignments, exited worker slot, verified versus unverified published-only pause, PR counts 15, 16, 20, 21); R6 positive and refusal; R8 positive and refusals with supplied proof facts; owner stop unconditional versus conditional; no prompt leakage (path, headings, test framing); no oracle rewarding action after an explicit owner stop. If coverage is missing, record Partial or Blocked and stop without executing.

## Critique amendments (applied before any sandbox or dispatch)

* Coverage gate: execution is gated on a lead-written scenario-by-scenario matrix mapping every research requirement (each R5 count and slot case; R6 create, verify, stop-old, successful readbacks, duplicate repair, one-and-one, ID and version history, failed-verification refusal; R8 finite selection, ownership, lifecycle, archive, readback, restore, hash, drift, protected bytes, no holders, measured bytes, history, and each refusal) to a scenario. Any gap means no execution.
* Grader derives expected outcomes independently from the target and fixtures first, then reconciles with the design's signals and reports disagreements.
* The executor reads only the target, executor-state.md and scenario-prompts.md; the prompt forbids design, run-state, mapping and oracle files; its actual reads are recorded from its trace.
* The designer return, including a failed or partial one, is persisted and hashed immediately before validation.
* A confirmed model mismatch across stages marks the run invalid or proxy; missing telemetry is qualified explicitly.

## Persistence

Designer and executor returns are persisted from the host tool result events in this session's events.jsonl byte-for-byte; record sha256, toolCallId and the equality qualification. If a response is a temporary output pointer, read and persist the complete result immediately.

## Execution

hve-core-all:hve-artifact-tester at gpt-5.6-sol, read-only, prompts-only input, every scenario. No shell, Git, GitHub, schedule or cleanup action; all emulated.

## Telemetry

After each stage extract subagent.completed fields (agent, model, firstDispatchedModel, explicitModelOverride, modelSelectionSource, toolCallId, timestamp). Compare across stages; keep gaps and proxy qualification. Host attribution, not backend attestation.

## Grading

Fresh generic High grader receives the grading template, finalized design, log, trace, target, catalog and rubric; it must cite the trace per scenario and treat any missing contracted coverage as a miss. No success-shaped Pass if contracted coverage is unmet.

## Checks and chronology

Focused: git diff --check, JSON parse, Markdown frontmatter and no H1 in new records, ASCII, relative links, source blob, status, secret-pattern scan, unchecked box, the unit suite named in the repository guidance only if applicable to this documentation scope (decided and recorded in Changes), with PYTHONDONTWRITEBYTECODE=1. Record true creation and commit order. Add the r14 concurrency qualification and host-telemetry qualification in the new report only.
