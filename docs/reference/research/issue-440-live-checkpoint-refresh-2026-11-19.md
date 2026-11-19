---
title: Issue 440 checkpoint triage refresh against head 1dddac2e0 (2026-11-19)
description: Which draft findings of the 2026-11-18 triage still hold at current main, and why criteria 7 and 8 cannot be ticked from the demo
ms.date: 2026-11-19
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `1dddac2e0bf1bf61413ff1333057c546e3cba47e`. Refs #440. No source change; no GitHub issue was created and no Azure resource was touched. This note refreshes [the 2026-11-18 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md) and preserves it unchanged.

## Fresh observations (local observed, 2026-11-19)

| Draft | Command at head | Result | Status change |
| --- | --- | --- | --- |
| D2 legacy-reference guard | `python3 tools/check-legacy-references.py` | exit non-zero, one violation: `docs/reference/README.md:1359: retired path without archive tag v0.21.0` | Narrowed from 11 violations to 1; the allowlist for the three `tools/test_*` files landed in #2105 (`e91b6fa81`). The residual is an index row that cites `mvp/` and `prototype/` without naming `v0.21.0`. |
| D3 unreachable `ChatIsolation.turn` | `grep -rn "\.turn(" src --include=*.py` excluding tests | no caller | Unchanged, still static only. |
| D4 AI golden path | `grep` of `ai_eval.py` and tests | `GOLDEN` honours `ZF_AI_GOLDEN`; `src/agents/tests/test_ai_eval.py:27` asserts the named configuration error | Largely delivered (`e3494f476`); the non-editable-install criterion is unverified. Withdraw as a new issue unless that test is wanted. |
| D1 `/api/time/status` 500 | not re-run | Entra sign-in flow not repeated; the 2026-11-18 observation stands | Unchanged; root cause still unproven. |
| Open issues matching D1 to D4 titles | `gh issue list --state open` search | none | No draft has been filed. |

## Criterion verdicts

| Criterion | Verdict | Reason |
| --- | --- | --- |
| 7 Triage into issues, gate epics, owner approval | Unproven | Drafts and gating exist in the 2026-11-18 note, but the criterion needs filed issues, and the owner must approve deferrals, requirement changes and pivots. Filing is coordinator or owner work and D1 touches SQL (FULL tier). |
| 8 Research, plan, changes and independent review artifacts in the PR; Major HVE Builder review | Unproven | Needs a PR (publication is the coordinator's) and an independent reviewer who is not this worker. The coordinator change itself is not part of this task. |

## Limits

* The D2 residual is a one-line documentation fix that belongs in its own RPI loop and branch, not in this checkpoint (#440 authorises no unrelated change).
* No criterion is ticked and the issue stays open.
