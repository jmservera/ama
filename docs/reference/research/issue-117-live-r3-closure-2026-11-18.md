---
title: Issue 117 live closure re-verification, third pass
description: Per-criterion proven and unproven table for document malware scanning, retention and legal hold on the synthetic demo, after the second pass and merged evidence
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Live Azure was authorised by the owner (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). Credentials were read at run time and never printed. Refs #117. This pass re-runs the checks in the [second audit](./issue-117-live-r2-audit-2026-11-18.md); raw output is in [issue-117-live-r3-raw](./issue-117-live-r3-raw/) and the probe is `.copilot-tracking/evidence/2026-11-18/issue-117-live-r3/probe.py`. No source file changed and no Azure resource was created or modified.

## Criterion result

| Criterion | Status | Basis |
| --- | --- | --- |
| Uploads are scanned before availability | Proven for the synthetic local scanner on the live demo (two refusals, no document kept) and offline for the Defender verdict path. Not proven for a real malware engine guarding the app path | Evidence table below |
| Retention job lists records past trigger and needs owner approval; legal hold blocks deletion (ticked) | Not re-opened. `/api/retention` again returned 200 with `as_of`, `label`, `records` and the synthetic placeholder label | [probe](./issue-117-live-r3-raw/live-upload-probe.json) |

The unticked criterion stays unticked: its wording does not say which engine, but a scan that only the synthetic signature scanner performs gives no malware assurance, and the code itself logs that warning for an Azure Blob store.

## Evidence

| Observation | Result | Output |
| --- | --- | --- |
| Source order | `Store.add_document` (`store.py:1709`) stores the blob, calls `scan_new_document` (`store.py:1732`) and appends the record only afterwards; `require_clean` gates reads (`store.py:1805`, `1870`) | [grep](./issue-117-live-r3-raw/source-order-grep.txt) |
| Offline tests | api `tests.test_document_controls`: 18 tests OK. core `test_document_rescan` and `test_resident_documents`: 46 tests OK, 20 skipped | [api](./issue-117-live-r3-raw/api-test_document_controls.txt), [core](./issue-117-live-r3-raw/core-tests.txt) |
| Live unsafe upload, synthetic marker (`.txt`) | HTTP 400 "That file failed the malware scan and was not kept." | [probe](./issue-117-live-r3-raw/live-upload-probe.json) |
| Live unsafe upload, non-PDF bytes (`.pdf`) | HTTP 400 "That file failed the content check and was not kept." | same |
| Availability after refusal | Document list 5 before and 5 after on the first case (`documents_unchanged` true), signed in as a Retrofit Programme Manager | same |
| Scanner in use | Env names include `ZF_DOC_STORE` and no `ZF_SCANNER`; the code default is `local` | [env names](./issue-117-live-r3-raw/live-api-env-names.txt), `doc_controls.py:102` |
| Defender for Storage | On the demo account `isEnabled` true, malware scanning on upload enabled (cap 10000 GB per month), sensitive data discovery enabled, no subscription override | [settings](./issue-117-live-r3-raw/live-defender-storage.txt) |
| Blob protection | Versioning on; soft delete 30 days | [blob service](./issue-117-live-r3-raw/live-blob-service.txt) |

## Why the real-engine path is not proven for the demo

* The app reads Defender verdicts only with `ZF_SCANNER=defender`. Setting it means changing the environment of the running demo API (`ca-cutover-test-demo-api`), which a new revision would roll out. The owner authorised no production changes and named no demo-configuration change, so this pass did not make it.
* The demo storage account's firewall default action is `Deny`, so this identity cannot upload a test blob (second pass observation, account list re-read: default action `Deny`). The EICAR path through Defender therefore cannot be driven from outside the app.
* The second pass already showed a throwaway account cannot enable malware scanning with this identity (`MissingPermissions` on `Microsoft.Security/datascanners/write`). That was not repeated.
* A clean upload becoming available live would leave a demo record that only the owner-approved retention flow removes; it stays proven offline only.

## Production-only (excluded from the demo)

* Approved retention periods from the DPO and Legal (PR-003, OD-14).
* Immutability or retention lock on production storage.

## Follow-up

* Owner approval to set `ZF_SCANNER=defender` on `ca-cutover-test-demo-api`, then one clean and one EICAR upload through the app, and removal of the clean record through the approved retention flow.
