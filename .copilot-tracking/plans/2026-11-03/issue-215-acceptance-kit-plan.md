---
title: Issue 215 acceptance kit plan
ms.date: 2026-11-03
---

## Plan (slice 1 of 2; slice 2 is the human run, owner-gated)

1. [x] Add `docs/reference/research/ux/regulatory-ux-acceptance-protocol.md`; index and log entry.
2. [x] Add `src/api/checks/regulatory_comprehension_score.py` and `src/api/tests/test_regulatory_comprehension_score.py`.
3. [x] Link from `src/api/README.md` protocol section.
4. [x] Focused validation: new unit tests, ruff check and format, mypy.
5. [x] Commit, push, PR with `Refs #215`.

Details: see [details](../../details/2026-11-03/issue-215-acceptance-kit-details.md).

## Critique (one pass, self)

Verdict: acceptable. Risk: a scorer pass could be read as acceptance; mitigated by output note and docs. Answer key avoids invented rule facts; it encodes only the protocol's critical errors. No security, infrastructure, SQL or deployment surface touched, so the focused tier applies.
