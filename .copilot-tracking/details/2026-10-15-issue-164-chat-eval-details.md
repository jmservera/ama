---
title: Issue 164 chat evaluation phase details
description: File-level detail for each phase
ms.date: 2026-10-15
---

## Phase 1

* `src/core/.../chat_panel.py`: `OUT_OF_SCOPE`, `out_of_scope()`, `REFUSED`, `_carry()`; refusal happens before any model call and is stored as an assistant message.
* Tests: `src/core/tests/test_chat_panel.py`, `src/api/tests/test_chat_panel.py`.

## Phase 2

* `src/agents/.../chat_eval.py` (`--json`, `--record PATH`); `src/agents/evals/chat_golden.json` (now 24 scenarios, 61 turns, one open critical grounding gap); `registry.json` entry; `tests/test_chat_eval.py`.

## Phase 3

* `web/chat.js`, `src/agents/README.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## PR 307 review-fix execution

P05-T01/P05-T02 cover `src/core` chat panel and tests, `src/agents` evaluator,
golden file and tests. Use NFKC, format-character removal, common Greek/Cyrillic
confusable folding and whitespace collapse before lexical refusal matching.
Drop assistant turns instead of trusting citation identifiers as proof of current
values; user history stays untrusted. Withhold lexical model approval/consent
action assertions, without claiming semantic grounding or model refusal.
Open critical known gaps must block report success, CLI and enablement.

P05-T03 covers all five existing src unittest suites, project ruff check/format
and mypy, ADR 0006 dependency tests, artifact reconciliation and an ordinary push
to the same branch. Dependencies may be restored with pip only if missing.
Documentation changes are limited to agents README, reference index/log and
existing task artifacts. No enablement, live inference, deployment or real data.

P05-T01/P05-T02 complete: the stale assistant-history and lexical prose-action
scenarios have no `known_gap` marker and pass the actual checks. Grounding is
critical; the unsupported cited claim remains listed, with two failed assertions.
The CLI and enablement block rather than treating the gap as a pass.

Validation: core 261, agents 70, api 459 (92 skipped), orchestrator 17, importer
39, all successful; ruff check/format and mypy successful in every project.
The existing environment lacked the orchestrator/importer editable installs;
initial imports failed, then pip restored those packages and both suites passed.
P05-T03 complete: source fix `2f6f73a` committed and pushed normally to
`feat/src-chat-eval-164`. Final delivery-record reconciliation follows on the
same branch. No force push, main push, merge or enablement.
