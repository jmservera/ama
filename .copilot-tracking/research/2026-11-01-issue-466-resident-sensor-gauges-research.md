# Research: resident sensor gauges and advisory assistant (issue 466), 2026-11-01

* Task: issue-466-resident-sensor-gauges; Research disposition: executed (current-main verification, no new investigation needed beyond it).
* Base: origin/main efebfc6d. Branch feat/resident-sensor-gauges.
* Issue state: open. Children #467-#469 and #471-#474, #480, #586, #603 delivered and merged; closure audit (2026-10-31) left only criterion 1 (owner confirmation) unmet.

## Evidence against each acceptance criterion

| Criterion | Current evidence | Status |
| --- | --- | --- |
| 1 Owner confirms scope and priority | Human approval; no owner confirmation exists in the issue. | Unmet (cannot be agent-granted) |
| 2 Own-home gauges and history, labelled synthetic | `src/api/src/zava_forward/api/resident_demo/web/demo.js` (`meter`, SVG chart with title/desc, caption, history table), `index.html` synthetic note; `src/core/tests/test_resident_sensors.py` | Met, re-verified |
| 3 Assistant answers status, documents, forms; advisory notice | `core/resident_assistant.py`, `resident_demo/aoai.py`, `web/assistant.js` notice text | Met, re-verified |
| 4 No other resident's data (tested) | `test_resident_assistant_api.py`, `test_resident_assistant_provider.py`, `test_resident_aoai.py` | Met, re-verified |
| 5 Accessibility checks with text alternatives | `meter` with `aria-valuetext`, `role=img` chart with title/desc, table fallback, `prefers-reduced-motion`; `test_resident_demo_check.py`, browser check | Met by engineering checks (previously accepted evidence; `test_resident_demo_check.py` covers sign-out mocks, SQL fixtures and import isolation, not gauge, chart or chat accessibility). Relevant browser checks are `checks.resident_sensors_browser_check` and `checks.resident_assistant_browser_check`; no fresh result for either was recorded in this run. Manual AT acceptance remains owner-run |
| 6 Model, cost cap, credential route decided and recorded | `docs/architecture/resident-assistant-prototype.md` (gpt-4.1-mini regional Standard, USD20 inference ceiling inside USD30, managed identity only; supersedes USD5) | Recorded |

## Findings

* Local verification run on main with pip venv: core `test_resident_sensors` and `test_resident_assistant` 15 tests OK; api resident suites (demo, assistant api/provider, api, demo check) 84 tests OK, 1 skip. ruff check and format clean for core and api. mypy core clean; api reports only optional `playwright` stub import errors (not installed locally, environmental).
* Inference tariff expiry (`EXPIRES` 2026-11-01T00:00Z) has now passed. With an enabled advisor the assistant takes the rules fallback with the stated reason "the AI exercise has ended" (covered by `test_resident_aoai.py` expiry cases). The architecture document records deployment AI as off; with no configured advisor, `app.py` labels typed-question answers "Summary by rules - AI is not enabled" instead. Both are code-path and test evidence, not a fresh live observation. No code defect found.
* No implementation gap exists within the acceptance criteria. Remaining work is human: owner scope confirmation, manual accessibility acceptance, live verification.

Planning Readiness: Ready (evidence/closure slice only; no new source).
