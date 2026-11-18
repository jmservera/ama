# Plan: case-domain chat grounding (Refs #164)

* [x] Add case facts for `grants`, PAS 2035 sign-offs (`pas2035.*`) and `sensor_review_drafts` (`sensor.*`).
* [x] Add `claim`, `pas2035` and `sensor` intents with deterministic answers, a `[Origin: decision_rule]` line and a domain-boundary rule that withholds legal conclusions and approvals.
* [x] Route those intents rules-first in `ChatPanel` via `RULES_FIRST`, so no model number or legal claim can appear.
* [x] Add `src/agents/tests/test_regulatory_chat_case_domain_grounding.py`.
* [x] Run focused tests, ruff and mypy with `/tmp` caches in core and agents.
