---
title: Review of the final unticked criteria of #891 and #107
description: Per-criterion evidence and Closes eligibility for #891 criterion 2 and #107 criterion 7
ms.date: 2026-11-13
---

## Review execution and outcome

* Executed once, by the implementing agent after implementation. It is not independent; independent exact-head review, hosted CI and human approval remain outstanding.
* Outcome: conformant for the scoped tests-only change; no material finding open. Boundary: the two test files plus tracking artifacts.
* Changes: [changes](../../changes/2026-11-13/891-107-final-criteria-2013-changes.md).

## Per-criterion evidence

| Criterion | Sub-clause | Evidence (test in `src/api/tests/`) | Result |
| --- | --- | --- | --- |
| #891 criterion 2 | (a) per-call gate | `test_a_per_call_gate_stays_in_force`: one call per request root, role and thread limits, mid-call revocation | Proven |
| #891 criterion 2 | (b) token and cost admission | `test_b_call_budget_...`, `test_b_token_budget_...`, `test_b_money_budget_holds_before_live_dispatch`: held, nothing sent, nothing reserved | Proven |
| #891 criterion 2 | (c) privacy refs | `test_c_privacy_refs_and_personal_data_safeguards_stay_in_force`: each missing ref refuses before dispatch; personal data redacted; export allowlist | Proven for the documented allowlist |
| #891 criterion 2 | (d) retention | `test_d_retention_policy_is_unchanged_by_the_demo_switch` | Proven |
| #891 criterion 2 | (e) refusals | `test_e_refusals_and_citation_checks_stay_in_force`: out-of-scope, memory-as-evidence, unsupported claims withheld | Proven |
| #891 criterion 2 | switch honoured | `test_switch_is_honoured_and_a_cited_model_answer_is_metered` | Proven |
| #107 criterion 7 | per assistant | `test_usage_per_assistant_and_accepted_proposal_is_attributable_and_content_free`: five registered assistants, tokens and charge match raw ledger and `by_capability` | Proven |
| #107 criterion 7 | per accepted proposal | Same test: one accepted per assistant, `tokens_per_accepted_proposal` and cohort `projected_token_charge` match; proactive proposals unreviewed stay out | Proven |
| #107 criterion 7 | no raw case content | Same test: sentinel address, name and case text absent from ledger, report and captured logs; positive control in provider request | Proven |

## Closes eligibility

* #891: criterion 2 is the last unticked one and every sub-clause has a passing test, so `Closes #891` is eligible once the coordinator verifies the exact head. The local commit uses `Refs #891` until then.
* #107: criterion 7 is proven, but the issue body also lists unticked non-scope items (release admission, serving-version attestation, SQL race, delivered-build evidence) per the research. The prompt states only criterion 7 remains, so eligibility rests on that statement; the coordinator must confirm against the live issue. The local commit uses `Refs #107`.

## Limits and follow-ups

* No live model, Azure or real resident data; fake transport and synthetic price. Charge is projected, not billed (`token_cost` Unknown).
* The `ruff`-formatted import reorder in `test_chat_panel.py` is a mechanical side effect.

| Rank | Follow-up | Evidence |
| --- | --- | --- |
| 1 | Coordinator verifies exact-head CI and issue state, then closes #891 and #107 | Closes eligibility above |
| 2 | Add a mutation check for the call-budget hold (test b) | Spot-check gap in changes artifact |
| 3 | Share the chat-demo fixture with the consumption test helpers | Duplicated fake-transport setup |
