---
title: Issue 1259 local Azurite emulator validation plan
description: Prospective plan to validate the frozen Blob ranking archive adapter and path-health behaviour against a local Azurite emulator, with stop conditions
ms.date: 2026-11-09
---

## Scope

Validation only on frozen HEAD `7fc680d0eb565ef1a41e7d90fa48bcfb5aa8e69e` (tree `2884fc28...`). No source, test or product edit, no parent reset, no merge. Demo-targeted tier (owner, 2026-11-09): this is a local emulator check, not the full gate, not hosted CI. Refs #1259 only.

Research: [research record](../research/2026-11-09-ranking-archive-path-health-1259-emulator-research.md). Phase details: [details](../details/2026-11-09-ranking-archive-path-health-1259-emulator-details.md).

## Phases

* [ ] P1 Commit the research, plan, details and critique before executing (repo-local noreply author and committer, Copilot trailer).
* [ ] P2 Qualify source: `git status --ignored` clean; export `git archive HEAD src/core` into scratch; record per-file SHA-256 against `git ls-tree` blob ids; run adapter from the export with `python3 -S`.
* [ ] P3 Install `azurite` and `@azure/storage-blob` into scratch with `npm install --prefix`, only after the recorded missing-tool check. Record versions and exit codes.
* [ ] P4 Fixtures: owned CA and leaf certificate (SAN `zfemu1259.blob.localhost`), random account key, owned free ports; start Azurite (blob only, `--blobHost ::1`, `--cert/--key`, `--location` in scratch, `--skipApiVersionCheck` NOT used) and record its PID.
* [ ] P5 Admission probe (stop gate): construct the actual `BlobRankingArchive` from `open_ranking_archive` with the environment configuration and call `names()` against an emulator-created container with a SAS. If the adapter cannot reach the emulator without a source patch, a weakened TLS or auth check, or a host-rewriting transport, record the exact incompatibility, stop P6 and P7, keep the logs, and finish with the blocked verdict.
* [ ] P6 Adapter checks through the actual adapter on the synthetic fixture: valid-empty listing, conditional create, repeat create returning false and the first bytes retained, read bytes and metadata, listing, name refusal, then `publish` twice and `verify` through `ranking_publication` with the test-local signed synthetic registry.
* [ ] P7 Path-health and manual controls through the actual runner and `main --blob`: real CLI publish refuses with `approval_missing` and writes nothing; `schedule` and `verify` with SAS lacking list permission (403), absent container (404), wrong-signature SAS (403), and an unused owned port (refused) give unknown `due`, `archive_unreadable` on publish, zero PUT (counted from Azurite debug log and by listing afterwards), and no secret, account, host, container or SAS in the output.
* [ ] P8 Stop the specific Azurite PID, confirm the ports are free, retain logs; remove nothing else. Re-verify the worktree is clean and the source tree byte-identical.
* [ ] P9 Write changes and one original Review record, state JSON, commit the evidence records only (no logs, keys or certificates), write the handoff in the coordinator files directory.

## Stop and non-claims

* Stop P5 onwards on any incompatibility; report it exactly. No bare-client test is labelled adapter acceptance. No emulator-only fake success.
* Not producible against a real emulator (malformed XML, endless pagination, 5xx, multi-page): remain mocked parent evidence and are reported unperformed.
* Azurite is not real Azure, not WORM, not RBAC, not network behaviour, not Bicep or deployment proof, and does not satisfy the full gate, hosted CI, independent review or human approval.
* Do not push, open or edit a PR, change the board, deploy, close issues or touch the 1259 acceptance boxes.

## Success criteria

* Every command, exit code, input and source identity captured in an external scratch log directory.
* Source remains byte-identical to `7fc680d0`; worktree clean after the evidence commit except for the new records.
* Clear per-check outcomes: performed, blocked or unperformed, each with the reason.
