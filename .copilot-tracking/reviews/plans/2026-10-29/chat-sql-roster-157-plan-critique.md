---
title: SQL roster chat revocation final-candidate plan critique
description: One independent bounded assessment of task 157-chat-sql-roster
ms.date: 2026-10-29
---

## Metadata

* Task ID: 157-chat-sql-roster
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/chat-sql-roster-157-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/chat-sql-roster-157-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; no delegation.

## Inputs and Criterion Boundary

* Caller requirements: repair PR #503's stale SQL roster authorization finding on feat/agent-chat-157; keep source changes in src/, use independent SQLite row mutations, focused chat tests and Ruff, and commit locally only. No push, az operations or rubric changes.
* Research considered: .copilot-tracking/research/2026-10-29/chat-sql-roster-157-research.md, C1-C8.
* Decisions considered: correct the shared roster-backed resolver, preserve verified Entra and non-SQL identity paths, reuse both existing panel checks, and avoid global cache invalidation or schema changes.
* Dependencies considered: regression red evidence before resolver modification; P01 before green validation; P02-T01 before independent Review and local commit.
* Acceptance boundary: FR1-FR3, AC1-AC4, the non-functional requirements, both phases and all four tasks, with implementation-parent test ownership and at most one new fixture class containing five test methods and helpers.
* Source inspection covered chat_isolation.py, chat_panel.py, chatthreads.py, sqlstore.py, identity.py, projection.py, assistants.py and regulatory_chat.py under src/core/src/zava_forward/core; relevant core/API tests, core pyproject.toml and core README were also checked.
* This assesses implementation-plan credibility, not an implemented fix, executed test results, deployment acceptance or publication eligibility.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1; C1-C4; P01-T01 | Covered | ChatPanel.ask and its post-model path both invoke current_user. The current roster branch reads cached staff; SqlStore._sync does not refresh populated staff on each turn. The proposed bound SELECT under dblock fixes both call sites without changing panel control flow. |
| FR2; C5; AC1-AC2 | Covered | projection.allowed denies unknown/contractor chat roles but does not check disabled/active flags. The plan explicitly adds these checks and refuses missing SQL rows without cached fallback. |
| FR3; C2/C7 | Covered | current_user checks identity.is_entra and identity.verified before roster lookup. Keeping that branch first preserves its distinct verified-identity contract; the non-SQL cache path remains in place. |
| AC1; P01-T02 | Covered | Pre-dispatch SQL deletion/demotion must raise ChatForbidden before user-message persistence or provider dispatch; unchanged cache snapshots make the regression specific to SQL authority. |
| AC2; P01-T02 | Covered | A separate SQLite writer commits during the model callback. Completion rejection must prevent assistant persistence/release and produce chat.turn access-rejected. Retaining the submitted question is explicitly allowed. |
| AC3; P01-T02 | Covered | A valid cited-answer canary, allowed-role-change withholding and unchanged-user success distinguish real protection from unconditional abstention or broken model dispatch. |
| C6; P01-T02 | Covered | The existing SQL history test's final role restoration changes only cached data. Persisting that restoration makes its original history-isolation assertions meaningful under SQL authority. |
| Non-functional requirements; C4/C8 | Covered | Parameter binding and a short dblock scope follow local patterns; no inference-spanning lock or SQL-error-to-cache fallback is planned. Existing Ruff exclusions remain unchanged. |
| AC4; P02-T01 | Covered | Red/green evidence, core chat modules, API isolation/panel coverage and changed-file Ruff checks are required. Sibling test paths support test_chat_isolation, which resides in src/api/tests. |
| P02-T02; owner constraints | Covered | One independent Review, retained original outcomes, privacy-safe local commit and explicit non-publication boundary are specified. No remote or Azure action is authorized. |
| Test ownership and change budget | Covered | One fixture class can group dispatch and completion mutation matrices using subtests, plus allowed-role-change and stable-actor cases, within five methods. The existing history test is amended rather than replaced. |

## Verdict

* Verdict: Pass
* The selected resolver repair directly addresses the demonstrated cache dependency at both required authorization points. Its identity boundary, SQL-only regression semantics, bounded change surface and local-only delivery sequence are credible.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings within the supplied criterion boundary.

## Strengths and Residual Risk

* Separate committed SQLite writes and explicit comparison of both cached staff views prevent a cache-mutation test from falsely proving SQL revocation.
* The valid cited-answer control proves the normal answer path remains usable. Completion denial and permitted-role-change withholding are correctly treated as different outcomes.
* Dispatch authorization occurs before ChatPanel.ask creates its audit receipt. The plan appropriately requires access-rejected audit evidence for completion denial, not a new dispatch-audit behavior.
* Research explicitly accepts that the completion lookup is not atomic with the eventual answer write. This correction does not promise transaction-wide revocation semantics.
* SQLite evidence is not SQL Server, live provider, operational or full publication-gate evidence. The plan preserves these limitations and does not claim issue closure.

## Questions or Blocking Evidence Gaps

None for this bounded plan assessment. No significant or divergent user decision is required.

## Limitations

* No implementation or validation command was executed during this critique.
* The initial rebase and remote PR context are supplied caller facts, not independently revalidated remote state.
* Core and API both contain test_chat_panel.py. Implementation evidence must identify the actual API selector separately so a repeated core-module import is not counted as API coverage; the plan already requires both.
* Only this critique artifact was written. Existing untracked plan, details, research and state artifacts were left untouched.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Implementation parent.
* Smallest next action: Record this single critique's Pass disposition, then write the bounded SQLite regressions and capture the old-resolver failure before implementing P01-T01.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/chat-sql-roster-157-plan.md](.copilot-tracking/plans/2026-10-29/chat-sql-roster-157-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/chat-sql-roster-157-phase-details.md](.copilot-tracking/details/2026-10-29/chat-sql-roster-157-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-29/chat-sql-roster-157-research.md](.copilot-tracking/research/2026-10-29/chat-sql-roster-157-research.md) | Supplied C1-C8 evidence |
| [.copilot-tracking/reviews/plans/2026-10-29/chat-sql-roster-157-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/chat-sql-roster-157-plan-critique.md) | This independent critique |

## Next Steps

The active implementation parent may continue the approved RPI sequence after recording this disposition. No user action is required. This critic stops after this one assessment and does not edit the plan or invoke another stage.
