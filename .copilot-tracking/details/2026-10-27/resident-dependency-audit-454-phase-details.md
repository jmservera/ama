---
title: Resident dependency graph audit phase details
description: Bounded correction, final comparison, Review and publication
ms.date: 2026-10-27
---

## Metadata

Task ID: jmservera/ama#454:dependency-audit-2026-10-27.
Plan: .copilot-tracking/plans/2026-10-27/resident-dependency-audit-454-plan.md.
Research: .copilot-tracking/research/2026-10-27/resident-dependency-audit-454-research.md.

<!-- rpi:phase id=P01 -->
## P01: Correct and verify the whole graph

Status: Complete. Both tasks are evidenced in the changes record, including
the single final graph reread, source hashes and Markdown/link/diff checks.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Apply graph, gate and narrative corrections

Use C1-C5 and the research mapping. Edit the existing backlog and active
proposal reconciliation only. Split groups without changing RB ownership.
Represent S10/S12 ordering inside their slices. R1 evidence covers identity,
grants, recovery, revocation and essential privacy/accessibility. R2 evidence
requires R1 and own case/documents/upload/review tests. R3 evidence requires
R2, appointment/events/assisted/accepted-handoff/no-detriment checks plus
the RB-01-frozen baseline. M1 remains a partial R2 composition.
RB-23 provides independently tracked stage scripts, not a whole-R5 blocker.
Governance inventory items remain evidence/approval records, not newly
sequenced execution. No new approval or runtime authority.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Re-read once and review Markdown, links and diff

After all edits, read final story table, stage gates and final backlog
together once. Check all twenty source mappings, every RB row, fixture
requirements, conditional freezes and absence of cycles. Check changed
Markdown table shapes/local links, preserved boundaries and git diff.
Record exact hashes and any residual finding. No full runtime/local gate,
uv or new dependencies. Do not repeat correction/Review on later findings.

<!-- rpi:phase id=P02 -->
## P02: Independent Review and publication

Status: P02-T01 Complete / Conformant with justified divergence, no findings.
P02-T02 remains pending, not implementation completion evidence. No
residual graph finding from the parent comparison or independent Review.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run one independent Review

Fresh reviewer activates rpi-review, reads canonical plan/details/research
and final sources, and writes only the designated review artifact.
Return execution, outcome, assessed hashes and complete findings.
Human approval remains unavailable; requirements FAIL remains open.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Publish and address threads

After Review, persist state and commit implementation plus original dated
evidence. Use `gh api user` identity with local noreply author/committer
and the supplied Copilot trailer. Normal pull/rebase handles bot latest.json;
compare assessed PRD/backlog/proposal hashes after synchronization and
immediately before push. If any assessed source changes, STOP publication
and thread resolution, report invalidation and changed paths, and do not
repeat correction, reread or Review. Bot-only updates may proceed only
with byte-identical assessed sources. This directly resolves PC-001 while
preserving the original Revise verdict.
Push without force and reply with immutable source/Review evidence to
PRRT_kwDOUU8JX86wwINw, PRRT_kwDOUU8JX86wwIOl,
PRRT_kwDOUU8JX86wwIPV and PRRT_kwDOUU8JX86wwXRl.
Resolve addressed threads only; verify remote head and OPEN/unmerged PR.
Any residual finding is reported, not a new correction cycle.
