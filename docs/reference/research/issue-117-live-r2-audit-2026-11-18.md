---
title: Issue 117 live audit, second pass
description: Per-criterion proven and unproven audit of document malware scanning, retention and legal hold on the synthetic demo, correcting the earlier Defender reading
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Live Azure authorised by the owner (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). Credentials were read from the owner's files at run time and never printed. Refs #117. This pass builds on [the first live note](./issue-117-live-scan-evidence-2026-11-18.md) and corrects one of its readings. Raw output is in [issue-117-live-r2-raw](./issue-117-live-r2-raw/); the probe is `.copilot-tracking/evidence/2026-11-18/issue-117-live-r2/probe.py`.

## Criterion result

| Criterion | Status | Basis |
| --- | --- | --- |
| Uploads are scanned before availability | Proven for the synthetic local scanner on the live demo and offline for the Defender tag path. Unproven for a real malware engine guarding the app | Table below |
| Retention job lists records past trigger and needs owner approval; legal hold blocks deletion (ticked) | Not re-audited. `/api/retention` returned 200 with keys `as_of`, `label`, `records` and the synthetic placeholder label; offline tests pass | [probe](./issue-117-live-r2-raw/live-upload-probe.json) |

## Evidence

| Observation | Result | Output |
| --- | --- | --- |
| Source order | `Store.add_document` calls `docstore.put`, then `scan_new_document`, and appends the record only afterwards. An infected or mismatched verdict deletes the blob and raises, and the error handler deletes the blob if no record exists. `require_clean` blocks reads until the scan is clean | `src/core/.../store.py:1709`, `doc_controls.py:216`; [grep](./issue-117-live-r2-raw/source-order-grep.txt) |
| Offline tests | api `test_document_controls`: 18 tests OK. core `test_document_rescan` and `test_resident_documents`: 46 tests OK, 20 skipped. They include clean upload available, Defender malicious result removes the document, pending Defender scan blocks | [api](./issue-117-live-r2-raw/api-test_document_controls.txt), [core](./issue-117-live-r2-raw/core-tests.txt), [names](./issue-117-live-r2-raw/api-test-names.txt) |
| Live unsafe upload, synthetic marker (`.txt`) | HTTP 400 "That file failed the malware scan and was not kept." | [probe](./issue-117-live-r2-raw/live-upload-probe.json) |
| Live unsafe upload, non-PDF bytes (`.pdf`) | HTTP 400 "That file failed the content check and was not kept." | same |
| Availability after refusal | Document list 5 before and 5 after (`documents_unchanged` true) | same |
| App scanner in use | Env names show `ZF_DOC_STORE` and no `ZF_SCANNER`, so the code default `local` (synthetic signature scanner) applies | [env names](./issue-117-live-r2-raw/live-api-env-names.txt) |
| Defender for Storage on the demo account | Corrected reading: `defenderForStorageSettings/current` on `<demo-storage-account>` reports `isEnabled` true, malware scanning on upload enabled (cap 10000 GB per month), sensitive data discovery enabled, `overrideSubscriptionLevelSettings` false. The earlier note reported `false` from the older advanced threat protection setting, which is a different resource | [settings](./issue-117-live-r2-raw/live-defender-storage-full.txt) |
| Blob protection | Versioning on; soft delete 30 days | [blob service](./issue-117-live-r2-raw/live-blob-service.txt) |

## Not proven, with reasons

* A real malware engine guarding uploads through the app. Defender scans the storage account, but the app does not read its verdicts: `ZF_SCANNER=defender` is not set, so a change to the demo API environment would be needed. That is a configuration change to a running demo app; this pass treated it as outside "no production changes" and left it.
* Defender scanning a blob live. The demo account's firewall default action is `Deny` with no IP rule, so this identity cannot upload. A throwaway account in `ama` was tried instead: shared-key upload is blocked by policy and enabling malware scanning on it failed with `MissingPermissions` on `Microsoft.Security/datascanners/write`. No blob was uploaded and the account was deleted (0 left; observed, raw listing output not retained); see the [note](./issue-117-live-r2-raw/throwaway-account-log.txt).
* A clean upload becoming available live: it would leave a demo record that only the owner-approved retention flow removes. Proven offline only.
* Live legal hold and approved deletion: both change state; not exercised.
* No blob residue after refusal: the evidence container is not listable from this identity. The record check shows no document.

## Production-only (excluded from the demo)

* Approved retention periods set by DPO and Legal (PR-003, OD-14); the demo uses labelled placeholders.
* Immutability or retention lock on production storage.

## Follow-ups

* Owner approval to set `ZF_SCANNER=defender` on `ca-cutover-test-demo-api`, then one clean and one EICAR upload through the app to prove the tag reader live.
* A principal with `Microsoft.Security/datascanners/write` if a throwaway scan test is wanted.
