---
title: Issue 215 AT record check plan
ms.date: 2026-11-03
---

## Plan (slice 2 of 3; slice 3 is the human run, owner-gated)

1. [x] Add `src/api/checks/regulatory_at_record_check.py` and unit tests.
2. [x] Link from `src/api/README.md` and the acceptance protocol; log entry.
3. [x] Focused validation: unit tests, ruff, mypy strict.
4. [ ] Commit, push once, open PR with `Refs #215`.

Details: [details](../../details/2026-11-03/issue-215-at-record-check-details.md).

## Critique (one pass, self)

Verdict: acceptable. Risk: complete records read as acceptance; mitigated by the output note and docs. The check is form-only and invents no conformance rule. Suppliers are exempt from the chat-unavailable run because they have static guidance with no chat.
