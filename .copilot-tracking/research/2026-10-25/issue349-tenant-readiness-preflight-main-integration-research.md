<!-- markdownlint-disable-file -->
---
title: Issue 349 current-main integration research
description: Prospective read-only research before merging main ea5577b2
ms.date: 2026-10-25
---

## Scope

Local-only. Draft PR #437 remote head 44ba5b77 (open, draft); local head
229c9199; merge-base f1e2d830; origin/main ea5577b2 (11 commits ahead). Worktree
clean. No Azure, Graph, SQL, browser or secret access.

## Findings from git history only

* Main contains the Entra-authoritative staff access change (7d4e89bb, #449,
  Refs #360) adding the ApplicationAdmin role to infra/entra/app-registration.json,
  plus grant-application-admin and a non-destructive demo seed merge. Owner
  statement (2026-10-25): login confirmed working and database staff are zero by
  intent. This is taken from the owner's instruction, not re-verified live.
* The checker reads the role contract from the manifest at run time and the
  unit tests do not hard-code role keys, so the new role needs no code or test
  change. The checker stays a separate read-only diagnostic.
* Main changed docs/reference/log.md and rubric files; this branch also appended
  log entries and a rubric score. Textual conflicts are possible and both
  append-only sets must be kept.
* Historical 2026-10-24 diagnosis (ingress Deny rule 403, literal
  systemAssignedIdentity audience, denied Graph reads) was true for that date and
  app and stays as dated adverse evidence. It must not be presented as a current
  blocker, and no database-staff dependency is introduced.

## Planning readiness

Ready: non-rewriting merge of origin/main; resolve conflicts preserving both
log sets; add a dated reconciliation note only; no source change unless the
focused tests fail.
