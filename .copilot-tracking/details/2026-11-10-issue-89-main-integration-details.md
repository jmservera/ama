---
title: Issue 89 parent main adoption details
ms.date: 2026-11-10
---

## Pins

* Start `a8593a7a8670aab27329a81fedee605b4913e7e9`; published parent `a05b7e6b29145e620ca70f69c6f3f5c00be493c2`; main `a6002219581b983132465e9dd1680f78e6aca542` (tree `c04d01256c3a...`, equal to e951 tree `9dad912b361e...` except `.github/rubric/scores/latest.json`). If `origin/main` moves, inspect and report; do not chase.

## Step 1 details

* Before any HEAD move run the witness `implement-start` (changes artifact exists as a started record). Then `git merge --ff-only a05`. Expect HEAD = a05 exactly.

## Step 2 details

* `git merge --no-ff -m "<conventional message>" a600`. Message: `chore(integration): adopt current main into parent 89 staging` with body naming both parents, `Refs #89`, and the Copilot trailer. Author and committer are `8036360+jmservera@users.noreply.github.com` (local config verified against `gh api user`). The merge tree must equal the prediction from `git merge-tree --write-tree a05 a600`.
* If the merge reports any conflict: `git merge --abort`, capture the raw output, STOP/HOLD. No manual resolution.

## Step 3 proof commands

* `git diff --name-only a05 HEAD` equals main's delta from the merge base (minus parent-only paths).
* For `docs/reference/log.md`: every line of each parent appears in the merge, in parent order.
* `git diff a600 HEAD --name-only` equals the parent-side delta; Stage A six source files `git diff a05 HEAD -- <file>` empty except `src/core/README.md`.

## Step 4 checks

* Core: `python -m unittest` for `test_aftercare_intake`, `test_aftercare`, `test_resident_decisions`, `test_resident_showcase`. API (with Core tests on the path via test modules as existing): `test_aftercare_screen`, `test_accessibility_baseline`, `test_static_assets`, `test_auth`, `test_role_endpoint_inventory`, `test_role_screens_conformance`, `test_simulator_admin`, `test_live_control`.
* `ruff check`, `ruff format --check`, `mypy` for `src/core` and `src/api` from each project directory with its configuration. A heavy shared lock is not needed for these non-browser checks; if one is later needed, take `flock -n /tmp/ama-rpi-heavy.lock` and on busy record the holder and hold that check only.
* A failing result is classified against the base: compare with the same test at a05 or a600 before any claim; no repair.

## Step 5

* Review artifact, final state, handoff in Root. One tracking commit after the merge commit.
