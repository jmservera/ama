---
title: Issue 79 plan, continuation r17
ms.date: 2026-11-07
---

Task `issue-79-r17-align-post-891`. Planning readiness: ready. Critique: single self-critique below.

## Executive summary

Rebase the 18 local topic commits onto the final `origin/main` after the 891 post-merge scorer finishes, keeping both ranking publication work and the merged 891 changes. Local only. Focused checks only; the one FULL stack gate is the coordinator's next step.

## User decisions and requirements

* Align the existing parent onto final current main; PR 1239 keeps its `main` base. Do not touch the child worktree or push.
* Use a conflict-free local rebase if possible; otherwise preserve both intents and record the resolution first. No skipped or guessed commits.
* Preserve backup ref `preserve/issue-79-pre-r17-align` and all older records. No policy, threshold, approval or source changes beyond conflict alignment.
* Bounded wait for run 42361331168; if it does not finish, return a base blocker and run no gate.

## Phases

* Phase 1: research, plan and details committed (this commit) while the scorer runs.
* Phase 2: wait, bounded, for the scorer; fetch main and record the final base identity.
* Phase 3: `git rebase` onto the final base; resolve `docs/reference/log.md` append collisions by keeping main's text then the topic's entries; prove blob parity for every non-log topic path.
* Phase 4: focused checks (publication, runner, API wiring tests, Ruff, format, mypy with pinned tools), Changes, state, author Review, commit.

## Acceptance criteria

* HEAD descends from the final main; the old head is an ancestor of nothing new but preserved by ref; 18 commits are replayed with the same subjects.
* Every topic-changed path other than the log has the same blob as the preserved head; the log keeps all main entries plus the four topic entries.
* Focused checks pass or failures are recorded as found.
* Ignored-inclusive clean worktree.

## Self-critique

* Risk: a rebase rewrites commit hashes that earlier evidence cites. Mitigation: the preserve ref keeps them and Changes maps old to new where feasible.
* Risk: the scorer adds a commit after the freeze. Mitigation: re-fetch immediately before the rebase and before the final report; report drift rather than hiding it.

## Follow-up items

* Coordinator: align child 1231 onto the final head, then one stack gate (`--stack parent --stack tip`) on the final main.
* Owner-approved lease push of the rebased topic if publication is wanted.
* Fresh independent exact-head review; policy signoff and Legal retention remain unmet.
