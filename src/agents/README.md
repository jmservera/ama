---
title: Zava Forward agents
description: Five retrofit assistants, the offline AI evaluation harness and their dated validation record for the agents project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

The agents project (`zava_forward.agents`) holds the AI evaluation harness and its golden data
(`evals/`). The five retrofit assistants and the AI task registry still live in `zava_forward.core`
(`assistants`, `assistant_release`, `ai_registry`, divergence A1 of the parity matrix) and are exposed by
the [api](../api/README.md) routes. The sections below are moved unchanged from the former
`mvp/README.md` (M6 of #199) and keep the dated 2026-10-13 and 2026-10-14 validation record. Commands in
them that start with `cd src/api` run from the api project.

## AI evaluation harness

* AI evaluation harness, offline: `python3 -m zava_forward.agents.ai_eval`
  runs golden scenarios (`src/agents/evals/ai_priority_golden.json`; the image sets `ZF_AI_GOLDEN`) with a scripted model
  and checks that ranking and case data never change, the output stays Proposed
  and needs a person's reason to edit or reject. It fails on any critical miss
  (a case with an open safety issue missing from the AI top-k) and on any cited
  fact that is not in the case data, and reports top-k overlap, Spearman rank
  correlation, run-to-run variation on identical input, latency, model and
  prompt version, reviewer accept/edit/reject counts with reasons, and the
  AI's added value against the deterministic and workflow-only orders on the
  same cases. `--json` prints the full report; managers can read it, with the
  live reviewer counts, at `GET /api/ai/report`. Negative controls in
  `tests/test_ai_tasks.py` break each property and expect the harness to fail.
  The report also carries an `evidence` block (issue #108): SHA-256 of the
  frozen golden file, prompt version, provider (scripted), "not evaluated" for
  actual-model and human effectiveness, calibration "not applicable", benefit
  claim "not permitted", and the open items (Foundry model, version and quota
  confirmation in the chosen region, authorised live calls, held-out split and
  thresholds, human protocol, Finance validation). Any critical miss fails the
  run.

## Validation record

### Five retrofit assistants (2026-10-13 implementation)

The existing workbench now has five separate v1.0.0 capabilities:
`stock-prioritisation`, `assessment-preparation`, `funding-evidence`,
`works-resident-coordination` and `quality-evidence`. Each case card exposes
the controls permitted for the current role. "Assistant proposals" opens the
shared role-owned queue. This is a proposal service, not a case automation
engine: generation and review never change ranking, ownership, funding,
consent, appointments, work orders, safety holds or quality sign-offs.

| Capability | Request and proposal-review roles | Synthetic proactive gap check |
| --- | --- | --- |
| Stock | Retrofit Coordinator, Retrofit Programme Manager | Missing home EPC/type/build year or conflicting disclosed survey values |
| Assessment | Retrofit Coordinator, Retrofit Programme Manager | Missing Survey/Design metadata or hash, missing design version, changed relevant source |
| Funding | Grants and Evidence Officer, Retrofit Programme Manager | Missing measures/route/reference/grant/budget, incomplete supplied invoice inputs, claim-phase source-history/Funding evidence gaps; changed relevant source/terms |
| Works/resident coordination | Retrofit Coordinator, Resident Liaison Officer, Retrofit Programme Manager | Offered handoff, missed recorded appointment or overdue open service-request update |
| Quality | Quality Inspector, Retrofit Programme Manager | Missing measure/checklist evidence, conflicting evidence, obsolete checklist or changed relevant source |

These are selected synthetic exercise rules (`synthetic-gaps-2026-10-13-v1`),
not approved company rules or an assessment of funding eligibility. Unknown
fields, missing document versions/content hashes and unavailable provider
usage remain explicit unknowns/nulls. Existing document records are not
backfilled or silently asserted to have hashes. New uploads record SHA-256
and version 1 in the existing document metadata.

Source capture is an allowlist safe for every permitted reader: stock excludes
resident support/safety ranking inputs and private ranking reasons; other
non-finance capabilities exclude finance. Coordination includes disclosed
contact/access preferences but no vulnerability reason, handoff free text or
complaint narrative. Funding includes structured budget, commitments, invoice
lines, grants and permitted evidence metadata, not an old `funding_draft`
invocation. Document filenames, AI summaries and arbitrary document contents
are not copied into shared proposals. Citations identify captured categories
and hashes, not passages or proof that the model's conclusion is correct.
Each response rechecks the current staff record, role and optional `case_ids`
and `areas` scopes. Contractors and unknown roles are default-denied. A revoked
staff role cannot read an earlier proposal merely by retaining a session.

Human review has two separate operations: first explicitly record source
verification with a note, then accept or edit-accept. The accepting person
must have their own current verification. Quality review additionally uses the
existing independence check against evidence submitters, recorders and fixers.
This is independent proposal review, not competent technical sign-off or
quality acceptance. Failed, malformed, template, missing-citation and stale
proposals cannot be verified or accepted. Rejection and history remain
available to authorized current readers; a rejected worker cannot complete
over that decision. Manual case work remains available during model calls,
disabled configuration, failure, exhaustion and stale evidence. Case controls
render before auxiliary assistant reads finish. Those reads share a 10-second
abort deadline with a visible manual fallback; detached/different-route panels
ignore late results.

#### Operator authority and finite allowance

The new service requires `ZF_STORE=sqlite` or `mssql`. JSON-only operation keeps
the existing app usable but exposes disabled assistance/manual routes.
No new AI/model dependency or resource is required. Existing AI endpoint and
standard deployment settings are used; no model is called by the test suites.

Automatic scanning is off by default. Both reactive execution and proactive
execution require a configured AI provider and a valid bounded operator
authority. Configuration alone is not approval: an operator must obtain
scoped approval for rollout, the authority reference, expiry and finite call/
token allowances before configuring these settings.

| Environment setting | Default | Effective constraint |
| --- | --- | --- |
| `ZF_ASSIST_AUTHORITY` | Empty (disabled) | Approved exercise reference, 1-120 characters; never a credential |
| `ZF_ASSIST_EXPIRES` | Empty (disabled) | Explicit timezone-bearing ISO timestamp; database time enforces expiry |
| `ZF_ASSIST_CALL_ALLOWANCE` | 0 (disabled) | Finite aggregate provider-dispatch allowance, 1-1000000 |
| `ZF_ASSIST_TOKEN_ALLOWANCE` | 0 (disabled) | Finite aggregate tokens, at most 1000000000000; must cover one full reservation |
| `ZF_ASSIST_PROACTIVE` | `0` | `1` enables periodic purpose-principal scans after valid authority/limits |
| `ZF_ASSIST_SCAN_INTERVAL` | 60 seconds | 5-3600 |
| `ZF_ASSIST_SCAN_SIZE` | 20 cases | 1-100; keyset cursor visits subsequent open cases |
| `ZF_ASSIST_INPUT_CHARS` | 12000 | 1000-24000 including system and evidence prompts |
| `ZF_ASSIST_OUTPUT_CHARS` | 8000 | 1000-16000; typed summary/findings/unknowns validation |
| `ZF_ASSIST_OUTPUT_TOKENS` | 600 | 100-2000 |
| `ZF_ASSIST_TIMEOUT` | 20 seconds | 1-40; bounded wall-clock dispatch wait; late output is not used |
| `ZF_ASSIST_ACTIVE_CALLS` | 2 | 1-4 local physical call slots and shared unexpired SQL attempt slots |
| `ZF_ASSIST_ATTEMPTS` | 2 | 1-3 per immutable proposal key |
| `ZF_ASSIST_BACKOFF` | 30 seconds | 1-3600, multiplied by the completed attempt count |
| `ZF_ASSIST_LEASE` | 60 seconds | 10-120, at least timeout + 5 seconds |

All replicas must use the same approved effective authority and limits.
SQL serializes reservations under the existing transaction/application-lock
adapter. Every dispatch, including a retry or lease takeover, reserves one
call and `INPUT_CHARS + OUTPUT_TOKENS` tokens before provider access. Input
characters conservatively upper-bound input tokens without adding a tokenizer.
Known valid usage replaces the token reservation with actual tokens. Missing,
out-of-range or timeout usage retains the full bounded reservation liability;
it is never recorded as zero. Uncertain failures retain a shared active-attempt
slot until the database lease deadline; a timed-out physical call retains its
local semaphore slot until it actually returns.

Allowance is keyed by the authority reference hash, shared across replicas and
restarts. The same reference cannot increase the existing allowance or extend
its stored expiry. There is no daily reset or indefinite replenishment.
Exhausted/expired shared allowance disables further automatic scans and is
visible through the registry and queue, not just at provider dispatch.
Another reference means a separately approved finite exercise, not an
automatic rollover. Token allowances are not a currency guarantee; the
operator must derive finite approved limits from deployment pricing and retain
unknown billing liability. Exactly-once inference/billing is not promised:
expired leases can lead to another bounded attempt while remote completion
remains uncertain.

#### SQL durability and lifecycle

Startup adds four idempotent tables (`assistant_tasks`, `assistant_allowance`,
`assistant_attempts`, `assistant_events`), a pending index and append-only
event protection. MSSQL startup DDL and assistant migrations serialize with
the existing transaction-owned `sp_getapplock` write lock. The startup identity
needs the existing schema-creation privileges (for example the already
documented `db_ddladmin`) and permission to use that application lock.
In a ledger-enabled database, `assistant_events` is explicitly created with
`LEDGER = ON (APPEND_ONLY = ON)`. Do not attach the ordinary SQL Server
INSTEAD OF trigger to a system-versioned ledger table: that is unsupported.
An existing updatable-ledger event table fails closed for operator repair;
startup never drops it or deletes its evidence. Non-ledger SQL and SQLite
retain their append-only triggers. Real SQL Server tests cover both database
modes, failed destructive event writes and restart persistence.
Runtime needs SELECT on cases/staff/meta and assistant state, INSERT/UPDATE
on task/allowance/attempt state, and INSERT/SELECT on assistant events. It does
not need new domain write permissions for assistance. Deployment/operator
privilege verification and real MSSQL acceptance are separate from local
dialect emulation. A failed assistant migration leaves assistance visibly
disabled with an operator-migration/manual-route message; it does not prevent
otherwise available ordinary case work or quietly start a provider worker.

Each short transaction uses an independently owned Store-adapter connection.
No provider network call holds the Store/domain/database lock. A durable SHA-256
task key includes capability/version, case, canonical intended proposal identity
(the registered purpose) and material permitted-source/schema/rule/document
signatures. Changed intent or dependencies cannot replay another proposal;
mode is separate append-only provenance. Repeated scans and reactive/proactive
collisions with the same identity recover the same proposal. Claims have an
owner, monotonic fence, database-time lease and CAS completion. Lost
acknowledgements are looked up, not blindly re-dispatched. Review compares the
current material signature and proposal revision in the same serialized SQL
transaction; unrelated contact notes do not stale a proposal.
MSSQL assistant transactions use serializable isolation so current role,
case and permitted metadata reads remain protected through review commit,
including against writers outside the application's cooperative write lock.
The independently owned connection resets to read-committed before closing.

The existing process starts at most `ACTIVE_CALLS` proposal workers and,
when enabled, one scanner. A scanner cannot overlap locally, and SQL capture/
enqueue transactions serialize across replicas. Local physical provider calls
are also bounded by a semaphore; shared unexpired attempt slots bound
replica-wide claims. Shutdown closes provider-thread admission under a short
dispatch gate, so a delayed poll/claim cannot admit inference after stop.
The gate holds neither SQL nor provider work. An existing reservation remains
conservative if shutdown intervenes; an already admitted call may still finish.
The interruptible stop event stops scans/polls and abandons dispatch waits;
outstanding daemon provider calls cannot make late domain or proposal writes.
Expiry/fencing, not thread ownership, governs recovery.
Disable assistance by removing its authority or setting proactive off, and
restore the previous image to roll back. Old images ignore the new tables;
do not delete evidence, reseed data or reset the allowance.

#### API and non-destructive exercise

These calls require a currently authorized signed-in session and, for the
trusted proxy, the existing `X-ZF-CSRF: 1` POST header. They write only
task/proposal/event/allowance state. Invocation can spend approved allowance
when workers are enabled: do not perform live invocation without its scoped
approval. Registry/list/detail are non-billable reads.

```bash
# $BASE is the existing service; use its authenticated session cookie.
curl -b "$COOKIE" "$BASE/api/assistants"
curl -b "$COOKIE" "$BASE/api/assistants/proposals?case_id=ZF-1"
curl -b "$COOKIE" "$BASE/api/assistants/proposals/$PROPOSAL_ID"

# 202 response contains id, state, revision, bounded snapshot and manual route.
curl -b "$COOKIE" -H 'Content-Type: application/json' -H 'X-ZF-CSRF: 1' \
  -d '{"case_id":"ZF-1"}' \
  "$BASE/api/assistants/stock-prioritisation/invoke"

# Repeat the invoke endpoint for any of the other four registered IDs.
# Use the latest revision returned by detail; verification precedes acceptance.
curl -b "$COOKIE" -H 'Content-Type: application/json' -H 'X-ZF-CSRF: 1' \
  -d '{"action":"verify","revision":3,"source_verified":true,"note":"Checked each cited source and retained unknowns."}' \
  "$BASE/api/assistants/proposals/$PROPOSAL_ID/review"
curl -b "$COOKIE" -H 'Content-Type: application/json' -H 'X-ZF-CSRF: 1' \
  -d '{"action":"accept","revision":4,"note":"Accept this proposal only, not a domain decision."}' \
  "$BASE/api/assistants/proposals/$PROPOSAL_ID/review"
```

List pages are bounded to 50 proposals and return `next_after`; pass it as
`?after=<cursor>` for the next page. Detail returns 50 latest history events;
`history_next_offset` supplies the next `?history_offset=<offset>` page.
Current roles/scopes are rechecked for each page, including earlier history.
The queue and case-card history controls expose these continuation reads.

`edit-accept` additionally supplies `output` with exactly `summary`, `findings`
(each has `text` and a non-empty `citations` list of captured `source:*` IDs)
and `unknowns`. `reject` supplies the current `revision` and a bounded `note`.
Stale revision returns 409; denied current role/scope returns 403; invalid
verification/output/state returns 400. Invocation, list/detail and review have
separate service authorization. Scanning has no staff-callable API: the
registered purpose principal is `service:retrofit-evidence-proposals`, not
a manager impersonation. The scheduler calls `Assistants.scan()` only with
valid authority/limits and proactive opt-in.

Release admission (issue #107, RAI delta; `assistant_release.py`): every
dispatch, claim, completion, list/detail, review and export reliance rechecks a
SQL `assistant_releases` record binding the task, registry/schema, provider,
endpoint, deployment, expected serving model, prompt, policy, data, provenance
and permission versions to a named approver, residual-risk decision and
expiry. `GET /api/assistants` shows the build's binding per assistant.
`POST /api/assistants/releases` records one (Programme Manager listed in
`ZF_ASSIST_RELEASE_APPROVERS`; `evidence_class` is `constructed-fixture` or
`actual`); `POST /api/assistants/releases/{id}/suspend|revoke` ends it, and a
revoked or suspended record is terminal. Absent, expired, suspended, revoked
or mismatched releases deny with zero provider calls, retain the denial and
name the owner (Juan Manuel Servera, Legal, Compliance and DPO owner) and the
manual route. For the five assistants, a returned model name that differs
from the released one quarantines the result and suspends the release. This is
a returned-model check on the provider's own response, not authoritative
attestation of what served the call. A `constructed-fixture` record never
admits a live `Ai` provider. Retained legacy tasks are gated on the SQL store
when AI is configured (`legacy:<task>` records). The gate is given the
deployment that will actually be called (`ai.fast`, or `ai.strong` for strong
paths and `read_document`) and compares it, with the registry, schema, prompt,
policy, data, provenance and permission versions (`ai_registry.legacy_binding`),
to the release. Legacy results are rechecked against the gate after the call
and discarded (`quarantined`) if the release was suspended, revoked, expired
or the task suspended meanwhile. Legacy paths get no returned-model check
(their text helper does not return the model) and a late legacy result is
discarded but does not suspend the release.

Open items for #107: authoritative serving-version attestation; Azure SQL race
evidence; a routine-versus-material change distinction; export reliance; the
JSON dev store has no durable release store and is not gated; delivered-build
acceptance; release approvers are unset (`ZF_ASSIST_RELEASE_APPROVERS`).

Validation: `tests/test_assistants.py` and `tests/test_assistant_release.py` exercise all five reactive/proactive
contracts, reader matrices, failure/disabled/malformed paths, current roles,
source review, unchanged controlled state, independent SQLite connections,
claims/leases/restart/lost acknowledgements, retries/aggregate liability,
shared limits, blocked-provider/manual access and shutdown admission. Conditional
`MssqlContractTests`, `MssqlReviewTests`, `MssqlDurabilityTests`, `MssqlApiTests`
and `MssqlLedgerTests`
run the same contracts on actual SQL Server. They require `ZF_TEST_MSSQL=1`,
the existing password/driver settings and a disposable local service
(`localhost`, `127.0.0.1` or Docker alias `sql`). They create/reset only
`zf_test_assistants`, `zf_test_assistants_ledger` and
`zf_test_assistants_ledger_invalid`; never point these tests at the pilot or
Azure SQL. The ledger fixtures replace only their fixed local test databases.
CI runs these alongside the existing general store parity suite. SQL-shape
emulation alone is still not actual SQL proof. The isolated non-billable browser
exercise uses fixtures, not the retained dataset:

```bash
cd src/api
PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p test_assistants.py
PYTHONPATH=tests:../core/tests python3 checks/assistants_browser_check.py
node --check src/zava_forward/api/web/assistants.js

# Disposable local SQL only; set the existing ZF_SQL_* test settings first.
ZF_TEST_MSSQL=1 PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest \
  test_assistants.MssqlContractTests test_assistants.MssqlReviewTests \
  test_assistants.MssqlDurabilityTests test_assistants.MssqlApiTests \
  test_assistants.MssqlLedgerTests
```

The browser exercise needs the existing Playwright test dependency and Chromium;
it can use installed Google Chrome or `CHECK_BROWSER_EXECUTABLE`. The parent
owns image build, real platform evidence, approved rollout and independent
Review. The historical reset cancellation was explicitly cleared on 2026-10-14.
Real operator provider/SQL/restart execution is now recorded below; local mocks
still do not substitute for real staff/human acceptance.

Corrected-source execution on 2026-10-13: 47 nonbillable assistant tests passed;
full discovery reported 379 tests, 310 passed and 69 conditional SQL skips.
The actual disposable SQL run passed all 69 tests: 26 existing store tests and
43 assistant contract/review/durability/API tests, including concurrent first
assistant-table creation on retained case/audit state. The isolated desktop Chromium
exercise passed 19 checks, including pending-assistance manual writes,
deadline fallback and late-result navigation, with no page errors. Both changed
JavaScript files passed syntax checks. Provider responses and human-verification
actions in these suites are test fixtures, not real model or human acceptance.
No retained dataset, private configuration, live provider or Azure deployment
was changed. Actual SQL Server proof does not establish deployed Azure SQL
identity/permissions, real provider quality or CON-009/AC-057 delivery.

Later generated-data validation on 2026-10-13 exposed a populated Visits
rendering defect: arrays of day groups were dropped although the API returned
38 bookings. The shared renderer now flattens node arrays before filtering.
The two-day/case-link regression brings the assistant browser exercise to
21 passing checks. Latest exact-source image05 additionally passes 21
nonbillable generated-data UI/API/local-restart checks with 38 visible visits,
12 Finance rows and 601 source work orders, preserved independent SQLite
domain hashes and five disabled/manual proposals with zero provider attempts.
Tenant bindings and Azure/model acceptance are not exercised by that isolated
validation. Subsequently, on 2026-10-14, the owner explicitly reauthorized
the exact exercise database reset and all offered bounded delivery. Image05
now serves in revision `--0000012`, pinned to manifest
`sha256:e0254cb3a0599c21802f0b6515f975550cf00ddce4849d04fd3fa3d50683af20`.
The restored ledger baseline has 980 cases, 11 tenant staff, 38 visits and
the generated queues. Process-local operator authority permitted five actual
registered Azure OpenAI calls: all five proposals are distinct/citation-validated
ready, with 6884 total tokens and 15 immutable ledger events. Independent
SQL domain and assistant-table content hashes survive actual revision restart.
No human verification/acceptance is recorded. Normal serving assistant
authority remains absent/proactive off; this is not standing spend approval,
staff-browser acceptance, semantic calibration or measured value.
