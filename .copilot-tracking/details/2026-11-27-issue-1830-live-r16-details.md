---
title: Issue 1830 live r16 details (2026-11-27)
ms.date: 2026-11-27
---

Phase 2: add helper `preflight_conflicts(args, parser)` returning option names whose value differs from `parser.get_default`; `main()` raises `GateError("--preflight cannot be combined with ...")` before `preflight()`. `--lock-timeout` and `--heavy-lock-fd` are also gate-only. Test: patch argv with `--preflight core:test_a --extra-test core:test_b`, expect exit 1 and `preflight` not called; a clean `--preflight` still calls it.
