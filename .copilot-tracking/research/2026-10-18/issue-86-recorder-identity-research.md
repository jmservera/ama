<!-- markdownlint-disable-file -->
---
title: Issue 86 historical recorder identity research
ms.date: 2026-10-18
---

## Research Brief

Focused, internal convergence research for the coordinator's bounded historical
decision-recorder identity gap. Audience: implementer and independent reviewers.
Exact base: `6c1e376ff1241316272df22a5a3a6853aae9f87b`.
Task identity: issue-86-recorder-identity; issue #86 remains open.

## Research Parameters and Direction Controls

Run Wider, Deeper, Contrarian in order. Verify supplied line-level hypotheses
with source and failing-first synthetic probes. Inspect direct callers, identity
helpers, persistence, projections, tests and component commands before editing.
No private inputs, support, environment files, Azure, IAM, Graph, contact,
inference, spending, web changes, unrelated roles or review-authority changes.
Maximum two corrective source cycles; one critique and one original Review.
Preserve adverse originals. Legacy unknown must not manufacture independence;
only dependent review assignment may fail closed.

## Extension Registry and Participation

Repository instructions and selected RPI skills apply. User explicitly requests
the whole ordered loop and publication, so no routine phase confirmation is
needed in this noninteractive execution. Research inline: tightly coupled trace,
no independent research lane warrants delegation. Independent critique and
original Review will use distinct bounded agents. Web/security-audit skills
not selected: backend identity correction, not a UI or vulnerability audit.

## Questions and Candidate Areas

1. How is current server identity resolved and compared?
2. What historical evidence exists and how are legacy unknowns handled?
3. Which persistence, API and privacy surfaces depend on this shape?
4. Can stable code/oid deny the changed-email recorder without blocking others?

Candidate areas: resident_decisions.py, direct Store/API callers, identity prior
art, projection, JSON/SQLite/MSSQL stores and existing tests/component guides.
External research is unnecessary for this repository-specific defect.

## Research Cycle Log

Cycle 1, Wider: traced decision writer, service opening/reassignment, Store detail,
API route, role projection and JSON-body SQL persistence. Existing implementation
is extensive; no replacement workflow or service is needed. Reflection: the
gap is historical identity, not missing resident-decision functionality.

Cycle 1, Deeper: verified code/oid comparisons already protect handler/reviewer
separation, but not contested-recorder separation. Current `_actor` resolves
and exactly validates registered staff; `_identity` copies a server snapshot.
`_operation` supplies atomic rollback and SQL writer replay, already used by
service actions but not decision recording. Reflection: decision snapshots must
use this transaction boundary to prevent stale/forged server evidence.

Cycle 1, Contrarian: finance legacy fallback looks up today's email owner and
is unsuitable for historical proof. Quality and hazard show explicit unknown
refusals and comparisons of recorded identity. Keeping email-only compatibility
would retain the demonstrated bypass; globally blocking consent would exceed
scope. Retention removes decisions but deliberately preserves service requests:
new review requests need their own bound immutable snapshot. Projection currently
redacts narratives from nonresident staff but does not remove unknown future
identity fields: explicitly strip the new snapshot there. Reflection: use narrow
review-assignment refusal for unknown historical identity, no backfill, keep
service/complaint and supplied consent recordable.

## Evidence Log

* C1: `src/core/src/zava_forward/core/resident_decisions.py:478-516` stores
  name/email only and checks contested recorder by email only.
* C2: `src/core/src/zava_forward/core/resident_decisions.py:595-604` compares
  handler identities by email/code/oid but reassignment recorder by email only.
* C3: `src/core/src/zava_forward/core/change_provenance.py:17-41`,
  `resident_decisions.py:56-57,124-211`: existing registered actor, snapshot,
  rollback and SQL replay controls.
* C4: `src/core/src/zava_forward/core/sqlstore.py:553-615` replays resident
  validation inside writer transaction; MSSQL inherits JSON-body persistence.
* C5: `src/core/src/zava_forward/core/projection.py:149-174` nonresident
  projection needs an explicit exclusion for the new nested identity.
* C6: `src/core/src/zava_forward/core/resident_decisions.py:375-399` retains
  requests after resident payload deletion. New reviews must retain their
  original version-bound snapshot independently.
* C7: `src/core/src/zava_forward/core/finance.py:41-56`,
  `quality.py:164-183`, `hazard.py:114-137`: prior art for normalized identity
  comparison and explicit unknown, with finance fallback rejected here.
* C8: `src/api/src/zava_forward/api/server.py:936-951`: existing route already
  maps denied/committed outcomes; no new API or web surface required.
* C9: `src/core/tests/test_resident_decisions.py:2047-2081`: local opt-in
  MSSQL test adapter and disposable fixture databases. Component READMEs and
  pyproject files supply test, Ruff and mypy commands.
* C10: `issue-86-recorder-identity-before.txt` and the adjacent reproducible
  probe: eight adverse JSON/SQLite open/reassignment probes failed their required
  denial assertion at the exact base. Stable code or oid remained unchanged,
  but all eight assignments succeeded and changed both case and successful audit.
  No recorder snapshot existed. Exit 1 is the expected failing-first result.

## Findings, Alternatives and Decision State

Select server-derived snapshots for new versions; bind review snapshots to exact
measure/version and compare normalized email/code/oid at opening and redress
reassignment. Reuse resident `_identity`, `_actor` and `_operation`; extract the
existing inline same-person comparison into a local helper for these paths.
Do not reuse finance's current-owner fallback. Legacy insufficient evidence stays
explicit Unknown and refuses only independent review assignment, consistent with
the caller's explicit narrow fail-closed direction. No material policy expansion
or source-approval invention is needed. Genuine distinct stable identities pass.
Existing history is never rewritten; old email ownership is never resolved into
historical code/oid. Original issue's formal complaints integration, historical
erasure, contact identity and human acceptance remain unmet, as do #130/#76 gates.

## Planning Readiness

Ready. Research disposition: executed. All three waves completed in order inline;
the focused questions are covered, and another cycle would duplicate source
evidence. Install failure: system Python lacked zava_forward; task-local venv pip
editable core/dev, agents and api/dev installation succeeded. SQL driver imports;
local SQL Server image exists. `odbcinst` is absent, but mssql-python does not
require that CLI, so this is not yet a SQL execution blocker.
