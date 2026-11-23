---
applyTo: ".copilot-tracking/changes/2026-11-23-issue-2313-whatif-upload-contract-changes.md"
---
# Plan: what-if upload contract test (Refs #2313)

* Add `InfraPlanWorkflowContractTests` to `infra/tests/test_infra_image_build.py`: the what-if job needs `changes`, runs only when `infra == 'true'`, uploads `what-if-summary.json` with a pinned `upload-artifact`, `if-no-files-found: error`, `if: !cancelled()`; only that job holds `id-token: write`; no apply, deploy, push or secrets step.
* Tier: FULL is not triggered (test only, no src, no workflow edit); focused tier.
* Validate: run the new tests; ruff check and format; mutation check by temporarily asserting on a modified document in-test.
