# Research: #216 regulatory assistant offline verification (1143)

Base 3b05143179f83235c5b4e80e70aad99bdc44d83f. Disposition: executed. Planning Readiness: Ready.

Required docs read at start: case study original and addendum, reference README and memory (sizes checked; targeted use only).

## Candidate test modules (no browser, no network)

* Core: test_rulecards, test_rule_engine, test_source_monitor, test_source_freshness, test_ai_statement_sources, test_import_refusals, test_regulatory_chat, test_regulatory_privacy, test_regulatory_usage
* Agents: test_regulatory_answers, test_regulatory_gates, test_alert_triage, test_candidate_comparison
* API: test_regulatory_chat_api, test_regulatory_at_record_check, test_regulatory_comprehension_score, test_regulatory_ux_check, test_rule_alerts

Risk: some modules may need optional prerequisites (browser, MSSQL); these are reported as skips or excluded, never worked around.
