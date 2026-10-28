---
title: Resident chat document correction details
description: Phase execution contract for issue 520 document correction
ms.date: 2026-10-28
---

## Metadata

Task ID: 520-documents-correction. Slug: resident-chat-documents-520.
Plan: .copilot-tracking/plans/2026-10-28/resident-chat-documents-520-plan.md.
Research: .copilot-tracking/research/2026-10-28/resident-chat-documents-520-research.md.

<!-- rpi:phase id=P01 -->
## P01: Own-case document contract and answer

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement projection, parser and bounded advisor wiring

Use immutable typed core records for requests, documents and resident issues.
Strictly parse a new documents_json view column. Absent canonical documents or
request list remains null, empty is known-empty. Project only named document
fields via OPENJSON/FOR JSON, and resident_issues only as explicitly labelled
resident-visible issue data. Unknown fields in original metadata stay private.
Generated placeholders do not satisfy request presence. Do not copy staff
checklist obligations or claim a clean scan approves content.

Attach the typed snapshot to CaseProgress with a compatible default. Keep the
existing rules answer as mandatory base, with source refs per request/document.
Guidance can ask staff for clarification; it cannot change the mandatory facts.
Route document-related typed questions before generic status or action refusal
when this is an explanation, not a sending/booking instruction. Preserve safety,
injection and other-resident refusals. Plain quoted issue text remains inert.

Validation: typed parser/renderer unit tests, SQL projection integration,
API own-session data and post-inference revocation/fallback assertions.
Completion requires all relevant canonical surfaces, not just constructed HTTP rows.
Completion evidence: typed core helper, fixed SQL projection/reader, CaseProgress
advisor wiring and document-first explanation routing implemented. Core, HTTP,
real SQL and actual browser checks pass; see changes record for commands/outcomes.
Before lossy SQL extraction validate original scalar/container types, using an
explicit invalid marker when source values would otherwise normalize. Keep text
untruncated. Test actual source-through-view/reader absent/null/empty, wrong-type
containers, numeric strings, oversized text/lists and exact valid boundaries.
No raw private document metadata is projected to solve validation.

<!-- rpi:phase id=P02 -->
## P02: Focused evidence and documentation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add semantic regressions and browser assertions

Core tests prove null vs empty, missing vs presented, generated placeholders,
multiple same-kind documents, all warnings/errors, stable refs, unknown codes,
strict keys/types/bounds and no acceptance inference. API uses constructed two-case
rows and fake advisor transport to assert facts/citations under AI and AI-off,
request tampering denial, no private fields and revocation. Extend existing
browser fixture with missing request plus warning and error; check text/citations,
typed routing, isolation, unknown data after sign-out and narrow/200% text layout.
Use pinned axe when available; absence blocks full gate, not claimed success.

No test removals; at most two new files and 24 methods. No new dependency manifests.
Table-driven scan matrix: clean (recorded result only, not approval), pending
(check unfinished), infected (recorded malware flag), mismatch (recorded file-type
problem), unknown (staff clarification). Every result retains document citations
and staff referral. Infected/mismatch are constructed historical/anomalous rows;
normal uploads reject and rescans normally remove them.
Component README documents source contract, unknowns, no-upload/manual route and
separate source-only view-apply requirement. No knowledge-base claim changes.
Completion evidence: one new core test file, 11 added test methods total, no
removals, API README and existing browser check extended. Browser checks actual
document citations remain reachable at 320 CSS px and 200% root text, not just
horizontal page width. Source-through-SQL tests cover valid exact limits.

<!-- rpi:phase id=P03 -->
## P03: Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Preserve independent Review, commit, rebase, gate and push

Run focused tests/lint/type checks first. Reconcile plan markers and changes before
one independent Review; route findings to later work, do not erase original outcome.
Resolve privacy-safe author/committer from gh api user, commit with Conventional
Commit and exact requested coauthor trailer. Fetch remote branch and rebase onto it
as requested. Any conflict is preserved and blocks push if not safely resolvable.
Fetch main, record reviewed `git rev-parse origin/main`, and run
`python3 tools/rpi-checks.py --all --lock-timeout 0 --base <reviewed-main-sha>
--out <new-external-directory>`. Runner holds the shared heavy lock.
Fetch main again; immediately before independent exact-head assessment and push run
`python3 tools/rpi-checks.py --verify-receipt <external-receipt.json>
--base <current-origin-main-sha>`. Moved main or any identity mismatch blocks
publication until reconciliation and a fresh run. No new candidate write after
the final gate; receipt remains external.
Update PR body without closing keywords, retaining pending human acceptance.
