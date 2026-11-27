---
title: Issue 2202 live research (third 2026-11-27 pass)
---

Refs #2202. Research disposition: executed. Planning Readiness: Ready. Evidence: [live note](../../docs/reference/research/issue-2202-live-2026-11-27-r3.md) and [raw output](../../docs/reference/research/issue-2202-live-20261127T090220Z/).

Findings: the estate is unchanged (API 0000131, resident 0000030, agents 0000004, hardening enforced on three apps and five jobs). All four unticked criteria re-prove except image digest to commit provenance and a rollback drill (not authorised). One new observation: one chat ask returned 500 with `cause=sql-write-lock-busy` while the receiver held the SQL write lock; the retry succeeded. Revision 0000131 (created 02:58 UTC) predates the answer-save retry in #2448 (merged 05:21 UTC), so the deployed image lacks it. In source, the question save at `chat_panel.py` line 857 has no lock retry, although it is the same single-transaction, nothing-written-on-timeout save.

Planning direction: add the same bounded retry to the question save through one shared helper, with a regression test. Do not deploy (outside this goal).
