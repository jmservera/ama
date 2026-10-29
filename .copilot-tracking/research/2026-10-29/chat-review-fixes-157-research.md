---
title: Chat review fixes 157 research
description: Focused evidence for three owner-selected Copilot findings
ms.date: 2026-10-29
---

## Research Brief

Task identity: `157-chat-review-fixes-2026-10-29`; slug `chat-review-fixes-157`.
Audience: implementation and independent review of PR 503, Refs #157.
Output mode: convergence. Posture: focused, selected for three named bugs.
Scope: callback accounting/completion, dispatched history budget, per-question role.
Non-goals: UI changes, cloud calls, push, other worktrees, rubric edits.
Evidence root: `.copilot-tracking/research/2026-10-29/`.

## Research Parameters and Direction Controls

The owner explicitly requests the full four-phase loop, focused regressions,
relevant tests and Ruff/mypy for core and agents, followed by a local commit.
No automatic-mode session is inferred. No clarification is needed.
Branch is the clean, open PR 503 branch, updated by the requested first command
`git pull --rebase` to `c5d8873a`; the rubric update came from the remote.

## Extension Registry and Participation

Repository instructions and source project READMEs govern package boundaries,
validation and local publication gates. RPI skills govern dated evidence.
No web skill applies to this backend/storage-only fix. Research is inline:
the failures form one tightly coupled code trace, not independent lanes.
Required independent critique and Review are reserved for later phases.
Initial internal areas: agents chat adapter, core panel/isolation/storage,
owning tests and persistence adapters. External research is unnecessary.

## Research Cycle Log

### Cycle 1: Wider

Initial reads identify a callback before dispatch and after provider return,
a raw-character history budget before delimiter neutralisation, and filtering
by the thread creation role. Prior knowledge is the owner's failure report,
treated as a claim to verify against source and tests.

Reflection: investigate existing failure envelopes, message metadata and
JSON/SQL persistence before choosing fixes; do not broaden into UI changes.

### Cycle 1: Deeper

Messages have no actor role; JSON copies full message dictionaries, but SQL
serializes the fixed MESSAGE_COLS tuple. Both SQLite and SQL Server need
additive migration of a dedicated `actor_role` field. Existing migrations
use empty-string defaults; retain unknown historical roles as empty and exclude
them rather than inventing provenance from the thread creation role.

Reflection: storing role in a panel-only dictionary would silently lose it
on SQL restart. The shared storage writer must derive it from its actor.

### Cycle 1: Contrarian

The worker always returns an envelope; disabled means no model invocation
and remains zero. Explicit completion revocation already preserves calls and
usage while withholding text; callback exceptions should follow that same
fail-closed pattern with distinct failure outcomes. The provider text must
not become a user-facing error. Legacy questions cannot safely inherit the
creation role because earlier role changes are unknowable. `block()` expands
delimiter tokens after truncation; measuring its final output, including
wrappers, avoids both expansion and double-neutralisation errors.

Reflection: no new research cycle is needed; these counterexamples are covered
by the planned regression matrix and existing adapters.

## Evidence Log

* C1: `src/agents/src/zava_forward/agents/chat.py:38` invokes admission outside
  an exception boundary before dispatch and after obtaining the envelope.
* C2: `src/core/src/zava_forward/core/chat_panel.py:447` preassigns one model
  call; an untyped admission error follows the generic exception branch.
* C3: `src/core/src/zava_forward/core/chat_panel.py:416` filters all messages
  using the fixed thread role; raw row lengths precede `block()` expansion.
* C4: `src/core/src/zava_forward/core/chatthreads.py:65` fixes SQL message
  columns; `:318` constructs messages from the actor and owns persistence.
* C5: `src/core/src/zava_forward/core/sqlstore.py:247` and
  `src/core/src/zava_forward/core/mssqlstore.py:250` implement additive
  idempotent chat migrations.
* C6: `src/core/src/zava_forward/core/chat_isolation.py:43` expands delimiters
  after slicing; `:55` re-reads current staff permissions.
* C7: `src/agents/tests/test_chat_model.py:45` establishes fail-closed
  completion revocation with retained consumption.
* C8: `src/core/tests/test_chatthreads.py:24` shares storage behavior across
  memory/SQLite and the opt-in SQL Server suite.
* C9: `src/README.md:76` documents the complete gate; owner prohibits other
  worktrees and az. This task will not publish; any gate requiring another
  checkout or az is blocked, not silently weakened.

## Alternatives and Decision State

Selected: adapt callback failures into ModelUnavailable with known calls/usage
and distinct admission/completion-check-failed outcomes; budget the exact
expanded thread block; persist server-derived actor_role per message.
Reject exposing completion-unverified text, measuring raw history, inferring
legacy actor roles, or storing metadata only in the JSON backend.
Preserve fail-closed answer handling: retaining provider accounting is not
authorization to show an unverified answer.

## Risks and Self-Check

Historical untagged questions are omitted from model history, but remain
visible in stored thread history. SQL Server execution needs a disposable
approved local server; SQLite parity does not establish SQL Server acceptance.
The existing `.venv` has no interpreter and global Python cannot import
the projects; restore project dependencies only after this observed failure.
All three questions are evidence-backed; no external or regulatory claims.

## Planning Readiness

Research disposition: executed, complete. Planning Readiness: Ready.
Parent continuation: owner explicitly requested Plan next in this full loop.
