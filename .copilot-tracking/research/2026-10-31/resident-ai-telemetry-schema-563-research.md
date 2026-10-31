<!-- markdownlint-disable-file -->
---
title: Resident AI telemetry schema correction research
ms.date: 2026-10-31
---

## Research Brief

* Target: PR #585 coordinator handoff query schema correction, Refs #563.
* Purpose/audience: give the coordinator a resource-specific future query without changing recorded observations.
* Scope: this PR's artifacts and documentation; canonical schema in infra/README.md.
* Non-goals: Azure access, secrets, source changes, query execution, issue closure and publication.
* Criteria: preserve earlier bytes; append dated corrections for every in-scope legacy query; record only local documentary proof.
* Output mode: convergence; prepares the requested sequential Plan, Implement and Review.

## Research Parameters

| Field | Value |
| --- | --- |
| Status | Complete |
| Posture | Focused, selected from the bounded caller request |
| Questions | Which schema applies? Where is the legacy query repeated? How can history be preserved? |
| Internal candidates | PR changed paths; 2026-10-30 resident-ai-diagnosis-563 artifacts; infra/README.md |
| External candidates | None; read-only GitHub PR metadata only |
| Explicit limits | Docs only; no Azure, secrets, source changes or push |
| Resolved evidence root | .copilot-tracking/research/2026-10-31/ |
| Research writes | Research evidence and required lifecycle state only |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and disposition |
| --- | --- | --- |
| Instruction | Repository AMA guidance | Selected: dated evidence, preserve history, local commit identity and publication gates |
| Skill | rpi-research | Selected: ordered wider/deeper/contrarian cycle |
| Specialist | RPI Researcher | Skipped: one small, tightly coupled documentary trace |
| Domain | Telemetry foundations | Skipped: no instrumentation or telemetry design; existing schema is the authority |

## User Participation and Direction Controls

The explicit request authorizes all four phases and a local commit on the named
open PR branch. No automatic-session mode switch is inferred. Manual mode with
explicit advance authorization for this task only; non-interactive execution.
Earlier records must remain intact. No live operation is authorized.

## Prior Knowledge Gate

Clean worktree on ops/resident-ai-diagnosis-563 at bbbd969b; PR #585 is open
against main on that branch. Supplied schema and rebase claims will be checked,
not treated as new live evidence. Repository context documents were read.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What is the resource-specific console query contract? | Straightforward | Open |
| Q2 | Which PR artifacts/docs repeat the legacy query? | Straightforward | Open |
| Q3 | What correction preserves history and proof boundaries? | Straightforward | Open |

## Research Cycle Log

### Cycle 1

* Wider: `git diff --name-only 4cb5964f...HEAD` identifies seven tracking-only
  paths, no production docs. A scoped sweep of all seven finds legacy query
  columns only in the original changes record. Reflection: two query blocks
  need different historical treatment, not a repository-wide rewrite.
* Deeper: read the recorded azure-monitor destination and both query blocks,
  then infra/README.md's resource-specific example. Reflection: map the table
  to ContainerAppConsoleLogs and columns to ContainerAppName, RevisionName and
  Log; retain TimeGenerated, aliases, filters, classification and projection.
* Contrarian: the first block records an actually attempted denied query,
  whereas the second is future guidance. Reflection: deleting either old
  block would rewrite history; append a controlling correction with both
  resource-specific variants. No access-denied result establishes schema
  validity, telemetry availability, dispatch, cost or runtime cause.
* Parent synthesis: accept C1-C4; reject rewriting the old blocks and reject
  executing a query. No further cycle is needed: exact scope covered, schema
  mapping explicit, historical/future distinction resolved.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Recorded destination is azure-monitor | .copilot-tracking/changes/2026-10-30/resident-ai-diagnosis-563-changes.md:127 | High, historical record only |
| C2 | Historical denied query uses legacy table/columns | .copilot-tracking/changes/2026-10-30/resident-ai-diagnosis-563-changes.md:140-154 | High |
| C3 | Future coordinator query repeats legacy schema | .copilot-tracking/changes/2026-10-30/resident-ai-diagnosis-563-changes.md:164-194 | High |
| C4 | Canonical guide uses resource-specific table and unsuffixed columns | infra/README.md:2905-2916 | High, documentary contract |
| C5 | Scope is seven tracking files; only C2/C3 contain legacy queries | git diff --name-only 4cb5964f...HEAD and scoped rg sweep, 2026-10-31 | High |

No external sources or live telemetry used. Cross-session lookup found no
additional matching recent context. Contradiction C1/C3 is resolved
prospectively using C4, without reclassifying C2's recorded denial.

## Findings, Alternatives and Decision State

| Question | Finding | Evidence |
| --- | --- | --- |
| Q1 | Resource-specific table and unsuffixed columns apply to the documented handoff | C1, C4 |
| Q2 | Only the changes record has two legacy blocks; no other PR doc query needs correction | C2, C3, C5 |
| Q3 | Append two replacements and explicitly supersede future guidance, preserving old observations | C2-C4 |

Selected: dated correction appendix with current future handoff plus an
unexecuted resource-specific equivalent of the historical aggregate.
Rejected: replacing old bytes (history loss), adding dual-schema fallback
(unnecessary and hides the known destination), Azure execution (out of scope).
Current decision: Refs #563 only, local-only commit. Unresolved live evidence:
access, ingestion, root cause, inference dispatch/spend and whole-issue acceptance.
Potential later research is coordinator-owned authorized private telemetry
acquisition, not part of this correction.

## Planning Readiness

Ready. Research disposition: executed, Complete. C1-C5 support the documentary
correction; no implementation blocker. Self-check: all questions answered,
three waves ordered, alternatives and limitations explicit, evidence scoped.
Parent next action: Plan under the caller's explicit full-loop request.
