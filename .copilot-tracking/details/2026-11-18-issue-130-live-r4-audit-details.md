# Details: issue 130 live audit, run 4

* Phase 1: `src/core` unittest of test_nomination_route, test_nomination_bootstrap, test_hazard_referral; `src/api` unittest of test_nomination_api_routes, test_representative_expiry_api, test_nomination_screen.
* Phase 2: `az containerapp show` (read only); probe1.py (five JSON writes) and probe2.py (form-encoded POST, Resident tab) under evidence/2026-11-18/issue-130-live-r4. Credentials read at runtime; literal scan afterwards.
* Phase 3: note `docs/reference/research/issue-130-live-r4-nomination-route-audit-2026-11-18.md`, README index entry, log entry.
* Phase 4: changes and review files, `git diff --check`, link check, commit.
