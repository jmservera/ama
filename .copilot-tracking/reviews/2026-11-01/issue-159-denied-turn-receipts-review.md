<!-- markdownlint-disable-file -->
---
title: Issue 159 denied-turn receipts review
description: Single post-implementation review of the receipt change
ms.date: 2026-11-01
---

## Review

* Execution: executed once by the implementing agent against the diff; not an independent review. Independent review remains a publication gate.
* Outcome: Conformant for the slice; no open material findings.
* Checks: no model call and no stored message on denial; the question text is not in the receipt; the actor falls back to `unknown` when no email; behaviour for permitted turns is unchanged (existing 99 + 43 tests pass, including foreign/missing thread receipts on both routes).
* Residual: a request rejected by the earlier role gate (`get_kind` projection, before `_chat`) records no chat receipt; a gateway-level audit exists separately. Routed as a follow-up.

* Publication: blocked until the complete local RPI gate runs with a verified external receipt; CI does not substitute.

## Criteria status

* Criterion 6 (named screen-reader test, announcements): unmet, needs a named human AT run.
* Tokenomics criterion: improved (denied turns now receipted) but not proven for the earlier role-gate path; left unticked.

## Follow-ups

1. Record a chat receipt for the earlier route-level role gate denial.
2. Named human screen-reader run (owner or accessibility tester).
