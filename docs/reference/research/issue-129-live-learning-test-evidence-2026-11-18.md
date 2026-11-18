---
title: Learning-test bundle evidence for the demo (issue 129)
description: Recorded 2026-11-18 run of the existing learning-test bundle suites with raw output retained, and a per-criterion proven or unproven result for the demo
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 129
  - learning-test bundles
  - non-AI comparator
---

## Scope and labels

Synthetic demo, desktop only. The criteria concern a protocol and a pure helper in `src/core`, so no Azure, browser or deployed-service action applies and none was taken. Every result below is a constructed-case unit test, not a measured experiment; saved minutes stay capacity until Finance validates them. The protocol is in [journey-learning-test-bundles.md](ux/journey-learning-test-bundles.md).

## Commands run (2026-11-18, local)

| Suite | Command (from the project folder) | Result | Raw output |
| --- | --- | --- | --- |
| src/core | `PYTHONPATH=src:tests python3 -m unittest -v tests.test_learning_test_bundles` | 26 tests OK, exit 0 | [core output](issue-129-live-learning-test-evidence-2026-11-18/core-learning-test-bundles.raw.txt) |
| src/api | `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest -v tests.test_learning_test_bundle_scenarios` | 6 tests OK, exit 0 | [api output](issue-129-live-learning-test-evidence-2026-11-18/api-learning-test-bundle-scenarios.raw.txt) |

The output files are unedited and contain no identifiers or credentials (checked for paths and addresses; none found).

## Per-criterion result

| Criterion | Result | Basis |
| --- | --- | --- |
| Bundles: story once, pre-visit pack, change impact and evidence reuse, accessible handover and aftercare, review-ready funding evidence | Proven as specified and scored for constructed cases, each with a non-AI comparator and a zero-measure stop rule. Observed, constructed; not a measured experiment | `test_ac1_bundles_each_have_a_non_ai_comparator_and_zero_measure`, `test_all_five_bundles_report_through_existing_scorer`, bundle 1 to 5 scenario tests |
| Opportunities O10 and O18 to O20 stay out of scope | Proven in code | `test_five_bundles_exclude_out_of_scope`, `test_governance_gate_excludes_out_of_scope_and_unapproved_runner_wiring` |
| Atlas owner confirms bundle to opportunity mapping | Unproven; cannot be proven for the demo | It is a named human owner decision. No confirmation is retained, and the O16 overlap question stays open. The tests enforce a single named O16 owner per run but cannot supply the confirmation |

Also unproven and out of this issue's tick list: running the bundles with real participants, and the ADR 0003 owner acceptance and DPO retention dependencies, which the owner decisions of 2026-11-18 exclude for the demo.
