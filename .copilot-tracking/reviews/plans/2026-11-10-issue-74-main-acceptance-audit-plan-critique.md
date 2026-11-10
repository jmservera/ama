# Issue 74 current-main acceptance audit: final-candidate plan critique

Executed once on the final candidate plan and details, on 2026-11-10, before Plan completion. Verdict: compatible with changes; all applied directly. No significant or divergent issue needed a user decision.

| ID | Finding | Disposition |
| --- | --- | --- |
| C1 | The API and core commands used module names that do not resolve: `tests` folders are not packages, and `test_home_case_api` needs `building_fixture` and `dataset` on the path. | Applied: details now use `unittest discover -s tests -p <file>` with `PYTHONPATH=../core/tests:../agents/tests` for the API. |
| C2 | The Chromium prerequisite was implicit. A version mismatch could tempt a shared `playwright install`, which is outside the "own environment only" rule. | Applied: details record that a mismatch is recorded as blocked and no shared download is made. |
| C3 | "Outcome" has no single home field; the matrix could imply more than the source shows. | Applied in details: outcome is defined as `stage`, `closed` and quality states, and the matrix must say so, with a remaining action to obtain a human definition. |
| C4 | The matrix could blur fixture-only observation and real acceptance. | Already planned (status vocabulary and separate evidence classes); retained, and the review must check it. |
| C5 | A static source read could be presented as verification. | Already planned: static read can only explain sourcing and renders as `implemented-unverified` unless a maintained check asserts the field. Retained. |
| C6 | Witness ordering and 40-hex commit claim risk. | Already planned; retained. |

Rejected advice: none. No conflict with a confirmed Root decision. No second critique will be run for this task.
