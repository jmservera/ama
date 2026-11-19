# Research: issue #126 live run 3

Refs #126. Task `2026-11-19-issue-126-live-r3`. Disposition: reused and re-executed.

* Prior runs (`issue-126-live-r2-*`, note `docs/reference/research/issue-126-live-2026-11-19.md`) found no code gap: residual and unassessed registers (22 findings), dispositions, release gates, breach pause and BG-011 MDE are implemented in `src/core/.../governance.py` and exposed at `/api/governance`.
* Unticked criteria are human approvals, an assessment run, populated evidence and SQL/Azure acceptance.
* Plan: rerun core and API governance tests, rerun the read-only live probe on `ca-cutover-test-demo-api`, record a r3 note. No Azure resource creation.
* Planning Readiness: Ready.
