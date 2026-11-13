---
title: Issue 74 criterion 2 populated-building probe independent Review
description: Independent Review outcome for the populated-building two-home probe evidence, with findings retained and routed
ms.date: 2026-11-13
---

## Execution and outcome

One independent code-review agent, read-only, executed once after the probe. Outcome: Conformant-with-findings. It did not rerun the probe.

## Findings retained as returned (all low)

* "Swap would fail" is a logical claim by construction, not mutation-tested. Qualified here; no mutated run was made.
* Sentinel `Waiting` is weak and `Accepted` is not checked in the building blob; leakage coverage rests mainly on the allocation and sibling-evidence sentinels.
* Run-1 hash is truncated and run-1 source not retained; it differed from run 2 only in the documents assertion, which ignores the contract-fixture document `SYN-COMMITMENT`. Run-1 failure was a runner expectation error.
* Source-correction history UNKNOWN: consistent, no action.

## Routing

Wording limits only; no source defect reproduced, no repair or new test admitted, criterion 2 not ticked, no human approval implied. API HTTP, browser, real SQL and conformance remain unperformed. Temporary runtime deleted after the raw evidence was preserved in the changes file. No second Review.
