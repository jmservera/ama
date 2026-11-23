# Changes, issue 117, 2026-11-23

Status: complete. Tier: Focused (tests and documentation only; no `src` non-test code changed).

## Files

* `src/core/tests/test_document_rescan.py`: new `DefenderTagReader` (3 tests).
* `docs/reference/research/issue-117-live-r8-2026-11-23.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

* `src/core`: `tests.test_document_rescan` 43 tests OK, 20 skipped (SQL Server). `ruff check`, `ruff format --isolated --line-length 100 --check` and bare `mypy` report no issue in the file (mypy has 3 pre-existing errors elsewhere).
* Not run: hosted CI, full local gate (not required for the Focused tier).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Uploads are scanned before availability | Proven: order of operations, local scanner, fail-closed Defender tag reader and factory. Unproven: Defender end to end, live EICAR refusal | Needs `ZF_SCANNER=defender` on `ca-cutover-test-demo-api` or a storage network-rule change; an estate change outside this brief. Defender for Storage is enabled per the 2026-11-19 live note |
| Retention listing, owner approval, legal hold | Proven (already ticked) | [third pass](../../docs/reference/research/issue-117-live-r3-closure-2026-11-18.md) |
