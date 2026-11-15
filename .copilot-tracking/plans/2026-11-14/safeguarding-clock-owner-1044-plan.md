---
title: Plan, safeguarding clock and named owner display
ms.date: 2026-11-14
---

## Decisions

* Optional structured `safeguarding_items` on a case: `referred_at`, `response_due_at`, `responded_at`, `owner{name,role}`, `closed`, `version`. No free text is read.
* `taskqueues.safeguarding_clocks` emits `safeguarding_clocks` only when `reason_ok` (existing need-to-know roles); otherwise an empty list and a constant held statement.
* Clock states reuse `timing`; no duration is invented. Missing owner shows Unknown with an ask-the-lead action.
* Queue membership, blockers and overdue are unchanged, so safeguarding presence cannot leak through filters.
* `workSummary` in app.js renders a text paragraph (class `safeguarding-clock`), used by queue rows and case card.

## Phases

1. Core function and context fields.
2. UI rendering.
3. Unit tests (core) and Node-run rendering tests (api).
4. unittest, mypy, ruff check and format.

## Critique (single pass, direct)

* Risk: leaking via queue membership, resolved by excluding from membership.
* Risk: free text leakage, resolved by explicit field allowlist and a canary test.
* Risk: policy invention, resolved by recorded due dates only; criterion remains unticked.
