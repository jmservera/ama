---
title: Zava Forward orchestrator
description: Scheduled job documentation (ledger digest publish and verification) for the orchestrator project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-16
ms.topic: reference
---

The orchestrator hosts the scheduled jobs: `zava_forward.orchestrator.token_store` and
`zava_forward.orchestrator.digest_blob`. Bicep selects `orchestratorImage` for
both jobs (#200); the [api](../api/README.md) image no longer packages them.
Token maintenance retains its own identity and ledger verification retains the
API identity/grants. This image change grants no new permissions. Build from the
repository root with `docker build -f src/orchestrator/Dockerfile -t zava-forward-orchestrator:local src`;
pass the versioned registry tag as `orchestratorImage` with the matching API tag.
New-tag deployment and healthy job executions remain cut-over evidence, not
established by changing the template. Tests are in `src/orchestrator/tests/` and run with
`PYTHONPATH=../core/tests python3 -m unittest discover -s tests`. The section below is moved
unchanged from the former `mvp/README.md` (M6 of #199).

## Offline source change job (#213)

`python -m zava_forward.orchestrator.source_monitor` runs a bounded local
observation page against the existing law store. It adds no network adapter,
hosted timer or approval command. Existing token/digest schedules and
infrastructure are unchanged. The job can compare and flag only; Legal,
Compliance and DPO exercise decisions remain with Juan Manuel Servera.
See the [core contract and acceptance audit](../core/README.md#source-change-monitoring-and-review-213).

An exercise operator must first seed the law store from public snapshots and
configure each source through the trusted `SourceMonitor.configure` interface.
Do not use private working data. For example, a local fixture file can contain:

```json
{
  "synthetic-monitor": {
    "content": "# Synthetic exercise\nConstructed text, not law.\n",
    "metadata": {
      "effective": "2026-10-18",
      "complete": true
    },
    "provenance": "SYNTHETIC local publication fixture, not official retrieval",
    "method": "local-fixture"
  }
}
```

The example ID requires an explicitly constructed exercise source, not an
invented entry in the official register. `complete: true` is discovery
metadata, never verification or approval. Omit content and supply `error`
for a failed retrieval. The job never loads a URL or a supplied content path.
The supplied file is explicit, local JSON; no environment file is loaded.

```bash
ZF_LAW_DB=/absolute/exercise/law.sqlite \
ZF_LAW_BLOBS=/absolute/exercise/law-blobs \
  /tmp/zf164/bin/python -m zava_forward.orchestrator.source_monitor \
  /absolute/exercise/observations.json --today 2026-10-16 --limit 100
```

Each configured source uses its own day cadence. Sources checked too recently
are skipped; failed attempts also count for cadence, with failures retained
for the owner. A due source with no observation becomes an explicit failure
review item. Output lists `checked`, `skipped`, `changes`, `failures` and
`next_after`; failures exit 1. Repeat with `--after <next_after>` until null
to cover subsequent pages, and start again from the beginning on the next
sweep. Limits must be 1..100. Dates are explicit exercise clock inputs, not
claims of real official retrieval. New configuration revisions invalidate
earlier release evidence and require a fresh observation/review.

Candidate observations stay outside the law-store index. Every discovered
change remains unverified until the named owner reviews provenance and
completeness. The job cannot interpret law, approve a card, activate a rule,
release a hold or send a staff/resident communication. No endpoint was added.
Live metadata/legislation/feed adapters, hosted scheduling and missing-run
alerts require later delivery and authorization; this recipe is not a
production monitoring claim.

Run from `src/orchestrator`, with installed editable local distributions:

```bash
PYTHONPATH="$PWD/../core/tests" /tmp/zf164/bin/python -m unittest discover -s tests -q
/tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && /tmp/zf164/bin/mypy
```

Tests use local synthetic fixtures only, including nonzero CLI failures and
persisted review items; they do not scrape or read private datasets.

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
