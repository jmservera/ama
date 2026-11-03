---
title: Issue 203 round 1 research
ms.date: 2026-11-03
---

Research disposition: executed. Planning Readiness: Ready.

## Prior delivery checked

* Merged: #289, #291, #321, #499 (retired legacy directories), #613, #706 (stale regulatory path), #799 (link repair and all-link audit).
* Criterion 3 (index and log) already met.

## Fresh evidence (2026-11-03, origin/main 2989576d0)

* `mvp/` and `prototype/` directories are absent.
* Live Markdown (excluding the append-only log and docs/capstone history): 1873 relative links, 0 unresolved.
* Literal `mvp/` and `prototype/` matches outside history are intentional: defensive `mvp/data` guards (tools/rpi-checks.py, infra tests, src-ci.yml, mvp-validation.yml), "moved from mvp/" provenance notes in src READMEs and pyproject files, the cut-over audit tool and its tests, rubric README dated records, and cut-over statements in README.md and src/README.md.

## Slice choice

Criterion 2 is now provable for live docs but nothing prevents regression. Smallest coherent slice: a unit test in src/core/tests that fails on any unresolved relative link in live docs. No docs, workflow or infrastructure change; focused tier.

## Unmet after this slice

* 1: literal search still returns intentional references that are not all archive-tag or dated-record form; owner wording decision pending.
* 2: met for live docs; history (log, capstone) still has historical link debt.
* 4: no post-cleanup main rubric comparison produced.
* 5: no deployed-app plus CI-green evidence produced here.
