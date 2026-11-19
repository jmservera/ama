# Issue #164 Cycle 1 domain-answer review fixes: changes

Branch `feat/demo-164-chat-next-steps-1445`, stacked on PR #1641. Task slug `164-dom-bf2239f94-fixes`. Research disposition: reused (independent review `independent-direct-164-dom-bf2239f94.md` findings, supplied in the task). Critique: one pass, findings compatible, applied directly. Mode: automatic.

## Findings and fixes

| # | Finding | Fix | Evidence |
| --- | --- | --- | --- |
| 1 | `OUT_OF_SCOPE` "approve" kind refused "Who gives PAS 2035 sign-off?" before rules ran | `out_of_scope` skips the "approve" kind when the question starts who/whose/what/when/where/which/status and has no action request (`for me`, `on my behalf`, `please`, `I want/need you`); other kinds and imperative asks still refuse | `src/core/src/zava_forward/core/chat_panel.py`; test `test_informational_signoff_and_sensor_questions_survive_skill_lenses` (ChatPanel.ask, all skills) |
| 2 | `skill_sources` dropped `pas2035.*`, `sensor.*`, `hazards.*` for non-general skills | Added the three prefixes to the common allowed keys | same test; lens canary test unchanged |
| 3a | `_sensor` cited `{case}/documents` without "Survey" | Cite only when "Survey" is in documents | `chat_case_answers.py`; `test_sensor_answer_cites_documents_only_when_survey_is_listed` |
| 3b | `_claim` no-grants branch lacked domain footer | Append `_domain_close` | `test_claim_without_grants_keeps_the_domain_footer` |

## Validation

* `ruff check`, `ruff format --check` (src/core, src/api): pass. `mypy src` in src/core: pass.
* Targeted tests (`test_chat_panel`, `test_chat_case_answers`): pass; the new case-answer tests fail without the fix.
* Full unit suites in src/core and src/api: see the commit message and final report.
* Validation ran with `PYTHONPATH` pointing at this worktree because the installed editable package resolves to another checkout.

## Review

Self-review once after implementation: the exemption is limited to the "approve" kind and informational leads, so action requests ("Approve it.", "Please sign-off for me") still refuse. Residual risk: an informational lead followed by an action ("What should I do, approve it") is answered by rules rather than refused; rules answers never act. Independent exact-head review and human approval remain required; not performed here. Tier: focused (non-gate chat answer code); not pushed.
