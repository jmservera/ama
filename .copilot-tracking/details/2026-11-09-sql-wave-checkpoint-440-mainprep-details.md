---
title: SQL wave checkpoint 440 current-main preparation details
ms.date: 2026-11-09
---

## Phase details

* P1 Prospective commit of research, plan, details, critique and state; `git status --short` shows only these files before commit.
* P2 `git fetch origin main`; `git rev-parse origin/main` equals `3a9767d5c...`; `git merge --no-ff origin/main -m "merge: bring main 3a9767d5c into SQL wave checkpoint (#440)"` with the privacy email and trailer.
* P3 Proof commands: `git diff --quiet origin/main HEAD -- src infra tools .github/workflows` and `git diff --name-only origin/main HEAD` limited to `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md` and `.copilot-tracking/`.
* P4 Edit only by appending: the pack subsection at end of file, one sentence in the index entry of the SQL-wave checkpoint, one new log entry at the end.
* P5 Preservation proof on the final committed tree (after P6): `git diff --numstat f2e07999 HEAD -- <pack> <log> <index>` and the same against `origin/main` must show 0 deletions for each, so every line of both parents survives in order (main's two pack insertions are the only additions versus `f2e07999`; the note, index sentence and log entry are the only additions versus `origin/main`). Log and index must additionally be a byte prefix of the final file versus `f2e07999` (main did not change them). Link check with a Python script over changed Markdown. Run source equality, path inventory and clean-tree checks after the final commit.
* P6 Record changes, Review (one), state and handoff.

## Wording constraints

ASCII only, no em dashes, no bolded-prefix list items, no approval, closure or hosted claim, dated source identities, explicit label of coordinator-reported items.
