---
title: Regulatory audit snapshot changes
description: Original implementation and validation evidence for 208-audit-snapshot
ms.date: 2026-10-29
---

## Scope and Opening State

Full plan P01; baseline 4998090e900082c34bac964d900e919a3f972430.
Research Ready; independent critique Complete / Pass, no findings.
P01-T01 starts with one deterministic real-file regression. P01-T02 and
P01-T03 follow only after original-code red evidence. No blockers or
follow-ups. Local-only commit; no push, az or rubric-score edits.

## P01-T01: Original-Code Regression

Added one regression in RegulatoryTests using a real file and wrapped reader.
Initial test setup exposed audit_path being a string; corrected with Path
before recording the genuine red result (not counted as reproduction).

From src/core:
`PYTHONPATH=tests ../../.venv/bin/python -m unittest test_regulatory_chat.RegulatoryTests.test_json_usage_snapshot_excludes_append_crossing_byte_limit -q`

Original implementation: FAILED, 1 test, 0.209s. JSONDecodeError:
Unterminated string starting at line 1 column 115 (char 114), from
usage_status -> json.loads. The injected append is a complete valid audit
record, but read(MAX_BYTES) cuts its detail string.

## P01-T02: Implementation and Documentation

Replaced read(MAX_BYTES) with read(size-start). Existing EOF capture, maximum
byte bound, partial leading-line removal, position limit, filtering and
explicit parse failures remain unchanged. Core README now documents the
captured-size/later-append boundary. No API or SQL change.

## P01-T03: Validation and Reconciliation

From src/core, existing installed editable package and Ruff 0.17.1:

| Command | Result |
| --- | --- |
| PYTHONPATH=tests ../../.venv/bin/python -m unittest test_regulatory_chat test_regulatory_usage test_regulatory_privacy -q | PASS, 29 tests in 22.391s |
| ../../.venv/bin/ruff check . | PASS, All checks passed |
| ../../.venv/bin/ruff format --check . | PASS, 110 files already formatted |
| git diff --check (repository root) | PASS |

The new test asserts captured size below MAX_BYTES, injected real file growth
above MAX_BYTES, exact read argument, full pre-append summary equality and
subsequent bounded_partial success. Existing JSON/SQL truncation, isolation,
restart and privacy tests remain intact. No dependency installation required.
P01-T01/T02/T03 complete and plan/details reconciled. One Review follows;
local commit remains pending. No human, hosted or complete local publication
gate is claimed; no publication is authorized.

## Amendments and Divergences

None.
