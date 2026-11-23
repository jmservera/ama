---
title: Issue 2303 live check, GET /api/ai/report on the demo (2026-11-23)
description: Evidence for each unticked acceptance criterion of issue 2303, taken against the demo API on 2026-11-23
ms.date: 2026-11-23
---

## Scope

Synthetic demo, desktop only. Read-only checks on `ca-cutover-test-demo-api` (resource group `ama`). No Azure resource was created, changed or deleted. Credentials were read at runtime by the probe and never printed.

## Findings

* The repository head already holds the fix: `src/api/Dockerfile` copies `agents/evals/chat_golden.json` and sets `ZF_CHAT_GOLDEN`; both `.dockerignore` files allow the file; `src/core/tests/test_cutover_audit.py::test_api_image_provides_every_runtime_golden_file` pins the contract. `python3 -m unittest tests.test_cutover_audit` in `src/core` ran 10 tests, OK, on 2026-11-23.
* The live app runs revision `ca-cutover-test-demo-api--0000057` (created 2026-11-23T17:34:20Z), image digest `sha256:94526f21...`.
* [probe_ai_report.py](probe_ai_report.py) signed in as a Retrofit Programme Manager and called `GET /api/ai/report`: HTTP 500. Result in [probe-result.json](probe-result.json), screenshot in [screens/asset-board-live.png](screens/asset-board-live.png).
* Container log at 2026-11-23T18:42:02Z: `http-error GET /api/ai/report status=500 exc=FileNotFoundError at=pathlib.py:1013:open`. This is the failure in the issue, so the running image still lacks the chat golden file.
* The Asset and board screen rendered no loaded AI report (the probe found neither "Loaded" nor the not-loaded notice in the captured text, which showed the case list; the screenshot is the record).
* Registry access from this host is refused (`az acr repository show-manifests` returned connectivity forbidden), so the image build commit could not be read.

## Per-criterion result

| Criterion | Result | Basis |
| --- | --- | --- |
| 1 Regression test fails when the image lacks the golden file or variable | Proven (delivered at head) | contract test above; earlier mutation runs recorded in the changes record |
| 2 Dockerfile copies the chat golden and sets `ZF_CHAT_GOLDEN` | Proven (delivered at head) | `src/api/Dockerfile` lines 30 and 34 |
| 3 After deployment `GET /api/ai/report` is 200 and the view shows a loaded report | Unproven, disproved for revision 0000057 | live 500 with the same `FileNotFoundError`; a new image build, push and revision is a production change the owner has not authorised |
| 4 Full tier gate and external receipt | Unproven here | the coordinator runs the gate; `rpi-checks.py --all` is not permitted for this worker |
