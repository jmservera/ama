---
title: Issue 1259 local Azurite emulator validation details
description: Phase details, commands and observation rules for the Azurite validation of the frozen Blob ranking archive adapter
ms.date: 2026-11-09
---

## Conventions

* Scratch `S=/home/azureuser/.local/share/ama/gates/g1259-emulator-1109.P6T1sb` (created by `mktemp -d`, owned, issue-qualified). Logs in `$S/logs/`, exports in `$S/export/`, fixtures in `$S/pki/` and `$S/azurite-data/`. Nothing in the worktree is written; the repository only receives these records.
* Each step is run through a small wrapper that appends the command line, start time, exit code and output to a numbered log. Secrets (account key, SAS) are generated per run in scratch, never printed to the repository records and never committed; logs that contain them stay external.
* Source identity per phase: `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, `git status --short --ignored`, and SHA-256 of every exported file against its git blob.

## P2 Source qualification

1. `git status --short --ignored` must be empty.
2. `git archive --format=tar HEAD src/core | tar -x -C $S/export`.
3. For each tracked file under `src/core` compare `git hash-object` of the export with `git ls-tree -r HEAD` ids; any difference stops the task.
4. Run Python as `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$S/export/src/core/src:$S/export/src/core/tests python3 -S ...` and print `zava_forward.core.__file__` to prove which source ran.

## P3 Tool install

`npm install --prefix $S/node --no-audit --no-fund azurite @azure/storage-blob` after the logged missing-tool check. Record `npm ls`, versions and exit code. No global change.

## P4 Fixtures and service

* `openssl` owned CA, then leaf with SAN `DNS:zfemu1259.blob.localhost`; trust through `SSL_CERT_FILE=$S/pki/ca.pem` only for the adapter process.
* Account `zfemu1259` with a random 64-byte base64 key via `AZURITE_ACCOUNTS`. Ports chosen free and recorded.
* Start: `azurite-blob --blobHost ::1 --blobPort <port> --location $S/azurite-data --cert --key --debug $S/logs/azurite-debug.log --silent` in the background; record PID; readiness by an HTTPS request with the CA (setup probe, labelled as such).
* Setup only (labelled fixture setup, not adapter acceptance): create container `ranking-archive` and issue container SAS values with the SDK: full (`rwcl`, no delete), no-list (`rwc`), wrong-signature (valid shape, altered signature).

## P5 Admission

Environment: `ZF_RANKING_ARCHIVE=azure-blob`, `ZF_BLOB_ACCOUNT_URL=https://zfemu1259.blob.localhost:<port>`, `ZF_RANKING_BLOB_CONTAINER=ranking-archive`, `ZF_BLOB_SAS=<full SAS>`. Call `open_ranking_archive(os.environ)` then `names()`. Expected `[]` (valid empty). Any exception is recorded with its type and text; a refusal for API version, host routing or certificate stops the task with the exact incompatibility.

## P6 Adapter checks (public synthetic fixture)

Use `dataset.case` via the test helpers `open_cases` and `signed_registry` (read-only import). Checks: names empty; `create(name, bytes, meta)` true; repeat with different bytes false; `read` returns the first bytes and `x-ms-meta-*` keys intact; `names` lists it; `create` with a bad name raises `ValueError` before any request; `publish` twice (written then already published), `verify` ok with count 1; Azurite debug log and a container listing confirm exactly one blob and no overwrite. Observations record headers/status only as seen through the adapter results and the Azurite debug log.

## P7 Path-health and manual controls

* Real `main` CLI with `--blob` and the shipped unsigned policy: `publish` exit 2 `approval_missing`, `--exercise` writes nothing.
* With the full SAS: `schedule` and `verify` on the valid-empty container: `due` true, not unknown.
* With the no-list SAS, an absent container name, a wrong-signature SAS and a refused port: `schedule`/`verify` report `overdue`/`due` unknown, `publish` (signed synthetic registry through `runner.run`) returns `archive_unreadable`, zero PUT (primary proof: setup-client container listing shows the blob count unchanged after the failure; secondary: Azurite debug log PUT count, reported only if the log format is readable), and the serialized output is scanned for account, host, container, SAS, key and URL strings (must be absent).

## P8 Teardown

`kill <exact PID>`; confirm the port is free with `ss -ltn`; keep `$S`; remove nothing else; re-run `git status --short --ignored` and the byte comparison.

## Observation record format

Each step: command, exit code, input identity, result, classification (adapter / setup / not producible), and whether it supports a stated claim. Mocked-REST parent results are not restated as emulator results.
