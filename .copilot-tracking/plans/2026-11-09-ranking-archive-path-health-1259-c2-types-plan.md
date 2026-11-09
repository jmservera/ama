---
title: Issue 1259 C2 typing correction plan
description: Prospective plan to remove the two child-owned mypy diagnostics in the added Blob test
ms.date: 2026-11-09
---

## Objective and boundary

Fix only the two confirmed child-owned strict-mypy diagnostics in the added test in `src/core/tests/test_ranking_archive_blob.py` (research record). Not in scope: the 84 inherited core and 9 inherited API diagnostics, parent lint errors, the fixture, any source, transport or API behaviour, the emulator fixture. No push, PR, board or cloud action. Parent publication stays held. Refs #1259 only.

## Ordering

Research, this plan, details and the single critique are committed before the edit. Then implement, validation, changes record, one Review, state, freeze.

## Cycles

C1 spent earlier; this is explicitly authorized C2 for these two diagnostics; three remain after it. No reset. If validation proves the fix needs a contract change, stop and scope new emulator evidence.

## Tier

Owner demo-targeted tier. Commands: `mypy` (core and API, CI profile, pins `mypy==2.4.0`, `ruff==0.17.1`), `ruff check .`, `ruff format --check .`, targeted unittest modules for Blob, publication runner and API wiring, with exits and counts retained outside the repo with hashes. No full matrix, SQL service or scanner.

## Success

Sorted diagnostic diff child-after versus parent shows no added diagnostic; core count 84, API 9; targeted tests keep their prior counts; no `Any`, cast or ignore added.
