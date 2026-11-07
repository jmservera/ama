---
title: Review of OS-process race and restart tests (#107, C10)
description: One author review of the test-only delta; independent exact-head review not yet done
ms.date: 2026-11-07
---

Execution: one author Review after implementation, by the implementing agent. It is not independent review and not acceptance. Boundary: the two commits on `test/assistant-process-races-107` over base `f0afa8d76`. Changes: [changes](../changes/2026-11-07-assistant-process-races-107-changes.md).

## Outcome: Conditionally conformant locally; actual SQL unverified; FULL NOT READY

## Assessed

* Scope: only the existing test file and one non-discovered helper changed; no production, tool, workflow, dependency or README change.
* Duplication: the merged PR 1255 test is not repeated; these are process-level race and restart cases it did not cover.
* Semantics: assertions restate existing claim linearization, the allowance clamp and release denial.
* Safety: fake provider, constructed data, simulated approver, minimal child environment, own temporary data, bounded waits and exact-child cleanup only.

## Findings routed to later work

* The actual-SQL execution of both new methods is unverified; the owned FULL runner must show them `ok`.
* The race case proves linearized outcomes under a claim-time barrier; it cannot force a specific interleaving inside the claim transaction, so it is a regression guard rather than an exhaustive proof.
* Hosted `src-ci.yml` MSSQL does not select this class.
* Real attestation, approver and attribution, live metering and the wider C10 evidence remain human or live gates, unticked.
* The independent exact-head review and hosted gates remain required; the earlier unleased-lane records and their adverse notes are unchanged.
