<!-- markdownlint-disable-file -->
# Research: Issue #104 end-to-end controlled-domain non-mutation proof

* Task: `104-controlled-nomutate-0230` (Refs #104), branch `test/demo-104-controlled-nomutate-0230`, base `origin/main` `ac70acafa`.
* Research disposition: `executed`. Planning Readiness: `Ready`.
* Criterion under test: "AI never approves, executes, ranks or mutates controlled records" (unticked in #104).

## Existing evidence

* `src/api/tests/test_ai_boundary.py`: scripted hostile model over the JSON `Store`; retained tasks only (briefing, message, summary, priority, funding draft). No HTTP, no chat, no assistants, no hazard, consent or ranking archive.
* `src/agents/tests/test_epic104_bounded_ai_invariants.py`: registry and AST guards (chat and worker adapters import no store module), offline dispatch. No HTTP state snapshot.
* `src/api/tests/test_chat_isolation.py`: injection set on the JSON `Store` compares `store.cases` only.
* `src/api/tests/test_assistants.py`: asserts `domain()` unchanged per capability, but does not combine chat, scan, review and hazard, consent, sign-off, finance and ranking archive in one snapshot.

## Interaction map (verified in code)

* Reactive chat: there is no `/api/cases/{id}/chat` route. Chat is `POST /api/chat/threads` (case-scoped thread), `POST /api/chat/threads/{id}/messages` and `POST /api/chat/unstored-ask` in `server.py` `_chat`. `chat_panel._ask` writes only chat thread messages and `chat.*` audit entries. The reply is labelled "AI suggestion, not approved" and unsupported status claims are withheld.
* Assistants: `POST /api/assistants/{capability}/invoke` queues a proposal (202); `Assistants.execute` claims, dispatches and completes it (`assistant_*` tables); `GET /api/assistants/proposals[/{id}]` reads; `POST .../review` takes `verify`, `accept`, `edit-accept` or `reject` by a named human. `Assistants.scan` is the proactive enqueue. None of these routes writes `cases`.
* Agent tools: `src/agents` workers import no store module; `src/core` assistants write only proposal, release and event tables.
* Controlled records and their human routes: case `stage`/`closed`/`owner` (handoff, decision routes), hazard hold (`hazard-raise`, `hazard-receive`, `hazard-accept`, `hazard-release`), resident consent (`/decision`), PAS 2035 sign-offs (`technical`, `signoff_give`), finance and grant approvals (`finance`, `grant`), ranking (`_ranking`, `/api/ranking/publish` writing the archive folder).

## Findings and decisions

* The snapshot must read raw SQL rows (case body, rowversion, stage, owner, closed, rank key, funding status, procurement meta, recommendations, staff) plus the ranking archive bytes, not only API projections; `meta.seq` and audit legitimately move.
* Audit growth is allowed only for `chat.*` and assistant actions; asserted separately.
* A positive control (an authorised human hazard action does change the snapshot) proves the snapshot is sensitive.
* Do not edit `src/api/pyproject.toml` (PR #1604) or `docs/reference/log.md`; the new module is auto-discovered.
* Gap recorded, not fixed: #104 owner sign-off and hosted CI remain required; this is local focused evidence.
