# Plan: surface retries in gate timing report

- [ ] 1 `analyse` adds `retries` and `retried_groups` (sorted unique groups).
- [ ] 2 `compare` arm adds `retries` (sum over receipts); markdown gains a Retries column.
- [ ] 3 Tests in tools/test_rpi_gate_timing.py; update the existing markdown assertions.
- [ ] 4 Research note under docs/reference/research/, index row, log entry.
- [ ] 5 Run tests, ruff, mypy; changes and review records; commit locally.
