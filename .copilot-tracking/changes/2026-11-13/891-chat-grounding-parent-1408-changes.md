# 891 parent changes

* Merged 1599446 (core), 4643283 (api web), e7daa01 (agents) with --no-ff; no conflicts.
* Integration fixes found by cross-package tests: core chat_panel skips settlement when no meter is configured (was AttributeError); agents golden/eval expectations and one API test updated for the new decision-rules fallback (previously abstain/withheld).
* Added API end-to-end tests: ZF-4 unblock/review/safety-visit questions return cited answers with answer_source and source_kind; post-dispatch failure settles meter_root as ineligible (meter patched with a mock; real tariff ledger covered by agents/core tests, not exercised end to end).
* Divergence: failing-first RED not observed for the new tests, since children already implement the behaviour; the two stale-test failures were observed red on the merge before fixing.
* Validation: core 145 OK (before the one-line guard); agents 62 OK; api panel 58 OK (1 skipped), widget focus/content standard/isolation OK; ruff check/format and mypy clean.
