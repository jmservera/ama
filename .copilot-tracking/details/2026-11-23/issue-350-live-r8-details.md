# Issue 350 r8 details (2026-11-23)

Test `test_easy_auth_never_exempts_api_paths` in `infra/tests/test_bicep_policy.py` reads `modules/containerapps.bicep` and `modules/edge-existing-auth.bicep`, extracts any `excludedPaths: [...]` list and asserts no entry equals or starts with `/api`. Tier FOCUSED; no `src/` change.
