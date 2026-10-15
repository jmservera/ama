<!-- markdownlint-disable-file -->
---
title: Generator coverage baseline research
description: Focused issue 167 research and planning handoff
ms.date: 2026-10-15
---

## Research Brief

Task #167, slug `src-generator-coverage-167`. Produce an auditable engineering
baseline against the merged needs inventory, reuse existing generators, and
leave owner decisions and unproduced evidence open. Audience: PR reviewer.
Output mode: convergence preparing planning. Posture: focused, selected from
the explicit caller scope. Evidence root: `.copilot-tracking/research/2026-10-15/`.

## Research Parameters and Direction Controls

Only the supplied worktree and branch may change. New tooling/tests belong in
`src/core`; no new generator, private dataset access, output in the repository,
SQL changes, deployment, billable inference or owner approval claims.
Do not touch `.env`, `.vscode`, or the issue-tracking export directory.
The caller explicitly requests the full loop and publication, so eligible phases
continue without routine approval. Non-interactive execution cannot obtain
missing owner scope decisions; those remain outside implementation.

## Extension Registry and Participation

Repository instructions, ADR 0006 and parity matrix selected for layout and
dependency rules. RPI phase skills selected for lifecycle evidence.
Python foundational skill applies to new typed tooling at implementation.
No research worker: this is one tightly coupled inventory/contract trace.
No external domain research: no new regulatory or model claim is proposed.
No intake question is needed; acceptance criteria and exclusions are explicit.

## Initial Questions and Candidate Areas

1. What remains after PR #243 and the src migration?
2. Does every partial/missing need have a durable route?
3. Can generator conventions be checked without private data or new assumptions?

Candidates: issue comments, merged moves #296-#302, needs inventory, provenance
register, scenario manifest, migrated tests and generator source.

## Research Cycle Log

### Cycle 1, Wider

Issue #167 has two acceptance criteria: route every gap and reuse seed,
identifier and synthetic conventions. PR #243 supplies a baseline but records
owner mapping confirmation and SN-01 regeneration scope as open. Moves
#296-#302 are merged. Reflection: do not repeat completed data generators;
investigate whether the metadata gate actually rejects broken closure records.

### Cycle 1, Deeper

C1 checks only truthiness: whitespace-only notes, malformed issue strings,
duplicate IDs and unexplained deferrals can pass. Existing generator tests
already exercise seeded byte reproducibility, stock links, fabric/EPC labels,
synthetic lifecycle states without approvals, and SQLite restart. Reflection:
reuse those tests instead of inventing another generator or private audit.

### Cycle 1, Contrarian

Closed children #169/#170/#173/#174 are not sufficient to mark their partial
inventory rows covered: private linkage, owner scope and full application
evidence differ from fixture engineering. Scale homes/events use a manifest
`source_type=SYNTHETIC`, while household records have `is_synthetic`; the
inventory's universal per-record wording exceeds existing evidence. Do not
silently relabel historical snapshots or claim conformity. Reflection: a
metadata report must label routing validation separately from generator-output
conformance and owner acceptance, preserving all open items.

Cycle complete. Further source discovery is unlikely to change this bounded
metadata implementation; private regeneration and owner decisions remain
explicit follow-ups rather than blockers to this engineering-only slice.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/167 (retrieved 2026-10-15) | Two criteria, reopened after baseline, src pivot preserves criteria |
| W2 | https://github.com/jmservera/ama/pull/243 (retrieved 2026-10-15) | Baseline delivered; owner mapping and stock-regeneration scope remain open |
| W3 | https://github.com/jmservera/ama/pull/298 (retrieved 2026-10-15) | Synthetic tools moved to core; outputs default to ZF_DATA |
| C1 | src/core/tests/test_needs_inventory.py:54 | Existing closure test checks truthiness, not issue shape or deferral rationale |
| C2 | docs/reference/research/retrofit-synthetic-data/needs-inventory.json:4 | Version 1.2.0 awaits owner review; partial coverage is intentionally retained |
| C3 | src/README.md:21 | Core imports no workload; API may import agents until #144 |
| C4 | src/core/tests/test_generated_dataset.py:48 | Existing generator tests exercise 980-case generation from a mocked fictional register |
| C5 | src/core/tests/test_synthetic_determinism.py:35 | Reproducibility and historical payload hashes already have regression coverage |
| C6 | src/core/src/zava_forward/core/synthetic/scale_fixture.py:40 | Homes/events lack per-record is_synthetic; manifest labels do not prove the universal convention |
| W4 | https://github.com/jmservera/ama/issues/168 (retrieved 2026-10-15) | Reopened after link/fabric implementation; remaining regeneration evidence is not supplied |

## Findings, Alternatives and Decision State

Select a small read-only metadata validator/report in core synthetic tooling,
with negative tests. Validate unique need IDs, coverage vocabulary, issue
references, nonblank rationale, explicit deferrals, and required conventions.
Report all rows, totals, and pending owner items without promoting coverage.
Existing generator suites supply limited engineering evidence only.

Reject a new generator: explicit caller exclusion and existing implementation.
Reject private full-stock run: unavailable owner scope/evidence.
Reject automatic GitHub-status-to-coverage updates: closure is not acceptance.
Reject a full generic JSON schema framework: unnecessary dependency/abstraction.

## Current Decisions and Residual Uncertainty

No inventory values, versions, owners, scope or deferrals are changed by this
slice; the report audits the merged v1.2.0 snapshot. Open: owner mapping
ratification, SN-01 register source/scope, SN-03/08/09 volume, approved refresh,
full #103/#144 evidence, and per-record synthetic-label reconciliation.
Live AI/SQL/Azure acceptance is not produced by metadata tooling or local tests.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready for the bounded
engineering-only slice. Wider, deeper and contrarian waves completed inline;
internal findings have C# paths and external findings W# URLs/date. Owner
dependencies remain excluded, not waived. Parent may advance to Plan.
