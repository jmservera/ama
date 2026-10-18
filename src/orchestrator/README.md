---
title: Zava Forward orchestrator
description: Scheduled job documentation (ledger digest publish and verification) for the orchestrator project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-18
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

Each configured source uses its own day cadence, measured from its last
successful retrieval. Sources successfully checked too recently are skipped;
failed attempts retain evidence for the owner but do not reset cadence.
A due source remains eligible on the next run, including the next day, until
a retrieval succeeds. Sources with no successful observation are always due.
A due source with no observation becomes an explicit failure
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

## Bounded document rescan job (#117)

Original Review status (2026-10-17): Complete / Not accepted, retained unchanged.
Coordinator-authorized correction ONE implements both Medium findings:
worker-owned SQL recovery prevents the nested diagnostic traceback, and closed
scanner-result validation plus explicit TypeError boundaries preserve controlled
reporting. Failing-first tests reproduced both defects before the changes.
Correction validation (2026-10-18) passed all 19 actual SQL worker tests plus 11
progress/resident recovery guards, full CLI root-stream checks and hardened
installed-image failures/successes. This is targeted implementation evidence,
not a second Review or independent coordinator acceptance. PR #395 stays draft.

`python -m zava_forward.orchestrator.document_rescan` consumes one bounded
SQL page through the existing scan service. It adds no daemon, Azure schedule
resource, network adapter, retention action or human approval. Existing token/
digest jobs and their identities/grants are unchanged.

Configure `ZF_DATA` explicitly and select `ZF_STORE=sqlite|mssql` and
`ZF_SCANNER=defender|local`. JSON and implicit scanner selection are refused.
Defender requires the existing `ZF_DOC_STORE=azure-blob` configuration; its
real account enablement and tag verification are still unmet. Local scanning
requires `--synthetic-local` and is only a labelled type/signature fixture,
not antivirus. No environment file or default private dataset is loaded.

For an explicitly constructed local exercise fixture with matching stored
document bytes, run from the repository root after pip installation:

```bash
ZF_DATA=/absolute/synthetic/seed.json \
ZF_STORE=sqlite ZF_SQLITE=/absolute/synthetic/cases.sqlite \
ZF_SCANNER=local ZF_DOC_STORE=local \
  .venv/bin/python -m zava_forward.orchestrator.document_rescan \
  --synthetic-local --limit 100
```

`--limit` is an integer from 1 to 100, default 100. Output includes `checked`,
`clean`, `pending`, `blocked`, `skipped`, `failed`, `committed`, scanner label
and `next_after`. If continuation is `["CASE", "DOC"]`, invoke the next page
with `--after CASE DOC`, using the same configuration. The exclusive composite
key advances even if a competing writer resolves a selected record. Continue
through all pages, even when earlier documents remain pending. Start every
new sweep without `--after`; pending or failed earlier pages need that next
sweep. There is no internal infinite retry or elected scheduling owner.

Exit precedence: 1 means failed attempts or committed-outcome reconciliation;
otherwise 2 means pending results or more pages; otherwise 0 means this page
settled. Terminal exit0 does not certify an earlier page or real malware
protection. Inspect the entire sweep. `committed` means the write succeeded
but acknowledgement/refresh failed: reload the persisted scan/audit before
retrying. Diagnostics use fixed markers, not filenames, bytes or private
scanner/transport exception text. Connections close on success and construction
failure. Attempt count is bounded, not end-to-end service latency.

The worker records infected/mismatched results as unavailable and retains
bytes, case hold and owner decisions. It cannot approve retention deletion,
release a hold or impersonate registered staff. Only exact clean becomes
available. The existing manual scan behavior remains separate; the worker
never calls its destructive bad-verdict path. Existing owner-approved deletion
and hold override are not replaced by this job.

From `src/orchestrator`, `PYTHONPATH=../core/tests ../../.venv/bin/python -m
unittest discover -s tests -q` includes actual subprocess SQLite CLI tests.
From the repository root, `PYTHONPATH=src/core/tests .venv/bin/python -m
unittest test_document_rescan -q` covers fair pages, exact 100-attempt bound,
pending/unavailable/unknown results, non-deleting quarantine, independent
connections, CAS retry, prior audit preservation and committed refresh.
`ZF_DOCUMENT_RESCAN_MSSQL=1` enables the same core tests on task-owned loopback
SQL Server with existing `ZF_SQL_*`; they reject other hosts and create/drop
only UUID-named `zf_rescan117_*` test databases. Never point them at live/shared
SQL. Docker uses the existing build context and hardening commands above;
actual image job checks must supplement ordinary version-only startup.

Correction ONE rebuilt `zf-issue117-orchestrator:correction1` with the existing
Dockerfile/context. All four installed runtime source hashes matched. With
UID10001, network disabled, read-only root, all capabilities dropped and
NoNewPrivs, six injected malformed/unknown/TypeError/outage runs returned exit1,
failed1/clean0, no private diagnostics or traceback, and no state/audit success.
Subsequent real module pages returned exit2/0/0 and clean1/2/0, exactly three
persisted success events with intact bytes, hold and ledger. Actual loopback
MSSQL main also exercised seven malformed/error cases and the original
competing-clean/recovery-failure reproduction. Owned SQL was stopped/removed.
These offline receipts do not enable Defender, approve retention or deploy a
recurring schedule; all service/human gates above remain unmet.

On 2026-10-17, actual owned loopback SQL ran all 17 rescan tests, and real
MSSQL CLI pages returned 2/0/0 with 1/2/0 clean results, three success events,
intact ledger and retained legal hold. The owned SQL container was stopped and
removed. The built UID10001 image also ran the offline job with read-only root,
dropped capabilities, NoNewPrivs and no network, persisting the same outcomes.
These are bounded engineering receipts, not real Defender, recurring hosted
schedule, Legal/DPO or owner approval acceptance.

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
