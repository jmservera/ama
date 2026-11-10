---
title: Review - numeric boundary D1 for the constructed paired report (Refs #216, #208)
description: Single post-implementation review of the local D1 delta
ms.date: 2026-11-10
---

## Execution

* Executed once after implement-done by the implementing agent, reading the final diff of `src/agents/evals/run_regulatory_gates.py`, `src/agents/tests/test_paired_report_command.py` and `src/agents/README.md` against the plan, details, critique, brief and the two Medium findings. No nested agent. This is a self-review, not the independent assessment, which Root owns.
* Assessed boundary: `ab365e53d024e269c9ad4f0b0e33a8361a43e30b` plus the uncommitted delta.

## Outcome

conformant-with-limits. Both findings are corrected without scorer, schema, threshold, cost, approval or default-output change.

## Evidence

* F1 (derived ratio): the paired subnormal-cards and maximum-chat input now exits 1 with empty stdout and `--constructed-paired-observations: derived values are not finite ...`, before report generation and before `--record`; a sentinel record file stays untouched. Red before: exit 0 with `Infinity`.
* F2 (huge negative): minus-401-digit seconds, `-1` and `-0.5` for both fields exit 1 with `observation N: <key> must not be negative`, no traceback. Red before: `OverflowError` traceback.
* Exact bound: 31536000 accepted for both fields; 31536001 refused with `exceeds 31536000`.
* Targeted tests, configured Ruff and mypy pass; default output hash is unchanged and `paired_trial.py` has no diff (see the changes record).

## Limits and residual risk

* R1 (unchanged, out of scope per brief and the reviewer): `--record` can still be pointed at a canonical path by an operator; no guard was added.
* The test for the ratio needed correction after a first red run used unpaired data (disclosed in the changes record); the final red was rerun against the pre-fix script.
* Only these inputs are covered; other non-finite derived values are caught generically by the strict dump. Self-review only; no mutation testing, hosted CI, browser, SQL, model, human or live validation.
* Whole issues #216 and #208 stay open; the constructed result is caller-declared, unverified, cost Unknown and `cards_only`.
