<!-- markdownlint-disable-file -->
# Changes: Issue #224 legal review pack

Plan: `.copilot-tracking/plans/2026-11-01/issue-224-adm-ai-act-legal-review-plan.md`

## Added

* `docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md`: official-source check, pending Legal/DPO decision record, review items RI-1 to RI-7, non-inference rules, #219 and #211 feeds.

## Modified

* `docs/reference/regulatory/README.md`: reviewed-update section.
* `docs/reference/README.md`: index row.
* `docs/reference/log.md`: appended entry.

## Divergences and validation

* No source or test change; rule card citation routed as RI-3 pending DPO decision.
* Validation: documentation-only; relative links and Git diff reviewed. No Python touched, so no ruff or mypy run needed.

## Correction cycle (PR #702 Copilot review, 2026-11-01)

* Fixed five review threads in the applicability review: two broken relative links, Article 22B added to the decision question, RI-2 expanded to the BRD controls (FR-034 disambiguated, RULE-021, RULE-022, CON-003; AC-072 is a PRD incident-suspension criterion, not an Article 22 control), RI-4 test coverage corrected and `test_rule_engine.py` added.
* Validation: links resolved; ruff, ruff format and the touched core tests rerun; no Python changed.
