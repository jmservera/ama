---
title: "Issue 2303 chat golden file in the API image (2026-11-23)"
description: Reproduction and fix evidence for GET /api/ai/report returning 500 in the demo image, with a per-criterion proven/unproven table
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Refs #2303, #2301, #440, #100, #157. No Azure change was made.

## Cause

`chat_eval.GOLDEN` resolves from `ZF_CHAT_GOLDEN`, otherwise to `/usr/local/lib/python3.12/evals/chat_golden.json` in the installed image. The Dockerfile copied only `ai_priority_golden.json`, and both `src/.dockerignore` and `src/api/Dockerfile.dockerignore` excluded every other eval file, so a Dockerfile change alone would also fail the build.

## Reproduction and fix (local Docker, 2026-11-23)

| Check | Baseline image | Fixed image |
| --- | --- | --- |
| Files in `/app/evals` | `ai_priority_golden.json` | both golden files |
| `ZF_CHAT_GOLDEN` | unset | `/app/evals/chat_golden.json` |
| `chat_eval.run_eval()` | FileNotFoundError at `.../python3.12/evals/chat_golden.json` | `passed True` |

Live state read with `az containerapp show -g ama -n ca-cutover-test-demo-api`: revision 0000055, image digest `sha256:b628e067...`, still the pre-fix image.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| Regression test fails without the golden file or variable | Proven locally | `test_api_image_provides_every_runtime_golden_file` in `src/core/tests/test_cutover_audit.py`; removing the Dockerfile lines or the ignore line makes it fail |
| Dockerfile copies the file and sets `ZF_CHAT_GOLDEN` | Proven locally | rebuilt image table above |
| After deployment `/api/ai/report` is 200 and the Asset and board view loads | Unproven | needs an image build, registry push and a new revision; not done for a local candidate |
| Full tier, local gate and external receipt | Unproven here | applies; coordinator runs the gate and receipt |

Working record: `.copilot-tracking/changes/2026-11-23-issue-2303-changes.md`.
