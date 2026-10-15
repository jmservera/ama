# Changes: issue 147

Added infra/governance.bicep, main.pilot.bicepparam, policy-exceptions.json, infra/tests/test_governance.py. Edited main.bicep (owner tag), infra/README.md, ADR 0001, docs/reference README and log.
Validation: az bicep build/lint clean; governance tests pass; mvp suite run.
