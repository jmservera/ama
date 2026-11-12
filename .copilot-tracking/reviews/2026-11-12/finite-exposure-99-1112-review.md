---
title: Finite exposure observation guard (issue 99) review
description: Original single Review outcome, preserved as returned
ms.date: 2026-11-12
---

## Execution

Executed once, by an independent code-review subagent (default model), read-only, against implementation commit `10a9d1e4c` versus base `d8509ebc4`. It ran the unit module (16 tests OK) but did not re-run ruff, mypy or the finance suite. Not repeated.

## Original outcome

Findings open (behaviour conformant; one scope-cleanliness finding).

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| RV-01 | Medium | The test edit dropped the `class LiveSignal(unittest.TestCase):` header, folding its members into `ExposureLimits` (`src/core/tests/test_exposure_limits.py:96`). No test lost (14 to 16 tests equals the two added), production code unaffected; contradicted "nothing else changed". | Own defect tightly coupled to this change. Corrected in a post-review commit (header restored; `git diff d8509ebc4 -- tests` shows no removed lines). Not re-reviewed, per one-Review rule; the independent exact-head review must confirm. |

Reviewer verified as correct: guard logic, exact-type preservation (bool, Decimal, numpy, subclasses still Unknown), no `OverflowError` for huge ints, +inf moving from Breach to Unknown (both pause, disclosed), test coverage, and that changes and evidence claims match the code.

## Post-review verification (not a second Review)

After the correction: unit module 16 tests exit 0 (`LiveSignal` tests present again), ruff check 0, ruff format check 0, mypy 0, finance tests exit 0 with 19 skipped by the runner. Raw outputs: `*-post-review.out` in the [evidence folder](../../evidence/2026-11-12/finite-exposure-99-1112/exit-codes.md).

## Residual items

Negative finite observations remain Within (unchanged, follow-up candidate). Full gate, hosted CI and human approvals are not run or claimed.
