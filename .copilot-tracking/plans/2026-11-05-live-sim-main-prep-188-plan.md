---
title: Plan for #188 current-main preparation
ms.date: 2026-11-05
---

* Ordinary `git merge --no-ff` of the pinned bb3a3b03c into the child; no rebase, amend, force, retarget or parent movement. A conflict stops the work.
* Then run small focused regressions only: retained_envelopes lossless replay, indoor observed_series exclusion, HANDOVER_SCHEMA_UNSUPPORTED refusal before statistics and replay, legacy-only handover, plus Ruff (no cache) and format check and mypy with an external cache for src/api and src/core. PYTHONDONTWRITEBYTECODE=1 and explicit worktree source paths, with an import proof.
* Excluded: model, feature, schema, threshold, consent, adapter, API or UI change; any gate, browser, SQL, build, scan or cloud call; any cleanup. Heavy lock owned by #96 runner 1592594; no queued or competing run.
* Critique (executed once inline): a clean merge with no overlapping files needs no source edit; compatible finding applied: commit the merge separately from the records. Verdict: proceed.
* Tier FULL; the complete gate stays pending and unclaimed.
* [ ] Human review required and left unchecked.
