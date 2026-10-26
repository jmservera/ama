<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-501 default fixture correction changes
description: Changes record for correction cycle 1
ms.date: 2026-10-26
---

Actual order: research, plan and details, critique (Revise, PC-601..605 applied), commit e3bba4c2, source edit, tests, one review (Non-conformant, RV-601/602), fixes, this record.

Source change: only `tools/test_check_demo_feedback.py`. Default `case_write()` (two earlier contacts written by `Store.log_call`, then the tested write, reload through a second `Store`, ledger reports from `verify_ledger`) and `ai_record()` (`Store.ai_priority` with scripted `_chat`) now return runtime-produced evidence from private JSON-text caches, deserialised per call. `RuntimeFixture.case_write` takes outcome, note, channel and prior contacts. The 120 character outcome is truncated by the runtime. `restart=False` only changes the declaration. The hand `contact` and `ledger_report` helpers are removed; `handcrafted_contact` remains only for the 40-contact cap boundary. `SkipTest` is replaced by an `AssertionError` when a helper resolves outside `src/core/tests`. Tests that hard-coded hand values were adjusted to read the runtime values (latency, request note) without weakening assertions. New tests: bundle sections are copies of the real runtime returns, fixtures are isolated copies, runtime truncation. Checker and `src` unchanged.

Command: `PYTHONDONTWRITEBYTECODE=1 /home/azureuser/rehearsal-350/venv/bin/python -m unittest tools.test_check_demo_feedback`: 88 tests OK (85 before). `__pycache__` removed.

Limits and residuals: JSON-store reload is not SQL durability; the offline test release is not release admission; HTTP routing is not exercised; 980 is the configured expected baseline, not live 443 open and 980 total; no gate, push or live action; fixes after review not re-verified; any re-review is a coordinator decision (cycle 2). A later gate uses `--lock-timeout 0`, base `c8d16059c0c0a22c4ffba88c6b65ac068f64accc`.
