---
title: Issue 114 per-year ledger verification test evidence
description: Retained raw unit-test run proving per-year audit and ledger digest verification before reliance
ms.date: 2026-11-18
---

Issue: #114, criterion C1 "Per-year audit and ledger digest verification proven by test before reliance".

## Run

* Command (cwd `src/core`): `PYTHONPATH=src:tests python3 -m unittest -v test_recovery test_sqlstore`
* Source: this worktree (`ledger.py` resolved under `src/core/src`), run 2026-11-18, exit 0, 40 tests OK.
* Raw output retained unedited apart from the header lines: [issue-114-per-year-ledger-test-run-2026-11-18.txt](issue-114-per-year-ledger-test-run-2026-11-18.txt).
* Redaction: the output holds no hostnames, accounts, paths or credentials; a grep for home paths and `@` found none.

## What each test proves

| Test | Proves |
| --- | --- |
| `test_recovery` per-year ledger tests (`test_each_year_verifies_alone_and_with_sealed_digests`) | Each year verifies alone and against its sealed digest. |
| `test_edit_in_one_year_is_reported_for_that_year_only_and_digest_catches_rewrite` | A tamper is reported for its year only; a self-consistent rewrite is caught only by the sealed digest. |
| `test_dropping_a_sealed_year_is_reported` | A dropped sealed year is reported as missing. |
| `test_sql_store_seals_past_years_once` | The SQL store seals past years once (idempotent) and detects later tampering. |
| `test_corrupt_or_malformed_digests_fail_closed_and_sealed_years_are_listed` | Corrupt digests fail closed. |
| `test_sqlstore` `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` | `require_verified_ledger_for_reliance` passes for 2024-2026, and blocks tampering and a dropped year. |
| `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head` | Head mismatch and missing head block reliance. |

## Per-criterion result

| Criterion | Result | Basis |
| --- | --- | --- |
| C1 Per-year audit and ledger digest verification proven by test before reliance | Proven by unit test (local SQL-store implementation, synthetic data) | Run above. |

## Limits

* The tests exercise the store implementation, not the deployed container. The 2026-11-18 closure review recorded that the deployed image lacks `verify_ledger_before_reliance`; rolling the image and running yearly sealing with retained output is owner work and was not done here (no production change is authorised).
* No live Azure action was taken; the criterion asks for a test, and none was needed.
* The ticked criteria C2 and C3 were not re-examined.
