---
title: "Issue 2190: log text glued before the next test header"
description: A thread log fragment without a newline can end right before the next verbose unittest header; the gate parsers missed that header and the exact-name parser failed a passing run.
ms.date: 2026-11-23
---

Scope: issue #2190, flake 1 (gate log interleaving) in `tools/rpi-checks.py`. Synthetic DEMO, desktop only. No Azure resource was read or changed; the issue concerns local gate tooling. Earlier notes: [2026-11-21](./issue-2190-live-20261121-2026-11-21.md), [r2](./issue-2190-live-20261123T071426Z-note.md), [browser test](./issue-2190-live-20261123T080144Z-browser-test-note.md).

## Finding

The earlier fix handled a log fragment glued to the result ("status=503ok"). The mirror case is a fragment glued to the next header ("status=503test_b (Mod.Cls.test_b) ... ok"). `_test_header_indexes` anchors on the line start, so that header was missed. On the prior head `_required_tests_passed` returned False for a fully passing run (a flaky gate failure), and `_classes_executed` stopped counting the test.

## Change

`merge_docstring_headers`, which all three parsers already call, now puts a newline before a `test_*` header that follows text on the same line. The split applies only to lines that do not start with a header and requires the full `name (dotted.Class.name) ... ` shape. No failure pattern, exact-name match or one-hit rule changed, so no check is relaxed.

## Evidence

* `tools/test_rpi_checks.py::test_log_fragment_glued_before_next_header_keeps_each_result_separate` passes; with `rpi-checks.py` stashed it fails (1 failure).
* `python3 -m unittest test_rpi_checks` from `tools/`: 132 tests OK.
* `ruff format --isolated --line-length 100 --check`: clean. `ruff check` with isolated defaults reports only older findings on lines this change does not touch.
* Not run: the complete local gate (coordinator-owned) and hosted CI for the exact head.

## Per-criterion verdict

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Each flake reproduced or explained | Proven for flake 1 (new variant reproduced by test); flakes 2 and 3 per earlier notes | Test fails on prior parser |
| Fixed with a regression test | Proven for flake 1 variant; flake 2 browser test and flake 3 timeout test per earlier notes | This note |
| No check relaxed | Proven | Failing and skipped glued results are rejected by the new test |
| Hosted CI and complete local gate on this head | Unproven | Coordinator-owned; not run |
