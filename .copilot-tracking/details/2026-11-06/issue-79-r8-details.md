---
title: Issue 79 details, continuation r8
ms.date: 2026-11-06
---

* Allowed diff: three new files for Changes, Review and state, plus these three prospective files. Nothing under `src/`, `docs/` (no knowledge-base log append) or earlier tracking records.
* Checks, read-only: `git diff --name-status` against `0ec823b1`; `git diff --quiet 0ec823b1 -- src docs <earlier tracking paths>`; `python3 -m json.tool` on the state; link target existence; `git status --short --ignored`.
* Not run: tests, Ruff, mypy, gate, SQL, Docker, browser, install, lock acquisition, cloud, push, cleanup or deletion of any kind.
* Wording rules: say "event preserved" not "raw log recovered"; say "author-only review"; no fresh test run claim; no #79 acceptance.
