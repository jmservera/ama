---
title: Issue 149 parent main ecb2 integration plan
ms.date: 2026-11-08
---

## Plan

* One normal `git merge --no-ff` of fetched origin/main ecb28815. No rebase, reset or force.
* Resolve only demonstrated append or document conflicts, keeping both intents (append-only log and rubric data kept from main where it is generated, parent records kept in full). Validate any resolved JSON with a parser.
* Prove that all `src/`, `tools/`, `infra/` and `.github/workflows` bytes and modes equal fd48abc9 after the merge (or are main-only and unchanged from the assessed main).
* Docs-only tier: parse JSON, check links and the diff. Run unit or browser checks only if a changed input demands it.

## Critique (single pass)

A normal merge preserves ancestry. Taking the rubric score file wholesale from main is acceptable only because it is automatic bot output; any other file conflict must keep both sides. If source bytes differ from fd48 beyond main-only changes, stop and reassess instead of reusing browser evidence.
