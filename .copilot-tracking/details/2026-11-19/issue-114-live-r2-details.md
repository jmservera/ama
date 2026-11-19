# Issue 114 live r2 details (2026-11-19)

* Phase 1: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_recovery test_sqlstore test_ledger_digest_blob -q`; `az containerapp show -g ama -n ca-cutover-test-demo-api` read-only for image and revision.
* Phase 2: new note `docs/reference/research/issue-114-live-r2-2026-11-19.md`; index entry in `docs/reference/README.md`; append to `docs/reference/log.md`.
* Phase 3: changes and review records, one Conventional Commit with trailers. No push.
