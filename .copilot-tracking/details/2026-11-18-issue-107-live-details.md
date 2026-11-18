# Details: issue #107 live proof

Phase 1 commands run from src/api with PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests; MSSQL via ZF_TEST_MSSQL=1 and a 127.0.0.1 container, generated password, shredded afterwards.
Phase 2 reads credentials at runtime only. Invoke probes create retained denial rows in the demo store (accepted, intended behaviour).
Phase 3 files: docs/reference/research/issue-107-live-assistants-evidence-2026-11-18.md, docs/reference/README.md, docs/reference/log.md.
