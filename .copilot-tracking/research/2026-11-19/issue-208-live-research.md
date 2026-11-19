# Research: epic #208 first unmet demo criterion (2026-11-19)

Disposition: executed. Planning Readiness: Ready.

Base: main `05e94d303`. Scope: synthetic demo, desktop only; read-only gh and local tests; no Azure writes, no credentials read.

## Unticked criteria of #208

1. Stabilization checkpoint (#440) before epic closure. First unmet. #440 is open with 2 unticked criteria; #215 (2 unticked) and #216 (1 unticked) are open.
2. Decision feature accepted, amended or closed. Met by evidence: #209 closed 2026-10-16; ADR 0005 Status "Accepted for synthetic development only" (2026-10-16). Ticking is the coordinator's act.
3. Children accepted in ADR phase order. ADR 0005 Phasing: 1 law store (#210), 2 rule cards and engine (#211, #212), 3 chat (#214), 4 change monitoring (#213), 5 broaden. Observed closure: #210 2026-10-15, #209 2026-10-16, #211 and #213 2026-10-27, #214 2026-10-31, #212 2026-11-04, #217 2026-11-18. Declared dependencies (issue bodies) hold, but #213 (phase 4) closed before #214 (phase 3) and #212 (phase 2): delivery deviated from the ADR sequence. No owner note accepting the deviation was found.

## Local-first regression (criterion 1)

* core: `unittest` of test_rulecards, test_rule_engine, test_regulatory_chat, test_regulatory_output_guard, test_regulatory_eval_gates_216, test_regulatory_privacy, test_regulatory_privacy_audit_217, test_regulatory_usage: 144 tests OK.
* api: test_lawstore, test_regulatory_chat_api, test_regulatory_watch_guard_api, test_regulatory_ux_check, test_regulatory_a11y_cues: 71 tests OK (14 skipped, browser or SQL prerequisites).
* agents: test_regulatory_gates, test_regulatory_answers, test_regulatory_non_advice_guard: 30 tests OK.

## Decision

Implement a repository-local, read-only audit (`tools/test_epic_208_child_order.py`) pinning the ADR phase order, the declared child dependencies, the implementing modules and the observed order deviation, so criterion 3 is traceable and drift is detected. It never asserts live GitHub state and never approves anything.
