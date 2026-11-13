---
title: Issue 232 resident engagement screens accessibility plan
ms.date: 2026-11-13
---

## Objective

Fix D1 and D2 from the [research](../../research/2026-11-13/232-resident-a11y-2220-research.md), extend the checks, record the evidence. Do not tick the #232 criterion.

## Phases

* [x] Phase 1: row headers. Add an opt-in `rowHeader` mode to `screenTable` and a `screenRecordTable` wrapper in `role-screens.js`; use it for the seven resident tables only.
* [x] Phase 2: textual state meaning. Show "State and meaning" (`serviceStatus`) in the choice screen's service request table.
* [x] Phase 3: tests and checks. Unit table-structure tests for both screens; browser check gains row-header assertions, queue-state axe and 320 px Tab reach for stories 232 and 232s.
* [x] Phase 4: validation (Focused tier, pip venv `/tmp/venv-232-2220`, no uv): focused unit tests, accessibility baseline, content standard, Playwright stories 232 and 232s with pinned axe, specialist keyboard walk, ruff, mypy.
* [x] Phase 5: records. WCAG baseline section, knowledge base log, RPI artifacts, one independent review, Conventional Commits, no push.

## Constraints

Fluent 2 tokens, plain-language standard and the zero resident-contact rule are preserved; no style change; no change to other screens' tables; no infra, #215 or ranking files.
