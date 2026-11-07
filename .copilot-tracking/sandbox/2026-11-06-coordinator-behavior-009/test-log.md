---
title: Test log, coordinator behavior run 009 (issue 1204)
ms.date: 2026-11-06
---

* Target blob acefb44a4d254ede6d86413343127b763dec42cb (unchanged). Planning commit 769d620b8ff4aec520fffac1a43e50a45d3b4954.
* Designer: general-purpose, host-reported claude-sonnet-5.5, session_inheritance, no override, toolCallId toolu_01GtLRsrNQWQRNVmLLEQxTFB. Return sha256 64b5f038a3902774e7fb88f0f37d781b22922b59089ec823afee5d3e07900e01 (test-design.md).
* Executor: hve-core-all:hve-artifact-tester, host-reported claude-sonnet-5.5, session_inheritance, no override, toolCallId toolu_01JLBY45dv5SXsdmP7PqgdDm, 337596 ms, status Complete. Trace sha256 3a467ef077b0c619b218ff4ea11adacb8b643b4c5f50857ebd67ec8706ba8371 (executor-trace.md, 562 lines, saved verbatim). Executor self-reports three files read and emulate-only; reads are self-reported.
* Executor inputs: scenario-prompts.md sha256 2913174847c66f3eae3b1c7cc431ecd512373c37e139b9a7f097a1c63ec41adb, executor-state.md sha256 e8745fbc1bb17c630342fb00a63689fdbc6be3d68be84cb1e4fddd769d5e693a. Fixture facts and requests only; no oracle, signals or arithmetic table.
* Lead pre-execution validation: capacity rows recomputed (H-03B 7 retained incl. exited #334, one free slot, literal launch, 7 to 8; H-03F 8 to 7 to 8); H-06 paths canonical, full SHAs and receipts, positive stack batch 14 to 18 PRs; F-03 facts supplied (tick_log 233, #342 outcome, full hash, #702 log path, checkpoint resume conditions, eight H-11 PRs). No material fixture defect found.
* Lead prompt edits (hint removal only): removed "Slots: 8 - 6 = 2 free" (H-01), "One free slot" (H-02), "Admission is moot" and "No outcome authorises stopping #36"; headings and labels sanitised.
* Observed vs simulated: all outcomes are supplied fixture facts; no real command, Git, GitHub, cloud, schedule or cleanup action ran. Live schedule state (delivery #4 every 5m, maintenance #5 hourly, 1,2,3 stopped) is supplied coordinator evidence, not read here.
* Post-dispatch: blob unchanged; git status showed only the sandbox directory.
* Limitations: simulation only; High is a rigor profile, not native Automatic; harness-default model differs from earlier explicit gpt-5.6-sol runs.
