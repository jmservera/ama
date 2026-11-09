---
title: Issue 1259 local Azurite emulator readiness research
description: Prospective research for a bounded local emulator validation of the frozen Blob ranking archive adapter and path-health behaviour (validation only, no source change)
ms.date: 2026-11-09
---

## Disposition

Research executed 2026-11-09 (rpi-agent, Sonnet 5.5). Planning Readiness: Ready for a bounded local emulator validation plan, with one admission question (account-name routing, below) that execution must answer first and stop on if unanswerable. Not a source-change, parent-reset or publication task. Refs #1259 only; nothing is closed.

## Frozen identities (read from the worktree)

* Worktree `/home/azureuser/source/ama-demo-wt/issue-1259-recovery`, branch `fix/ranking-archive-path-health`, clean including ignored files at start.
* HEAD `7fc680d0eb565ef1a41e7d90fa48bcfb5aa8e69e`, tree `2884fc2868668a8abf6221c197756bda8856de0b`, `src/core` tree `e1498c71d11ce345b6b9b1c7a3592db2b9172f43`, `src` tree `22b07eff706f61fa897304d9d129e07d621fec3d`.
* Frozen parent `52f9b61bb` (unmerged, merged as second parent of `d16b25c7b`); target is the 1258 topic, not main. Moving parent, main and siblings are not merged or consulted. Correction budget: contradiction flagged, not resolved. The parent c5 handoff records "1 of 5 used, four remaining"; this brief reads "Budget 1 of 5 productive remains 1". Either way this task makes no source correction, resets nothing and consumes none; the coordinator reconciles the count.

## What the adapter supports (read from source)

Source: `src/core/src/zava_forward/core/ranking_archive_blob.py`, `documents.py` (`AzureBlobDocumentStore`, `urllib_transport`), `ranking_publication.py`, `ranking_publication_runner.py`.

* Configuration (`open_ranking_archive`): `ZF_RANKING_ARCHIVE=azure-blob`, `ZF_BLOB_ACCOUNT_URL`, `ZF_RANKING_BLOB_CONTAINER`, then `ZF_BLOB_SAS` or the managed identity (`ZF_BLOB_CLIENT_ID` optional, `IDENTITY_ENDPOINT`/`IDENTITY_HEADER`). The constructor also accepts `transport` and `env`.
* TLS: `AzureBlobDocumentStore` refuses any URL whose scheme is not `https`. The default transport is `urllib.request.urlopen`, so certificate verification is the Python default and honours `SSL_CERT_FILE`. An owned CA fixture can therefore be trusted through the environment with no production change.
* URL shape: `self.base = https://{netloc}/{container}`. The path of `ZF_BLOB_ACCOUNT_URL` is discarded. Azurite's default path-style address (`https://127.0.0.1:10000/{account}/{container}`) therefore cannot be expressed. The account must travel in the host name (production style, `https://{account}.blob.{domain}:{port}/{container}`), which Azurite documents as supported for host names that resolve locally. The sandbox resolves `*.blob.localhost` to `::1` (read in the missing-tool log), so no hosts-file or resolver change is needed; the emulator must listen on `::1`.
* Auth: SAS is appended to every URL. The managed-identity path needs a token endpoint and, for Azurite, `--oauth basic` (token shape only; it does not prove Entra or RBAC). The SAS path signs with an account key and exercises Azurite's real signature and permission checks, so SAS is the admitted credential; the bearer path is recorded as unperformed with this reason.
* Operations: `create` (PUT BlockBlob with `If-None-Match: *` and `x-ms-meta-*`; 200/201 true, 412 or 409 BlobAlreadyExists false, 408/5xx uncertain), `read` (GET with metadata), `names` (List Blobs, prefix `ranking-`, marker paging up to 1000 pages, strict structure check). No delete, overwrite or caller-chosen location. The adapter sends no `maxresults`, so a multi-page listing needs more records than the emulator's page size (5000); that is not exercised.
* Behaviour above the adapter: `ranking_publication.publish` (single conditional create, read-back validation on exists) and `verify` (listing failure raises, metadata check per record); `ranking_publication_runner.run` and `main --blob` map an unreadable listing to `archive_unreadable` with unknown `due`/`next_window_start` and no write; the shipped policy is unsigned, so the real CLI refuses publish with `approval_missing`. The test file builds a signed synthetic registry (`signed_registry`) for publish; that helper may be imported read-only.

## Available tools (missing-tool check)

Recorded in the external scratch log `00-missing-tool-check.log` before any install: `azurite` and `azurite-blob` MISSING; no global npm Azurite; no Azurite Docker image; ports 10000-10002 and 8443 free; `node`, `npm`, `npx`, `openssl`, `curl`, `python3` 3.12.3 present; npm registry reachable. Docker images and caches are not touched.

Plan consequence: install `azurite` and `@azure/storage-blob` (SAS generation only) with `npm install --prefix` into the new issue-qualified scratch directory. No global install. Core has no Python dependencies (`dependencies = []`), so the adapter runs from a `git archive` export of the frozen commit with `python3 -S` (no site, hence no editable install pointing at another checkout) and `PYTHONDONTWRITEBYTECODE=1`.

## Admission question

Can the actual adapter reach Azurite using only existing configuration and injection? Hypothesis: yes, by account `zfemu1259` (owned name) and key generated in scratch, `ZF_BLOB_ACCOUNT_URL=https://zfemu1259.blob.localhost:<owned port>`, owned CA through `SSL_CERT_FILE`, and a container SAS. Unknown until run: whether the Azurite release accepts API version `2021-08-06` and routes the production-style host. If either fails, report the exact incompatibility and stop that check. Injecting a transport that rewrites the host would be a test-side change of what is being validated, so it is not used to rescue an incompatibility.

## Controls and what they can prove

Container creation and SAS issue are fixture setup done with the Azure SDK or curl and are labelled as setup, never as adapter acceptance. Adapter behaviours to observe on the emulator: conditional create, repeat idempotence with a retained first body, read-back bytes and metadata, listing, valid-empty listing (container exists, no `ranking-` record), publish and verify through the runner, and path-free failures from real emulator responses (SAS without list permission 403, absent container 404, wrong signature 403, connection refused on an unused owned port). Not producible against a real emulator without faking it: malformed listing bodies, endless pagination, 5xx. Those stay mocked-REST evidence from the parent suite and are named unperformed.

## Boundaries and non-claims

* Azurite is a local emulator. It is not a real Azure account, not WORM or immutability, not RBAC, not network ACL behaviour and not Bicep or deployment proof.
* No real account, credential, private data, model call, firewall or network-policy change. Synthetic public fixture only.
* Owned artefacts only: scratch `g1259-emulator-1109.P6T1sb`, ports and key generated per run, one service PID stopped afterwards.

## Open items

* PC-1 from the parent c5 task (first-`NextMarker` parsing) remains an owner choice; this task neither patches nor decides it.
* Hosted CI, independent review, human approval and the full gate are outside this task.
