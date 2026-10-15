# Plan: issue 147

1. Subscription-scope infra/governance.bicep (policy assignments in audit mode, Defender plans Free until owner approves).
2. main.pilot.bicepparam with locks; owner tag in allTags.
3. policy-exceptions.json, tests, README section, ADR 0001 open item, KB index and log.
Critique (single pass): keep audit-only to avoid blocking the exercise; no invented prices. Applied.

## Review-fix plan
1. Rename pilot file to main.pilot.example.bicepparam, label non-deployable, add rejecting test.
2. EX-001 expiry 2026-12-31 with test (valid date, <=180 days).
3. Document DoNotEnforce and Defender Free in README and ADR 0001.
Critique (single pass): compatible, applied.
