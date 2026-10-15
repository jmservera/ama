---
title: Zava Forward core library
description: Domain, store, ledger, law store, chat storage and synthetic-data documentation for the core project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

The shared domain library (`zava_forward.core`): stores (JSON, SQLite, Azure SQL), ledger, law store,
rule cards, governance, continuity, chat storage and isolation, and the synthetic tools. It imports no
workload. The sections below are moved unchanged from the former `mvp/README.md` (ADR 0006, issue #199,
M6); the staff-facing behaviour and configuration are in [api](../api/README.md).

Test paths named `tests/...` are in `src/core/tests/` unless they name another project:
`test_chat_isolation` and `test_continuity` are in `src/api/tests/`. Run the suite from `src/core` with
`python3 -m unittest discover -s tests`. Data fixtures and generated datasets are written to the
per-user `ZF_DATA` folder, never under `src/`.

## Datasets, fixtures and synthetic tools

* Evaluation dataset registry (`src/agents/evals/registry.json`) lists every golden and
  evaluation dataset with version, owner and purpose; a test fails for an
  unregistered file in `mvp/evals/` or any `src/<project>/evals/` folder. The stock-scale fixture (60,000 homes, 600,000
  events, wholly fictional, seeded) is rebuilt with
  `python3 -m zava_forward.core.synthetic.scale_fixture` (moved in M3), writes to
  `scale-fixture/` under the per-user `ZF_DATA` folder (default
  `~/.zava-forward/data/`, outside the repository) and is never committed. Dataset owners are
  an open owner decision.
* Chat and memory fixtures (#172): `PYTHONPATH=src/agents/tests python3 -m
  chat_fixture` (test support, moved to `src/agents/tests` in M3) writes seeded, labelled-synthetic personas
  (two per PRD perspective, mapped to existing app roles), threads, memory
  items, opt-in states, exclusion probes, and isolation, expiry and deletion
  cases to `chat-fixture/` under the `ZF_DATA` folder. Case IDs come from the
  60,000-home stock. Retention is an illustrative 90 days, not a policy
  (BRD OD-45/OD-46 open); expectations are targets for #160 to #164.
* Sensor backfill (#183): `python3 -m zava_forward.core.synthetic.sensor_backfill
  --estimate-only` prints the volume and size estimate for two years of hourly
  temperature and humidity across all 60,000 homes (about 1.05 billion rows,
  about 118 GiB as CSV, measured on a 20-home sample); `--homes N` writes
  sharded CSV, `sensors.csv`, `estimate.json` and `manifest.json` (seed,
  versions, climate source, parameters, hash) to `sensor-backfill/` under
  the `ZF_DATA` folder. Same seed gives identical bytes. Every row is
  `SYNTHETIC` with a stock home ID and `SENS-SYN-` sensor ID; `load_into()`
  validates and appends idempotently on sensor ID plus reading ID, and
  `SQL_DDL` is the Azure SQL schema. Open: Met Office and Environment Agency
  open data are not yet retrieved (climate is a labelled synthetic model),
  #110 consumer validation is mirrored by `validate_reading()` and must be
  reconciled when #110 lands, and a full-stock run needs a storage and cost
  decision.
* Sensor plausibility tests (#191): `tests/test_sensor_plausibility.py` runs in
  the existing MVP CI unittest step over 150 stock homes for two years. It
  fails on out-of-bounds or flat-line series, checks seasonal and diurnal
  structure and humidity by age band and dwelling, and checks that dropout,
  outlier and stuck fault rates match the configured injection. Expected
  outdoor ranges are labelled exercise values until the climate source in #178
  is retrieved and recorded (open item).

## Law store (ADR 0005, phase 1)

`src/core/src/zava_forward/core/lawstore.py` loads the dated snapshots in `docs/reference/regulatory/`
into append-only tables (`reg_source`, `reg_version`, `reg_provision`, `reg_gap`) and
writes each snapshot once, content hashed, through a snapshot interface. The target is
Azure only: `ZF_LAW_STORE=mssql` uses Azure SQL (the `ZF_SQL_*` settings of the main
store; append-only ledger tables when the database is ledger enabled, otherwise an
append-only trigger) and `AzureBlobSnapshots` (`ZF_LAW_BLOB_ACCOUNT_URL`,
`ZF_LAW_BLOB_CONTAINER`, `DefaultAzureCredential`; writes never overwrite). SQLite and a
local folder (`ZF_LAW_DB`, `ZF_LAW_BLOBS`) are local test doubles only. Seed with
`python -m zava_forward.core.lawstore REGULATORY_DIR DB_FILE BLOB_DIR` (or
`ZF_LAW_STORE=mssql python -m zava_forward.core.lawstore REGULATORY_DIR`); a changed file
becomes a new version and nothing existing is altered. Partial sources carry
`completeness: partial` and results say so. Leasehold, complaints handling, TrustMark
and licensed PAS 2035 are gaps answered as "no source held". The keyword index
(`rebuild_index`) is derived from SQL. The same suite runs on SQL Server in the CI
`mssql` job (`test_lawstore.MssqlStoreTests`). Open items: the Azure Blob container
immutability (WORM) policy and the Azure SQL deployment are infrastructure and are not
verified here; the Azure Blob client is tested only against a fake container. The
read-only viewer at `/law.html` and `/api/law/*` serves staff roles with no AI. Seeded
versions are `not_reviewed` with owner "to be named"; this is a reference copy, not
legal advice or approval. Seed metadata is `src/core/src/zava_forward/core/law/law-source-register.json`.

## Rule cards (ADR 0005, phase 2)

`src/core/src/zava_forward/core/rulecards.py` (moved from `mvp/` in M1 of #199) holds versioned rule cards in append-only tables
(`rule_card_version`, `rule_card_event`, `rule_card_review`, `rule_card_review_event`) with a draft, approved,
active, held, retired lifecycle. A card is drafted by the `rule_author` role and only
its named `rule_owner` can approve, activate, hold, release or retire it; an author
cannot approve their own card. Versions, approver, approval date and effective dates
are retained. `source_changed` records an open review item (RULE-021, AC-068) naming the
affected card, active version, requirements and tests, source versions and effective date,
and never alters an approved card. `assess_review` lets only the card's named owner record
the interpretation, tests, effective date, notification, rollback and any hold; it never
activates a rule, so activation still needs propose, approve and activate by named humans.
The card-to-requirement and test trace for the two seed cards is a static exercise map;
unmapped cards are flagged for the owner. The two seed cards (hazard awareness clock, automated decision
safeguard) are labelled exercise fixtures with simulated approvals only; they are not
law or real approval, and the owner, clock durations and citations remain open items
for named Compliance and DPO approval. Mapping the roles to Entra app roles (#116)
and the rule engine are not done here.

## SQL store

`ZF_STORE=sqlite` uses `sqlstore.py` on stdlib sqlite3 as the dev and test
driver, with the same `Store` interface. Each case row has a row version and a
save is `UPDATE ... WHERE rowversion = ?`; a lost race returns HTTP 409, and
nothing is written. The audit table is full-content, append-only (triggers
refuse update and delete) and hash-chained. Indexes cover the list filters,
owner, open safety issues, postcode, address and the ledger sequence, and a test
checks the query plans use them. No per-process state is needed for
correctness: a second process catches up from a database sequence before every
operation, and dev sign-in cookies are signed, not held in memory.

List reads are answered by SQL: each row carries derived, indexed columns
(a fixed-width rank key built by `ranking.sql_key`, days, owner, contractor,
stage, flags, search text). Filters, sorts, search, totals, header counts and
paging run in SQL, and ranks are global (a window over open cases). The default
sort also has keyset paging (`after` cursor, `next_cursor` in the response),
which the work list uses for "Show more"; other sorts use offset in SQL. A
migration adds the columns and rebuilds keys when the ranking policy version
changes. Tests check parity with the in-memory store, query plans and a
60,000-case timing.

Azure SQL is implemented by `mssqlstore.py` and has run with the API managed
identity. It uses explicit `BIGINT` row versions, `NVARCHAR(MAX)` JSON bodies,
binary text collation and a transaction-owned `sp_getapplock` writer lock.
The audit table is append-only ledger when the database supports/enables it,
otherwise an `INSTEAD OF UPDATE, DELETE` trigger rejects mutation. External
immutable digest anchoring and the per-year ledger-table design in ADR 0002
remain open; a hash chain alone does not prove those proposed controls.

## Azure SQL store

`ZF_STORE=mssql` uses `mssqlstore.py`, a T-SQL dialect over the same `SqlStore`
logic, with the pinned `mssql-python` driver (`src/api/requirements.txt`, hashes
checked in the image build; the image adds `libltdl7` and `libkrb5-3`). Writers are
serialised across replicas by a transaction holding an exclusive application
lock (the equivalent of SQLite's write lock), every compared text column uses a
binary collation so ordering matches the other stores, and a connection dropped
between requests is reopened. Sign-in is Microsoft Entra with the app's managed
identity (`ZF_SQL_AUTH=msi`, plus `ZF_SQL_CLIENT_ID` for a user-assigned one), so
there is no database password. The audit table is an append-only ledger table
when the database has Azure SQL ledger enabled (the engine refuses update and
delete), otherwise an `INSTEAD OF` trigger does it. Every other table in a ledger
database also keeps row history, which matters for erasure and retention
(DPIA item to resolve before real data).

The first start seeds an empty database from `ZF_DATA`; the image carries no data,
so seed once from an operator machine with `ZF_SQL_AUTH=token` and
`ZF_SQL_TOKEN=$(az account get-access-token --resource https://database.windows.net/ --query accessToken -o tsv)`.
The app identity needs a contained user with `db_datareader`, `db_datawriter` and
`db_ddladmin` (see `infra/scripts/create-sql-users.sql`). `tests/test_mssqlstore.py`
runs the SQL store suites and the list-read parity suite against a real SQL Server
when `ZF_TEST_MSSQL=1` (and `ZF_SQL_*` point at a throwaway database).

## Frozen protocol, benefits register and release gates (issue #126)

`src/core/src/zava_forward/core/governance.py` records, and never decides, the pilot governance in the existing store (JSON or SQL, so it survives a restart). Managers use `GET /api/governance` and `POST /api/governance/{protocol-freeze,protocol-approve,benefits-record,benefits-approve,release,breach,restart}`. No AI assistant, ranking or tool has any part in it.

* Protocol (RULE-019, AC-062): a version freezes all thirteen required fields. A different person approves it with the OD-36 DPIA and lawful measurement-basis references. A change needs a reason and a new approval. `capture_gate()` keeps Phase 0 capture closed until the latest version and the BG-011 register are approved.
* Benefits register (BG-011, OD-18): event definitions and the MDE are recorded. `target_verdict` never returns pass or fail when the MDE is missing or exceeds a target (20% cycle time, 25% coordination hours); it returns "Not assessable" or "Interval estimate only".
* Release decisions (RULE-020, AC-063): each phase (Phase 0 capture, Shadow testing, Live pilot) and tranche has a Release or Withhold record with requirements, evidence, unresolved issues, cost and risk envelope reference and named approvers. Releasing Phase 0 capture needs the capture gate; Shadow testing needs entry evidence, and Shadow testing and Live pilot need Phase 0 capture released first.
* Guardrail breach (RULE-024, AC-078): `breach_record` (managers, quality inspectors and building safety liaisons, so a hazard-aware role can raise a breach without waiting for a manager) pauses the home, work package, archetype or workstream. `breach_restart` needs a different person, the OD-35 authority reference, accepted remediation evidence and a Release decision recorded after the breach. `guard_case_event` calls `require_not_paused` (home by case id or address, archetype by home type) and, for cases flagged `pilot`, `require_capture_open` in `log_call`, `set_decision`, `advance` and `return_case`; emergency and statutory hazard response continues outside any pause.

Tests: `tests/test_governance.py` (JSON and SQL stores, labelled synthetic demonstration values). Open items, not invented here: the real OD-18 definitions and MDE, the OD-36 DPIA and lawful basis, the OD-35 named authority, actual approvers, how cases are enrolled in the pilot cohort (the `pilot` flag), pause scopes for work package and workstream, and extending the guard to the remaining case workflows. The RAI closure registers in the issue (eleven residuals and eleven unassessed checks, a fresh current-source assessment, owner acceptances) are not delivered or claimed closed by this change; every item stays proposed or insufficient until qualified owners and fresh evidence exist, and live use stays blocked.

### Per-year ledger digests, load check and recovery drill (issue #114)

* `python -m zava_forward.core.ledger --seal-years` writes one immutable `year-YYYY.json`
  digest per completed year (entries, first link, head); `--by-year` verifies every
  year on its own, the links between years and each sealed digest, and reports a
  dropped sealed year. A self-consistent rewrite of a sealed year is caught only by
  its digest, so those files belong in the immutable Blob container. Proven in
  `src/core/tests/test_recovery.py`; run the scheduled `--by-year` check before relying on the ledger.
* `python -m zava_forward.core.synthetic.loadcheck --data zavaforward.json --homes 60000` runs the
  NFR-002 mix (five sessions, two writers) against the configured store and prints
  p50/p95/max per class. Local SQLite on 2026-10-15 over 60,000 labelled synthetic
  homes for 30 s: list p95 0.28 s, detail 0.30 s, write 0.33 s, no errors (limits 1 s,
  1 s, 2 s). Open items: the same run against Azure SQL, dashboard and import preview
  classes, and cost (needs Azure meter rates and measured vCore time).
* `src/core/src/zava_forward/core/recovery.py` erases a resident's personal fields and keeps a
  personal-data-free deletion register outside the database. The register is one
  write-once entry per erasure under the reserved case id `_erasures` in the document
  backend: Azure Blob Storage when `ZF_DOC_STORE=azure-blob` (same configuration as case
  documents), a local folder only as the local-test backend. The entry is written
  before the redaction, so a crash between the two leaves an erasure that
  `reapply_deletions` completes (audited as `erasure_reapplied`), never an unrecorded
  one; if the register cannot be written, nothing is redacted, and an unreadable
  register is an error, never an empty one. Tests: a SQLite backup restore proves the
  erasure returns, a fake Blob transport proves the register backend and the write
  ordering.
* Unverified: the Azure SQL point-in-time restore drill (DH-005) has not been run;
  the register has not been run against a real storage account, nor has its
  retention or immutability policy been configured or tested; the Blob container
  should carry a WORM/immutability policy, which is infrastructure and unproven here;
  cost (storage, transactions, restore) is not measured.

## Per-user chat thread storage (issue #160)

`chatthreads.py` stores chat threads and messages per user (ADR 0004 decision 3), behind the `Store` interface: the
in-memory `Store` keeps them in its live file, `SqlStore` and `MssqlStore` in the additive, idempotent `chat_thread` and
`chat_message` tables (Azure SQL in deployment, SQLite for local tests). A thread carries the server-derived owner,
case reference, assistant task and version, and model identity; a message carries its role, evidence references and,
for assistant messages, the model. `chat_create_thread`, `chat_add_message`, `chat_list_threads`, `chat_resume`,
`chat_archive` and `chat_delete` always filter on the owner (another user's thread is reported as not found). Writes use
the thread row version and raise `ConflictError` when a caller's expected version is stale. The audit ledger receives
metadata only (thread id, case, counts, role), never message text or title, so deleting a thread leaves the chain intact.
Not in this slice: the panel (#159), model calls, memory (#161), isolation hardening (#162), retention and export
(#163; retention policy is unlocked for the exercise, legal retention lock deferred). Fixtures are synthetic.
Tests: `tests/test_chatthreads.py` (in-memory and SQLite parity; `MssqlChatThreads` runs with `ZF_TEST_MSSQL=1`).

## Chat and memory isolation (issue #162)

`chat_isolation.py` sits on the #160 repository and #163 privacy rules and adds no tables. Endpoints (staff roles only; contractors and unknown roles are denied, default deny): `GET/POST /api/chat/threads`, `GET /api/chat/threads/{id}`, `POST /api/chat/threads/{id}/messages|archive|delete`, `GET/POST /api/chat/memory` (the POST needs `task` and a prior opt-in), `GET /api/chat/memory/status?task=`, `POST /api/chat/memory/opt-in|opt-out|erase|global|task` and `POST /api/chat/memory/{id}/edit|delete` (the #285 lifecycle; `global` and `task` switches are administrator-only), `POST /api/chat/breakglass`. The owner is always the authenticated user; request fields such as `owner` or `email` are ignored, and another user's thread, or a case outside the caller's scope, is reported as not found (404, so existence cannot be probed). Prompts carry the masked question and only memory from `privacy.prompt_memory` (opt-in, switch-gated, labelled non-authoritative); stored model replies are redacted like user messages.

* Every turn re-reads the user's current role and re-projects the case through the same `store.detail` projection as the case card, so a changed or revoked role applies on the next turn.
* The prompt holds only the caller's own thread, own unexpired memory and the projected case, each inside `UNTRUSTED` blocks with the block delimiters neutralised. The channel has no tools; replies are text only, labelled as unapproved, and a reply carrying tool-call or record-change syntax or a withheld reason is replaced by a refusal.
* Break-glass is refused until `CHAT_BREAKGLASS_REF` (owner policy reference) is recorded and the caller role is named in `CHAT_BREAKGLASS_ROLES`. When allowed it needs a purpose, expires within 60 minutes, returns counts and ids only (never content) and writes granted and refused attempts to the audit ledger.
* Open items: the break-glass and administrator content-access policy is an owner decision (BRD OD-46) and is not decided here; whether contractors may use chat is undecided (denied); the injection set in `src/api/tests/test_chat_isolation.py` is a recorded regression set, not evidence of complete coverage; real-model behaviour was not exercised.

Tests: `src/api/tests/test_chat_isolation.py` (extends the role matrix; replays the synthetic isolation fixture cases).

## Service continuity, versioning and export (issue #122)

`continuity.py` adds a persisted AI suspension (whole release or one registered task), a restart gate, a versioned
change register and a supplier-independent evidence export. Synthetic demonstration data only.

* Suspend: `POST /api/continuity/suspend` records scope, incident owner, containment, constructed communication
  (never sent), and the affected queued, leased and ready proposals, and raises an epoch.
* Enforcement: the epoch is read on the caller's own SQL connection at invoke, scan, claim, dispatch, complete and
  review, and shown in list and detail views; it does not depend on disabled buttons. In-flight provider calls may
  finish and stay charged or unknown; late results are quarantined and never actionable. No remote cancellation or
  exactly-once billing is claimed.
* Manual fallback: suspended AI paths return the workflow template with the reason; case work, resident challenge
  and hazard response are unaffected. Reject stays available.
* Restart: `restart-propose` (corrective evidence) then `restart-decide` by a different manager, with the current
  epoch and a named authority reference. Self-approved, stale, replayed or unauthorised restarts fail. The authority
  reference is recorded, not verified.
* Changes: `POST /api/continuity/change` and `change-reverse` version model, rule and configuration changes with an
  evaluation result (a failed evaluation is Blocked); reversal is a superseding record.
* Export: `GET /api/continuity/export` returns `zf-evidence-export/1` with a digest and ledger chain checked offline by
  `continuity.verify_export`, with no AI supplier needed. The bundle carries `complete` and `incomplete_reasons`: when
  the 5,000 assistant-proposal limit is hit it is flagged incomplete (with total and exported counts) and
  `verify_export` reports it not valid, so a truncated bundle is never presented as whole. The bundle records the ledger
  head (count and hash) and any sealed digests; `verify_export` fails when the entries do not reach that head. A
  recorded head can be rewritten together with the entries, so pass `expected_head` from a copy held outside the
  application (an immutable digest) to detect that.
* JSON store: AI task suspension, restart gating, the change register and export are enforced and tested on the JSON
  store. The five assistants are durable SQL only, so the bundle states `assistants.supported: false` and exports no
  assistant proposals there; assistant suspension on a JSON store is unsupported.
* Open owner items: witnessed authorised drill, recovery and response limits, supplier contract terms, Azure SQL
  drill evidence, interface identifier mapping, and the named restart authority.
