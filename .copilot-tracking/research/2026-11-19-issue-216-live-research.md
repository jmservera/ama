---
title: Issue 216 live research, 2026-11-19
description: Is any unticked demo criterion of #216 unmet
ms.date: 2026-11-19
---

Opening note. Issue #216 has one unticked criterion: citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set. Prior evidence: docs/reference/research/eval-gates-live-216-2026-11-18.md (third pass, raw output retained). Research disposition: reused, plus a local test rerun below.

## Findings

* The single unticked criterion is, for the synthetic desktop demo, already proven in [eval-gates-live-216-2026-11-18.md](../../docs/reference/research/eval-gates-live-216-2026-11-18.md) (third pass): gates in `src/core/.../regulatory_eval_gates.py` with a recorded synthetic owner and provisional 1.0 thresholds; live measurement on 30 declared prompts with raw output kept (refusals 10 of 10, cited model answers 9 of 9 valid, adversarial 10 of 10, 18 model calls, 20,128 tokens, inside the 30-call and 60,000-token authorisation).
* Local rerun on this branch (2026-11-19, base e3494f476), from `src/agents`: `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest test_regulatory_gates test_regulatory_citation_card_gates test_ai_eval test_paired_trial test_gate_agreement test_regulatory_eval_gates_216`. Result: 100 tests, OK (309.8 s).
* No new live model call or Azure action was made today. A repeat would add spend and, per the 2026-11-18 note, replicate the same author, case and set without independence.
* Still unproven and not demo-provable (owner decision 2026-11-18 waives DPO and Legal approval): named Legal and Compliance gate owners, an independent grader, a multi-case set, and citation validity against regulatory rule cards (the regulatory chat needs a role the test account lacks and is deterministic).

## Planning readiness

Ready: no unmet demo criterion, so no source change. Tier FOCUSED (no src edit).
