<!-- markdownlint-disable-file -->
# Task Research: controlled-bulk-preview-78

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-17/controlled-bulk-preview-78-research.md |

## Research Brief

Research issue #78, parent #73, for ordered implementation and review.
Output mode: convergence. Determine the exact FR-005/006/007 contract,
existing edit permission/audit/SQL transaction patterns and a narrow permitted
bulk preview/apply design. Preserve existing UI and every controlled boundary.
Audience: implementer and PR reviewer.

## Research Parameters

Focused posture selected from explicit bounded caller scope. Internal candidates:
PRD/BRD, core store/controls/SQL implementations, API routes and synthetic tests.
External candidates: issue #78, parent #73 and concurrent PR #377 inventory.
No cloud, paid inference, Docker escalation, private data, frameworks or services.
Research writes only evidence and required lifecycle tracking.
Resolved root: .copilot-tracking/research/2026-10-17/.

## Extension Registry and Provenance

Repository instructions selected for all paths: canonical documents, branch
safeguards, synthetic testing, audit preservation and privacy-safe commits.
rpi-research selected for three ordered waves. UI skills deferred because
backend-only implementation is preferred. Specialist research delegation skipped:
one continuous bounded permission/transaction trace.

## User Participation and Research Decisions

User explicitly requests full ordered RPI and final pushed PR. This is confirmed
automatic continuation, with no routine approval prompts. Stop at pushed PR as
explicitly directed. Clean worktree and requested topic branch verified.
Issue declares no dependencies; #73 is hierarchy, not an implementation dependency.
PR #377 is open and owns forms.py/new forms routes; no dependency assumed.

## Direction Controls

Allowlisted inconsequential fields only; no widened edit authority, approval
fabrication or arbitrary JSON patch. Server-side preview must expose targets,
changes, validation failures and per-case outcomes before apply. Recheck rights
and freshness transactionally. Preserve actor/source/version/time/reason audit.

## Research Questions

| ID | Question | State |
| --- | --- | --- |
| Q1 | Exact criteria and existing permitted fields? | Open |
| Q2 | Durable preview and atomic stale/authority enforcement prior art? | Open |
| Q3 | API/audit/test overlap and minimum safe implementation? | Open |

## Prior Knowledge Gate

Original, addendum, reference index and memory read. Issue's claim that controlled
edits exist is a starting claim to verify in source, not implementation evidence.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Opening: inspect requirements, component guides and permissions/store/API inventory.
Reflection: no general field-edit or bulk preview exists. Existing domain actions
are intentionally separate. Ownership moves only after handoff acceptance.
PRD and BRD use the same FR numbers for different requirements; use the PRD's
exact edit/bulk wording and preserve the BRD's lifecycle/sign-off constraints.

#### Wave 2: Deeper

Prioritized core store, workflow and SQL commit hooks. Existing `_stock_actor`
verifies registered named staff and owner/manager checks establish the relevant
case-write boundary. `_SyncLock` refreshes cases but caches staff; apply must
read SQL staff inside the writer transaction, not trust that cache. SQL
`save()` checks all touched case rowversions, appends audit, and updates shared
documents in one transaction. `DOCS` is the durable document extension point.
Reflection: persist server-owned preview in one checked document; bind exact
case/staff snapshots, actor and original normalized request. Revalidate inside
`save()`'s existing cross-process writer lock.

#### Wave 3: Contrarian

Challenged direct owner reassignment, approval-field denylisting, client-carried
preview and sequential per-case save. Reject all: ownership requires receiver
acceptance; denylisting misses new controls; client snapshots can be forged;
sequential save permits hidden partial writes. Preserve existing owner and
resident-update commitments, hazard clocks, source evidence and controlled
decisions. Only administrative `case_reason`, `handoff_due_at` and
`handoff_next_action` are candidates. Handoff edits require an existing active
handoff, affect no acceptance/ownership/resident commitment, and retain normal
staff-note visibility. `case_reason` uses existing reason visibility.
Reflection: narrowly bounded fields satisfy permitted case/task detail editing
without a new ownership/approval route. Batch is all-or-nothing; any preview
failure blocks every write. No UI work needed for this additive API capability.

## Evidence Log

| ID | Evidence |
| --- | --- |
| C1 | docs/prds/zava-forward-retrofit-programme-demonstrator.md:840-842,1453-1456: FR-005/006/007, AC-007/009/010 exact contract |
| C2 | docs/brds/agentic-retrofit-programme-brd.md:1400-1402: same-number BRD requirements concern lifecycle, immutable transition and technical release; not equivalent numbering |
| C3 | src/core/src/zava_forward/core/store.py:398-451: named registered staff and owner/manager stock writes; detail clones case history at 358-395 |
| C4 | src/core/src/zava_forward/core/workflows.py:155-235: staff lookup, owner/manager handoff offer, immutable handoff events and acceptance-only ownership transfer |
| C5 | src/core/src/zava_forward/core/sqlstore.py:420-451,501-637: cached staff, rowversion writes, shared checked documents, atomic audit and rollback |
| C6 | src/core/src/zava_forward/core/projection.py:43-66,115-172: staff/contractor default deny and free-text reason visibility |
| C7 | src/api/src/zava_forward/api/server.py:668-855: authenticated POST, trusted-proxy CSRF and standard 400/403/404/409 mappings |
| C8 | src/core/src/zava_forward/core/mssqlstore.py:58,160-178: BEGIN IMMEDIATE maps to SQL Server cross-process application lock |
| C9 | src/api/tests/test_role_endpoint_inventory.py:25-66: explicit route inventory must grow; shared with concurrent forms PR |
| W1 | https://github.com/jmservera/ama/issues/78 retrieved 2026-10-17: three issue criteria, no dependencies, parent #73 |
| W2 | https://github.com/jmservera/ama/pull/377 retrieved 2026-10-17: forms module/routes plus store DOCS and role inventory overlap; no unmerged dependency |

## Findings, Alternatives and Decision State

Q1-Q3 answered by C1-C9/W1-W2. Accept server-owned durable preview plus
transactional revalidation and explicit closed allowlist. Reject arbitrary
JSON patch, direct owner transfer and controlled evidence/decision edits.
Case history holds versioned old/new values, actor, source/version, UTC timestamp,
reason and batch ID; hash-chain audit retains the full same event.
Preview contains only permitted target identifiers and proposed old/new fields;
foreign/noneditable cases expose only submitted ID and failure, never record data.
Unknown/invalid input is an auditable rejection, without recording raw hostile
payload or private field values.

## Risks and Residual Uncertainty

JSON store cannot provide cross-process or multi-file transactional durability;
existing SQLite/SQL path owns durable atomic guarantees. Azure SQL execution
is prohibited in this task, so use inherited transaction hooks and portable SQL,
with offline dialect coverage only. Generic backend API is not a new UI workflow
or WCAG acceptance claim. Current field-authority remains an exercise contract,
not actual operational approval. No regulatory currentness claims.

## Self-check and Re-entry

All three waves executed inline in order. No independent lane justified.
Scope/refinement completed within Research; no broadened service or framework.
No remaining source gap changes this bounded implementation. One cycle sufficient
under focused coverage/materiality; re-enter only if commit-hook evidence fails.

## Planning Readiness

Ready. Research disposition: executed. Handoff: C1-C9 and W1-W2; no blockers.
Missing installed package observed with system Python; own repository venv
created and editable distributions/dev tools installed. No private data used.
