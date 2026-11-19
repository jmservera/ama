---
title: Issue 118 live changes (run 20261118T1512Z)
ms.date: 2026-11-18
---

Tier: FOCUSED, docs-only. No src, workflow or infra file changed. Read-only az only; no throwaway resource created.

Files: research note and evidence folder under docs/reference/research/issue-118-live-20261118T1512Z*, docs/reference/README.md, docs/reference/log.md, tracking artifacts, state file.

Validation: `pytest infra/tests/test_governance.py infra/tests/test_bicep_policy.py` 72 passed, 253 subtests. mypy, ruff and web checks not applicable (no source or web change). Link review of new note done.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Non-root, read-only root FS, dropped capabilities in Dockerfile | Proven earlier (ticked); USER 10001 re-confirmed, rest not re-audited | repo-ticked-criteria-checks.txt |
| Image scan and tests in CI | Proven (ticked); Trivy and unittest steps confirmed | repo-ticked-criteria-checks.txt |
| Application defined in Bicep | Proven (ticked); containerApps module confirmed | repo-ticked-criteria-checks.txt |
| Front Door Premium, WAF, Private Link before public edge | Proven (ticked); edge.bicep and guard confirmed | repo-ticked-criteria-checks.txt |
| Azure Policy and Defender plans decided | Proven for demo as recorded decision (audit-only, Defender deferred) | defender-decision.json, governance tests |
| Live Defender plan tiers | Unproven: Microsoft.Security/pricings/read denied | azure-readonly-probes.txt |
| Repo policy assignments active live | Unproven: none deployed at subscription or group scope | azure-readonly-probes.txt |
