<!-- markdownlint-disable-file -->

# Task Research: issue-117-document-rescan-scheduler

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-17/issue-117-document-rescan-scheduler-research.md |

## Research Brief

Investigate the missing bounded pending-document rescan invocation for issue
#117, for coordinator implementation planning. Reuse the existing scan service,
orchestrator/job/configuration and persistence contracts. Output mode:
convergence. Prove fail-closed behavior, boundedness, retry/concurrency and
audit correctness without rebuilding delivered retention or hold controls.

## Research Parameters

Focused posture, selected from the caller's bounded engineering objective.
Internal candidates: src/core document controls and stores, src/orchestrator,
src/api scan configuration, component tests and READMEs, ADR0002 and PRD DH-003.
External candidates: GitHub issue117 and merged PR270 metadata only.
Resolved evidence root: .copilot-tracking/. Research edits only evidence/state.
No mvp reads, private data, web changes, Azure deployment, paid services,
invented retention periods, deletion authority or human approvals.

## Extension Registry and Provenance

| Kind | Candidate | Match / provenance | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository instructions | All paths; source layout, branch and evidence boundaries | Selected |
| Skill | rpi-research | Ordered RPI user request | Selected |
| Specialist | RPI Researcher | Available, but one tightly coupled source trace | Skipped; inline investigation |
| Domain | Regulatory / web skills | No new legal interpretation or web work | Skipped |

## User Participation and Research Decisions

Explicit full-loop direction is automatic-mode confirmation. No further
routine phase confirmation is needed. User authorizes exact branch/base and
publication, but main movement requires coordinator integration authorization.

## Scope and Success Criteria

Answer whether an existing scheduler satisfies the gap; otherwise identify the
smallest existing-pattern invocation and its real persistence/CLI validation.
Never promote pending/unavailable/error to clean. Retention listing is not
deletion; worker identity is not owner authority.

## Task Research Requests

All phases must be contemporaneous. One critique and one original Review;
preserve adverse outcomes and route corrections separately.

## Direction Controls

* Narrow: missing rescan scheduling only, current src packages.
* Exclude: service activation, actual Azure schedule resources and approvals.
* Preserve: merged102 document/audit recovery, resident guards, sensor exports.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What does PR270 deliver in current source? | depth | Answered |
| Q2 | Which scheduler/job/configuration contracts are reusable? | depth | Answered |
| Q3 | What race/retry/audit boundaries must invocation preserve? | depth | Answered |

## Prior Knowledge Gate

Read original, addendum, knowledge-base index and owner memory first. Read-only
GitHub metadata confirms PR270 merged as e6df6b7; issue comment leaves scheduler,
Defender enablement and approvals open. Historical mvp test claims are not
current execution or permission to read mvp.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline source/README discovery complete; no worker dispatched. Existing
`rescan_pending` visits every pending/missing document under one lock, with no
bound, cursor or executable job. Orchestrator source_monitor demonstrates a
bounded one-shot module command and explicit continuation cursor. Current base
is merged #102/PR394, matching fresh origin/main.

Reflection: the issue comment remains accurate for the executable scheduler.
Existing scanner and store factory are reusable; the legacy job's automatic
malicious-document removal cannot be inherited by a worker lacking deletion
authority. Prioritize transactional scan updates and non-deleting quarantine.

#### Wave 2: Deeper

Investigating `_scan_stored`, SQL optimistic writes, pending-audit recovery and
committed-refresh detection before selecting an invocation contract. Existing
JSON is not cross-file/process atomic; SQL is the concurrency acceptance target.

Reflection: `_scan_stored` receives a case document but does not touch its case
for SQL tracking on the clean/pending path. The legacy loop reads `self.cases`
directly, so a wrapper alone is not adequate proof of persisted rescans. The
new bounded path must use `_case`, per-document recovery, and CAS save.
Existing staff-controlled context cannot authorize a service principal.

#### Wave 3: Contrarian

Challenge the need for a new hosted timer, the safety of inheriting automatic
removal, the assumption that SQL save alone contains failed audit, and the
assumption that retries may use local synthetic scanning implicitly. Search
existing infra/job entry points for a delivered rescan and check existing
scanner selection and post-commit semantics.

Reflection: infra schedules token, rules and digest jobs, not document rescans.
Adding hosted resources is neither necessary nor authorized. The factory's
default local scanner would silently weaken a real Defender retry unless the
job requires explicit scanner configuration and explicit synthetic-local opt-in.
SQL-only invocation follows the existing bounded rule-engine job boundary and
avoids promising cross-process correctness for JSON.

#### Parent Synthesis and Disposition

* Accepted (C1-C8): a bounded one-shot SQL job, callable with stable composite
  continuation, using the existing configured scanner and store factory.
* Accepted (C4-C6): per-document CAS, rollback of failed success audit while
  preserving any earlier prefix, and committed-refresh outcome separation.
* Rejected: daemon/timer/framework or Azure resources; no evidence of need or
  authority within scope. Rejected unbounded legacy-loop wrapper (C1).
* Rejected automatic malicious removal by worker: extend the existing scan
  service with a non-deleting result path; infected/mismatch remain unavailable
  with bytes/hold retained. Existing manual behavior is unchanged.
* Deferred: actual Defender enablement, deployment cadence/missing-run monitoring,
  deletion/hold delegations and approved retention triggers/periods (W1-W2).

#### Cycle Re-entry Evaluation

No further cycle needed: current contracts, alternatives, operational boundaries
and test seams are grounded. Test implementation may expose divergences, which
must be recorded rather than retroactively changing this research outcome.

## Evidence Log

| ID | Source | Observation |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/117#issuecomment-6192623419 (retrieved 2026-10-17) | Scanning, retention listing and hold delivered; scheduler, Defender and approvals remain open. |
| W2 | https://github.com/jmservera/ama/pull/270 (retrieved 2026-10-17) | Merged historical implementation; scanner fake transport and synthetic-only scanner caveats explicit. |
| C1 | src/core/src/zava_forward/core/doc_controls.py:155-197 | `_scan_stored` reads/scans/saves, legacy `rescan_pending` has no paging and treats any ValueError as removal. |
| C2 | src/orchestrator/src/zava_forward/orchestrator/source_monitor.py:15-103 | Existing bounded offline module command, explicit limit/cursor and nonzero failure exit. |
| C3 | src/core/src/zava_forward/core/factory.py:9-25 | Existing configured JSON/SQLite/MSSQL store factory; no new backend needed. |
| C4 | src/core/src/zava_forward/core/sqlstore.py:485-664 | Touched-case tracking, CAS writer, prior-pending quarantine in `_discard`, and post-COMMIT snapshot update. |
| C5 | src/core/src/zava_forward/core/change_provenance.py:86-149 | Controlled actor writes distinguish committed refresh errors from rollback and retain prior pending audit. Worker must not impersonate staff. |
| C6 | src/core/tests/test_progress_event_capture.py:102-219 | Current source regressions assert original error, safe failure audit, prefix preservation and failed-recovery notes. |
| C7 | src/core/src/zava_forward/core/store.py:644-683,971-976 | Download/assistant enforce clean; `_case` touches the SQL record. Generated records are a distinct path. |
| C8 | infra/modules/containerapps.bicep:250-257,343-344,384-396; src/orchestrator/src/zava_forward/orchestrator/__main__.py:1-3 | Existing schedules/module do not run rescans. No hosted rescan currently delivered. |

## Findings Mapped to Questions and Evidence

Q1: scan-before-availability, listing/approval and hold code exists (C1,C7,W2).
Q2: no current scheduler; bounded module/factory patterns suffice (C2,C3,C8).
Q3: SQL touching, CAS, prior-audit recovery and committed outcome must be
explicitly exercised, including actual independent SQL connections (C4-C6).

## Alternatives and Decision State

Choose one-shot SQL pages (1..100 attempts, stable case/document key order),
not a timer and not JSON delivery. Repeat continuation pages even if earlier
documents remain pending; restart from the beginning each sweep. No internal
infinite retries. Require explicit data/store/scanner configuration.

## Open Questions, Risks, and Residual Uncertainty

Scanner, Blob and SQL availability remain operational dependencies. A bounded
attempt count is not a service latency SLA. Repeated pending scans legitimately
produce repeated attempt events, not duplicate successful completion. No live
Azure/Defender or real-document assurance follows from synthetic tests.

## Current Decisions

Proceed to planning the bounded SQL invocation with explicit synthetic opt-in,
non-deleting malicious result, fair paging and safe failure reporting.

## Potential Next Research

Authorized operational enablement would require real Defender account evidence,
named schedule owner/cadence and minimum scanner permissions. Not part of this loop.

## Self-check

Wider, deeper and contrarian executed in order, inline; sources traced to current
src, with no mvp/private reads or legal-currentness claims. All questions answered
within the engineering boundary; no specialist execution was implied.

## Planning Readiness

Ready for the bounded engineering plan, not operational acceptance.
Research disposition: executed. Status: Complete.

Post-Review metadata reconciliation: the original Review noted the stale
opening Status cell. It now agrees with the contemporaneous completed cycle
and readiness sections; research evidence/outcome and original Review are
unchanged.
