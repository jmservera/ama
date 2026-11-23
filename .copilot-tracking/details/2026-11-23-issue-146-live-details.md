# Details (2026-11-23)

Classes: job_failure (`alert-job-*-failed`), poison_queue (`*-agent-tasks-poison`), ledger_digest (`*-ledger-digest-mismatch`, `*-ledger-verify-missing`), iot_ingestion (`alert-*-iot-*`). Status per class: enabled if any matching rule enabled, disabled if matches exist but none enabled, missing otherwise. Overall: `partial` or `none`; never `proven`. CLI: `--metric-alerts FILE --scheduled-queries FILE [--json]`; exit 0 always unless input invalid (2).
