---
title: Chat receipt audit locking research
description: Focused research for issue 157 and PR 503
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

# Task Research: chat-audit-locking-157

## Research Brief

* Target: serialize chat-panel receipt appends with shared store writes without locking inference or deadlocking nested callers.
* Audience: implementer and independent PR reviewer.
* Scope: `src/core/src/zava_forward/core/chat_panel.py`, its callers, store lock semantics and focused chat regressions.
* Non-goals: global store redesign, chat activation, Azure operations, remote publication or unrelated issue acceptance.
* Criteria: intact hash chain under concurrent rejected turns; all sibling unlocked appends addressed; existing focused chat tests and Ruff checks pass.
* Output mode: convergence. Status: Complete.

## Research Parameters

* Posture: focused, selected from the caller's bounded source target and supplied review finding.
* Evidence root: `.copilot-tracking/`.
* External research: none required; local code defines lock semantics.
* Caller constraints: pull first; branch `feat/agent-chat-157`; local commit only; `/tmp/mv`; no `az`; never manually edit rubric scores.
* Research edits: evidence and workflow state only.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | Repository guidance supplied in conversation | Selected: branch safeguards, Python validation, original RPI evidence and publication gate |
| Skill | rpi / rpi-research | Selected: dated phase evidence and three-wave research |
| Specialist | RPI Researcher | Skipped: a single tightly coupled trace, handled inline |
| Skill | Web design skills | Skipped: backend-only locking change |

## User Participation and Research Decisions

The explicit full-loop request authorizes this bounded Research, Plan, Implement,
Review execution without routine phase prompts. No request to change a pre-existing
manual session was inferred. The non-interactive environment precludes questions.

## Direction Controls

Reuse the open PR's branch and preserve its bot rubric commit, fetched first by
`git pull --rebase`: baseline `feccc77dcfa3fb21c14ea48bd9edba7c239a3eaa`.
No push, merge, acceptance claim, Azure action or unrelated cleanup.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Which chat receipts run without the store lock? | depth | Answered, C1/C2/C5 |
| Q2 | Which paths already own the lock and what nesting is safe? | depth | Answered, C3/C4/C8 |
| Q3 | How can tests deterministically expose and verify the shared chain race? | depth | Answered, C7/C9 |

## Prior Knowledge Gate

Read original case study, addendum, knowledge-base index and owner memory.
Memory is context, not evidence. Recent session lookup found no matching records.
PR 503 is open on the requested branch with base main; issue 157 is an unclosed
epic whose wider acceptance is not established by this fix.

## Research Cycle Log

Cycle 1 executed inline, in order:

1. Wider: enumerated both direct panel audit calls and the thread-message
   callbacks, plus JSON/SQLite lock and repository transaction contracts.
   Reflection: `chat.turn` is not the only unlocked append; `chat.answer` and
   the message methods' post-transaction events also need serialization within
   this panel's paths.
2. Deeper: traced JSON `last_hash` read/append/update, repository transactions
   and SQL lock depth/pending audit behavior. Reflection: short store-lock
   sections at message persistence and receipt append cover the panel without
   holding the lock across inference.
3. Contrarian: tested the design against nested-lock callers and SQL's separate
   repository transaction. Both store locks are reentrant; SQL repository writes
   already nest `dblock` under the store lock in existing code. A lock across the
   whole turn would unnecessarily block inference. A global `Store.audit` change
   would widen scope and alter unrelated callers, so it is rejected.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | `src/core/src/zava_forward/core/chat_panel.py:374-377` | Finally appends chat.turn without store.lock, including rejected turns |
| C2 | `src/core/src/zava_forward/core/chat_panel.py:403-415` | finish appends chat.answer without store.lock |
| C3 | `src/core/src/zava_forward/core/store.py:46-47,111-116` | JSON store uses RLock but audit itself reads and updates last_hash without locking |
| C4 | `src/core/src/zava_forward/core/sqlstore.py:103-145,856-875` | SQL store lock is reentrant; nested audit is queued and flushed on outer exit |
| C5 | `src/core/src/zava_forward/core/chatthreads.py:104-107,317-342` | JSON message transaction releases its lock before chat.message.added audit |
| C6 | `src/core/src/zava_forward/core/chat_panel.py:491-535` | Inference occurs between separate persistence and reauthorization stages |
| C7 | `src/core/tests/test_chat_panel.py:175-209,346-485` | Existing synthetic JSON panel and independent-connection SQLite roster fixtures can cover behavior |
| C8 | `src/core/src/zava_forward/core/chatthreads.py:174-192` | SQL repository transaction owns dblock, not a non-reentrant store lock |
| C9 | `src/core/src/zava_forward/core/ledger.py:25-51` | Real ledger verification checks predecessor and entry content, not just receipt counts |

`/tmp/mv` has Python 3.12.3, the current checkout's editable core/agents/API
distributions and pinned Ruff 0.17.1. No dependency installation is needed.

## Findings, Alternatives and Decision State

Q1-Q3 answered by C1-C9. Accepted: lock each panel persistence section and the
final receipt only; keep model dispatch outside all newly acquired locks.
Lock the question-message call as well as finish's message/answer event so
their indirect `chat.message.added` events cannot race panel receipts.

Regression design: start concurrent rejected turns together and wrap the real
ledger entry builder with a bounded barrier after the predecessor argument is
captured. Unlocked callers overlap and deterministically fork; serialized calls
break the bounded barrier and continue with the genuine ledger builder.
Verify the whole chain, exact receipt count/outcomes and a later locked append.
Also cover completed/refused turns, nested callers and a competing locked writer
during inference. Synthetic fixtures only, no live inference.

No material unresolved research questions. Cross-process JSON writers and other
modules' independent unlocked callers are outside this module-scoped fix.
No new knowledge-base synthesis is needed for this bounded code correction;
the component README is the durable behavioral contract.

## Planning Readiness

Ready. Research disposition: executed, complete. Focused scope is covered,
alternatives and counter-evidence resolved; another cycle would be redundant.
Self-check: all questions mapped to code evidence; no external evidence or
unsupported legal, activation or operational claims.
