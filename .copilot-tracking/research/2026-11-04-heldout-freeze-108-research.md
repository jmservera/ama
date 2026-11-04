# Research: issue 108 held-out freeze slice (2026-11-04)

Task: 108-heldout-freeze. Planning Readiness: Ready. Disposition: executed (issue, merged PR and source review).

## Already delivered (merged)

* #258 and #405: offline harness, critical-miss failure, per-run model/prompt/latency/reviewer evidence.
* #909: candidate_comparison (cost per accepted proposal with dated price or Unknown, tokens and spread, one lever, cheaper-but-worse is failure).
* #636, #821, #939: cohort record, approval bound to manifest digest, per-cohort report.
* #223 and #817: human-review protocol and manual session intake.

## Unmet criteria

Regional model/version/quota; frozen held-out split and thresholds (C5); five-assistant coverage (C6); subgroup and coverage record on real data (C7); human detection trials (C8); Finance-validated effort comparison (C9); actual-serving evidence bundle (C10); finite call authorization and participant consent (C11); real AI/SQL/Azure proof (C13); held-out cheaper-failure and one-lever measurement (C15, C16).

## Gap found

No code checks that a freeze manifest is complete before evaluation (versions, independent labeller, split seed, denominators, prompt/tuning leakage, cohort sample, bound threshold approval). That is an engineering precondition of C5 and C10 that needs no live model, human or Azure.

## Chosen slice

Pure offline `heldout_freeze.check_freeze` in src/agents. Later slices (stacked): wire it into the AI evaluation report; five-assistant coverage matrix.
