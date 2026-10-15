---
title: Zava Forward orchestrator
description: Scheduled job documentation (ledger digest publish and verification) for the orchestrator project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

The orchestrator hosts the scheduled jobs: `zava_forward.orchestrator.token_store` and
`zava_forward.orchestrator.digest_blob`. Until the job image split in #200 (A4) the Container Apps jobs
still run in the [api](../api/README.md) image. Tests are in `src/orchestrator/tests/` and run with
`PYTHONPATH=../core/tests python3 -m unittest discover -s tests`. The section below is moved
unchanged from the former `mvp/README.md` (M6 of #199).

## Ledger digests

### Immutable Blob ledger digests and scheduled verification (issue #115)

* `python -m zava_forward.orchestrator.digest_blob [--publish]` uploads the head and sealed
  year digests to the `ledger-digests` container (create-only, managed identity
  via `ZF_DIGEST_ACCOUNT_URL`, `ZF_DIGEST_CONTAINER`, `ZF_DIGEST_CLIENT_ID`), then
  verifies the ledger against the digests read back from the container, not local
  files. A broken chain is never anchored. Any mismatch, empty container or
  unreachable container prints `LEDGER_DIGEST_ALERT` and exits 1.
* `infra/modules/storage.bicep` adds the container with a time-based retention
  policy (created unlocked); `containerapps.bicep` adds a daily
  `job-*-ledger-verify`; `main.bicep` adds a log alert on the marker to the
  action group. Tests: `tests/test_digest_blob.py` (in-memory immutable container
  fake over the labelled synthetic stock). A second alert,
  `alert-*-ledger-verify-missing`, fires when no `LEDGER_DIGEST_OK` line
  arrives within 26 hours, so a job that fails to start or run is caught as well
  as a mismatch.
* Trust-on-first-use gap: `--publish` seeds digests from the current ledger and
  verifies only the chain, so a ledger already tampered with before the first
  publish is anchored as genuine. Review the first publish by a second person
  against an independent record before relying on the digests.
* The retention period must be chosen by the owner (no shorter than the legal
  audit retention period) before the policy is locked; locking is irreversible.
* Open items, not invented here: the Log Analytics table names
  `ContainerAppConsoleLogs_CL` and column `ContainerJobName_s` are unconfirmed
  and must be checked in the deployed workspace; the legal retention period,
  the owner's irreversible policy lock and a deployed run also remain open.
