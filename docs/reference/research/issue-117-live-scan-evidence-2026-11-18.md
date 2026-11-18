---
title: Issue 117 live scan evidence
description: Per-criterion proof for document malware scanning, retention and legal hold on the synthetic demo, with retained raw output
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, live Azure read-only plus one signed-in Playwright probe against `ca-cutover-test-demo-api`, 2026-11-18 about 12:50 UTC. Credentials were read from the owner's files at run time and never printed. The production-only retention lock is excluded. No source, Azure resource or setting changed. Refs #117.

Raw output is retained in [issue-117-raw](./issue-117-raw/). The probe script is `.copilot-tracking/evidence/2026-11-18/issue-117-live/probe.py`.

## Criterion result

| Criterion | Status | Basis |
| --- | --- | --- |
| Uploads are scanned before availability | Proven for the synthetic local scanner on the demo; unproven for a real malware engine | Offline and live evidence below. Defender for Storage is disabled live, so no real malware scan guards the blob store |
| Retention job lists records past trigger and needs owner approval; legal hold blocks deletion (ticked) | Not re-audited; live queue reachable | `/api/retention` returns 200 with keys `as_of`, `label`, `records` and the label "synthetic-demo placeholder period ... not an approved retention schedule". Offline tests pass |

## Evidence

| Observation | Result | Retained output |
| --- | --- | --- |
| Source order | `Store.add_document` stores the blob, calls `scan_new_document`, and appends the document record only afterwards; infected or mismatched content deletes the blob and raises, so no record exists. `require_clean` blocks reads until the scan is clean; a missing or pending scan is rescanned on first use or by the bounded job | source review |
| Offline tests | api `test_document_controls`: 18 tests OK. core `test_document_rescan` and `test_resident_documents`: 46 tests OK, 20 skipped | [api](./issue-117-raw/api-test_document_controls.txt), [core](./issue-117-raw/core-tests.txt) |
| Live scanner config | The demo API sets `ZF_DOC_STORE=azure-blob` and no `ZF_SCANNER`, so the code default `local` applies: the synthetic signature scanner, which logs that it gives no malware assurance on a blob store | [env names](./issue-117-raw/live-api-env-names.txt) |
| Live Defender for Storage | `isEnabled` false on `stcutovertestrzsrg` | [atp](./issue-117-raw/live-storage-atp.txt) |
| Blob protection | Versioning on; soft delete 30 days | [blob service](./issue-117-raw/live-blob-service.txt) |
| Live unsafe upload, synthetic marker (`.txt`) | HTTP 400 "That file failed the malware scan and was not kept." | [probe](./issue-117-raw/live-upload-probe.json) |
| Live unsafe upload, bytes not a PDF (`.pdf`) | HTTP 400 "That file failed the content check and was not kept." | [probe](./issue-117-raw/live-upload-probe.json) |
| Availability after refusal | The first case's document list was 5 before and 5 after (`documents_unchanged` true): neither refused file became a record | [probe](./issue-117-raw/live-upload-probe.json) |
| Unauthenticated access | `/api/cases` and `/api/retention` return 401 | [probe](./issue-117-raw/live-unauth-probe.txt) |

## Not proven

* A real malware engine: Defender for Storage is off and enabling it is a change outside the brief. The code supports `ZF_SCANNER=defender` (offline tests `test_defender_malicious_result_removes_the_document` and `test_pending_defender_scan_blocks_until_clean` pass), but that path is unexercised live.
* A clean upload becoming available live: it would leave a demo record and blob, so it was not run. The clean path is proven offline only (`test_clean_upload_is_available_and_scan_is_recorded`).
* No blob residue after refusal: the evidence container list was refused to this identity ([blob count](./issue-117-raw/live-blob-count.txt)). The record check shows no document, and the code deletes the blob before raising; the blob itself was not observed.
* Live legal hold and approved deletion: both change state and were not exercised.

## Adverse observations

* The live demo relies on a synthetic signature scanner, which catches only the test marker and type mismatches. The criterion text ("scanned before availability") holds for that scanner, not for real malware.
* Playwright's out-of-page POST returned an empty 403 at the Easy Auth edge, as in the #116 record; the successful probe used an in-page `fetch`. The first run (out-of-page POST) returned 403 and the second returned 400 "Enter the source reference" for missing provenance fields; only the third run reached the scanner. The first two outputs: Observed; raw output not retained.

## Follow-ups

* Enable Defender for Storage and set `ZF_SCANNER=defender` on the demo, then repeat the probe (needs cost approval; outside the demo brief).
* With owner agreement to a state change, upload one clean synthetic file and show availability, rescan and legal hold live.
