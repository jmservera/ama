---
title: Issue 114 live Azure SQL evidence research
ms.date: 2026-11-18
---

# Research (opening)

* Task: issue-114-live. Refs #114. Branch test/sql-ledger-scale-live-20261118T0728Z.
* Scope: prove the three unticked criteria (C1 per-year ledger verification, C2 measured load/latency/cost, C3 backup/restore/deletion re-application) for the synthetic desktop demo; live Azure authorised in resource group ama (cap USD 700, no drills, no Key Vault rotation, no production changes).
* Research disposition: executing. Findings are filed in docs/reference/research/ as the research note.
* Planning Readiness: Ready. Disposition: executed (live evidence gathered before the note was written).
* Findings: C1 tests on main pass locally (62 tests: test_recovery, test_sqlstore, test_ledger_digest_blob); deployed demo image lacks `verify_ledger_before_reliance` on MssqlStore (job failed with AttributeError). C2: 30-minute five-session run against ca-cutover-test-demo-api passed all four p95 limits. C3: PITR restore of a throwaway database on the same logical server, deletion register in a throwaway blob container, reapply_deletions proven; PITR cannot target another server.
* Concurrent workers share the logical server; one other restore ran at the same time.
* Process note: a credential file line was printed once by mistake while checking file shape; it was not stored in any artifact. Rotation is the owner's decision (no Key Vault rotation authorised).
