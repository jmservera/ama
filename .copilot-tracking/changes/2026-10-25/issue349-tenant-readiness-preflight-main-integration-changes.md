<!-- markdownlint-disable-file -->
---
title: Issue 349 main-integration changes
description: Changes evidence for the non-rewriting merge of main ea5577b2
ms.date: 2026-10-25
---

## Changes

* Non-rewriting merge commit of origin/main ea5577b2 into the local topic branch
  (pre-merge SHA equality check passed). Local pre-merge head 229c9199; remote
  PR head 44ba5b77 unchanged.
* One conflict: .github/rubric/scores/latest.json (generated). Resolved to
  main's version; the branch's earlier score record (55/100) remains in history
  at 229c9199 and 44ba5b77 and is not deleted.
* docs/reference/log.md merged with no conflict; no line of the branch log was
  removed, and no earlier entry was edited.
* No source, test, manifest or infra change. The checker reads the app-role
  contract from the manifest at run time, so main's new ApplicationAdmin role is
  covered without edits.

## Reconciled historical claims

| Claim | Status |
| --- | --- |
| 2026-10-24: ingress Deny rule 403, literal systemAssignedIdentity audience, denied Graph reads on ca-cutover-test-demo-api | Historical, dated adverse evidence for that app and date; kept unchanged, not re-checked |
| Current login | Owner-reported working via main's Entra-authoritative app-role path (#360); not independently verified here |
| Database staff | Owner-reported zero by intent; no dependency on database staff is introduced |
| #349 acceptance criteria | Unticked; no live evidence collected |
| Original Conformant review (2026-10-23/24) | Untouched |

The tenant preflight remains a separate read-only diagnostic and grants no
authority over Entra or login. No live, SQL, browser or secret access occurred.

## Amendment A1: test alignment

The merged tree failed test_contract_matches_runtime_role_maps (1 of 35).
Cause: the manifest now lists 13 roles; ApplicationAdmin is the ADMIN_ROLE
constant in src/api auth.py, not in the role maps the test read. Changed only
infra/tests/test_tenant_readiness_preflight.py to also read ADMIN_ROLE and
expect 13 roles. The checker is unchanged.
