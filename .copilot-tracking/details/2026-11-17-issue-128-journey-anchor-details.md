---
title: Issue 128 plan details
ms.date: 2026-11-17
---

## Phase 1

Add `_anchor(code, name)`: lowercase `f"{code}: {name}"`, drop characters other than letters, digits, spaces and hyphens, replace spaces with hyphens. This matches the GitHub slug for headings `### J1: Choose each proposed measure`. Use it in `draft()` for `design_ref`. No change to hashing semantics beyond the new ref value.

## Phase 2

Test reads `jr.DESIGN_DOC`, slugs all headings the same way, and asserts every draft `design_ref` path equals `DESIGN_DOC` and its anchor is in the set. It fails on main (0 of 7).

## Phase 3

Commands: `python3 -m unittest tests.test_journey_register` from `src/core`; `ruff format --isolated --line-length 100 --check`; `mypy` for src/core.
