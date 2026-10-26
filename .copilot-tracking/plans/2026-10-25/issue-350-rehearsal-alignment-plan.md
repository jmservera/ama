<!-- markdownlint-disable-file -->
---
title: Issue 350 rehearsal alignment plan
description: Prospective plan for evidence alignment, merged-main re-rehearsal and lineage publication
ms.date: 2026-10-25
---

Research: [research](../../research/2026-10-25/issue-350-rehearsal-alignment-research.md). Details: [phase details](../../details/2026-10-25/issue-350-rehearsal-alignment-phase-details.md).

## Phases

* [x] Phase 1: Re-run the local synthetic rehearsal against merged main on a separate disposable SQL container and port 8351; stop only those helpers.
* [x] Phase 2: Write the changes artifact: dated alignment addendum that supersedes the stale tenant/staff blocker wording and discloses the corrected review accuracy findings.
* [ ] Phase 3: (review done once) commit; fresh fetch; full gate with new external output and lock timeout 14400; verify receipt.
* [ ] Phase 4: Normal push to the same PR branch and accurate PR body (draft, Refs #350).

## Constraints

* No source, auth, README or main change; no Azure, Graph, network test, paid AI, deployment or role assignment.
* Services on 8350, 8444, 8445 and `ama-350-feedback-sql` are not restarted or mutated.
* No history rewrite; no closing keyword; issue acceptance unchanged.
