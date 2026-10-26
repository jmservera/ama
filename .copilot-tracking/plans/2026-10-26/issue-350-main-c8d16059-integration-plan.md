<!-- markdownlint-disable-file -->
---
title: Issue 350 main c8d16059 integration plan
description: Prospective plan for a normal merge of current main and bounded focused checks
ms.date: 2026-10-26
---

Prospective. Written after the research and before the critique and merge.

* [ ] Phase 1: one independent critique of this plan.
* [ ] Phase 2: `git fetch origin main`, re-verify the target SHA, then `git merge --no-ff origin/main` (normal merge; no rebase, reset, amend or force). On any conflict keep main's content for main-owned files (rubric scores take the main baseline) and append-only logs retain both sides; the checker, app, auth and features stay unchanged unless a real conflict forces an intent-preserving resolution.
* [ ] Phase 3: verify ancestry for origin/main, a9bdae31 and the prior HEAD; list the merge file delta.
* [ ] Phase 4: small focused tests in an existing environment only, no new install or env, no Docker or browser: the checker tests and the new resident-preview unit tests if an existing environment can import the merged packages. If none can without an install, record that limit instead of installing.
* [ ] Phase 5: one genuine bounded independent review of the merge, writing the review artifact; outcomes preserved as returned.
* [ ] Phase 6: changes record and state, commit, report candidate gate readiness. Stop.

Out of scope: push, PR body, acceptance ticks, issue closure, heavy gate, cloud, SQL, Graph, roles, deployment, live capture, checker default or fixture changes.
