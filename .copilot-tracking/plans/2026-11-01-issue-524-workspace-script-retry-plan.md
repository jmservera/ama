# Plan: close out evidence for #524

* Scope: acceptance criteria only; no new source (retry from #527; release-URL reuse and the expanded four-test suite from #594 and #538, all already in main).
* Phases:
  * [x] Re-run `test_workspace_scripts` to confirm the retry and failed-first-load test pass.
  * [x] Record cause evidence and unresolved parts in the research artifact.
  * [x] Append knowledge-base log entry in `docs/reference/log.md`.
  * [x] Commit, push, open PR with `Refs #524` (live authenticated verification still pending).
* Critique (single pass, direct): adding code would duplicate the existing retry; raising the timeout is a behaviour change not in the criteria, so it is recorded as follow-up. Verdict: proceed docs-only.
* Validation: unit tests for the touched area; no Python touched, so ruff/mypy are unaffected.
