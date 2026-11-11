<!-- markdownlint-disable-file -->
# Plan Critique: issue 1420 resident-choice CSV page summary (2026-11-10)

* Execution: one critique, run once by a rubber-duck sub-agent on the final candidate plan, details and research (read-only, no edits). No repeat critique.
* Verdict: Approve with changes. Compatible findings applied directly; none conflicted with a confirmed decision; no user decision required.
* Artifacts: [plan](../2026-11-10-issue-1420-choice-csv-research-1110-plan.md), [details](../../details/2026-11-10-issue-1420-choice-csv-research-1110-details.md), [research](../../research/2026-11-10-issue-1420-choice-csv-research-1110-research.md)

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Measure names are free text (`resident_decisions.py:869`) and could carry excluded personal data | Applied: fail closed to `Measure name withheld` unless in a controlled vocabulary; statuses limited to closed sets; Root question Q5 added |
| 2 | Blocking | The UI stop predicate returns false on missing evidence, so unknown could read as `None recorded` | Applied: `Unknown (evidence unavailable)` for incomplete measures; `None recorded` only with complete evidence; tests added |
| 3 | Non-blocking | Declined then Waiting keeps `Needs human review` but may be invisible | Applied: retained Declined review listed in the stopped column, noted as a deliberate UI difference; Root question Q6; test added |
| 4 | Non-blocking | No HTTP loader-failure test | Applied: patched store failure test for 5xx JSON without Content-Disposition or CSV |

## Residual risks

* Q1 to Q6 remain open for Root; defaults are the conservative option.
* Role parity, vocabulary source and 1419 integration order are unverified hypotheses; nothing was run.
* Findings were not independently re-reviewed (one pass by design). Post-implementation Review is not executed and not claimed.
