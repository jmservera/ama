---
title: Issue 86 light propagation of local parent e888a49 research
description: Prospective research for one normal merge (Refs #86)
ms.date: 2026-11-08
---

Scope: Refs #86 only; LIGHT propagation, not FULL or publication. Start `43c9f4662167d57edce2c6e1fc6ec65f6766b5f0`, tree `ef3aeb46…`, ignored-clean. PR 1243 OPEN, target `feat/controlled-lifecycle-integration-81` unchanged.

* Local parent `e888a4995dac70acb2afd61d7aca1f9bbc92f6f5`, tree `07136e4b…`, branch `feat/controlled-lifecycle-integration-81`, ignored-clean; fetched as a local object only. It contains the child's prior parent `34729c4f` and main `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (current `origin/main`).
* Incoming delta from `34729c4f`: 20 non-tracking paths: rubric score, cutover evidence pack, reference README/log, scenario manifest, API server/role-screens/checks/tests, ranking publication source, runner, tests, `src/core/README.md`, `pyproject.toml`, `store.py`.
* Real overlap with child-owned files: `src/core/README.md` and `src/core/.../store.py` (child holds the `complaints_receiver` TYPE_CHECKING declaration; parent holds ranking archive/stage hunks). `git merge-tree` reports a clean merge (tree `34ac7a4b…`); hunks are disjoint but must be confirmed in the result.
* Limits and open items unchanged: original Medium findings, adverse browser outcome, 1238 supersession (separate, human-blocked), per-store registry, point-in-time guard, no real receiver.
