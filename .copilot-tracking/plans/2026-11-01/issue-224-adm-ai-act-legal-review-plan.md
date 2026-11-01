<!-- markdownlint-disable-file -->
# Plan: Issue #224 legal review pack

Research: `.copilot-tracking/research/2026-11-01/issue-224-adm-ai-act-legal-review-research.md`

## Scope

Documentation-only slice, no source change (rule card edit is a routed review item for the owner, not made here because the DPO has not decided).

## Phases

* [x] Phase 1: create `docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md` with the currentness check (source date, retrieval date, commencement), an unsigned per-regime decision record, review items (requirements, decisions, tests), non-inference rules and feed notes for #219 and #211.
* [x] Phase 2: link it from `docs/reference/regulatory/README.md` and `docs/reference/README.md`; append `docs/reference/log.md`.
* [x] Phase 3: validate links and diff; commit; push; open PR with `Refs #224` naming unmet criteria.

## Critique (single pass)

* Risk: presenting an agent check as a Legal/DPO decision. Mitigation: decision fields read `Pending`, no checkboxes ticked.
* Risk: treating secondary EU Omnibus claims as fact. Mitigation: recorded as unverified discovery only.
* Risk: changing the rule card citation without DPO approval. Mitigation: routed as review item RI-3.
* Verdict: proceed; no conflicts with confirmed decisions.

## Success

Criteria 2, 3 and 4 evidenced as prepared content; criteria 1 and 5 unmet pending Legal/DPO decision.
