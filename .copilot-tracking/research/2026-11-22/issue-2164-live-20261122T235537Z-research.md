# Research: #2164 (2026-11-22 r3)

Research disposition: reused (docs/reference/research/issue-2164-roster-scope-recheck-2026-11-22.md) and re-verified. Planning Readiness: Ready.

## Evidence

* The issue has two asks and no checklist: decide whether roster-bound Entra staff inherit the bound row scope, and add tests for view_only with an eligible role and for scope bypass.
* `git merge-base --is-ancestor 6a03928ccb HEAD` succeeds; `Assistants.authorize` (src/core assistants.py near line 1515) re-reads the bound roster row and refuses view_only.
* src/api `test_assistants.ReviewTests` scope-bypass and view-only tests: 2 OK. src/core `test_assistants_identity`: 5 OK.
* Live API app revision is now `ca-cutover-test-demo-api--0000054`, digest `sha256:3f2be664...faf945` (the earlier note recorded revision 0000053). `az acr repository show-tags` is refused by registry network rules, so the digest cannot be mapped to a commit.
* No credentials were used; no Azure change.

## Gaps

* Deployed behaviour is unproven; a live proof needs a roster-bound Entra test user and the issue does not require it.
