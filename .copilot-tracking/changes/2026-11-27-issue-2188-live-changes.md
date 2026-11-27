# Changes: issue 2188 live (2026-11-27)

Tier: focused (tools/ and docs only; stricter verification).

Files:

* tools/rpi-checks.py: `validate_retries` requires `sha256` to be a 64-hex string equal to the hashed log in `files`.
* tools/test_rpi_checks.py: three forged-retry cases added; failed before, pass after.
* docs/reference/research/issue-2188-live-retry-verify-2026-11-27.md, docs/reference/README.md, docs/reference/log.md.

Validation: `python3 -m unittest tools.test_rpi_checks` 134 OK; ruff format clean; ruff check 19 findings identical to baseline. Hosted CI for the exact head not observed (no push).

| Criterion | Status |
| --- | --- |
| Drop `--no-cache` | Proven (unit level) |
| Four concurrent image builds | Proven at scheduler level only |
| Shard API tests | Proven (unit level) |
| Retry failed class once, recorded | Proven at shard level, not class level |
| Receipt records retries | Proven (unit level) |
| Verify rejects tampered evidence | Proven (unit level); retry-record hole closed |
| Wall time before and after, same tree | Unproven (needs two full gates; `--all` forbidden) |
