<!-- markdownlint-disable-file -->
# Critique: #74 home case regression slice (issue-74-home-case-regression-2300)

Executed once on the final candidate research, plan and details by an independent rubber-duck subagent (read-only, no author context), 2026-11-12, before any implementation. Not repeated. Verdict: Revise. Every finding was compatible with confirmed decisions and applied directly; no significant or divergent issue needs a user decision.

| ID | Severity | Finding (summary) | Disposition |
| --- | --- | --- | --- |
| CR-001 | Blocking | Finance assertions contradicted the response: allocation includes `source`, and finance responses omit `building.costs_restricted` instead of setting it false. | Applied: assert the real allocation shape (`shared_cost_id`, `amount_gbp`, `source`) and treat an absent restriction flag as unrestricted (`not .get(...)`). |
| CR-002 | Blocking | The existing ZF-2 sibling-absence check cannot run unchanged on ZF-3, which must show "Loft insulation" and the sibling survey name; `SIBLING-EVIDENCE` id is not rendered. | Applied: the existing check stays scoped to ZF-2; ZF-3 uses rendered names for positive checks and own-token absence; ids are not used as sentinels. |
| CR-003 | Blocking | Mutating the pip-installed `app.js` would not affect the served file: the harness puts the checkout source directories on the server `PYTHONPATH`. | Applied: mutation controls run the whole check from an external scratch copy of `src/` and the check, with the served asset identity verified by hash; the repository tree is never mutated. |
| CR-004 | Non-blocking | "Shared ventilation" also appears in "Shared ventilation renewal" (WORK-1), so substring checks do not identify the system. | Applied: assert the exact list item `SYS-1: Shared ventilation. Source: SYN-SURVEY` and mutate only that item. |
| CR-005 | Non-blocking | Mutation controls did not establish each assertion family (cookie swap fails flags before amount leaks; seed removal does not test quality). | Applied: one targeted control per family (document, quality, system, restricted amounts, finance amounts); the intended assertion name must fail. |
| CR-006 | Non-blocking | Homes share several document names, so unique sentinels cannot prove all sibling documents are absent. | Applied: the claim is limited to the tested sentinel records (own and sibling survey names and quality measures); it is stated in the changes and review. |

The critique is author-side advice, not independent exact-head review. The #82 insertion is a separate hunk; the append-at-end mitigation was judged credible.
