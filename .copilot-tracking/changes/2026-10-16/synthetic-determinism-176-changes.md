---
title: Issue 176 implementation evidence
description: Offline fabric provenance and acceptance evidence
ms.date: 2026-10-16
---

## Scope

Full bounded plan for task 176, synthetic-determinism-176. One plan critique,
PC-001/002 accepted. No original stock generator reconstruction or live
refresh approval is claimed.

## P01: Provenance and regression implementation

P01-T01 complete: fabric CLI reads each input once, preserves newline=""
CSV semantics including BOM/quoted CRLF, and hashes exactly those consumed
bytes. Strict optional --as-of is null when omitted and labels metadata only.
Input hashes have logical register/cases keys with cases omitted when absent.
Algorithm version, row draws, linked case histories and default paths retained.

P01-T02 complete: two added methods in the existing test file plus receipt
assertions in the existing CLI repetition test. No golden assertions removed.
Tests cover exact raw digests, independent BOM/JSON whitespace mutations,
unchanged payloads on date-only changes, read-once consumption, unknown date,
absent cases, seed sensitivity, invalid-date no-write, nonempty refusal and
preservation of every existing byte. No new production/test files.

## P02: Validation and delivery

Local Python 3.12.3 isolated pip environment at /tmp/ama-176-venv.
Initial no-build-isolation install failed because setuptools was absent.
Normal pip editable install with declared dev extra succeeded; no manifest
changes or new dependencies.

P02-T01 complete:

* `cd src/core && PYTHONPATH=/home/azureuser/source/ama-wt/issue-176/src/core/tests /tmp/ama-176-venv/bin/python -m unittest -q test_stock_fabric test_synthetic_determinism test_sensor_stock test_generated_dataset`
  passed 45 tests, no skips, final run 10.718 seconds.
* Scoped Ruff check passed. Ruff format applied only to the changed test;
  final format verification passed for both changed Python files.
* Scoped mypy passed, no issues in two files. Initial run found a test stream
  variable reused with different inferred types; renamed the second stream,
  then reran the full targeted command.
* Local installed CLI smoke passed with 30 wholly fictional rows: two complete
  snapshots exactly equal, exact source digest, as-of label and refused
  nonempty refresh with all existing bytes unchanged. TemporaryDirectory
  cleaned generated outputs. No HTTP service is relevant to this CLI change.

P02-T02 complete: core README, existing synthetic-data README, reference
index and appended log describe replay inputs, policy and acceptance boundary.
No historical output/manifest, private data, source snapshot or issue ticks changed.
`git diff --check` and all three added Markdown path/anchor links passed.
An initial broad historical-document link scan hit an unchanged legacy anchor
in the append-only log; narrowed validation to added links, leaving unrelated
history intact.

## Amendments and divergences

No scope divergence. Critique adds precise compatibility oracles and
review disposition gates within the original file/test budget. Post-implementation
Review is inline/read-only, not delegated: the bounded diff fits the current
context and adds no independent review uncertainty. The plan critique was
independently delegated once.

## Acceptance and remaining work

| Criterion | Audit |
| --- | --- |
| AC1 all generator bytes, including original register | Unmet overall: original register generator/pinned OSM inputs absent. Available generator/sensor regressions pass on fictional supplied inputs. |
| AC2 manifests seed/version/revision | Partial overall: all available generator receipts pass, missing original generator/historical receipts remain unmodified. |
| AC3 policy cadence/approval/live protection | Met as documentation only, not owner adoption or live reset authority. Proposed trigger/approval/version rules explicit; directory refusal and SQL restart tested offline. |

Post-implementation Review complete once: execution Complete, outcome Residual
work; RV-001/002 are disclosed acceptance/owner follow-ups, no introduced defect.
Publication (P02-T03) pending.
This is review-ready source implementation, not full issue acceptance.
No source implementation blocker remains. Operational policy adoption and
original register reconstruction stay follow-up work, not invented approvals.
