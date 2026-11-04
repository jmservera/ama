---
title: Issue 104 round 2 research
ms.date: 2026-11-04
---

Research disposition: reused (round 1 evidence re-verified on origin/main 844346329). Planning Readiness: Ready.

## Prior delivery checked

* Children: #105 and #106 closed; #107, #108, #432 and #435 open; #440 open.
* Merged and relevant: #913 (round 1 boundary test, Refs #104), #602 and later #432 metering work, #863, #405, #909. No open PR references #104.
* Round 1 research named one gap it left: the `read_document` path. `controlled()` in `test_ai_boundary.py` strips `documents[].summary`, but no test calls `Store.read_document`.

## Findings

* `Store.read_document` (src/core/src/zava_forward/core/store.py) writes only the model description to `document.summary` as a filing note and audits start and end. It extracts nothing into the case.
* Workflow-only mode (`mode="off"`) returns a template note and the same single write.

## Slice choice

Smallest coherent slice: one added test in `src/api/tests/test_ai_boundary.py` that reads an uploaded text document with hostile scripted output and with workflow-only mode, and asserts only `summary` changes. Test-only; no security, infrastructure, SQL or deployment surface; focused tier applies.

## Unmet after this slice

* All remaining epic criteria need human, Azure or owner decisions: stabilization checkpoint (#440 open), children #107, #108, #432, #435 closed or deferred, and the #432 tokenomics criteria (OD-51, price source, spend authority, Azure billing period). Cost stays Unknown.
* Criterion 3 (AI never approves, executes, ranks or mutates controlled records) is now proven for the JSON store on all retained paths including `read_document`. SQL store parity and the independent scan-pending and refusal cases are not covered here.
