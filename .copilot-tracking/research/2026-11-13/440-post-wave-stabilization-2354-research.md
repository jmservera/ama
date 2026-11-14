# Research: #440 post-wave stabilization checkpoint (2354)

Disposition: executed. Planning Readiness: Ready.

## Pins (read 2026-11-13)

* Branch `docs/demo-440-stabilization-checkpoint-2354`, HEAD `839774883641e54c33cc37a8f34df1bf08d51ffe` (merge of PR 1578), tree `ced1bfc08c1f0fe919902c543b022f35a2257ca3`.
* After `git fetch`, `origin/main` is `8924b501c6a24bacbf0f429b9e54f3e62fa5b223`; the diff to the source commit is only `.github/rubric/scores/latest.json`.
* Previous checkpoint: `34b11967b` (PR 1527), recorded in the cut-over evidence pack. The span holds 35 non-rubric commits.
* BRD 0.21.0 `draft`, PRD 0.21.0 `in-review`, ADR 0003 and 0006 Accepted, ADR 0007 Proposed; blobs unchanged.

## Wave (from `gh pr view`)

* 1571 for #228: procurement and contractor browser check with axe and keyboard cues.
* 1572 for #358: `test_setup_entra.py` expiry and Key Vault preservation tests.
* 1575 for #232: role-screen WCAG cues, unit tests and browser check.
* 1578 for #165: synthetic coverage status and PII guard with core tests.

## Contract

The checkpoint contract is the "Stabilization checkpoints" section of `.github/agents/ama-backlog-delivery-coordinator.agent.md` and the #440 issue acceptance criteria: pins, covered PRs, traceability, commands and exits with evidence classes, findings, and a continue, fix or pivot recommendation.

## Findings

* `test_synthetic_test_data_guard` and `test_web_shell` do not exist at this commit; nearest existing tests are substituted and the gap is recorded.
* A non-editable pip install breaks `ai_eval.GOLDEN` (resolved relative to the source tree), producing HTTP 500 on `/api/ai/report` in `test_role_endpoint_inventory`. `ZF_AI_GOLDEN` fixes it. Environmental, not a regression.
* Issues #228, #358, #232, #165, #155, #521, #203 and #440 are all OPEN; no closure is supported.
