---
title: Issue 435 current capstone deck assessment plan critique
ms.date: 2026-11-12
task_id: current-capstone-assessment-435-1112
---

## Execution and verdict

One independent critique (rubber-duck agent) of the final candidate plan, executed once. Original verdict: Revise. No user decision was required and the critique is not repeated.

## Original findings and dispositions

* PC-001 (blocking): scope validation compared HEAD blobs and `git diff --stat` omits untracked files. Applied: validation compares protected working-file hashes and lists staged, unstaged and untracked paths before commit.
* PC-002 (blocking): Tokenomics completeness was not testable. Applied: a regex inventory of cost, token, price, saving, payback, TCA, budget and billing terms over visible text and notes of all 55 pages was run and every hit page reconciled into the register or listed as non-Tokenomics (GBP works and funding, Fabric, authorisation disclaimers).
* PC-003 (non-blocking): note-comparison wording. Applied: the assessment states that raw manifest `notes` differ from delivered notes (builder rewrites, revised notes, route lines), without attributing every difference to one cause; delivered notes were compared with the generated script (54 of 55 exact, page 28 absent).
* PC-004 (non-blocking): the plan permitted pip on failure. Applied: no installation; standard-library extraction was sufficient.

The critique spot-check confirmed the blob ids and that pages 22 and 53 are S18 and B25.
