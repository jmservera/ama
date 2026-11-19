---
title: Issue 1847 live changes
ms.date: 2026-11-19
---
# Changes
No source or test change. Artifacts only. Refs #1847 (no closing keyword; criterion 6 unproven).

Head tested: 910adb0a1. Tier: FOCUSED.

| # | Criterion | Demo status | Evidence |
| --- | --- | --- | --- |
| 1 | Layouts documented, rejection behaviour | Proven | src/core/README.md "Nomination test layouts (#1847)"; prior note docs/reference/research/nomination-bootstrap-isolation-proof-1847-2026-11-18.md |
| 2 | Both orders, fresh processes | Proven | Source layout re-run today: bulk-first 55 OK, nomination-first 55 OK. Editable and noneditable probes in the 2026-11-18 note (not re-run today) |
| 3 | Origins and identities | Proven | 2026-11-18 probe outputs; the same bootstrap file is unchanged on this head |
| 4 | Regression fails on original, passes with fix | Proven | Adverse output retained 2026-11-18; today test_nomination_bootstrap + both modules: 58 OK |
| 5 | No family purge, foreign checks kept | Proven | test_nomination_route.py reads sys.modules only; unchanged |
| 6 | Full gate and external receipt | Unproven | Forbidden for the demo by the brief and not triggered (no src change) |

Validation: ruff format --isolated --line-length 100 --check on both test files: pass. mypy in src/core: 22 errors in 3 files, e.g. missing opentelemetry stub in tests/test_telemetry.py, unrelated to the nomination files and not caused by this change (no code changed).
Unmet DEMO criteria: none.
