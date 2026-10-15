# Research: per-user memory lifecycle (#161)

Disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue #161 acceptance criteria (six); parent #157; ADR 0004 accepted; owner decisions in the task brief.
* `mvp/zavaforward_mvp/chatthreads.py` already has `chat_memory` (id, owner, content, redactions, created_at, expires_at) and repo methods; `chat_privacy.py` (#163) has `add_memory`, redaction, `decision()` retention Unknown until `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS`.
* No administrator Entra app role exists in `auth.DEFAULT_ROLE_MAP`. The registry (`assistants.REGISTRY`) is hashed into proposal identity, so per-task state is kept in a control table, not the registry dict.
* Portability rule: no INSERT OR REPLACE, AUTOINCREMENT or PRAGMA in shared SQL; upsert is update-then-insert in one transaction.

## Decisions

* Extend the existing repository and `ChatPrivacy`; add columns to `chat_memory` and one table `chat_memory_control` (scope global, task, user).
* Retention stays Unknown per class until DPO references exist; no period invented.
* Open: memory administrator role (placeholder Programme Manager); UI and endpoint wiring (chat not built).
