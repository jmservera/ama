# Changes: #157 Criterion 4 proof after PR #1547 (157-c4-post1547-proof-1921)

Tracking-only change. No `src/` or `docs/` file edited. Base: `origin/main` e3e5f60e3, which contains #1547 (ecdd707c4). Tier: Focused.

Criterion 4: "Chat consumption is bounded and reported before activation: calls per request, context size per thread, memory use and per-role limits, with a fallback to the workflow-only path when a limit is reached (BRD AC-103)".

## Local test evidence (venv `/tmp/venv-157c4-1921`, pip install of core, agents, api)

| Command | Result |
| --- | --- |
| `cd src/core/tests && python -m unittest test_chat_panel` | 53 tests, OK |
| `cd src/api/tests && PYTHONPATH=../../core/tests:../../agents/tests python -m unittest test_chat_panel test_chat_widget_focus` | 71 tests, OK (1 skipped: the opt-in Chromium test, needs `ZF_BROWSER_TESTS=1`) |

Not run: the opt-in browser test, hosted CI, any live model or Azure call. Passing local tests do not establish release acceptance.

## Strict proof table

Rule: PROVEN needs source enforcement, reporting before activation (status endpoint or widget, not a post-request receipt) and a passing asserting test.

| Clause | Verdict | Evidence | Gap |
| --- | --- | --- | --- |
| Calls per request | NOT FULLY PROVEN | `role_limits().calls_per_request` is 1 or 0; `over_limit` skips the model when 0; status reports `calls_per_request: 1`; `test_status_reports_role_limits_and_bounds`, `test_receipt_reports_usage_and_thread_limit_falls_back` pass with a mocked model. | Production adapter `agents/chat.py` logs "dispatch count is unverified; assuming one call" and sets `calls=1` when no trusted dispatch record exists, so the physical provider-call count is assumed, not measured. `retries: 0` and `calls_per_turn: 1` in the status are literals. The widget note shows `calls_per_turn` and `retries`, not `calls_per_request`. |
| Context size per thread | NOT FULLY PROVEN | Per-prompt cap `MAX_INPUT_CHARS` 16000, history 4000, question 1000 and `MAX_THREAD_TURNS` 30; all reported in status and the widget (`test_panel_states_limits_and_per_turn_consumption`); over-cap questions return `fallback` (`LIMIT_REACHED`, `THREAD_LIMIT_REACHED`). | The thread cap is a turn count, not a cumulative character or token cap. The turn limit stops model calls but turns past the cap are still stored. No test of cumulative size. |
| Memory use | NOT FULLY PROVEN | `memory_used: False` in status and receipt; `chat_panel._ask` does not call `ChatIsolation.build_prompt`, so memory is not in the prompt; test asserts the flag. | The flag is a constant, not a measurement. Memory caps (`MEMORY_LIMIT` 50 items, `MEMORY_MAX` 1000 chars, applied before redaction) exist in `chat_privacy.py` and are not reported by the chat status or receipt. No bound or report of process or host memory. |
| Per-role limits | NOT FULLY PROVEN | `role_limits`, `all_role_limits`, `your_role_limits` in status; `test_status_reports_role_limits_and_bounds` and `test_role_with_no_model_calls_gets_zero_bound_and_no_access` cover one allowed role, reported values for both denied roles, and 403, zero calls and no model prompt for one denied role (`Contractor`) only. | All seven chat roles share identical constants; only chat versus no-chat differs, and limits are not configurable. Enforcement is tested for one allowed role and one denied role (`Application Administrator` 403 is untested), not each reported role. |
| Reported before activation | PROVEN for the limits that exist, qualified | `GET /api/chat/status` returns `limits`, `role_limits`, `your_role_limits` beside `activation` (`demo-only` or `disabled`); the widget renders `#chat-limits` after the status call and and `input.disabled = false` follows it in `chat.js` (widget test asserts the note text); tests assert both. | Only for the limits listed; the clauses above that are NOT FULLY PROVEN stay so. AC-103 also asks for agent depth, which the chat status and receipt do not report (single-agent by design, but no field states depth). |
| Fallback to workflow-only when a limit is reached | PROVEN for the two tested limits, qualified | Thread-turn limit: `kind="fallback"`, `workflow_only=True`, `model_calls=0`, no prompt sent; question and context overrun: `fallback` with `LIMIT_REACHED` (core and api tests); widget text names workflow-only help. | Evidence is the flag and message; no test shows the ordinary case workflow continuing end to end after fallback. Denied roles get 403, not a fallback. The widget renders only the generic limits note, not the per-role limits. |

## Outcome

Criterion 4 is NOT FULLY PROVEN. The reporting and fallback mechanics landed by #1547 are demonstrated; four clauses carry gaps that need either code or an owner-accepted scope decision.

## Follow-ups (not done here)

* Report and test a measured provider-dispatch count (or label it as assumed in the status and receipt) and show `calls_per_request` in the widget.
* Add a cumulative per-thread size cap or record the owner decision that the turn count suffices.
* Report memory state and caps in the chat status, or record that chat never reads memory; clarify whether process memory is in scope.
* Decide whether per-role limits must differ by role; test enforcement per role.
* Add an agent-depth field if AC-103 applies to chat, and an end-to-end workflow-continuation check after fallback.
* Issue #157 was not edited; criterion checkbox status is for the owner.
