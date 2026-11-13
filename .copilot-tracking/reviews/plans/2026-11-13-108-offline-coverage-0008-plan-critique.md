<!-- markdownlint-disable-file -->
# Plan critique: 108-offline-coverage-0008

* Execution: one genuine independent critique by a separate rubber-duck agent (read-only), before implementation; not repeated.
* Verdict: Revise. No user decision required; all findings are compatible with the task brief and applied directly.

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | Blocking | Dispatch-time `source == ai` is observed before `finish()` can quarantine or financially hold the result; priority late quarantine keeps `source=ai`. | Applied. Coverage needs both a dispatch observation (scripted `_chat` reached) and a harness-recorded final outcome with `source=ai`, `mode=ai`, status not Quarantined or Hold, no financial attribution; unverified output alone never proves a positive check. |
| C2 | Blocking | An unobserved retained task is only "not evaluated" and could still pass. | Applied. Every retained id must be `exercised offline` or the run fails; tests cover missing and fallback-only. |
| C3 | Blocking | Funding and document checks mutate documents, summary and funding, conflicting with the unchanged-state baseline. | Applied. Isolated stores for funding and document checks with their own baselines: only the intended fields change; ranking and unrelated case state stay unchanged. |
| C4 | Non-blocking | Briefing assertion is not discriminating. | Applied. Distinctive cited briefing answer; assert final AI source, text, citations and comparison record; fallback negative control. |
| C5 | Non-blocking | Document citation is injected by `run_document`, so a resolver mutation need not fail the check. | Applied. Test forces resolution failure and expects the Unverified outcome; non-text type stays template without a model call and is not coverage. |
| C6 | Non-blocking | `_scripted` returns early without outputs, later replaces `_chat`; existing `Ai.run` mocks omit `off`; mypy ignores and ruff-format excludes these files. | Applied. `observe` is installed independent of `_scripted`, wraps the current `_chat` per call with `try/finally`, passes arguments through unchanged; the 10/11 scenario and 14-run denominators stay; the mypy and ruff-format limits are reported accurately. |

Confirmed sound by the critique: assistants dispatch through the core planner, so a spy on `Ai.run` and `Ai.look_at` cannot establish assistant coverage; the five assistants, chat and the concern pack stay fixed as not evaluated by this harness.
