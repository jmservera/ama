---
title: Issue 79 plan, continuation r15
ms.date: 2026-11-06
---

Task `issue-79-r15-d654-review-corrections`. Planning readiness: ready. Critique: self-critique below; single pass.

## Executive summary

Tests first (real RED), then the minimal helper and store corrections for the d654 independent review: durable first-writer-wins publication, validated existing records, unsigned-policy audit visibility, and structured status on listing errors.

## User decisions and requirements

* Edit only `ranking_publication.py`, `store.py` publish and status paths, their tests, and necessary documentation and r15 RPI records.
* No push, no FULL gate, no heavy checks, no lock. Focused unit tests only with external caches.
* Preserve the adverse review and all older records. Target stays parent 73; #1231 will need a rebase afterwards.

## Phases

* Phase 1: Research, plan and details committed before any test or source edit.
* Phase 2: add regression tests, observe RED.
* Phase 3: minimal source corrections, observe GREEN.
* Phase 4: focused checks (Ruff, format, mypy with pinned tools in the r13 venv if present), documentation, Changes, Review, state, commit.

## Acceptance criteria

* HIGH 1: temp file fsynced, unique temp name, `os.link` publication, directory fsync, no overwrite, no leftover temp, only one of several concurrent writers returns `written` True and retained bytes match its reported date.
* HIGH 2: corrupt, truncated or different-content file at the final name raises `PublicationError`, stays unchanged, and the API does not audit `already_published`.
* MEDIUM: API response and audit detail say `policy_signed` true or false; `run_key` and same-window semantics documented; status listing `OSError` returns a problem entry, not a 500.
* Tests: corrupt, truncated, race (deterministic interleaving using real `os.link` plus a multi-process run), unsigned publish recorded, status `OSError`.

## Self-critique

* Risk: validating the existing file against the caller's snapshot could reject a legitimately older record with the same name. The name embeds policy, as_of and hash prefix, so equal name with different snapshot content is corruption. Accepted.
* Risk: registry check at publish. Not added; `verify` keeps that role.
* Out of scope: runner unchanged, as_of loose validation, non-directory archive path, #1231 manual API.

## Follow-up items

* Rebase #1231 child onto the corrected head.
* Fresh FULL and independent re-review of the corrected head; named policy signoff and Legal retention remain unmet.
