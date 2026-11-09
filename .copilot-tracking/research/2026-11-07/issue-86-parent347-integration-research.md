---
title: Issue 86 integration of local parent 34729c4 research
description: Prospective research for one normal merge (Refs #86)
ms.date: 2026-11-07
---

Scope: Refs #86 only. Start `ed5bddf4faa5071487e1f805d5159a2cd488b4ce`, tree `9b1fef74…`, ignored-clean, preserved at `backup/issue-86-pre-347-ed5bddf`. PR 1243 OPEN, target `feat/controlled-lifecycle-integration-81` unchanged.

* Local parent `34729c4f11e19757154b08e7a35df12b3ddf6a8d`, tree `d52dcb86…`, ignored-clean; contains prior parent `a0ec0834` and `origin/main` `23b26a7f3a4693cd20dcf0447303d97491096cb3` (admitted by coordinator: score-only over `c1a164`).
* Earlier attempt against `a0ec` stopped before any write because main moved; log `/tmp/rpi-86-parenta0ec-preparation-1107.log` kept. New pins replace `c1a`/`a0ec`, no bypass.
* Incoming non-tracking delta from the child's last parent `6cae8cbe`: `.github/rubric/scores/latest.json`, `src/api/tests/test_assistant_release.py`, `tools/rpi-checks.py`, `tools/test_rpi_checks.py`. No child-owned overlap; merge-tree clean (`1179284a…`). Production source is unchanged; not all of `src/`.
* Open and historical: original Medium findings, adverse browser outcome, 1238 supersession (separate, human-blocked), 308 tests/110 skips baseline. Limits: per-store registry, point-in-time guard, no cross-process proof, no real receiver.
