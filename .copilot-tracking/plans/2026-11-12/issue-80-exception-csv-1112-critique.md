<!-- markdownlint-disable-file -->
# Critique: #80 browser-built exception-summary CSV (issue-80-exception-csv-1112)

Executed once on the final candidate plan, details and research by an independent rubber-duck subagent (read-only), 2026-11-12. Not repeated. Verdict: Revise; every finding was compatible with confirmed decisions and applied directly. No significant or divergent issue needs a user decision.

| ID | Finding (summary) | Disposition |
| --- | --- | --- |
| CR-001 | The fail-closed rule ignored `data.state`; a `roles_not_named` response carrying items could offer a file. | Applied: D1 requires `state === "ok"`; test added. |
| CR-002 | O3 ledger and data evidence was omitted. | Applied: Store-level O3 test in `test_exception_register.py`; browser check proves zero requests on activation. |
| CR-003 | A direct `addEventListener` breaks the existing mocks in the host harness and `test_data_operator_ai_state.py`. | Applied: both mocks updated; both suites run. |
| CR-004 | Using every own `exceptionKinds` key would silently admit future kinds. | Applied: frozen six-key list in the exporter; extension test. |
| CR-005 | Anchor cleanup was not unconditional on failure. | Applied: removal in `finally`, URL revoked on failure; tests for failure before and after click. |
| CR-006 | Evidence gaps: both-role scope, Space activation, focus visibility, note and status association. | Applied: added to the tests and the browser check. |

The critique is author-side advice, not independent exact-head review.
