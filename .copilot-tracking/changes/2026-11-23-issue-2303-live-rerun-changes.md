---
title: Issue 2303 live rerun artifacts (2026-11-23, session rpi-2303-live)
---

# Research (executed, Ready)

Head already holds the fix and its contract test (see the research note [issue-2303-live-2026-11-23](../../docs/reference/research/issue-2303-live-2026-11-23/README.md)). Open question: does the live demo serve `/api/ai/report` with 200? Probe found 500 on revision 0000057 with the same FileNotFoundError.

# Critique (executed once, accept)

* No source change is needed; adding a handler fallback would change `src` and force the Full tier for no demo value, and criterion 2 is already met by the Dockerfile route.
* Deploying a new image is a production change, not authorised, so criterion 3 stays unproven.

# Plan

1. Probe live read-only. 2. Record evidence in a research note. 3. Update changes, review, state and log; commit without pushing.

# Changes

Files: the research note and probe under `docs/reference/research/issue-2303-live-2026-11-23/`, this record, log and index entries. No `src` edit; the fix and the test were delivered earlier at head and `python3 -m unittest tests.test_cutover_audit` (src/core) passed 10 tests on 2026-11-23.

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1 Regression test fails without the golden file or variable | Proven (at head) | `test_api_image_provides_every_runtime_golden_file` |
| 2 Dockerfile copies chat golden and sets `ZF_CHAT_GOLDEN` | Proven (at head) | `src/api/Dockerfile` lines 30, 34 |
| 3 Live `/api/ai/report` 200 and loaded view | Unproven; live 500 on revision 0000057 | probe-result.json, container log 18:42:02Z |
| 4 Full tier gate and external receipt | Unproven | coordinator owns the gate |

# Review (executed once, conformant)

Evidence matches claims: criterion 3 is stated disproved for the running revision, not proven. No open material findings. Routed follow-ups: build, push and deploy an image from head, then re-run the probe; run the Full gate.
