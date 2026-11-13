# Details: #216 regulatory offline verification (1143)

Commands (cwd = package tests parent; module names `tests.<module>` via unittest, PYTHONPATH per repo guide `../core/tests:../agents/tests` for api):

* core: test_rulecards test_rule_engine test_source_monitor test_source_freshness test_ai_statement_sources test_import_refusals test_regulatory_chat test_regulatory_privacy test_regulatory_usage
* agents: test_regulatory_answers test_regulatory_gates test_alert_triage test_candidate_comparison
* api: test_regulatory_chat_api test_regulatory_at_record_check test_regulatory_comprehension_score test_regulatory_ux_check test_rule_alerts

Each run: `env -u ZF_DATA -u ZF_TEST_MSSQL python -m unittest -v <modules>`; exit code captured with `echo $? > file`. Skips are reported verbatim. A module that needs a browser is reported as skipped or excluded, not worked around.
Acceptance boundary: issue text for #215 and #216 quoted literally; only offline unit evidence is claimed, not hosted CI or browser checks.

Critique amendments: add core test_chat_case_funding_sources; bare module names with PYTHONPATH; record versions, import origins, post-run git status of src/.
