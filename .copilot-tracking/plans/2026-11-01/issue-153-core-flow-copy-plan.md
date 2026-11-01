---
title: Issue 153 core-flow copy plan
date: 2026-11-01
task_slug: issue-153-core-flow-copy
---

## Phases

* [ ] P1 Copy: replace "gate" in `role-screens.js`; plain generic fallback in `app.js`; adjust `ops.js` sentinel via a flag; plain `ranking_snapshot` error; `law.js` fail message with owner and next action.
* [ ] P2 Tests: extend `AUDITED_FILES`; add tests for fallback message (reason, owner, next action), ranking error, role-screens wording.
* [ ] P3 Docs: update content-standard open findings and acceptance table; append `docs/reference/log.md`.
* [ ] P4 Validate: api and core unit tests, ruff check, ruff format --check, mypy for touched projects.

## Critique (single pass, direct dispositions)

* Verdict: proceed. Keep "Closes" out; AC2, AC3 and AC5 stay partial or unmet, so PR uses "Refs #153".
* Do not change stored values or safety/approval logic.
