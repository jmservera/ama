---
title: Issue 164 chat claim-support research
description: Research disposition for closing the open critical grounding gap in the chat evaluation
ms.date: 2026-11-01
---

## Disposition

Research executed (new investigation; the 2026-10-15 research is reused for scope).
Planning Readiness: Ready.

## Evidence

* Issue #164 criteria 1, 2 and 5 are already ticked from #307; criteria 3 and 4 plus the RAI and tokenomics
  conjunctions need owner decisions, held-out data, actual-model calls or human exercises that this
  session cannot supply (closure audit 2026-10-31 on the issue).
* `python3 -m zava_forward.agents.chat_eval` on main: 24 scenarios, 61 turns, 2 critical failures, both from
  `grounding-unsupported-claim-with-valid-citation` ("Funding is secured." cited to a stage fact). Enablement: fail.
* `parse_reply` in `src/core/src/zava_forward/core/chat_panel.py` keeps an answer when any citation id is permitted;
  it never checks that the claim text is supported by the cited value.
* Existing answers in `src/agents/evals/chat_golden.json` use paraphrase words, so a general word-overlap check
  would false-positive; a closed list of status assertions plus numbers does not.

## Scope decision

Smallest demo-ready slice: a deterministic, fail-closed claim-support check, closing the known critical gap.
No threshold approval, reviewer assignment, enablement, model call or held-out claim is made.

## Environment note

Tests need `pip install -e src/core -e src/agents` and `PYTHONPATH=../core/tests` for the agents suite.
