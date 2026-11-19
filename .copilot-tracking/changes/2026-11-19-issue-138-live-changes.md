# Changes: issue 138, eighth demo run

Added docs/reference/research/issue-138-live-r8-2026-11-19.md, tracking artifacts and a log entry. No src change; tier FOCUSED.

| Criterion | Proven/unproven | Reason |
| --- | --- | --- |
| OIDC federated credentials per environment | Unproven | 0 federated credentials on 6 identities |
| what-if on infra PRs attached | Unproven | 0 runners, 0 runs |
| Approval per environment | Unproven | 0 protection rules, admin bypass |
| Versioned image pushed and referenced | Unproven | No run |
| Post-deployment checks fail the run | Unproven | Unit tests only, no in-run execution |
| No secret in logs or repository | Unproven | No logs to audit |

Validation: git diff review; relative link check of the r8 note (links to r7 note exist).
