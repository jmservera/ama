---
title: Research for issue 114 live re-verification
ms.date: 2026-11-18
---

Scope: the only unticked criterion of #114 is "Per-year audit and ledger digest verification proven by test before reliance". Prior notes: docs/reference/research/sql-ledger-live-2026-11-18.md and sql-ledger-live-r2-2026-11-18.md. Planned: rerun the targeted tests, read-only Azure checks of the deployed image, record in a research note.

## Findings

* Only criterion 1 is unticked on #114 (live `gh issue view`, 2026-11-18); criteria 2 and 3 are ticked.
* Local run on base 4c45ae3f: `test_recovery`, `test_sqlstore`, `test_ledger_digest_blob`, 62 tests OK in 22.6 s. They cover per-year verification, sealing, tampered or dropped years, pre-reliance blocking, SQL store and MssqlStore inheritance.
* Deployed API image is `zava-forward-api@sha256:5368f4e4...`, revision `ca-cutover-test-demo-api--0000032`, running. ACR access is denied from this host, so the image's build commit cannot be read; the prior note shows it lacks `verify_ledger_before_reliance`.
* Rolling the image is a deployment change outside this brief; not done.
* Planning readiness: Ready. Disposition: executed.
