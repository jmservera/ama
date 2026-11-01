---
title: DPIA scope drift guard plan (issue 217)
description: Plan for a test that pins the retention report classes to the DPIA draft
ms.date: 2026-11-01
---

## Plan

* [x] P01 Add `DpiaScope` tests in `src/core/tests/test_regulatory_privacy.py` asserting each
  `CLASSES` storage term and `reg_chat_turn` appear in the DPIA draft, and that the usage class
  states it inherits parent access, retention and audit.
* [x] P02 Run focused validation: unittest for the file, ruff check, ruff format --check, mypy (core).
* [x] P03 Commit, push, open PR with `Refs #217` naming unmet criteria.

Details: [phase details](../../details/2026-11-01/regulatory-security-privacy-217-dpia-scope-phase-details.md).

## Critique (single pass)

Verdict: Proceed. Finding: do not claim criteria 1-4, 7, 8 as proven; the PR uses `Refs`.
Applied directly.
