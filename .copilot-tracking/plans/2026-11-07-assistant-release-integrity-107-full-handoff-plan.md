# Plan: FULL handoff for the #107 candidate

Research: [research](../research/2026-11-07-assistant-release-integrity-107-full-handoff-research.md). Details: [details](../details/2026-11-07-assistant-release-integrity-107-full-handoff-details.md). Critique: [critique](2026-11-07-assistant-release-integrity-107-full-handoff-critique.md).

## Decisions

* Exactly one normal (merge or single rebase, chosen then) integration of the eventual admitted fresh main; none now and none gratuitously.
* Preserve the test commit, all RPI records, skips and adverse outcomes. No new behaviour.
* No gate, SQL, browser, scanner or image service now; no push, PR, main move or criterion tick.

## Phases (not started)

* [ ] Phase 1: when the coordinator admits a fresh main, record its SHA and fetch; confirm the candidate is still source-identical.
* [ ] Phase 2: one integration, then light checks (ruff, mypy, 46-test selector from `src/api`, PYTHONDONTWRITEBYTECODE=1, pip-installed packages) and freeze.
* [ ] Phase 3: separately admitted FULL gate, then independent exact-head review and hosted gates.

## Prospective amendment 2026-11-07 (after coordinator feedback; original text above is unchanged)

---
title: Amendment to the 107 FULL handoff plan
description: Corrects a research claim and fixes the integration choice, light selectors and later gate conditions
ms.date: 2026-11-07
---

* Correction: the research statement that 1248 was not resolvable as an issue was false. Issue 1248 existed ("Investigate saved-call History browser readiness failure"), was CLOSED 2026-11-07T12:48:22Z through PR 1249, which is MERGED as 7551e50e904cd4d696ed74ecd6fb1e0cb6be1ba8. The failed lookup used the PR namespace only. The original research file is preserved unedited.
* The original critique is author-only and is not independent approval; it is not relabelled. No phase beyond what the dated records show is claimed as executed.
* Provenance: admitted main 7551e50e904cd4d696ed74ecd6fb1e0cb6be1ba8 (after a7f166c74608fe025d047a79448d5d2234622287, docs-only 1247); start head dec3bc5da343a3f964c7fd77e29eaa76f969f5e5, tree f19a7af68c5e14cefbb197b200cb08cdbd6b0297; merge base 0f420dc95; local ref `backup/issue-107-dec3bc5da-pre-merge` preserves the start head.
* Integration choice: exactly one normal merge of the pinned main; no rebase, force or history rewrite. Stop on drift or unreconcilable intent.
* Light selectors, from `src/api` in an own-worktree venv with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH=tests:../core/tests:../agents/tests`: `python -m unittest test_assistant_release -q` (module `test_assistant_release`, classes DependentPolicyRelease, Release, Legacy, TaskReleaseRelease record class as named in source), then `test_assistant_release test_assistants test_continuity`; plus `ruff check .`, `ruff format --check .`, `mypy`, and an import-origin check that `zava_forward.*` resolve under this worktree.
* Later FULL (not run now): read the command from current tools and README, `--all --base 7551e50e904cd4d696ed74ecd6fb1e0cb6be1ba8` (or the then-current main), new external directory, stdin from /dev/null, no cached-image or partial substitute, one nonqueued heavy holder after actual and logical resource admission, external verified receipt.
