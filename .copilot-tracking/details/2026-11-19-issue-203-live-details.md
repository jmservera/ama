# Details: issue 203 live proof

* Search: `git grep -nIE` on tracked files excluding `.copilot-tracking`; classification uses the checker's own record, guard and dated-package lists so the literal result and the gate agree.
* Live: `az containerapp show/revision list` for `ca-cutover-test-demo-api` and `ca-resident-demo` (read-only), unauthenticated `curl` of `/healthz` and `/health`, `gh run list` for `src-ci.yml`, `src-deploy.yml` and `main`.
* No Azure resource is created or changed; no credentials are read; no Playwright sign-in is repeated (see the 2026-11-18 deployed-parity note).
* Deliverables: `docs/reference/research/issue-203-live-20261119-2026-11-19.md` plus evidence folder, index row and appended log entry.
