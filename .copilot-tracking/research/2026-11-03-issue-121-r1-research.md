---
title: Issue 121 r1 research
date: 2026-11-03
---

Task: issue 121 (data protection, retention and rights controls), branch feat/issue-121-r1. Disposition: executed. Planning Readiness: Ready.

## Prior delivery checked (merged PRs referencing the issue)

* #281, #649, #745, #728 and the 2026-11-03 retention purge (all Refs #163): chat and memory DPIA record, provider position, DPO decision pack, demo storage with owner-recorded references, retention purge. Scope is chat only.
* #353 and #506 (Refs #217): `regulatory_privacy` readiness, retention report and `minimise_query`. Scope is the regulatory assistant only.
* #673 (Refs #145): SQL pilot parameters; states #121 retention remains undecided.
* No merged PR delivers a whole-system data class register, a cross-class model-dispatch gate (DH-006) or a rights-request clock.

## Evidence

* PRD DH-001 (purpose, lawful basis, owner, retention trigger per data class; Article 9 named), DH-002, DH-006 (no resident personal data to a model until transfer position approved), DH-007 (audit retained in full; DPO confirms Article 17(3)), PR-001.
* `chat_privacy.DATA_MAP` and `MODEL_PROVIDER_POSITION` give chat-only classes; retention Unknown, provider terms not DPO accepted.
* No persisted rights log or one-month clock exists in `src/`.

## Acceptance criteria status before this slice

* All four issue criteria unmet. All RAI processing criteria unmet except the checked constructed-fixtures one.

## Smallest coherent slice (slice 1 of a stacked set)

Pure core module: whole-system register with missing approvals, reference-gated model dispatch, declared task field limits, rights due-date clock. No SQL, no deployment, no security control change; focused tier applies.

## Later slices (not delivered)

* Persisted rights-request log and answer evidence (SQL; complete gate).
* Wire `model_dispatch` into assistant call sites.
* DPO and Legal decisions: lawful basis, Article 9 condition, Article 17(3) position, retention period, transfer position (human gates; blocked on named owners).
