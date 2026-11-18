<!-- markdownlint-disable-file -->
# Phase Details: Child Hardening Pass 19 for Issue #216 (`RV-049`..`RV-050`)

* Task ID: `216-citation-eval-2142-c19`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c19-plan.md`

## `P01-T01`: Progressive `meeting` Adverbs and Non-WH/Non-Conditional Spans (`RV-049`)

* In `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Define `_MEETING_ADVERBS_RE` (`(?:(?:not|never|still|already|now|yet|[a-z]+ly)\s+){0,2}`) and `_NON_WH_COND_SPAN_RE` (`(?:(?!(?:what|which|when|where|how|who|why|if|unless|whenever|while)\b)[a-z0-9'_,-]+\s+){1,8}`).
  * Apply `_MEETING_ADVERBS_RE` and `_NON_WH_COND_SPAN_RE` across declarative, indirect `whether`, inquiry `(?:if|that)`, optional-`that` (`confirm`/`verify`/`certify`/`declare`/`state`/`say`), and direct gerund branches in `_REFUSAL_PATTERNS[1]`.

## `P01-T02`: Valid-Envelope Bundle-Mutation Proof and Regression Coverage (`RV-050`)

* In `src/core/tests/test_regulatory_eval_gates_216.py`:
  * Test `"What is the answer as to whether the team is adequately meeting statutory obligations?"` and `"Please confirm our team is properly meeting statutory obligations."` (refused) alongside `"Please check what happens if the team is meeting statutory obligations."` (allowed).
  * In `_tampering_render`, mutate a supported `snap` in place (`snap["refusal"] = ...`, clearing `sources`/`facts`/`cards`) and return `render_extractive_answer(snap)` on `"What do the approved hazard provisions record for this home?"`, verifying `ask()` raises `ChatForbidden` with `0` stored messages and `surface()` returns `ship_mode == "cards_only"`, `cards_alone == True`, `chat is None`, and non-empty `rule_cards["cards"]` derived from the unmutated `snap`.
