<!-- markdownlint-disable-file -->
# Critique: post-fix-wave checkpoint plan for #440 (2026-11-12)

* Execution: one independent read-only critique by a fresh `rubber-duck` worker after the final candidate plan, details and research were written. Not repeated for this task. The worker could not create the file (read-only), so the coordinator persisted its returned findings here verbatim in substance, with dispositions.
* Verdict: Revise. Four findings (2 blocking, 2 non-blocking). All are compatible with confirmed user direction, so all are applied directly; no user decision was required.

| Id | Severity | Finding (worker) | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | The form-export test fixture uses an in-process SQLite `SqlStore` (`src/core/tests/test_form_review.py:31`); the plan said "no SQL" | Applied. The plan's exclusion is SQL Server, disposable databases and any shared service (`ZF_TEST_MSSQL`). In-process SQLite is a local synthetic test store, not a heavy shared resource, and the record must say so and list it as executed local coverage |
| PC-002 | Blocking | `server.py:1204` calls `draft_export`, not `export_freshness`; the API test cannot show HTTP freshness enforcement | Applied. The record separates core freshness evidence (#98) from held-download HTTP regression evidence, and states that no HTTP freshness surface exists or is demonstrated |
| PC-003 | Non-blocking | Preflight requires a clean tree but the plan inputs are untracked | Applied. Baseline is: tracked tree clean and untracked paths limited to this task's `post-fix-wave-440-1112` artifacts |
| PC-004 | Non-blocking | The infra class is skipped with exit 0 when Azure CLI is absent (`test_bicep_policy.py:234`) | Applied. Run with `REQUIRE_AZ_BICEP=1`, run the specific marker test first and require 1 ran and passed; `az` is present at `/usr/bin/az` (Bicep 0.48.1, local compile only); a skip is unverified, never a pass |

Verified by the worker against git: the PR identities, the three source changes, the infra test and the `server.py` call site matched the research. No wrong requirement ID or path was found.
