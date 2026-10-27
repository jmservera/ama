---
title: Resident assistant publication changes
ms.date: 2026-10-27
---

## Scope and Current State

Task 469-publication-2026-10-27, full publication plan P01-P03.
No application, infra, Azure or ingress changes. Original implementation
Review remains Not accepted for whole-task/live acceptance.
Research Complete / Ready; Plan Complete / Ready after one independent
critique and parent dispositions. Implementation is active.

## P01: Preparation

Fetched main 49c942b33b89100c084d48a91215989e22de5887 already belongs to
candidate ancestry. Initial head 8f51686a3fbc4b1ca9a6e258a921b96f4fdeb8a6.
No rebase/merge needed; no existing head PR. Acquired shared lock with
`flock -w 0` in attached foreground process, not nohup/disown.
Authenticated GitHub id/login resolved; repository-local privacy-safe email
will be used for author and committer.

## Amendments and Divergences

Critique reported two concerns. Parent rejected the claimed temporary-path
prohibition as absent here (explicit owner tmp lock instruction and actual
successful acquisition), and the claimed automatic full-scope mismatch as
contradicted by runner `main()` selecting partial/full automatically.
Standalone partial verification was clarified in details. Original critique
is unchanged; no repeated critique, user decision or source modification.

## P02: Validation

Pending cleanup preservation, evidence commit and scoped gate. Existing
global Python lacks project distributions/pyodbc; isolated pip bootstrap is
the supported route. Do not equate any previous focused result with this run.
External receipts/logs are authoritative and never committed as final receipts.

## P03: Review and Publication

Pending this child's one independent Review and final exact-head gate/
verification/assessment. No branch push or PR yet. Private SQL migration
and authenticated managed-identity resident smoke remain explicitly unmet.
Do not deploy or alter deliberately open demo ingress.
