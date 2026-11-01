---
title: Issue 164 chat claim-support plan
description: Single-phase plan with single critique for the lexical claim-support check
ms.date: 2026-11-01
---

## Plan

* [x] Phase 1: add `STATUS_CLAIM` and `unsupported_claims` to `chat_panel.py`; withhold an answer with unsupported
  status words or numbers (fail-closed, lexical).
* [x] Phase 2: remove the `known_gap` marker from the golden scenario; update `test_chat_eval.py` for the new
  pass and `insufficient` enablement outcome and add direct unit assertions.
* [x] Phase 3: update `chat-memory-dpia.md` and `docs/reference/log.md`.
* [x] Phase 4: ruff check, ruff format --check, mypy and tests for core and agents.

## Critique (executed once)

* Risk: false positives on legitimate paraphrase. Accepted: abstention is the safe outcome and routes to the
  case card; the golden answers all pass.
* Risk: bypass by synonyms ("financed"). Accepted and documented as lexical, not semantic; human and
  actual-model evidence remain required.
* Risk: overclaiming. Mitigated: criteria 3, 4 and RAI items stay unticked; PR uses `Refs`.
* Verdict: proceed unchanged.
