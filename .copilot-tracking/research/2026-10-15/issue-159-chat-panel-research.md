---
title: "Research: conversational assistant panel (#159)"
ms.date: 2026-10-15
---

## Task and disposition

* Issue #159, parent #157. Research disposition: executed. Planning Readiness: Ready.
* Location decision: ADR 0006 (Accepted) moves all code to `src/`; `mvp/` receives no new code.

## Evidence

* Issue #159 acceptance criteria (six) and the 2026-10-15 src pivot comment: criteria unchanged, location changes.
* `src/core/.../chatthreads.py` (#160): owner-keyed threads, messages with `evidence` list, `chat_add_message`.
* `src/core/.../chat_privacy.py` (#163): storage refused until DPIA, lawful basis and notice references exist; redaction.
* `src/core/.../chat_isolation.py` (#162): `current_user` re-reads role per turn, `case_context` applies the user's projection, `turn` returns text only, `_withheld` blocks tool or record-change syntax.
* `src/core/.../assistants.py` and `src/agents/.../dispatch.py`: proposal-only assistants with source check and independent review; `AgentWorker.provider_call` returns a never-raising envelope.
* `src/api/.../server.py`: `/api/chat/*` routes (role category `chat`, contractors refused); `web/assistants.js` shows the case proposal panel.
* Gap: `ChatIsolation.turn` returns uncited free text with no abstention, no fallback signal and no UI; no web chat code exists.

## Design constraints (ADR 0006, instructions)

* Dependency rule: core imports no workload; agents has no core[sql] or blob; api imports agents only until #144.
* Portable SQL: no new tables are needed, so none is added.
* AI enabled in prototypes; human approval gates, resident consent and no private data stay in force.

## Options

| Option | Result |
| --- | --- |
| Extend `ChatIsolation.turn` | Rejected: changes the response contract that `test_chat_isolation` pins. |
| New `core/chat_panel.py` plus `agents/chat.py` adapter and new endpoints | Chosen: additive, keeps the merged contract. |

## Acceptance criteria that cannot be closed here

* Screen-reader tested: needs a manual run with a named reader and browser; not producible by an agent.
* Live model behaviour: no Azure endpoint locally; stub only.
* Real chat data: DPIA, lawful basis and notice references (OD-45 to OD-49) are unset; storage stays refused in a default deployment.
