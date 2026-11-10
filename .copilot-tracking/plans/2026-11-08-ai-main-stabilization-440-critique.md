<!-- markdownlint-disable-file -->
# Critique: AI and employee chat current-main stabilization checkpoint (#440)

* Date: 2026-11-08. Executed once, prospectively, by a read-only rubber-duck agent before implementation. Verdict: Revise. Not repeated.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Major | Installed `chat_eval` cannot find its unbundled golden file and `test_chat_model.py` imports `dataset` from core tests | Applied: details set `ZF_CHAT_GOLDEN` and add `core/tests` to the agents `PYTHONPATH` |
| PC-002 | Major | Research said every turn rereads the staff register; `ChatIsolation.current_user` verifies the supplied Entra principal and only non-Entra principals reread it | Applied: research corrected |
| PC-003 | Major | Research implied requester-independent review; `Assistants.review` enforces role, scope, source verification and same-reviewer verify-then-accept, with extra independence only for quality-evidence | Applied: research corrected |
| PC-004 | Minor | F1 grep scope: the `src`-only archive lacks `tools`; result is "no static callers" | Applied: run against the checkout, qualify as static |
| PC-005 | Minor | "Single provider boundary" ignores inventoried resident-demo call sites | Applied: scoped to assistants and employee chat |
| PC-006 | Minor | #161 recorded as closed and later called open | Applied: closed status kept |

Spot-check by the critic found F1 (no callers, `Ai._chat` without `chat_admission`) and F2 (live prompt has no memory) supported. No finding conflicted with a user decision; none required a user question.
