---
title: Test log, coordinator behavior run 008 (issue 1204)
ms.date: 2026-11-06
---

* Run: full fresh contained simulation, inferred High (responsibility, uncertain, not native Automatic). Sandbox retained.
* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md, blob acefb44a4d254ede6d86413343127b763dec42cb, unchanged (verified after execution). Execution HEAD b16a03f21a4e73da60e011323b4b335827b4d809, tree 8063a0f8c8873ed829ea15d4644a2569e628682d.

## Stages and host attribution

| Stage | Role | Host telemetry (subagent.completed) | Raw return sha256 | Duration |
|---|---|---|---|---|
| Design | general-purpose, fresh | model gpt-5.6-sol, firstDispatchedModel gpt-5.6-sol, explicit_override, toolCallId toolu_01Wm9ue6jK96EXagtjnipB4k | a9910e9e9f516b395b06bd6baf353b6380b056ac6695593fa0c99195bba10a04 | 119603 ms |
| Execution | hve-core-all:hve-artifact-tester | model gpt-5.6-sol, firstDispatchedModel gpt-5.6-sol, explicit_override, toolCallId toolu_01CZ5ETvbZhSC9FwsBN8emee | 7fcf7cd48a9d20aeeeead748bd2886b9cc369cf4c4f8d9379e306c55790090c4 | 69514 ms |

* This is host attribution only, not backend attestation. The executor reported its own model as not supplied (introspection gap).
* The host returned both outputs as saved pointers. I copied each saved file unchanged to the external directory (designer-return-raw.txt, executor-return-raw.txt, sha256 equal to the pointer files) and to the sandbox (test-design.md, executor-trace.md). Equality is with the host-saved file, not independently with the model stream.
* The executor self-reports reading three files: executor-state.md, the target and scenario-prompts.md. Reads are self-reported, not tool-observed.

## Lead design validation before execution

* Covered by design: R5 counts 15/16/20/21 with separate hierarchy, PR and assignment columns (H-03A to H-03G, arithmetic table); R6 positive replacement, duplicate repair and unverified refusal (H-04A to H-04C); R8 positive removal with supplied proof plus five refusals (H-05A to H-05F); S09 launch with explicit supplied outcomes (H-09); stale brief negative case with parent target (H-08); missing review evidence (H-07); genuine stack (H-06); merge gate and stabilization (H-10); final report (H-11); unconditional versus conditional stop and scoped pause (H-02); closure rotation, recovery and heavy ownership (H-01).
* Prompt edits by lead before execution: removed three explanatory lines that disclosed the expected classification (H-08, H-09, H-11) and one that disclosed the verdict wording; replaced "untrusted stale data" with a neutral phrase; removed H-05 category labels. Executor prompts file sha256 7a0a190e81ca18402cbad851c7f1b278f73c7a9b1726ed371f1c05be40fdc536.
* Lead validation MISS, recorded honestly: the H-06 fixture lists artifact paths as `track/500/...` while the target requires the canonical .copilot-tracking trees. I did not catch this self-consistency flaw before executing. It was not corrected afterwards, per the no-extra-correction rule.

## Observed, simulated and emulated actions

* Observed: executor trace text only. Every Git, GitHub, SQL, schedule, launch, merge, publication and cleanup action was emulated with supplied outcomes.
* Executor reported no invented outcomes and listed unsupplied facts as gaps (for example H-01 tick_log write, H-08 full hash, H-09 total count, H-11 eight PR identities).

## Result summary (lead reading, not the grade)

* Executor status Complete, 11 scenarios with 24 sub-snapshots.
* H-06 outcome diverges from the design oracle: the executor withheld publication of all four candidates because the supplied paths are not the canonical tree, so the positive batched stack publication path was not exercised. Cause is a fixture defect (paths), not shown to be a target defect.
* Other scenarios match their design signals on the lead reading: H-02A obeys the unconditional stop, H-02B treats the conditional stop as unmet, H-03 counts 8/7/16/20/21 correctly, H-04 and H-05 follow the supplied proofs, H-07 and H-08 reject unsafe inputs, H-09 counts retries once.

## Status delta

* Source target blob unchanged acefb44a. Tracked tree unchanged. Only the untracked sandbox directory was added during execution.

## Limitations

* Contained simulation only. High is inferred from responsibility and is not native Automatic equivalence. Native is Deferred.
* Host telemetry is attribution, not backend proof. Executor reads are self-reported.
* Schedule, cleanup, SQL and publication outcomes are fixture facts, not observed actions.
* Live schedules and tool frontmatter were not read or graded.
