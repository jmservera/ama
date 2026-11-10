<!-- markdownlint-disable-file -->
# Details: issue 148 C1 clock erratum

Plan: `.copilot-tracking/plans/2026-11-10-issue-148-c1-clock-plan.md`.

* New file `.copilot-tracking/changes/2026-11-10-issue-148-c1-clock-erratum.md`: table of the six original files with their claimed times, each withdrawn as unobserved; commit provenance table labelled provenance only, not phase times; ancestry proof command and result; statement that no exact phase wall time was captured.
* Checks: `git diff --name-only d305..HEAD` limited to `.copilot-tracking/`; `git diff d305 HEAD -- src infra docs .github` empty; `git rev-parse d305:src HEAD:src` equal; relative links resolve; `git diff --check`.
* No original file is edited, no new test run; d305 targeted results (112 tests OK, Ruff, format, mypy) apply only because the product tree is unchanged.
