# Research: issue 147 governance as code

* Sources: issue 147 and parent 136, ADR 0001 open items, infra/README.md (SecurityControl exception), main.bicep (enableLocks, tags).
* Built-in policy IDs verified against Azure/azure-policy (SQL public access audit, storage public access, Key Vault recoverable, resource-group require tag).
* Planning Readiness: Ready. Unverifiable items (Defender price, exception expiry) recorded as open.

## Review-fix loop (2026-10-15)
Research: findings 1-3 from PR review; placeholders in main.pilot.bicepparam, EX-001 expiry null, audit-only/Defender wording needed. Disposition: reused existing evidence.
