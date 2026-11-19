# Changes: issue 349 live prerequisite evidence

No source code changed (`src/`, `infra/`, `tools/` untouched). Tier FOCUSED. No Azure resource created, changed or deleted; no throwaway resources.

## Files

* docs/reference/research/issue-349-tenant-prerequisites-live-2026-11-18.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/evidence/2026-11-18/issue-349-live2/ (script, redacted outputs, 2 screenshots (the signed-out welcome capture was deleted as mislabelled); a picker screenshot showing a display name was deleted)
* .copilot-tracking/{research,plans,details,critique,changes,reviews}/2026-11-18-issue-349-live-r2-*.md and the r2 state file (issue-349-live-r2-state.json)

## Per-criterion status (demo; none ticked on the issue)

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions single-tenant app, roles, credential | Unproven in part (GUID registration, vault credential and role claim exist; provenance, audience, role definitions unreadable) | auth-show-redacted.json, graph-*.txt, prereq-run1.json |
| 2 | Credential reaches private vault in-VNet; nothing published or weakened | Proven for the demo (KV reference via user-assigned identity; public Disabled, Deny, approved private endpoint) | secret-source.txt, kv-show.json, private-endpoints.txt |
| 3 | Audience and callback use real registration; prior callbacks preserved | Unproven in part (IDs, issuer, audiences consistent; callback works; redirect list unreadable) | config-consistency.txt, prereq-run1.json |
| 4 | Private roster reconciled; no fictional identity | Unproven; not applicable to the demo (`bound` false) | prereq-run1.json |
| 5 | Real user callback, role-scoped /api/me, workbench, logout, switching, denials | Proven with the test account only; real user, second role and unknown-staff unproven | prereq-run1.json, employee-app-entry.png, entra-wrong-password-denied.png |
| 6 | Anonymous and forged-header denial in browser mode; positive request | Proven with qualification (302 to Entra, XHR 403, bad bearer 401, /api/cases 200 with session, forged headers ignored) | prereq-run1.json |

## Validation

* Credential-value scan of all text evidence for the three credential files: no match.
* Screenshots reviewed: addresses masked.
* No unit tests, mypy or ruff apply (no code change). `rpi-checks.py --all` not run.
