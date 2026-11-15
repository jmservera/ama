# Plan: #435 held-out batch live adapter preparation (1953)

Research: [research](../../research/2026-11-13/435-heldout-batch-execution-prep-1953-research.md). Details: [details](../../details/2026-11-13/435-heldout-batch-execution-prep-1953-details.md). Tier: Focused (agents code, no workflow, dependency, infra or deployment change; no live call made).

## Scope

* New `src/agents/src/zava_forward/agents/heldout_aoai.py`: opt-in Azure OpenAI chat-completions adapter returning the existing `Call` envelope.
* `heldout_batch.main`: new `--endpoint`, `--deployment`, `--model`, `--auth {az-cli,managed-identity}`; `--execute-live` builds the adapter only when all are given and the authorization validates; otherwise exit 2 as today. An injected `provider` still wins.
* New tests `tests/test_heldout_aoai.py` (mocked HTTP, subprocess and credential) and README update.
* Out of scope: any live call, proposals fixture (owner supplies frozen held-out proposals), pricing values, issue edits, push.

## Phases

* [x] 1 Research
* [ ] 2 Plan, details, independent critique (rubber-duck, once)
* [ ] 3 Implement adapter, CLI wiring, tests, README; run tests, ruff, mypy
* [ ] 4 Independent review (code-review, then code-review-security), commit locally without push

## Acceptance

* Dry-run unchanged and still offline. `--execute-live` without endpoint, deployment, model or valid authorization (<= USD 5.00) makes no network call and exits non-zero.
* Token never printed, stored in the report, or put in an exception message; no redirect following; no retries; each failure is an unmeasured envelope.
* Response model must start with the declared `--model`, else unmeasured.
* 100% line coverage of `heldout_aoai.py` with mocks; existing 40 tests still pass; ruff and mypy clean.
