---
title: Issue 530 chat local-unit validation plan
ms.date: 2026-11-08
---

* Research: [.copilot-tracking/research/2026-11-08-issue-530-chat-local-unit-research.md](../research/2026-11-08-issue-530-chat-local-unit-research.md)
* Details: [.copilot-tracking/details/2026-11-08-issue-530-chat-local-unit-details.md](../details/2026-11-08-issue-530-chat-local-unit-details.md)
* Tier: FOCUSED, tracking-only. No source, test, runner, workflow or dependency change.

## Phases

* [x] Phase 1: record source identity and import-origin proof in the isolated venv.
* [x] Phase 2: run one bounded `python -m unittest` over the selected ids, one process, record exit and skips.
* [x] Phase 3: confirm source blobs unchanged and tree clean; write changes and review records.
* [ ] Phase 4 (blocked: heavy lock, gate not run): commit tracking records, freeze, inspect `tools/rpi-checks.py` first; run `--changed --lock-timeout 0` only if it neither takes the canonical lock nor schedules Docker, Trivy, SQL or browser work. Otherwise report focused-gate admission as pending.

## Critique

Final-candidate critique: see the critique record linked from the details file. One critique and one Review only.
