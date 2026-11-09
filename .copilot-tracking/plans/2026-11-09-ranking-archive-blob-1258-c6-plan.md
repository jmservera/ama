# Issue 1258 C6 plan (2026-11-09)

Refs #1258. Research: `.copilot-tracking/research/2026-11-09-ranking-archive-blob-1258-c6-research.md`. Details: `.copilot-tracking/details/2026-11-09-ranking-archive-blob-1258-c6-details.md`. Critique: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-c6-critique.md`. C6 of C6 to C10 (finite owner extension, comment 6747925505).

## Objective

Make the maintained CI profile green for this parent workstream: core mypy 84 to 0, api mypy 9 to 0, api ruff check 10 to 0 and api ruff format clean, without relaxing any config, then compose with current main and re-verify. Tier: owner-selected demo-targeted; no blanket full gate.

## Phases

* [ ] Phase 1: commit research, plan, details and the independent critique before the main merge or any source edit (ordering gate).
* [ ] Phase 2: ordinary `git merge --no-ff` of freshly fetched `origin/main`; no rebase, amend or force; stop on an ambiguous conflict.
* [ ] Phase 3: type the Blob fixture, the Blob archive test and `snap`; format the wiring test and fix its import order.
* [ ] Phase 4: re-run the CI-profile checks from each project root in the owned venvs, plus targeted regressions (Blob adapter, publication, runner, API wiring, failure paths), once with the core venv without optional SDKs and once with the api venv with the declared SDKs.
* [ ] Phase 5: write changes, one original review, state, local handoff; commit; stop (no push, PR, issue or board write).

## Success criteria

* Core and api `ruff check .`, `ruff format --check .` and `mypy` exit 0 from each project root with pinned tools.
* No new `type: ignore`, `noqa`, `Any` hiding, override or config change; assertions unchanged or stronger.
* Affected tests pass with zero unexplained skips; failures stop the task.
* Both main's and this branch's intents preserved in `server.py` and `store.py`.

## Out of scope

Azure deployment, identity, WORM or retention, production access, unrelated JSON migration, filesystem or mount hardening, archive SQL redesign, child 1259 or 136 source, push, PR, board.

## Cycle accounting

C6 is spent when source is edited (Phase 3). C7 to C10 remain unused unless a documented defect needs another bounded correction.
