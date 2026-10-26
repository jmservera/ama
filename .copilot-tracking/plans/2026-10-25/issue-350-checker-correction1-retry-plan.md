<!-- markdownlint-disable-file -->
---
title: Issue 350 checker correction 1 retry plan
description: Prospective plan for the forward-ordered retry; written before critique and execution
ms.date: 2026-10-25
---

Plan status: prospective. Written after the retry research and before critique, checks and review.

* [ ] Phase 1: independent critique of this plan and the retained minimal fix (one pass, read-only).
* [ ] Phase 2: apply critique findings that are compatible. Source changes only if the critique identifies a genuine behaviour gap, and then only after a focused failing regression is written first.
* [ ] Phase 3: execute checks on the unchanged tree: the 80 checker tests, the CLI on a 10000-deep file (expect blocked and exit 2), and the admin fixture (expect me_contract pass, admin_account not-run, overall blocked).
* [ ] Phase 4: one independent post-implementation review of both defects and the full `me` contract.
* [ ] Phase 5: record results and commit artifacts. If no source change was needed, the existing head 16e6d12d receipt covers source and only artifacts are added, so a fresh complete gate on the new exact head is required before any push (a new head invalidates the old receipt).

Constraints: no unrelated application or auth change, no artificial code churn, no Azure, Graph, roles, live AI, services or data changes, no rewrite, amend or force push, no receipt-only commit, PR 436 stays draft, issue 350 open, no merge. Resident gate PID 768864 owns the heavy lock and is not interrupted. Stop with a blocker if any of this cannot be complied with.
