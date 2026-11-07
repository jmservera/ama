---
title: Workbench browser check queue-transition synchronization
description: Created issue record and actual failed-run evidence, separate from any product claim
ms.date: 2026-11-07
ms.topic: reference
---

## Created Issue

* Issue: #1262, https://github.com/jmservera/ama/issues/1262
* Created: 2026-11-07T20:37:35Z (state OPEN when read).
* Title: test(api): wait for rendered queue identity in browser checks
* Template: generic; `.github/ISSUE_TEMPLATE` is absent. The issue skill's shared instructions file was missing in this environment, so none was applied and none is fabricated.
* Labels/assignees: none.
* Severity and scope as filed: Medium, maintained browser-test reliability and delivery blocker. No production defect or lost case is established.
* Related, referenced not closed: #77, #76, #79, #1231, #440.

## Actual Evidence Recorded In The Issue

* Fresh FULL run at ranking root `8010a4867ef4db5df355531f5a8c1839f19ac7b2`, child `c18f45f23eca34ee960050027750597bd21d5dac`, main `f0afa8d76d7be13ec4278321e09e16e23eaeb37c`.
* Receipt failure text: `browser: browser failed (1); see 0084-browser.log; mssql: blocked by failed prerequisite`.
* Browser command 2026-11-07T20:22:12Z to 20:22:23Z failed at `workbench_browser_check.py:501`, `AssertionError: overdue queue exact expected IDs`. New and stale queue checks, queue reset, reflow and briefing recovery passed first.
* Native receipt verification: `BLOCKED: Receipt does not establish an eligible run`. No current FULL pass, MSSQL execution or publication.
* Original, unchanged references (disposable VM paths): `/mnt/ama-gates/g1231-r31-full-c18-1107/receipt.json` and `0084-browser.log`. The earlier 7990 pass is neither current nor failed.
* The ranking sources, failed receipt and old logs are not changed by this work.

## Acceptance Criteria (verbatim intent, unticked at creation)

1. Genuine prospective Research, Plan/critique, implementation and original Review, dated and committed.
2. Reproduce the equal-count stale-to-overdue problem, recording actual IDs and queue/result state, separated from any product claim.
3. Focused regression failing with the old synchronization; equal-count transition and empty results.
4. Preserve exact membership/order and final assertions; wait for the rendered result; diagnostics; no sleep/retry/waiver.
5. Unit, format/types and the maintained browser journey on synthetic data under exclusive nonqueued admission; literal exits and skips.
6. Independent exact-head assessment and hosted checks before publication/merge; ranking candidate keeps its own FULL receipt.
