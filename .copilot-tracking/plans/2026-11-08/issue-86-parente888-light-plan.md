---
title: Issue 86 light propagation of local parent e888a49 plan
description: Plan, one normal merge and light checks (Refs #86)
ms.date: 2026-11-08
---

Final tier FULL (security-sensitive); this step is LIGHT only, no FULL, lock, SQL, browser, images, scanner or model.

1. Commit records; one independent critique recorded before the merge.
2. Re-verify identities; stop on drift.
3. `git merge --no-ff e888a49` (local object); no rebase or force.
4. Prove two parents; each incoming path blob/mode equals the parent except the two overlap files, which must contain both intents (child `complaints_receiver` declaration and complaint source blobs intact, parent hunks present); prior RPI/log prefix bytes; rubric JSON parse.
5. From a whole git archive with a new non-editable own-source install under `/home/azureuser/.local/share/ama/gates/g86-e888-light-1108`: core `test_resident_decisions`, `test_ranking_publication*`; API selected tests; canonical mypy/ruff for core; real `.out/.err/.exit`.
6. Changes and author Review; commit; freeze.

Amendments from critique (see challenges file): run only `ManifestDefaultsMatchApi` from the workbench defaults module (no Chromium); log proof is in-order preservation of existing entries; origin proof covers core `store`, `resident_decisions`, `ranking_publication` and API `server`; blob and mode proof for every child-changed path versus `34729c4f` and both overlap files; first parent is the records commit.
