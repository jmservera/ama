---
title: Issue 107 end-to-end execute probe changes
description: Probe result for Assistants.execute and tariff-enabled ChatPanel at 3b05143179f8 (Refs #107, #159, #432)
ms.date: 2026-11-13
---

## Summary

Write surface: tracking files only; no `src/` or `docs/` edit. Venv `/tmp/venv-107e2e-1105`
(`--system-site-packages`, `pip install --no-deps -e src/core -e src/agents -e src/api`) was removed afterwards.
`__file__` of `assistants`, `agents.chat` and `api.server` verified inside this worktree.

Run: cwd `src/api/tests`, `PYTHONPATH=../../core/tests:../../agents/tests` (test fixture dirs only, not `mvp`).
Producer exit code: 0 (saved with `$?` directly, no pipeline). Output ends `PROBE-OK`.

| Artifact | sha256 |
| --- | --- |
| [probe script](107-e2e-execute-1105-probe.py) | f77ef919b0ae1ff0a4034f8e3cb015e07cda99f2c5d0dde738c67319201acc46 |
| [probe output](107-e2e-execute-1105-probe-output.txt) | 3f775fcf3a02001de3380009e1f02c84f0379282192cac3eed6ce999056485d7 |

## Result

* All 5 registered assistants: invoke, `Assistants.execute`, human verify, human accept on SQLite `SqlStore`.
  Executed set = accepted set = `REGISTRY`; no skips.
* Per assistant, reserved, completed, output and review ledger rows joined one-to-one by meter id, root
  (`reference(task id)`), attempt, configuration and prompt hash; tokens 120 (cached 10) equal the envelope.
* `report()`: `accepted_proposals` 5; each capability calls 1, proposals 1, accepted 1, 120 tokens,
  `tokens_per_accepted_proposal` "120"; no unjoined outputs or reviews.
* ChatPanel with synthetic tariff: `meter_root` populated, one model call, output row ineligible and joined to
  `chat:{thread}:{seq}`, accepted count unchanged (5), report calls 6, ledger rows 30, audit rows 5.
* Leak scan: six unique sentinels. Excluded content (notes, document summaries) never reached any provider
  request; the captured address and chat text did, as designed. Sentinels appear only in domain tables
  (`cases`, `chat_message`, task body and event `output`). Zero hits in ledger rows (`ai-consumption`
  partition), audit, attempts, allowance, dispatch gate, schedule, releases, every task envelope, every non-output
  event field, both reports and the chat receipt.

## Boundaries

* The fake provider is a 127.0.0.1 loopback HTTP stub (existing fixture); no external network, Docker, browser or live model.
* Synthetic price and authority; cost fields stay `Unknown`; this is not billing or quality evidence.
* The scan covers one run with this sentinel set; it is not a proof of absence for other content paths.
* No `src/` change, so no change to hosted CI coverage; Focused tier, no complete local gate claimed.
