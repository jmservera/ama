# Details: issue 2206 round 2

Phase 1: check_health catches TimeoutError, retries with timeout 90, appends "(cold start, retried)". http_get gains a timeout argument. Test: test_health_cold_start_timeout_retries_once.
Phase 2: research note round 2 section and docs/reference/log.md entry.
