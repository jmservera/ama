# Research: issue 2303 image lacks chat golden file (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

## Findings

* `src/agents/src/zava_forward/agents/chat_eval.py` resolves `GOLDEN` from `ZF_CHAT_GOLDEN`, else `parents[3]/evals/chat_golden.json`. Installed in site-packages that resolves to `/usr/local/lib/python3.12/evals/chat_golden.json`.
* `src/api/Dockerfile` copies only `ai_priority_golden.json` and sets only `ZF_AI_GOLDEN`.
* Second cause not named in the issue: both `src/api/Dockerfile.dockerignore` (used by BuildKit for `-f src/api/Dockerfile`) and `src/.dockerignore` allow only `agents/evals/ai_priority_golden.json`, so a `COPY` of the chat golden would fail with "not found" unless both allow lists change.
* Existing contract test `src/core/tests/test_cutover_audit.py::test_api_runtime_golden_is_the_only_eval_context_exception` pins `src/.dockerignore` to exactly one golden; it must be updated.
* No test reads `src/api/Dockerfile` or `Dockerfile.dockerignore`.

## Local reproduction (baseline image, built from this worktree HEAD)

* `docker build -f src/api/Dockerfile src` gave image `zf-2303-before`.
* `docker run zf-2303-before ls /app/evals` printed only `ai_priority_golden.json`.
* `docker run zf-2303-before python -c "from zava_forward.agents import chat_eval; chat_eval.run_eval()"` raised `FileNotFoundError: ... /usr/local/lib/python3.12/evals/chat_golden.json` (pathlib open), the same exception class and site as the production log.

## Live state (read-only, 2026-11-23 ~14:46 UTC)

`az containerapp show -g ama -n ca-cutover-test-demo-api`: latest revision `ca-cutover-test-demo-api--0000055`, image digest `sha256:b628e067...`, i.e. still the pre-fix image. No Azure change was made.

## Acceptance criteria evidence plan

| Criterion | Status after research |
| --- | --- |
| 1 Regression test fails without the golden file/env var | To implement: Dockerfile contract test |
| 2 Dockerfile copies chat golden and sets ZF_CHAT_GOLDEN | To implement; verify with a rebuilt image |
| 3 After deployment `/api/ai/report` is 200 on the demo | Not provable by a local candidate: needs an image build, registry push and revision update (shared-system change owned by the coordinator). Local container proof substitutes only for the image-content half |
| 4 Full tier, local gate and external receipt | Applies (src and Dockerfile change). Worker never runs `rpi-checks.py --all`; the coordinator runs the gate and receipt |
