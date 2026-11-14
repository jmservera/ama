---
title: Phase details, src cutover repoint contract (Refs #201)
ms.date: 2026-11-14
---

## Phase 1

Create `tools/test_src_cutover_repoint.py` (16 tests, PyYAML for workflows):

* Workflows: parse, zero retired `mvp/` or `prototype/` targets or `PYTHONPATH=mvp`, src-ci lint/type/test/image build from `src`, src-deploy matrix of four images with context `src`.
* Dockerfiles: COPY sources only from the five distributions, files exist under `src/`, wheels not PYTHONPATH.
* Infra: no retired runtime paths (cutover-proof files excluded), Bicep `loadJsonContent` targets resolve into `src/`, image guidance names `src/` Dockerfiles, README `az acr build ... src`.

## Phase 2

Run the focused-tier commands from the task.
