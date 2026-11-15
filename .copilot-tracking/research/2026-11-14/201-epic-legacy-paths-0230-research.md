---
title: Issue 201 epic legacy-path research
ms.date: 2026-11-14
---

* Disposition: executed. Planning Readiness: Ready.
* Scope: `src/`, `infra/`, `.github/workflows/` for epics #113, #136, #165, #157, #149 (Refs #201).
* Finding: `mvp/` and `prototype/` directories are absent. Remaining matches are historical notes (archive `v0.21.0`) in READMEs and pyproject comments, the cut-over audit data and its tests, negative `git ls-files mvp/data` guards, and a `PYTHONPATH=mvp` prohibition in `src/README.md`.
* Kept names: workflows `mvp-ci.yml` and `mvp-validation.yml` are retained by instruction until a post-cut-over protection update; they hold no legacy path execution.
* Constraint: do not edit `docs/architecture/cutover-evidence-pack.md` or `docs/reference/log.md` (open PR #1605).
