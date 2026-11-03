# Issue 198 plan: drop dead mvp excludes (2026-11-03)

* Slice 1 (this PR): remove `mvp/data/**` and `mvp/web/vendor/**` from the `solution-code` excludes; update the README rubric section.
* Stacked later slices (not planned for delivery here): none feasible; ACs 3, 4 sequencing and 7 are historical and cannot be proven retroactively. Close the issue only on an owner decision to accept that.
* Out of scope: workflow Markdown or lock, `rubric_version` bump (not recommended), test repairs for the 17 failures.
* Validation (focused): JSON parse, `test_prepare.py`, ruff and mypy on the rubric scripts, git diff review.
* Critique (single pass): compatible, no conflict with the 2026-10-14 owner decisions. Risk: registry edit reopens criteria after merge; README records a no-change expectation for the 77 total. Accepted.
* Details: [details](../details/2026-11-03-issue-198-registry-excludes-details.md)
* PR uses `Refs #198`.
