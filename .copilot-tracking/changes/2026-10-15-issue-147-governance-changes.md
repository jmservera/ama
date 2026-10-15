# Changes: issue 147

Added infra/governance.bicep, main.pilot.bicepparam, policy-exceptions.json, infra/tests/test_governance.py. Edited main.bicep (owner tag), infra/README.md, ADR 0001, docs/reference README and log.
Validation: az bicep build/lint clean; governance tests pass; mvp suite run.

## Review-fix changes
Renamed pilot param file to main.pilot.example.bicepparam; set EX-001 expiry; README, ADR 0001, log updated; tests added. Merged origin/main (log.md kept both sides).
