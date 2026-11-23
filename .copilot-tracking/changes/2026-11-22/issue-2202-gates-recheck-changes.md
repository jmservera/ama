---
title: Changes, issue-2202-gates-recheck
ms.date: 2026-11-22
---

## Changes

* Added docs/reference/research/issue-2202-gates-recheck-2026-11-22.md and its evidence folder (probes, JSON, az state, two screenshots).
* Appended a log entry in docs/reference/log.md and an index paragraph in docs/reference/README.md.
* No source, infra or Azure change; the unowned job-tmp-probe-2061 was left as found. Documentation-only, focused tier; no tests apply.

## Per-criterion table for #2202

| Criterion | Status | Evidence |
| --- | --- | --- |
| Images rebuilt from main and rolled | Partly proven | API 0054 and resident 0026 live; no source commit visible from the CLI for any image |
| Revisions Running and Healthy; hardening enforced, rollback noted, agents difference explained | Proven for state; rollback not exercised | az-state.txt; api and agents enforced, resident has no variable |
| Owner demo checks (charts, map gauges, consent, routing, half of homes) | Routing proven; rest unproven on 0054/0026 | earlier proofs on 0053/0025 and 0024 |
| Live receipt and log entry | Proven | research note and log entry |
| Generative AI answers (owner gates) | Unproven | SUS-1 open (scope all, 2026-11-18); resident ledger expiry not directly readable, SQL public access Disabled |
