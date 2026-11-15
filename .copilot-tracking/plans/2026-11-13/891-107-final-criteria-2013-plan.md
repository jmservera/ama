---
title: Plan for the final unticked criteria of #891 and #107
description: Tests-only increment proving #891 criterion 2 and #107 criterion 7
ms.date: 2026-11-13
---

## Overview

Research: [891-107-final-criteria-2013-research.md](../../research/2026-11-13/891-107-final-criteria-2013-research.md). Details: [891-107-final-criteria-2013-details.md](../../details/2026-11-13/891-107-final-criteria-2013-details.md).

## Phases

* [x] Phase 1: create the isolated venv `/tmp/venv-891c-2013` with pip only (done during research) and confirm baseline tests pass.
* [x] Phase 2: add `DemoActivationGuardrailPersistenceTests` to `src/api/tests/test_chat_panel.py` covering sub-clauses (a) to (e) with the demo switch active.
* [x] Phase 3: add one all-five-assistants attribution and content-free telemetry test to `src/api/tests/test_ai_consumption_api.py`.
* [x] Phase 4: fix any source gap the new tests expose (none expected; record any change).
* [x] Phase 5: run focused tests, ruff, mypy and content-standard; remove only `/tmp/venv-891c-2013`.
* [x] Phase 6: one Review with the per-criterion table, then a local commit with `Refs #891` and `Refs #107`.

## Constraints

* No push, no GitHub edits, no `uv`, no change to registry, workflow, dependency or schema files.
* Synthetic fixtures only (ADR 0005); fake transport; no claim of Legal, DPO, RAI or human approval.
