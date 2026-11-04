---
title: Issue 217 metering wiring research
date: 2026-11-04
---

* Research disposition: executed (code and merged PR check). Planning Readiness: Ready.
* Merged for #217: PRs 353 (synthetic security, privacy, audit; criteria 5 and 6), 642 and 695 (DPIA scope pin, readiness gate), 839 (Foundry minimisation guard), 884 (Art 22 decision builder), 964 (closed metering schema). No open #217 PR.
* Gap: `metering_record` (PR 964) is not called by any live path. Stored regulatory usage (`offline_usage`, read by `summarize`) is a separate closed shape that is validated but not against the metering schema.
* Smallest slice: add `usage_metering` and make `summarize` validate every stored usage through it, so chat and check usage cannot carry content or free text and stay in the `usage` retention class.
* Branch note: the worktree is on feat/issue-217-r3 (from main da29b6b); used as is.
* Unmet and unchanged: DPIA with DPO, DPO retention periods, live Foundry wiring, Entra roles, Art 22A-22C approval wiring and Legal/DPO confirmation.
