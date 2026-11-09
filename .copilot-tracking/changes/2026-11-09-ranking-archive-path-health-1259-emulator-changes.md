---
title: Issue 1259 local Azurite emulator validation changes
description: Executed commands, outputs and observations for the local Azurite validation of the frozen Blob ranking archive adapter
ms.date: 2026-11-09
---

## Summary

No product, test or tooling file changed. The only repository changes are the RPI records for this task. Execution happened 2026-11-09 15:22 to 15:27 UTC in owned external scratch `/home/azureuser/.local/share/ama/gates/g1259-emulator-1109.P6T1sb` (`$S`); logs are in `$S/logs/` (SHA-256 manifest `$S/logs.sha256`, 29 files). Logs, keys, certificates and SAS values are not committed and are not quoted here.

Tier: owner-selected demo-targeted tier. This is a local emulator check. It is NOT real Azure, WORM, RBAC, network, Bicep or deployment proof, and not the full gate, hosted CI, independent review or human approval.

## Identities

* Frozen source `7fc680d0eb565ef1a41e7d90fa48bcfb5aa8e69e`, tree `2884fc2868668a8abf6221c197756bda8856de0b`, `src` tree `22b07eff706f61fa897304d9d129e07d621fec3d`, `src/core` tree `e1498c71d11ce345b6b9b1c7a3592db2b9172f43`. Prospective-record commit `4f76f7fa84fbb9547165ae5a1ed4edfb4305f52b` (records only; `git diff 7fc680d0e HEAD -- src tools infra` empty, log 19).
* Qualification: `git archive 7fc680d0e src/core` exported to `$S/export`; 285 of 285 files byte-identical to their git blobs before (log 03) and after (log 20) execution. The adapter ran from the export (`python3 -S`, `PYTHONDONTWRITEBYTECODE=1`, no site packages, so no editable install of another checkout); `adapter_file` in log 10 shows the export path.
* Emulator: `azurite@3.37.0` (API up to 2026-06-06), `@azure/storage-blob@12.31.0` for fixture setup only, both installed with `npm install --prefix` into `$S/node` after the missing-tool check (log 00: `azurite`, `azurite-blob` MISSING, no Docker image, ports free). No global install.

## Command log (exit codes)

| Log | Step | Exit |
| --- | --- | --- |
| 00 | Missing-tool check before any install | 0 |
| 01 to 03 | Source identity, export, byte compare (285 files) | 0, 0, 0 |
| 04, 05 | `npm install --prefix $S/node azurite @azure/storage-blob` and `npm ls` | 0, 0 |
| 04b | Setup-tool SDK pinned to `@azure/storage-blob@12.31.0` | 0 |
| 06 | Owned CA and leaf (SAN `zfemu1259.blob.localhost`), `openssl verify` | 0 |
| 07 | `azurite-blob --blobHost ::1` with owned cert/key, custom account and key, debug log; PID 2972196 | running |
| 08 | Setup with SDK 12.34.0: container creation | 1 (see Deviation) |
| 08b, 08c | Setup with SDK 12.31.0: containers `ranking-archive`, `ranking-empty`, SAS values | 0, 0 |
| 09, 09b, 09c | Setup-client blob counts before any write | 0 each (09: 400 before the SDK pin) |
| 10 | P5 admission probe through `open_ranking_archive` and `names()` | 0 |
| 11 | P6 adapter checks | 0 |
| 12 | Setup count after adapter checks | 0 |
| 13 | P7 CLI and runner controls | 0 |
| 14, 15, 16 | Counts, failure controls, counts after | 0, 0, 0 |
| 17 | Azurite debug-log operation tally | 0 |
| 18 | `kill 2972196` (exact PID) | 0 |
| 19, 20 | Post-run worktree and byte checks | 0, 0 |

## Deviation

Step 08 failed: the first SDK install (12.34.0) sends API version 2026-10-06, newer than Azurite 3.37.0's 2026-06-06 (HTTP 400 InvalidHeaderValue; log 08). It is a fixture-tool mismatch, not an adapter finding. The setup SDK was pinned to 12.31.0 (the repository's Python pin number) and setup rerun. The adapter sends `x-ms-version: 2021-08-06`, which Azurite accepted (log 10 onward). No `--skipApiVersionCheck`, no adapter edit.

## Admission (P5): admitted

The actual adapter reached the emulator with existing configuration only: `ZF_RANKING_ARCHIVE=azure-blob`, `ZF_BLOB_ACCOUNT_URL=https://zfemu1259.blob.localhost:<owned ::1 port>` (production-style host; the adapter drops the URL path, so the account must be in the host), `ZF_RANKING_BLOB_CONTAINER`, a container SAS, and the owned CA trusted through `SSL_CERT_FILE` for the process (certificate verification and https stay on; no transport injection). The readiness probe (curl, anonymous list) returned 403 with the owned CA, which indicates the TLS chain verified; its output was shown in the session only and is not a retained log. The adapter's own successful call (log 10) is the retained evidence. The first adapter call `names()` returned `[]` (log 10).

## Observations (adapter on the emulator; public synthetic fixture)

* Valid-empty listing: `names() == []` on an existing empty container (logs 10, 11); runner `schedule` shows `due: true`, count 0, no problems, status `due`; runner `verify` count 0, no problems, `overdue: true` (log 13).
* Conditional create: first `create` true; a repeat with different bytes returned false (log 11).
* Retained bytes and metadata: `read` returned the first bytes exactly (`equals_first` true, `equals_second` false); metadata keys `as_of`, `policy_version`, `published_on`, `record_sha256`, `snapshot_hash` round-tripped and matched `metadata_for`.
* Listing and get: `names()` returned the created record; `read` of an absent name raised path-free `BlobArchiveError` "read refused (HTTP 404)" with no secret, host or container text.
* Name guard: three invalid names raised `ValueError` before any request.
* `publish` twice: written true then written false with the same path; `verify` count 2, no problems, latest `2026-11-06`. Runner first-run publish on `ranking-empty` published, the repeat reported `already_published`, same run key, `verify` ok.
* Manual control: real CLI `publish --blob` with the shipped unsigned policy refused `approval_missing` (exit 2); `--exercise` wrote nothing (exit 0, written false); setup counts stayed 2 and 1 blobs (logs 13, 14, 16). The CLI schedule/verify results against records created with the test-local signed registry list "policy version or hash is not in the policy registry". That is expected, because those records belong to the synthetic signed policy and not to the shipped registry; it is not an adapter finding.
* Path-free failures (real emulator or real refused socket), each with schedule/verify `due`/`overdue` unknown (`null`), publish refused `archive_unreadable`, and zero writes: SAS without list permission, HTTP 403 text "listing refused (HTTP 403)"; tampered SAS signature, 403; absent container (SAS for `ranking-absent`), 404; unused owned port, "listing failed: storage unreachable". A scan of the outputs for account, host, container, port, key, SAS and `sig=` found no leak (`leaks: []`, log 15). Zero-write proof: setup-client counts before and after were identical (main 2, empty 1, absent container still 404, logs 14 and 16). Secondary: the Azurite debug tally shows 6 Upload requests, matching 3 created blobs plus 3 BlobAlreadyExists conflicts, none in the failure phase (log 17).

## Not producible or not performed

* Malformed listing bodies, endless pagination and 5xx cannot be induced on a faithful emulator without a fake; they remain the mocked-REST parent evidence only. Multi-page listing (needs more than the 5000-record page default, the adapter sends no `maxresults`) not exercised.
* Managed-identity bearer path not performed: Azurite basic OAuth validates token shape only and would not prove Entra or RBAC.
* Not performed: real Azure account, WORM or immutability, RBAC, network rules, container/role provisioning, Bicep, deployment, folder-record migration, concurrent writers, PC-1 duplicate-marker behaviour, hosted CI, full gate, independent review, human approval.

## Teardown

PID 2972196 stopped by `kill 2972196` (exit 0); Azurite logged "successfully closed"; no listener remained on the owned port; nothing else killed or pruned. `$S` retained (including data, keys and certificates, all expired by design in 2 days) for review. Worktree status clean (including ignored) after execution.

## Count discipline

No source correction and no parent reset in this task; no review-correction cycle consumed here. The 1-of-5 versus "four remaining" wording conflict stays with the coordinator.
