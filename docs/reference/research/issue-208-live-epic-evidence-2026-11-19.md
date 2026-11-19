---
title: Epic 208 demo proof, per-criterion results (live run 2026-11-19)
description: Proven and unproven results for the three unticked acceptance criteria of the regulatory compliance assistant epic, with a child-order audit that records two delivery-order deviations
ms.date: 2026-11-19
ms.topic: reference
---

Refs #208, Refs #440. Scope: synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Only read commands ran (gh and local tests); no Azure resource was created or changed and no credential was read. Base: `05e94d303` (main). Tier: FOCUSED; the only code change is `tools/test_epic_208_child_order.py`, with no `src/` change.

## Result

| # | Unticked criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | Stabilization checkpoint (#440) before closure | Partly proven | Local regression passes (below); #215 (2 unticked) and #216 (1 unticked) are open, #440 itself has 2 unticked criteria; owner pivot or defer decision not agent-provable |
| 2 | Decision accepted, amended or epic closed | Proven in repository evidence | #209 closed 2026-10-16; ADR 0005 Status: accepted for synthetic development only, 2026-10-16. Ticking is left to the coordinator |
| 3 | Children accepted in ADR phase order | Not met as stated | ADR Phasing is law store (#210), rule cards and engine (#211, #212), chat (#214), change monitoring (#213). Observed closure: #213 (2026-10-27) before #214 (2026-10-31) and #212 (2026-11-04); #214 before #212. No owner note accepts the deviation. Dependency-wise, #210 (2026-10-15) closed one day before #209 (2026-10-16) |

## Local regression (criterion 1)

* core: test_rulecards, test_rule_engine, test_regulatory_chat, test_regulatory_output_guard, test_regulatory_eval_gates_216, test_regulatory_privacy, test_regulatory_privacy_audit_217, test_regulatory_usage: 144 tests OK.
* api: test_lawstore, test_regulatory_chat_api, test_regulatory_watch_guard_api, test_regulatory_ux_check, test_regulatory_a11y_cues: 71 tests OK, 14 skipped (browser or SQL prerequisites; not passes).
* agents: test_regulatory_gates, test_regulatory_answers, test_regulatory_non_advice_guard: 30 tests OK.
* tools: `python3 -m unittest tools.test_epic_208_child_order`: 6 tests OK; `ruff format --isolated --line-length 100 --check` and `ruff check` clean.

## Child-order audit

`tools/test_epic_208_child_order.py` pins the ADR phase order, the declared child dependencies, the implementing modules and the two deviations above. Closure dates are observations of 2026-11-19, not live assertions, and the test accepts nothing.

## Unproven and why

* Criterion 1 remainder: #215 comprehension testing with staff and WCAG acceptance need person-run work, out of scope for the demo; #216 needs named owners for gate thresholds. Azure-only residuals were not exercised.
* Criterion 3: only the owner can accept or amend the delivery order.
