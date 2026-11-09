---
title: Issue 530 chat local-unit validation details
ms.date: 2026-11-08
---

## Command (from `src/api`, venv `/tmp/rpi-530-venv-1108`, output under `/tmp/rpi-530-out-1108/`)

```text
env PYTHONPATH=../core/tests:.:src:tests:../core/src:../agents/src:../agents/tests \
  ZF_DATA=/tmp/rpi-530-synthetic-1108.json PYTHONDONTWRITEBYTECODE=1 \
  /tmp/rpi-530-venv-1108/bin/python -c "<origin asserts then unittest.main(argv=[..., '-v', ids])>"
```

Selected ids (single process):

* `test_chat_model`, `test_chat_provenance`, `test_chat_case_answers`, `test_chat_privacy.MemoryStoreChatPrivacy`, `test_chat_widget_focus`.
* `test_chat_panel` classes `PureTests`, `OutOfScopeTests`, `ActionClaimTests`, `LabelTests`, `UnstoredAskTests`, `GroundedUnstoredTests`, `StoredRulesFallbackTests`.
* `test_chat_panel.StoredQuestionTests` JSON-only methods: `test_concurrent_rejected_turns_preserve_shared_audit_chain`, `test_concurrent_completed_turns_serialize_all_panel_events`, `test_inference_does_not_hold_store_lock`, the three `test_expanding_redaction_*` methods, `test_history_budget_measures_expanded_dispatched_block`, `test_questions_follow_asking_role_through_a_b_a_switch`, `test_legacy_question_without_actor_role_is_not_dispatched`. The two SQL-restart methods and the nested-lock SqlStore method are excluded.

Critique dispositions applied: the wrapper asserts in the same process that every `zava_forward` module and each selected test module `__file__` lies under this worktree (and that `test_chat_panel` is the core file), and records executed counts and skips; the run fails on mismatch. `../core/tests` is first on the path because `test_chat_panel` exists in both core and api.

## Pass rules

* Exit 0, zero errors/failures, every skip recorded with its reason.
* Missing dependency: install only the missing item into the new venv via pip from local `src/*` distributions, then rerun and record both runs. Installation is offline-only from verified local artifacts; if build dependencies would need the network, stop and report.
* A real unit defect: keep the red log, record the smallest reproduction and a separate fix scope, change nothing.
* Never run SQL, browser, Docker, scanner or FULL, and never wait on the heavy-lock holder.

## Critique

Recorded in [.copilot-tracking/challenges/2026-11-08-issue-530-chat-local-unit-critique.md](../challenges/2026-11-08-issue-530-chat-local-unit-critique.md).
