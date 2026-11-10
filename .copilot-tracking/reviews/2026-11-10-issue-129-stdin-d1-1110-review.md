<!-- markdownlint-disable-file -->
# Review: closed-stdin refusal D1 (single self review, not independent)

* Executed once by the implementing agent after implement-done; boundary: working-tree delta over `5cec9663559bebfae3b3a2a7d38fd179b8c84b10`. Outcome: conformant for the scoped defect; no open material findings.
* Delta: 2 files, 21 insertions (guard 4 lines, one real closed-fd subprocess test 17 lines). The guard raises the existing handled `ValueError` before `isatty`/`buffer`; no broader catch, no fallback input.
* Evidence: red on original (new test fails, `AttributeError`), green after (21 tests OK, ruff check/format and mypy exit 0), actual CLI with descriptor 0 closed exits 1 with one refusal line and empty stdout. Adverse E501/format result preserved and fixed.
* Unchanged: engine, render, comparators, zero targets, bundles, O16, schema, bounds, labels, README, config, dependencies, KB index/log/protocol.
* Dispositions: original R1 resolved by this D1 (one debit, no reset, no automatic D2/D3). R2 stays routed. The test relies on `preexec_fn`, which is POSIX-only and unsuitable if threads are used; acceptable for this module's Linux CI and noted as a nonblocking limitation.
* Independence: this is NOT an independent pass. The original independent record is preserved in `2026-11-10-issue-129-original-independent-assessment-1110.md`; follow-up independent review of the exact delta remains outstanding.
* Remaining gates unchanged: real experiment, Atlas mapping confirmation, representative-data retention decisions, whole #129/#123 acceptance.
