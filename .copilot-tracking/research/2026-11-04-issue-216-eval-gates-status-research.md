---
title: Research for #216 regulatory evaluation gates status record
ms.date: 2026-11-04
---

* Task: feat/slice-216, Refs #216 (parent #208).
* Research disposition: executed (merged PR list, issue comments, focused test run).
* Prior delivery check: merged PRs #355 (gates), #506 (offline usage), #632 (re-verification), #684 (owner-authorised limit guard), #834 (paired-trial scorer), #890 (alert precision and acknowledgement scorer) and #963 (fail-closed owner agreement for citation and refusal gates).
* Evidence this session: `tests/test_regulatory_gates.py` in `src/agents` ran 18 tests, all OK, against the current head (fc92d53c4).
* Ticked criteria stay proven: hazard misses critical, recall baseline before thresholds, out-of-cadence labels, per-check reporting, finite-limit guard.
* Unmet, each needing a human or owner authority:
  * Criterion 1: owner-set citation and refusal thresholds and an independent grader on a graded and adversarial set.
  * Criterion 4: measured chat-over-cards value needs a real staff paired trial; cards ship alone until then.
  * Tokenomics 1: AI cost per accepted check stays Unknown (price source, accepted-check definition, allocation, usage and covering authority missing).
  * Tokenomics 2 live-run part: no owner-authorised model-calling run exists; no spend authority is assumed.
* Conclusion: no further engineering slice exists without those decisions. A code change would only restate delivered scorers.
* Planning Readiness: Ready for a docs-only record.
