---
title: Issue 1231 r29 research, final root d99e6901 and main f0af reconciliation
description: Evidence for adopting the rebased root into the child on current main f0afa8d7
ms.date: 2026-11-07
---

Task `issue-1231-r29-final-mainf0af-reconciliation`, parent task `issue-1231-r28-root-stagecleanup-propagation`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Child start: HEAD `5630fb25c93cb030b14e38eae61e1cd8dee9d1a5`, tree `03c63bb4be3f274e7eb213be9942722928f578a3`, ignored-inclusive clean. PR #1242 target stays `feat/ranking-publication-runner-79`.
* Current main (fetched): `f0afa8d76d7be13ec4278321e09e16e23eaeb37c`, tree `d9414abc0a8c696c7f0069e30a827b2dad92b1c2`. This supersedes the earlier 38990b19 pin; the only change since then is the rubric score JSON (score 77 unchanged). The earlier r29 attempt stopped at the base check with no write; that stop is adverse history, not a failed gate.
* Root `issue-79-publisher`: `d99e6901e5fb7e4c8ea46ba3766ff23f31be0f7c`, tree `900c772c7c2b22b729b99eb0c37eb030d6261684`, ignored-clean, read only; main f0af is its ancestor. Root delta over its earlier b6fc0d9b: score JSON (equals main), a 4-line append to `docs/reference/log.md`, and six root r27 RPI files. No source, tools, workflows or tests change.
* Root src delta over bb7e044c (the root the child already merged in r28) is only UI: `role-screens.js`, `test_data_operator_screen.py`, `test_exception_register_screen.py` (main UI #1260). Root core, Store, runner, server and ranking wiring blobs equal bb7e044c.
* The child differs from bb7e044c in the ranking source by design (unique stage, `_remove`, `_confirmed`, typed `DurabilityUnconfirmedError`, retained-stage metadata, tests adapted to `.ranking-*.tmp`).
* Dry-run merge of d99e6901 into the child: conflicts in the ranking README, helper, runner (add/add), two core tests and the API wiring test. They come from the rebased history having a different merge base, not from new root source intent.
* The Config unit is the class `Config` at `src/api/tests/test_exception_register.py:163`; root's earlier note that it was absent is preserved unchanged and corrected separately here.

## Conclusions

* For the ranking paths, root d99 equals bb7e044c, which is an ancestor of the child; keeping the child's blob for each conflicted path is an intent-preserving resolution. Prove it by showing the child blob equals the r28 merge result for those paths.
* Take the root's UI source, tests, score JSON, log append and RPI files unchanged.
* One normal `--no-ff` merge; no rebase, no history rewrite.
