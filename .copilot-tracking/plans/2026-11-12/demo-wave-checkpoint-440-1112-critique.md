---
title: Plan critique, demo wave checkpoint 440 (2026-11-12)
description: Original single independent pre-implementation critique with dispositions
ms.date: 2026-11-12
---

Executed once, by a read-only `rubber-duck` subagent, on the final candidate of the [plan](./demo-wave-checkpoint-440-1112-plan.md), [details](../../details/2026-11-12/demo-wave-checkpoint-440-1112-details.md) and [research](../../research/2026-11-12/demo-wave-checkpoint-440-1112-research.md). Verdict: not ready as written (two blocking findings); all findings are compatible with confirmed decisions and applied directly. Critique is not repeated for this task.

## Findings (original text, summarised without change of meaning) and dispositions

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | Blocking | Bare module names will not resolve without the tests directory on the import path; use `unittest discover -s tests -p ...` | Applied: details use `discover -s <abs tests dir> -p <file>` |
| C2 | Blocking | T5 imports `zava_forward.agents`; the owned venv installed only core and API so agents would resolve to the primary checkout | Applied: `src/agents` is also installed (`--no-deps -e`) and the agents origin is added to the preflight |
| C3 | Significant | SHA-256 of files cannot be compared with Git SHA-1 blob ids | Applied: compare `git hash-object <file>` with `git rev-parse HEAD:<path>`; also check imported source dependencies, not only tests |
| C4 | Significant | `test_ai_consumption_api.py:53` sets `tempfile.tempdir` to the cwd, so transient files could enter the worktree | Applied: run from an owned external cwd with absolute test paths and check `git status --porcelain --ignored` before and after |
| C5 | Significant | `test_finance_exposure_api.py` does not test non-finite observations | Applied: T3 is described as consumer regression only; non-finite behaviour is attributed to T2 alone |
| C6 | Minor | "No services" overstated: T3 and T5 start loopback HTTP servers and T6 uses Node | Applied: the record distinguishes ephemeral loopback fixtures from external services and preflights Node |

The critic did not independently verify hosted checks and ran no tests; the record therefore states hosted state from the author's own read and claims no Source CI success.
