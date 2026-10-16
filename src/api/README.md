---
title: Zava Forward API and web workbench
description: Staff features, configuration, local run, honest limits and container checks for the api project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-16
ms.topic: reference
---

## Rule-card approval API (#211)

The existing law store now exposes exercise rule cards, without an AI call or
approval tool for agents. Configure the existing `ZF_LAW_DB`/`ZF_LAW_BLOBS` local
test doubles or `ZF_LAW_STORE=mssql` deployment backend. Startup retains two
labelled, unassigned draft seed cards. Creating a later assigned-email version
does not approve it or change the seed's retained history.

| Method and path | Contract |
| --- | --- |
| `GET /api/law/cards` | Latest version of each card, with exercise label and approval history |
| `GET /api/law/cards/{card_id}` | Every version and event, plus currently eligible active version |
| `GET /api/law/cards/reviews` | Source-change review records; no automatic interpretation |
| `POST /api/law/cards` | New immutable exercise draft; authenticated rule author required |
| `POST /api/law/cards/{card_id}/{version}/approve` | Named owner, distinct from the version's author |
| `POST /api/law/cards/{card_id}/{version}/activate` | Named owner; version must be approved |
| `POST /api/law/cards/{card_id}/{version}/hold` | Named owner; active card and nonempty `note` required |
| `POST /api/law/cards/{card_id}/{version}/release` | Named owner; held card only |
| `POST /api/law/cards/{card_id}/{version}/retire` | Named owner; approved, active or held card only |

Draft body (synthetic example, replace the owner with a provisioned staff email):

```json
{
  "card_id": "synthetic-example",
  "title": "Exercise human review",
  "trigger": "Synthetic proposed resident decision",
  "applicability": "Synthetic exercise only",
  "provisions": ["Illustrative citation, requires owner verification"],
  "clock": "No operational duration approved",
  "safe_default": "Route to the human review queue",
  "escalation_role": "Named exercise owner",
  "approver": "owner@example.test",
  "effective": "2026-10-16",
  "retirement": null
}
```

Other POST bodies are `{}`, except hold: `{"note":"Exercise source doubt"}`.
Actor, author, role, event date and exercise status are server-derived; attempts
to supply those fields are rejected. Dates must be canonical ISO dates, with
retirement after effective date. Domain/state denials return 409, malformed HTTP
fields 400, insufficient capability 403, absent authentication 401 and an
unconfigured law store 503. Unknown card history/routes return 404.

All reads require an existing staff law-view role; contractors/unknown roles are
denied. All writes additionally require the trusted-proxy provider and dedicated
Entra claims `ZavaForward.RuleAuthor` or `ZavaForward.RuleOwner`, respectively.
These reserved capabilities cannot supply a workbench role themselves, even
through `ZF_ROLE_MAP`. They are derived only after one unique tenant/object-ID
match to provisioned staff. Email fallback still permits existing workbench
login but never rule authority. Password sessions and staff-file `rule_roles`
cannot grant write authority. Existing `X-ZF-CSRF: 1` protection applies.
The canonical provisioned email is retained, not a claimed email or display name.
Having both capabilities never permits self-approval.

These are code-level contracts, not tenant role assignments or legal delegation.
The ingress must validate principals and prevent direct access; local synthetic
principal tests do not verify signatures or hosted ingress. Legal/Compliance/DPO
owner nomination in #209 is not approval of any card. Approval events remain
explicitly simulated, and non-exercise cards remain refused. Legacy display-name
events are preserved verbatim and do not confer new email-bound authority.
Rule-engine integration, a rule-card UI, real card/legal approvals, real tenant
assignments and SQL Server/Azure acceptance are not delivered by this slice.
The current infrastructure registration script/manifest defines only workbench
roles; adding and assigning the two dedicated rule capabilities is still an
explicit administrator deployment follow-up, not an implicit role grant.

The local app exercise in `tests/test_auth.py:RuleHttpTests` starts a loopback
HTTP server over temporary synthetic data, checks health and app responses,
executes the lifecycle and deny matrix, reopens persistence, then stops the
server and removes its temporary files. Run it from `src/api`:

```bash
PYTHONPATH="$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests" \
  python3 -m unittest tests.test_auth.RuleHttpTests -q
```

## Stock reconciliation API (#84)

`POST /api/cases/{id}/stock-reconciliation` records an unresolved staff query:

```json
{
  "field": "epc",
  "query_owner": "sam@example.test",
  "left": {
    "value": "D",
    "source_id": "SYN-REGISTER-84",
    "date": "2026-01-01",
    "version": "1",
    "validation_state": "Unvalidated"
  },
  "right": {
    "value": "E",
    "source_id": "SYN-SURVEY-84",
    "date": "2026-02-01",
    "version": "2",
    "validation_state": "Disputed"
  }
}
```

The example is constructed, not a real home. Allowed fields are `epc`, `type`
and `built`; the owner must be registered non-contractor staff. Each assertion
needs exactly the shown fields; validation is `Unvalidated`, `Validated`,
`Disputed` or `Unknown`. Dates cannot be future; EPC is A-G, build year an
integer and home type bounded text. Equal values and identical source/version
pairs are rejected. The authenticated session supplies recorder identity.
Invalid inputs return 400, unauthenticated requests 401, denied roles/bulk
requests 403. The response is the projected case detail; contractors receive
neither comparisons nor technical decisions.

Opening additionally requires the registered case owner or programme/manager
role. Staff role membership alone does not grant responsibility for every case.

`POST /api/cases/{id}/stock-query-event` appends a disposition:

```json
{
  "query_id": "SQ-1",
  "action": "withdraw",
  "reason": "Duplicate of another recorded query"
}
```

The original raiser or a programme/manager role may withdraw. For a human
reconciliation attestation use `"action": "resolve"` and add a nonempty
`"evidence": "SYN-HUMAN-REVIEW-84"` reference. Resolution is restricted to
registered named humans with the existing Retrofit Programme Manager or
Programme Support Officer role. The server binds identity from the session,
not the body; agents cannot resolve or sign off. Every disposition needs a
reason, refers to a query on this case and is terminal. Invalid/repeated
dispositions return 400; unauthorized requests return 403.

The response derives each query's current `Unresolved`, `Withdrawn` or
`Reconciled` status and retains the separate `stock_reconciliation_events`
history (event ID, query ID, status, action, reason, optional evidence,
timestamp and recorder identity). The original comparison remains unchanged
in storage. The read-only panel shows the status and human event provenance.
Only unresolved queries block technical approval; disposition never releases
other stock, safety, building or independent approval gates. No source or
home field is automatically selected/updated. Source-authority, resolution
rules and eligibility stay Unknown/owner-approval-needed, not an approved
operational reconciliation policy.

The case view displays both values, source metadata and query owner, with
authority/resolution/eligibility explicitly `Unknown`. A different case shows
its own comparisons, never a carried-over rationale. Existing technical forms
record named human decisions, not AI approval; separate sign-offs show the
design version each person reviewed. Conflict, building and hazard holds reuse
the [core controls](../core/README.md#stock-comparisons-and-human-technical-sign-offs-84).
No stock source wins automatically, no resident decision is inferred and no
case is silently excluded or automatically reprioritised.

Support status and input coverage are explicit in staff detail/list. Missing
flags are `Unknown`, not `"None"`; compatibility Boolean notice indicators
still represent observed support only. Existing governed AI proposal paths
remain available, with release admission and human approval unchanged.

Local synthetic HTTP tests run from `src/api`:

```bash
PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_stock_reconciliation_api.py' -v
ZF_STOCK_BROWSER=1 PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_stock_reconciliation_api.py' -v
```

The second command requires the existing development Playwright dependency
and Chromium. It runs the real loopback application with synthetic SQL state,
checks rendered values, source metadata, owner, Unknown labels, heading/keyboard
access and navigation to another case. The default unit suite skips that
opt-in browser method. This is engineering evidence, not direct human
accessibility/competence acceptance, live inference, SQL Server or Azure proof.
Source-authority/resolution/eligibility rules, operational delegation and
real-platform acceptance remain unmet; nomination/tenure routing is separate.

A working case-management application for the Zava Forward retrofit programme.
It follows the simplicity requirements SA-001 to SA-010 in the
[PRD](../../docs/prds/zava-forward-retrofit-programme-demonstrator.md) and the
[prototype learnings review](../../docs/reference/research/ux/prototype-learnings-and-simplicity-review.md).

This file is the former `mvp/README.md` (ADR 0006, issue #199, M6), split by owning project. It keeps
the staff-facing behaviour, configuration, sign-in, local run, honest limits and container checks of
the `api` project. Domain modules are documented in [core](../core/README.md) (law store, rule cards,
SQL stores, governance, ledger, chat storage, continuity and synthetic tools), the ledger digest job in
[orchestrator](../orchestrator/README.md), and the assistants, AI evaluation harness and dated
assistant validation record in [agents](../agents/README.md). The index of projects is
[src/README.md](../README.md).

Paths such as `tests/test_x.py` and `web/` below are relative to `src/api/` unless a `src/` path is
given. Module names without a path (`store`, `ranking`, `projection`, `quality`, `procurement`,
`finance`, `documents` and so on) are `zava_forward.core.<module>` in `src/core/src/zava_forward/core/`.
Run the suites from `src/api` with
`PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests`, after
`pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator`. When `ZF_DATA` is not
set, the data file defaults to `~/.zava-forward/data/zavaforward.json`, outside
the checkout. `ZF_DATA` accepts an explicit JSON file or a data directory;
an explicit filename is preserved. Runtime and generator resolve the same folder.

## Resident decisions and representative API (#86)

The resident panel records only supplied human decisions. Answer and answered-by
selectors start blank; the displayed default is `Not recorded`. The historical
case-wide answer is labelled as history, with no consent editor; its legacy
`decision` endpoint remains role-checked history only and cannot release work.
First record a technical design, then the exact measure scope and source.
The [core contract](../core/README.md#resident-decisions-and-representatives-86)
defines currentness, authority, release dependencies and evidence limits.

Authenticated resident-workflow staff use `POST /api/cases/{id}/resident`:

For decision/scope/authority/safe-contact recording and disclosure checks,
only registered named Liaison Officers (Neighbourhood/Resident Engagement) and
Retrofit Coordinators may write. Managers and Programme Support view only;
their attempts, including the legacy `decision` route, return 403. Existing
complaint/redress actions retain separate named-owner restrictions. The panel
uses server-projected `can_record_resident`, rather than treating every manager
as a resident recorder. Other staff do not receive private evidence narratives.
Contractor detail contains `resident_readiness: [{"measure": "...", "flag":
"Proceed"}]` (or `Hold`), never decision reasons, wishes, authority or safe routes.
Unrelated vulnerability restrictions remain unchanged for staff.

Staff detail includes `resident_retention`: five calendar years from first
recorded resident contact, including withdrawal and expired authority. Unknown
first-contact history is explicit. `GET /api/retention` includes due
`doc_id: "resident-decisions"` entries for manager review. A manager posts
`{"id": "resident-decisions"}` to `/api/cases/{id}/retention-approve` to remove
the current resident payload; legal hold returns 403, not-yet-due or unknown
origin returns 400. At expiry, work and representative disclosure reliance hold
even before deletion. See the [core retention contract](../core/README.md#resident-decisions-and-representatives-86)
for the exact deletion inventory and ledger/backups/cross-case limitations.

| `action` | Required input and control |
| --- | --- |
| `scope_record` | `measure`, `scope`, integer current `design_version`, `source`; creates a new context revision and no answer |
| `decision_record` | `measure`, integer `context_revision`, supplied `status`, `answered_by`, `source`; `note` for decline/pause/withdrawal; `representative_ref` for representative; `review_ref` when accepting after a review flag |
| `safe_contact_record` | Resident-confirmed `safe_contact_ref`, supplied `source`; increments contact history, does not send anything |
| `representative_record` | `representative_ref`, `measure`, integer `context_revision`, `status`, `tasks`, `source`, `authority_date`, `review_date`, `resident_wishes`, current `safe_contact_ref`; appends authority version |
| `disclosure_check` | `representative_ref`, `measure`, integer `context_revision`, `task`; checks current task authority only, sends nothing |
| `service_open` | Existing service fields (route, summary, desired outcome, handler/redress owners, next update); `Independent review` also needs `review_measure`, integer `review_decision_version`, `review_reference` |
| `service_update`, `service_close` | Existing request ID/status/update/outcome; independent review is update/close-only for its named independent reviewer |

Answer statuses: Waiting, Accepted, Declined, Paused, Withdrawn. Authority
statuses: Confirmed, Unclear, Disputed, Revoked. Tasks: Receive information,
Communicate, Attend, Works decision. Review and authority dates use YYYY-MM-DD;
authority cannot start in the future, review follows evidence, and reliance
stops on the review date. The UI records one task per authority version; the API
supports a list of evidenced tasks. Register separate task/scope authority
references when multiple active authorities are needed; latest version of each
reference is authoritative, never the most recent representative globally.

The API ignores forged recorder/actor fields. Missing/stale/invalid context,
source or authority returns 400, wrong staff/reviewer role returns 403, and
blocked controlled release returns 409. `disclosure_check` is not a send token:
no downstream transport consumes it and no message is sent. Legacy
representative-addressed templates remain refused; authorized staff AI
proposals are non-addressed drafts and still require human review.

Work-order issue/reissue/correction requires `resident_bindings`, for example:

```json
{"resident_bindings": [{"measure": "Loft insulation", "context_revision": 1}]}
```

The manager UI accepts `Measure|revision; Measure|revision`, with no inferred
binding from free-text scope. Booking/completion checks the saved version.
Quality evidence accepts an explicit integer `context_revision`; unbound
evidence can be recorded via the API but cannot be accepted or handed over.
The quality UI asks which scope revision the evidence covers. A withdrawn
sibling cannot block an explicitly independent bound work order or QA record.

Complaints and independent review stay available after pause/closure and AI
failure. They record an owned request, not delivery to the association's formal
complaints service. The panel directs staff to the named officer and accessible
non-digital route without inventing a real complaints URL, response timetable
or delegation. The real route, human independence/accessibility and
without-detriment acceptance remain unproven.

`tests/test_resident_api.py` starts the actual app on loopback with synthetic
staff/home data and SQLite, checking health/static assets, authentication,
decisions/withdrawal, redress, authority/privacy and restart. Core semantic tests
also use a synthetic AI adapter, not live model inference. Real inference,
SQL Server/Azure and human acceptance remain unmet; no private data or new
deployment is used. Docker build/run depends on CI when local daemon access is
denied.

## RAI task release API (#219)

`GET /api/assistants` now includes role-filtered `registered_tasks` for the
merged eleven-task registry: intended/prohibited use, stakeholders, current
`binding`, selected `release` (ID/version/digest), structured `release_denial`
and the explicit OQ-017 authority gap. Existing five-assistant fields remain.
Configured JSON-store AI denies without durable SQL release evidence; use
SQLite locally or Azure SQL for deployment, not a JSON bypass.

`POST /api/assistants/releases` uses the existing authenticated Programme
Manager plus `ZF_ASSIST_RELEASE_APPROVERS` allowlist. Copy the task's current
binding and supply the [core contract](../core/README.md#task-bound-rai-release-records-219)
fields, `task` (assistant ID or `legacy:<retained-task>`), `evidence_class`,
`serving_model`, residual-risk note and future ISO expiry. The server records
the authenticated approver, never a client-supplied approver identity. Posting
a replacement revokes previous active records for that task across endpoints
and deployments; it does not overwrite historical proposals. Suspend/revoke
routes are unchanged; restart requires a newly recorded release.

Denials expose missing evidence, the unappointed authority/project contact and
manual route, and persist in assistant events or the legacy audit/comparison
record. Web draft notes show the denial reason. Superseded priority proposals
are visibly non-actionable; server-side accept/edit checks remain authoritative.
Release does not grant sending, works consent, safety, financial or domain-write
authority. It permits bounded proposals that still require human review.

Local synthetic HTTP exercise (no real AI, Azure or private data):

```bash
cd src/api
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest \
  test_assistants.ApiTests.test_release_record_local_http -v
```

This starts the real App on an ephemeral loopback port, checks health,
authenticated registry/release/invoke/detail/revoke routes, zero calls while
denied, one nonbillable scripted provider call when released, unapproved output
and unchanged domain state. It shuts down the listener and removes its temporary
synthetic files. Direct human, live model and Azure acceptance are not implied.

## Hazard referral and retrofit hold API (#85)

Authenticated staff use the existing safety panel on open or closed retrofit
records. It labels observations as unverified, shows source/awareness, referral
destination, follow-up owner, whole-home hold scope, separate sent/received/
accepted evidence, external service response/resident-update times and explicit
unknowns. It sends no referral or resident communication itself. Use the
existing hazard service directly for urgent concerns; neither AI nor a
retrofit hold may delay that route.

| Path after `/api/cases/{id}/` | Body and control |
| --- | --- |
| `hazard-raise` | Reported `category`, `priority`, optional `note`, required `source`, timezone-aware `aware_at` not in the future; staff, including closed retrofit records |
| `hazard-refer` | `index`, `to`, external case/job `job`, sending `evidence`; staff; prospective binding for active legacy records |
| `hazard-receive` | `index`, receipt `evidence`; named safety receiver, once |
| `hazard-accept` | `index`, acceptance `evidence`; named safety receiver, after receipt, once |
| `hazard-times` | `index`, external timing `evidence`, at least one of timezone-aware `response_due_at`, `responded_at`, `resident_update_due_at`, `resident_updated_at`; accepting receiver; no overwrite |
| `hazard-repaired` | `index`, external repair `evidence`; accepting receiver; observation only |
| `hazard-release` | `index`, release reason `note`, external supporting `evidence`; independent safety-role actor, after repair evidence; home retrofit hold only |

Missing evidence/invalid state or index returns 400; wrong role/receiver or
non-independent release returns 403. Active holds return 409 on controlled
retrofit progression. No classify, pause-clock, reset-clock or close-hazard API
exists. Server-supplied actors and home scope ignore forged client authority.
All actions are manual, one-case decisions; consent and other home/building
gates stay independent. See the [core contract](../core/README.md#hazard-referral-and-home-retrofit-holds-85).

The listed release-role checks are demonstrator safeguards, not ratified
release authority. Repairs, Safety and Housing owner approval of release
responsibility, response/resident-update timing and escalation policy remains
outstanding (RV-002). Human-recorded due times do not establish an approved
service timetable. These acceptance criteria remain unchecked.

`tests/test_hazard_api.py` runs a real HTTP application on loopback with
fictional staff/home data and SQLite state. It exercises health/static serving,
authenticated closed-record intake, receipt/acceptance/timing/repair/release,
role isolation, legacy binding and restart durability. This is local synthetic
application evidence, not real model inference, verified service transport,
SQL Server durability, Azure deployment or human/browser acceptance.
The existing AI release and human-review gates are unchanged; no fallback or
model output can waive a hold. Full #85 acceptance and the mandatory
real-platform application exercise remain unmet without the outstanding
owner/live evidence. Docker image checks are delegated to CI if the local
daemon is inaccessible.

## Design-system foundations (#150)

The [design-system inventory](../../docs/reference/research/ux/design-system.md)
records the owner's Fluent UI (Fluent 2) adoption decision, the sourced token
mapping, seven component states and AI draft-review boundaries. This is a partial
native-foundation/non-colour slice, not a completed Fluent UI runtime migration.
Markers use circle/O, square/W and triangle/! with matching key and status names.
Clusters show home and safety counts (including zero); filter tiles visibly say
"Selected". Overview data tables use named keyboard-scrollable regions on narrow
screens. Existing consent, approval, AI and server authority are unchanged.

From `src/api`, after installing the projects and `.[dev]` with pip:

```bash
python -m playwright install chromium
python -m checks.design_system_browser_check
```

This check starts the real API on a temporary loopback port against 505 fictional
homes from the shared test fixture. Real map APIs exercise point and cluster modes;
only basemap tiles are replaced by a synthetic pixel, so no external tile service
or private dataset is used. It checks rendered tokens, non-colour signals,
keyboard navigation, 320/390/1280px reflow, forced colours and reduced motion.
The source API CI job runs it with pinned Playwright as a development-only
dependency; production requirements/images do not gain a browser dependency.
Human/screen-reader acceptance, full Fluent component integration and live
AI/SQL Server/Azure validation are not established by these local checks.

## Shared workbench information architecture (#152)

`/api/me` includes `navigation` entries with `href`, `label` and `scope`,
computed by the API from existing endpoint/Finance/manager rules. The client
renders these entries without a new role map. Metadata is not authorization:
direct API calls retain all existing server checks. The default remains the
signed-in person's assigned cases, or assigned contractor jobs; programme
directories and overview are explicitly labelled broader scopes. There is no
role simulator. No role-specific screen redesign or new permission is included.

The shell has a keyboard skip link, named navigation, visible/semantic current
destination and a persistent scope/result announcement. Each staff case row has
one case-opening link, plain recorded status and a recorded next action, not an
AI-invented workflow decision. Cases open full screen. Back to the list keeps
the last mine/all scope and filters, but deliberately reloads page one: it does
not promise restored pagination, selected row, scroll position or row focus.
Direct case entry falls back to the own queue.

"Reset my queue" clears search, stage, authority area, wave, owner, flag, work queue, sort
and all-cases override; it restores own cases in the existing safety-first
policy order, focuses the reset control and announces refreshed results.
Obsolete loads/debounce are cancelled on route replacement; failed loads show
an explicit retry, and session expiry returns to sign-in. An empty own queue
is distinguished from no filter matches. Reset does not modify records.
Cancelling a pending briefing invalidates its cached panel so the next queue
requests it again; a completed briefing remains cached. Briefing failures show
an explicit retry. The browser check holds responses across My cases -> All
cases -> My cases and verifies recovery without stale-response replacement.
Safety reports and stopped-work details remain expanded ahead of routine case
forms, with existing named owners, external timings and explicit unknowns.
Contractors retain their minimum-necessary projection, not staff safety data.

The versioned [shared-IA manifest](./checks/workbench-manifest.json) declares
eight implemented auth roles, exact synthetic own queues/navigation and all
eleven PRD perspectives/nine workflows with partial or deferred coverage.
It is not full AC-034/043, accepted role mapping or validated user research.
From `src/api`, using the installed src packages and `.[dev]`:

```bash
python -m checks.workbench_browser_check
python -m checks.design_system_browser_check
```

The second command is the existing CI entry point and runs both browser suites.
Each starts and stops its own healthy loopback API with constructed data in an
automatically cleaned, ignored repository-root `.venv/` scratch subdirectory;
no credentials, model endpoints or private data settings are inherited.
The IA checks cover eight roles, mine/all/reset/back/history, delayed and failed
requests, expiry, contractor projection, queue/case reflow at 320/390/768/1024/
1280 CSS pixels and 200% root text enlargement. This is Chromium engineering
evidence, not browser-zoom, screen-reader or human acceptance. The baseline
also exercises return from a queue with more than 50 rows.

Supported devices/browsers and field/mobile use still need the owner's
decision. The full eleven-profile/nine-workflow journey manifest remains
incomplete. AI routes, real-provider configuration and human review/release
gates are unchanged; the isolated checks make no live model call and do not
satisfy mandatory real-inference/SQL Server/Azure exercise acceptance.
No SQL, deployment, resident consent or controlled approval behavior changed.
Local Docker access was permission denied; image evidence must come from CI.

## Role task queues and shared case context (#76)

This is a bounded offline extension of the existing role workbench, not a new
identity provider, role simulator, permission policy or operational acceptance.
The [parity audit](../../docs/architecture/mvp-to-src-parity-matrix.md#role-task-queue-offline-slice-2026-10-16)
records each issue criterion before and after the change. The authenticated
role still determines access; own/all scope, queue, search and other filters
intersect and never grant rights.

Staff `/api/me` now publishes `work_queues`: version `work-queues-1`, six
definitions, availability/limitations, default filter state and null selection.
The single existing reset consumes that server default, restores own cases in
the existing deterministic order on page one, focuses itself and announces
scope, all filters, version and result count. No case is selected automatically.
No changes to records, ranking, assignments or approvals result from filtering
or reset. No matches and no assigned open cases remain distinct.

`GET /api/cases?queue=new` and `/api/cases.csv?queue=new` use the same filter
before totals, ordering and pagination. Other filters/sorts still apply.
Unknown queue IDs return 400 on both endpoints; an unavailable approved-priority
queue returns an empty result, with its explanation in the visible definitions.
Contractors cannot use staff queues and receive no new context or staff metadata.

| Queue ID | Visible definition and source |
| --- | --- |
| `new` | Current `stage_since` is between zero and seven days old, inclusive. This describes arrival in the current stage, not case creation. |
| `priority` | Open cases under an explicitly approved ranking policy with a named owner. The existing policy is draft, so this queue is unavailable/empty. Accepted AI advice never qualifies as approved programme priority. |
| `stale` | Last supplied EPC record's `documents.at` is older than 30 days, Survey older than 180 days, or a technical sign-off explicitly needs reassessment. Record timestamps are review triggers, not certificate expiry or proof of source validity/currentness. |
| `blocked` | Existing safety, unresolved stock and shared-building stops, plus unmet funding/resident/technical final-check prerequisites. Future-step prerequisites are labelled separately from current stops. |
| `overdue` | An outstanding recorded handoff acceptance, case resident-update or external safety-service response/update deadline is strictly before the snapshot. Each completion is checked independently; accepting a handoff does not complete a resident-update commitment. No deadline is invented from stage age. |
| `unowned` | Handoff Offered, Received or Escalated, with no accepted receiver. A proposed receiver is not a confirmed owner, and the sender keeps chase responsibility. Accepted/Completed/Declined/Withdrawn are excluded. |

Evaluation uses the dataset `as_of`, with date-only values interpreted at UTC
midnight. This reproducible snapshot is displayed, not presented as a live
safety-service clock. Missing, malformed or future observation/record dates
remain Unknown; timezone-less datetime values are Unknown. Future deadlines
are not overdue; equal deadlines become overdue only after the snapshot.
External timing authority remains with the existing hazard and repairs service.
Legacy `noticed` alone cannot establish precise awareness or elapsed hours.

Staff list/detail share the same `work` object: case/current owner, reason,
one next action, origin/evidence/version/snapshot, blocker step/reason/named
owner/responsible role/action, separate handoff owners, evidence-review status,
outstanding deadlines and recorded hazard-clock observations. Safety/stock/
building stops take precedence over a pending handoff, current-stage return
or final-check prerequisite. A role-only responsibility keeps named owner
Unknown; no person is assigned by inference. Missing next action prompts
the case owner to record it rather than fabricating a workflow instruction.

The case, current-context part of history, proposed-reviewer panel and
"Task sources" disclosure reuse this same object. Historical events retain
their event-time owner/reason; context refresh never rewrites those events.
Case switching cancels obsolete loads and binds the displayed context to the
selected case. Domain source comparisons and sign-off records remain intact.
Human-written reason/action/source aliases follow existing need-to-know rules
before serialization, including derived list/status fields; this does not
approve the operational role/redaction matrix.

The new core semantics/store tests and real loopback SQLite HTTP tests use
constructed data, exact threshold/lifecycle expectations and 120 interleaved
matching/nonmatching cases to verify pre-page filtering, cursor totals/order,
sorting and CSV agreement. The extended existing Playwright check exercises
the actual local app, all eight implemented roles, visible definitions,
queue membership, current-context agreement, case switching, delayed responses,
all-filter reset, focus/status and responsive layout. An alternate server
default proves reset is not hardcoded in the browser.

From the repository root, with `/tmp/zf164` already containing the project
development dependencies (pip only), for targeted checks:

```bash
ROOT="$PWD"
BASE="$ROOT/src/core/src:$ROOT/src/agents/src:$ROOT/src/api/src"
(cd src/core && PYTHONPATH="$ROOT/src/core/tests:$BASE" /tmp/zf164/bin/python -m unittest discover -s tests -p 'test_taskqueues.py' -v)
(cd src/api && PYTHONPATH="$ROOT/src/api/tests:$ROOT/src/core/tests:$ROOT/src/agents/tests:$BASE" /tmp/zf164/bin/python -m unittest discover -s tests -p 'test_task_queue_api.py' -v)
(cd src/api && PYTHONPATH="$BASE" /tmp/zf164/bin/python -m checks.workbench_browser_check)
```

Operational queue-definition ratification, named ranking-policy approval and
OQ-005/OD-14/OD-19 role/field/redaction/delegation decisions remain open.
These engineering checks do not establish direct human accessibility/usability,
real AI, SQL Server, Azure deployment or complete eleven-profile/nine-workflow
acceptance. Refs #76; the issue is not closed by this slice.

## Return and handoff API (#83)

All mutations below are authenticated, one-case human actions. The server
supplies authority and receiving/current owner; client-supplied authority or
owner fields cannot override them. Source references are human-recorded text,
not automatically verified evidence.

| Path after `/api/cases/{id}/` | Body and control |
| --- | --- |
| `return` | `to_stage`, `reason`, `source`, `next_action`; authorised staff, earlier stage only |
| `reopen` | `reason`, `source`, `next_action`; manager, closed case only |
| `offer-handoff` | `to`, optional `note`, `urgency` (Routine/Urgent), timezone-aware `due_at`, `next_action`, `resident_update_to`, `resident_update_due_at`; owner or manager |
| `receive-handoff` | Empty object; named receiver, Sent only; not acceptance |
| `accept-handoff` | Empty object; named receiver, Sent/Received/Escalated |
| `decline-handoff` | `reason`; named receiver, Sent/Received/Escalated |
| `withdraw-handoff` | Empty object; sender or manager, Sent/Received/Escalated |
| `escalate-handoff` | `to` (manager email), `reason`; sender or manager, Sent/Received |
| `complete-handoff` | `note`; accepting current owner, Accepted only |
| `handover` | Legacy alias for an offer; never immediate reassignment |

`GET /api/handoffs` returns unaccepted work visible to the sender, receiver and
managers, including canonical `status` and separately labelled responsibility
fields. Persisted `state` keeps Offered/Declined compatibility; detail returns
versioned `returns` and `handoff_history`. Unauthorized or replayed transitions
return an explicit error without a transition. New return/reopen requests
without source/next action now fail with HTTP 400.

BG-010's approved-time escalation criterion stays unmet: due dates are
human-selected and escalation is manual; OD-09 policy and operational acceptance
are not available. No timer, automatic resident contact, live model effectiveness,
SQL Server result or Azure deployment is claimed by local synthetic tests.
AI assistance remains available under its existing configuration/release/human
review gates; this deterministic workflow adds no model authority.

## Building shared context (issue #75)

Staff can follow an explicitly linked home to `#/building/{building_id}` and
back to either linked home. `GET /api/buildings/{building_id}` returns the
[core source-backed model](../core/README.md#building-shared-context-issue-75),
with separate systems, dependencies, stopped-work reasons, works and shared
costs. Missing/unknown data is labelled, not interpreted as an approval.
Linked homes expose only their case ID, stage and closed flag in this view,
not resident details, home evidence, decisions or allocations.

Only existing staff roles can read buildings; contractors and unknown roles
receive 403, unauthenticated requests 401, missing records 404 and invalid
building data 400. Building costs and home `cost_allocation` are returned only
to the existing `FINANCE_VIEW` roles. Other staff see a restricted-cost notice,
with amounts omitted server-side. The building screen is read-only and cannot
approve, instruct works, release safety restrictions, contact residents or pay.
Home AI assistance remains available through its existing proposal-only and
human-review paths; shared free text and costs are not added to prompts.

`tests/test_buildings.py` starts the real application on loopback with a
wholly fictional two-home SQLite fixture. It checks health/static serving,
authenticated navigation, role/amount isolation, scoped blocked advancement,
unaffected sibling advancement and availability of the existing assistant
registry. No live model inference, Azure deployment, actual SQL Server or
human/browser accessibility acceptance is implied. There is no register
editor or automatic retrofit of building data into an already populated store.

## What staff see

* Sign in once and land on "My cases today", with open safety issues first.
* A full-screen case card: contact details, preferences and support needs, a
  plain status line, owner, contractor, next visit and history.
* Log a call, record the resident's own answer, hand a case to a colleague and
  draft a message. Nothing is sent automatically.
* "Ready to book" is checked on the server: the resident's decision, funding
  and any open safety issue must all be confirmed. Unknown never passes.
* Filter the list by stage, local authority, wave, owner or flag, and sort by
  urgency, longest wait, last contact, name or next visit.
* The default "Most urgent first" order is a deterministic ranking
  (`src/core/src/zava_forward/core/ranking.py`): open safety issue, then priority support or an
  adjustment, then longest time in stage, then earlier stage, then case id as
  the fixed tie-break. Each card shows its rank and plain reasons, the list
  header shows the policy version, policy hash and as-of date, and
  `GET /api/ranking/policy` returns the versioned rules. The rules live in
  versioned files in `src/core/src/zava_forward/core/policies/` (for example `ranking-v1.json`) with a policy
  id, version, owner, status, effective date and a SHA-256 content hash over
  the canonical JSON. Every file is verified when loaded and a mismatch stops
  the load. Old versions stay in the folder and can be re-run. Ranking takes
  the case data, a policy and an explicit `as_of` date and reads no clock.
  `GET /api/ranking/snapshot?policy=1.0.0` (managers only) returns the
  snapshot: policy version and hash, as-of, and per case the rank, reason codes
  and deciding rule. It is also written beside the data when it changes. The
  policy owner is "to be named" and the rule order is an unsigned draft.
* "Suggest my top 5" on My cases asks AI for a second opinion beside the
  rule-based order, labelled "AI suggestion, not approved", with a cited reason
  per case. It is stored in a separate recommendations list and is never read
  by the ranking, owners, stages or queues. A person accepts, edits (untick
  cases) or rejects it, with a reason for edit and reject, and the answer goes
  in the audit log. Without a model a rules-based template is used.
* The case list loads 50 at a time ("Show more"; the API allows up to 100 and
  returns the total). The Overview map is requested by viewport and shows grid
  clusters with counts when more than 500 homes are in view. List and map totals
  agree for the same filter. The CSV download still returns the whole filtered list.
* Filters sit in a left panel and update the list without reloading the page.
  The briefing is cached until case data changes.
* Overview: counts that filter the map when clicked, a zoomable OpenStreetMap
  of open cases (Leaflet bundled in `web/vendor`; circle/O normal, square/W waiting
  60+ days, triangle/! open safety issue; status names and matching list),
  charts by stage, authority, wave and waiting time,
  contractor and team workload. Visits lists booked appointments by day.
  The dated synthetic generator now guarantees six additional forward
  assessment visits and retains historical attended/no-access/cancelled
  contrasts. See the [coverage recipe](../../docs/reference/research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13)
  for reproducible dates, queue counts, private outputs and safety limits.
* "Who could take this on": top three colleagues with plain reasons (role
  fit for the stage, current workload, who already knows the resident).
* AI assistance, always a draft for a person: a morning briefing, a drafted
  message, a "catch me up" summary, funding application wording, and reading
  an uploaded document. It runs on Azure OpenAI through the managed identity.
  Output is checked, every run is audited, and a plain template is used when
  the model is unavailable. Each output carries source citations that must
  resolve to a real field or record of the case (for example "Stage: Survey
  booked", "Case history 2026-09-30"). They are checked on the server: output
  whose citations do not resolve is marked Unverified, uncited summary bullets
  and uncited priority items are dropped, and the sources are shown beside the
  "AI suggestion, not approved" label. Output stays "Not reviewed" until a person accepts, edits or
  rejects it. Workflow-only mode (request flag `mode: "workflow"`, the "Workflow
  only" tick box, or `ZF_AI=off`) skips the model for every task and is
  recorded. Each task leaves a comparison record (case ids, AI output,
  workflow-only output, fallback reason, reviewer action and override) in the
  recommendation store, in both the JSON and the sqlite store.
* Documents: upload pdf, png, jpg, docx, xlsx, csv or txt (5 MB), see an
  evidence checklist (EPC, survey, design, consent) and download files.
  Every upload is scanned before it can be downloaded or read by the document
  assistant (`doc_controls.py`; `ZF_SCANNER=local|defender`). The local scanner
  is a labelled synthetic test: a marker and a type check, not an antivirus
  engine. The Defender scanner reads the Defender for Storage blob tag through a
  fake transport only, and a pending result keeps the file unavailable. A
  programme manager lists documents past their retention trigger
  (`GET /api/retention`), approves each deletion (`retention-approve`) and can
  place or release a case legal hold (`legal-hold`, `legal-hold-release`); a
  hold blocks deletion. Periods are synthetic-demo placeholders, not an approved
  schedule, and the deletion log keeps no file name or content.
* Funding: a person moves each application through draft, approved,
  submitted and confirmed. Approval needs complete evidence and the Grants
  and Evidence Officer or a manager. The system never submits anything.
* A hash-chained audit log records every change. `GET /api/audit-check`
  (manager) and `python -m zava_forward.core.ledger` verify the chain; a digest of
  the head can be written to `ZF_DIGEST_DIR` (`POST /api/ledger/digest`) and is
  re-checked on verify. The digest is a local file, not yet an immutable Blob.
* Role-based field projection is enforced on the server (`projection.py`).
  Contractors see only their own cases with "needs notice" and a named contact
  (the case owner), never the vulnerability reason, resident name or contact
  details. Staff see the reason only for the roles in `ZF_REASON_ROLES`
  (default Resident Liaison Officer, Building Safety Liaison, Retrofit Programme
  Manager); others see "Extra support noted". Every role is tested against every
  endpoint (`tests/test_role_matrix.py`, plus `tests/test_role_endpoint_inventory.py`,
  which fails when a server route is missing from its inventory and checks
  contractor canaries across API, CSV export, search, audit and AI prompts).
  Free-text notes (decided for the exercise): no pattern redaction, which gives
  false assurance. Free-text fields are excluded by allow-list from contractor
  responses and AI prompts, and roles without a recorded need see "Held for
  roles with a recorded need" for contact notes and outcomes, appointment and
  hazard notes. The reason-role list remains a proposal (OD-14, OD-19).
* Workflow screens on the case page: return to an earlier stage or reopen a
  closed case (manager), recording reason, source reference, next action,
  authenticated authority and existing receiving owner. Offer, record receipt,
  accept, decline, manually escalate to a manager, withdraw or complete a handoff.
  Receipt does not imply acceptance; the sender keeps case/chase ownership until
  the named receiver accepts. Pending sender/receiver/manager work lists and case
  detail distinguish accountability, destination, proposed/confirmed receiver,
  chase owner, urgency, due date, next action and resident-update commitment.
  Missing values remain unknown; no message is sent automatically. Existing
  resident-update commitments survive every transition and subsequent offers.
  Safety referral has separately evidenced receipt/acceptance and an
  evidence-backed independent home-hold release; see the #85 contract above.
  All actions use server-side checks; the old `handover` endpoint now offers
  rather than immediately reassigning. See the [core contract](../core/README.md#return-reopen-and-handoff-accountability-83).
* Contractor screens: "My jobs" and a job page show only the address, stage,
  next visit, "needs notice" and a named contact. The server projects the data
  (`projection.py`); the screens never request resident detail. The rank and
  reasons are not sent to contractors either.
* Quality acceptance (FR-017, `quality.py`): per measure, evidence against a
  versioned checklist (every check needs a note of what was seen), then accept
  or return with a defect and an owner, fix, reinspect, resident handover and
  aftercare notes. States move one step at a time on the server and are
  audited. Whoever accepts must differ from whoever submitted, recorded or
  fixed the work, and nothing is accepted automatically. Provider submissions
  are stored as evidence only.
* Procurement and capacity (FR-016, `procurement.py`): packages with period,
  versioned scope and contract reference; offered capacity kept apart from
  capacity committed with evidence; controlled work orders (each change a new
  version with its issuer, none issued beyond evidenced commitment);
  appointment outcomes, completion and correction. Managers get "Capacity and
  work orders"; contractors see only their own orders, with "needs notice" and
  no reason. Packages and orders are held as one document in the JSON file or
  the sqlite `meta` table, so they work in both stores.
* Documents sit behind a `DocumentStore` interface (`documents.py`). The local
  filesystem store is the default (`ZF_DOC_STORE=local`, `ZF_DOC_DIR`). The Azure
  Blob store (`ZF_DOC_STORE=blob`) uses urllib against the Blob REST API with a
  SAS token (`ZF_BLOB_SAS`) or a managed identity token (`ZF_BLOB_CLIENT_ID`
  optional); config is `ZF_BLOB_ACCOUNT_URL` and `ZF_BLOB_CONTAINER`. Uploads
  allow an extension list and 5 MB, need a staff role (contractors cannot
  upload or download) and write audit entries for upload, download and failure.
* The map has a "Show the map areas as a list" alternative: a keyboard and
  screen reader list of clusters (zoom in) or homes (open case), with a polite
  live status line. The tile provider comes from `ZF_TILE_URL` (https only) and
  the CSP follows it. With `ZF_ENV=production` and no `ZF_TILE_URL` no tiles
  load and only the list works.

* Staff time capture (PR-004) is off by default. It records only when
  `ZF_TIME_CAPTURE=on`, `DPIA_APPROVED`, `ZF_TIME_CONSULTATION` and
  `ZF_TIME_NOTICE_APPROVED` each hold a reference, one manager has requested
  enabling (`POST /api/time/request-enable`, audit
  `time_capture_enable_requested`) and a manager in a different role has taken
  the audited enabling action (`POST /api/time/enable`, audit
  `time_capture_enabled`, which names the requester; void if a reference later
  changes), and the person has acknowledged the staff notice
  (`POST /api/time/acknowledge`, audited); own entries only; screens at `#/time`;
  reports are manager-only, aggregated and suppress groups under
  `ZF_TIME_MIN_GROUP` (default 5). The enabling record, entries and
  acknowledgements are tables (`time_request`, `time_enabled`, `time_entry`,
  `notice_ack`) in the shared SQL store (SQLite, or Azure SQL with
  `ZF_STORE=mssql`), apart from case data, with portable DDL. Only the JSON demo
  store falls back to a local SQLite file (`ZF_TIME_DB`). Why the requester and
  the enabler differ: one role should not both propose and switch on monitoring
  of staff. The demo data has a single manager role, so enabling there needs a
  second user with the `Programme Support Officer` role (Entra app role
  `ZavaForward.SupportOfficer`); the status reason says so.
* Download any list for Excel, and check a spreadsheet: columns are matched
  for you, rows to fix are listed and the file is never changed.

* Finance, grants, sign-offs and resident decisions (FR-018, FR-019, FR-013,
  FR-014; code in `finance.py`, `grants.py`, `signoffs.py`,
  `resident_decisions.py`, `controls.py`):
  * Budgets, commitments, invoice or valuation intake, line-level match
    exceptions, payment holds and a Finance decision are recorded per case
    (`POST /api/cases/{id}/finance`, queue at `GET /api/finance`). Nothing is
    ever paid; payment status is a note. Unknown inputs (no budget, no
    milestone evidence) block a match.
  * Grant stages (opportunity, award, claimable, submitted, accepted or
    rejected, cash received) are kept apart from invoices, each with a source
    and a second approver (`/grant`; also shown in the funding list).
  * Assessment, design, building and coordination sign-offs by separate roles
    with a design version; a design change sends only the affected sign-offs
    back for human reassessment, and missing items join the "ready" checks
    once a design is recorded (`/technical`).
  * The resident's answer is recorded per measure with versions, pauses and
    withdrawals, starts as "Not recorded" and is never inferred; service and
    complaint requests carry a desired outcome, a redress owner and coded
    contact needs (`/resident`).
  * Whoever prepares an approval cannot give it, and these refuse any bulk
    request. Contractors get none of it and other staff roles do not see
    finance or grant detail.

## Conversation panel (issue #159)

An optional, collapsed panel on the case card ("Ask the assistant about this case") for staff roles that may chat.
It is never needed to finish a task: every ordinary control stays on the page and works when chat is refused or
the model is down.

* `POST /api/chat/threads/{id}/ask` returns `{kind, reply, citations, label, model, workflow_only}`. The logic is
  `zava_forward.core.chat_panel` (core); the provider call is `zava_forward.agents.chat.ChatModel` (agents),
  composed in `server.py` in process until #144. Thread storage, consent gate (`CHAT_DPIA_REF`,
  `CHAT_LAWFUL_BASIS_REF`, `CHAT_NOTICE_REF`), redaction and per-user isolation are the merged #160 to #163 code.
* Every turn re-reads the staff role and the case through the user's own projection, so a revoked role or a case
  out of scope stops the next turn (403 or 404).
* Citations are ids of the projected case facts (`ZF-1/stage`). Uncited or unknown citations are dropped; with none
  left, or no case facts, the panel abstains and says so. Every reply carries "AI suggestion, not approved".
* A model failure (`disabled`, `timeout`, `provider-unavailable` or an unusable reply) returns `kind: fallback`,
  `workflow_only: true` and a plain message. A reply that carries tool or record-change syntax is withheld.
* `POST /api/chat/threads/{id}/proposals` with a `capability` calls the existing `Assistants.invoke`, so the request
  follows the existing source check and independent role review. The chat has no other write path.
* Web: `web/chat.js` (a `details` disclosure, a labelled form, an `aria-live="polite"` log and a `role="status"`
  line). Tests: `tests/test_chat_panel.py`, `core/tests/test_chat_panel.py`, `agents/tests/test_chat_model.py`.
* Not evidenced here: a screen-reader test (needs a manual run with a named reader), a live model run (no Azure
  endpoint locally) and real chat data (DPIA, lawful basis and notice references are unset, so storage stays refused).

## Configuration

| Variable | Purpose |
| --- | --- |
| `ZF_STORE` | `json` (default), `sqlite` or `mssql` (Azure SQL, see below) |
| `ZF_SQL_SERVER`, `ZF_SQL_DATABASE`, `ZF_SQL_AUTH`, `ZF_SQL_CLIENT_ID`, `ZF_SQL_PORT`, `ZF_SQL_TRUST_CERT`, `ZF_SQL_TOKEN`, `ZF_SQL_USER`, `ZF_SQL_PASSWORD` | Azure SQL connection; `ZF_SQL_AUTH` is `msi` (default), `default`, `token` or `password` (CI container only) |
| `ZF_SQLITE`, `ZF_STATE`, `ZF_DATA`, `ZF_DIGEST_DIR` | database file, state folder, seed data, ledger digests |
| `ZF_AUTH` | `password` (dev, default) or `trusted-proxy` (Entra) |
| `ZF_ENV` | `production` refuses the password provider and the OSM tile default |
| `ZF_SESSION_KEY` | signs dev session cookies; set the same value on every replica |
| `ZF_ENTRA_TENANT_ID`, `ZF_TRUSTED_PROXY`, `ZF_ROLE_MAP`, `ZF_AUTH_EMAIL_FALLBACK` | Entra provider |
| `ZF_REASON_ROLES` | roles that may see a vulnerability reason |
| `ZF_TILE_URL`, `ZF_TILE_ATTRIBUTION` | map tile provider |
| `ZF_TIME_CAPTURE`, `DPIA_APPROVED`, `ZF_TIME_CONSULTATION`, `ZF_TIME_NOTICE_APPROVED`, `ZF_TIME_DB`, `ZF_TIME_MIN_GROUP` | time capture |
| `ZF_DOC_STORE`, `ZF_DOC_DIR`, `ZF_BLOB_ACCOUNT_URL`, `ZF_BLOB_CONTAINER`, `ZF_BLOB_SAS`, `ZF_BLOB_CLIENT_ID` | document store |
| `ZF_SCANNER` | `local` (default) or `defender` content scanner |

### Entra ID on Container Apps

Code: `auth.py`. The current demonstrator uses this provider in Azure;
the owner confirmed working workbench sign-in on 2026-10-12. Local tests and
provisioning checks do not substitute for each user's consent/acceptance.

* Create an app registration (single tenant) and define app roles whose values
  match the map (default `ZavaForward.Coordinator`, `.LiaisonOfficer`,
  `.ProgrammeManager`, `.Contractor` and so on, see `DEFAULT_ROLE_MAP`) or
  supply `ZF_ROLE_MAP` JSON. Assign users and groups to them.
* Enable built-in authentication on the Container App with "require
  authentication" so unauthenticated requests are blocked, and make the ingress
  the only route to the container so `X-MS-CLIENT-PRINCIPAL` cannot be forged.
* Set `ZF_AUTH=trusted-proxy`, `ZF_TRUSTED_PROXY=1`, `ZF_ENTRA_TENANT_ID` and
  `ZF_ENV=production`. The platform principal type must be `aad` or `Bearer`,
  from that tenant, with exactly one distinct mapped role; the role comes from
  the validated platform principal, never the staff file.
* Provision each staff record with the Entra object id (`oid`). Email matching
  is off unless `ZF_AUTH_EMAIL_FALLBACK=1`. Contractor guests need the same.
  Use the [tenant staff initializer](../../infra/README.md#tenant-staff-and-application-role-initialization)
  to reconcile enabled tenant members, app roles and SQL bindings together.
  It replaces current generated staff/owner labels while preserving workload
  codes and historical actors, then restarts the startup-cached roster.
  Assigning an enterprise-app role without this binding still fails closed.
* Sign-out redirects through `/.auth/logout` to the public welcome;
  "Use another account" instead enters `/sign-in?switch=1` directly with
  `prompt=select_account`, without signing out of Microsoft first. Choosing
  another account is deliberate, not automatic; cancelling need not clear
  the previous session. See [flow diagnostics and acceptance](../../infra/README.md#account-selection-and-safe-flow-diagnostics).
  State-changing requests need an
  `X-ZF-CSRF` header under this provider.

The public `/` page shows Zava Forward and its logo without loading workbench
scripts or data. Its button enters `/sign-in`; `/app` is protected. Production
session/role failures show Microsoft sign-in or an authorisation message,
never the local shared-password form.

The native account panel shows the authenticated Entra display name/email,
existing workbench role and own Microsoft profile photo. It does not rewrite
synthetic staff records or broaden contractor projections. Escape/outside
click closes the panel; keyboard focus and a 375-pixel layout are supported.
Missing photos/access errors display initials and an explicit status.

`/api/account/photo` authenticates and authorises the current user before
fetching the fixed Graph `/me/photo/$value` URL. The delegated platform token
stays server-side, redirects are refused, and timeout/type/signature/2 MiB
limits apply. There is at most one provider refresh attempt for token expiry.
See [staged token-store setup and permissions](../../infra/README.md#public-welcome-and-microsoft-account-photos).
This uses only delegated own-user `User.Read`, not tenant-wide application
photo access. Local password development shows initials without requesting
Microsoft tokens.

The CSP permits temporary `blob:` URLs only for images, so the server-proxied
photo can render; script/default/frame source permissions are unchanged.

## Run it locally

The working data is built from the private stock-geography register. It holds
real OpenStreetMap addresses with invented residents, contractors and staff, so
it is git-ignored, binds to loopback only and must never be committed, deployed
or shared. The repository must stay private.

```bash
python3 -m pip install --no-deps -e src/core -e src/agents -e src/api   # modules moved in M1 to M5 (ADR 0006)
python3 support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py --seed 20260901   # writes to ZF_DATA, default ~/.zava-forward/data/zavaforward.json
ZF_PASSWORD=choose-a-password python3 -m zava_forward.api
```

Open `http://127.0.0.1:8088` and sign in with a staff email from the data (for
example `aisha.rahman@zavanorthhomes.example`). Without `ZF_PASSWORD` a random
password is printed at start-up. The data builder shifts all dates so the
history ends today and prints no real personal data.

## Honest limits

Current scope is the continuing exercise, not production acceptance. Dated
earlier observations remain in the ADRs and pinned #58 evidence; they must not
be read as the current deployment state. The
[current infrastructure handover](../../infra/README.md#current-exercise-handover-2026-10-13)
records the tested/deployed image and identity initialization.

* The data is constructed. The generator (`zf_names.py`, `build_mvp_dataset.py`)
  makes names, phone numbers on Ofcom drama ranges and example email domains.
  The product screens do not say so; this README and the repository do.
* The 2026-10-12 rebuild ran the retained 980-case programme on real Azure SQL
  with workload-identity reads/writes, both real model tiers and restart
  persistence checks. Blob is the configured evidence store. Generated stock
  remains 60,000 homes; it is not 60,000 live SQL programme cases. No Azure
  load, full recovery, backup-restoration or production acceptance is claimed.
* Shared-password sign-in remains local development only; production rejects
  it. Azure uses built-in Entra authentication, app roles and explicit SQL
  staff bindings. The owner reports working administrator/Coordinator sign-in.
  A tenant-member Contractor allocation now exists, but browser acceptance
  for all roles, B2B guests, own photo and actual different-account replacement
  remains unproved. Unit principals and an anonymous chooser are not that proof.
  Contractor status text can still mention a safety stop and free-text notes
  are not redacted.
* AI needs `AI_ENDPOINT` (and optionally `AI_DEPLOYMENT`,
  `AI_DEPLOYMENT_STRONG`) and a managed identity with the Cognitive Services
  OpenAI User role. Both model tiers were exercised with `source=ai`; a
  template result alone is not real-inference acceptance. Nothing is
  sent; there is no live integration with housing or repairs systems.
* In development the map loads tiles from tile.openstreetmap.org unless
  `ZF_TILE_URL` is set. No licensed provider has been chosen or tested.
* Local development defaults to local state/documents; Azure selects the
  SQL/Blob backends through configuration. Do not apply local-disk durability
  claims to that deployment or infer tested Blob restoration/erasure from
  configuration alone. Upload checks are an extension list and a size cap:
  no content sniffing or malware scan. Local files/digests on Container Apps
  remain ephemeral and do not establish external immutable audit anchoring.
* Scale: the in-memory store handles 60,000 synthetic cases for filtered pages
  in tens of milliseconds (about 0.6 s for the first, cold ranking build). The
  sqlite store answers list pages, search, sorts and counts in SQL at 60,000
  cases in roughly 50 to 150 ms on a development machine. These are dev
  machine figures, not production latency, and not Azure SQL.
* The ranking policy is a hash-checked file but not signed off: no named
  owner yet. The hash detects edits, it does not prove who approved them.
  Snapshots are written when a manager requests one and the data has changed,
  as a file, not on every change or in a database table. The as-of date is the
  date the store was first loaded, and day counts come from the stored
  `days_in_stage`, not recomputed from it. AI value against the deterministic
  order is only captured as the overlap on each recommendation record.
* SQL Server parity tests and live Azure SQL checks supplement sqlite tests;
  neither establishes production scale or every full-workflow requirement.
  Lists, search, sorts and counts
  use SQL, but case detail, map, statistics, visits, facets, the CSV export,
  the closed list and every write still use the in-memory copy that is kept
  in step with the database. Keyset paging covers the default sort only.
* Quality and procurement: checklists are examples, not signed-off standards;
  there is no contractor login to submit evidence (a staff member records it on
  their behalf); capacity is counted in homes, not hours or money; procurement
  data is one document, so two managers writing at once get a conflict and
  retry; the screens were syntax-checked and exercised through the API, not
  run in a browser or with a screen reader.
* Time capture is enabled by environment references plus a requested and
  separately enabled audited action; the screens were exercised through the
  API, not in a browser. The staff notice text is a draft and the
  consultation reference is a flag, not evidence of the consultation. The AI
  evaluation uses a scripted model, so it checks behaviour, not model quality:
  latency, run-to-run variation and added value are scripted figures, not
  live-model measurements, and the golden cases are small and constructed.
  Citations prove a cited fact exists in the case, not that the claim made from
  it is right, and document reading cites the document record, not a passage.
* Browser checks: `src/api/checks/browser_check.py` drives the real server with
  Playwright (login, list with rank and reasons, show more, return, reopen,
  map list). It is run by hand, is not in the unittest run or CI, and was
  run in desktop Chromium only. No screen reader or mobile run was done.
* The Dockerfile pins a base digest and runs as UID 10001 with no data baked in.
  Versioned images have been deployed; MVP CI test/image/mssql jobs and both
  validation workflows passed for source head `8ca4a3d` on 2026-10-13.
  The deployed account-switch image is linked in the infrastructure handover,
  not assumed rebuilt from later documentation-only commits. Future edits need
  their own checks; a scorer's successful execution is not product acceptance.
* Finance and sign-off rules are a proposal on constructed data: the role
  mapping (for example Quality Inspector for assessment) is a stand-in for the
  PAS 2035 roles, matching is simple exact comparison, amounts are not tied to a
  real ledger, there is no supplier or contract master, and the screens were
  syntax-checked but not run in a browser or with a screen reader. The product
  has no bulk edit yet, so the bulk refusal is tested on the API only.
* Retention periods and legal bases remain proposals for the DPO and Legal.

## Container hardening checks in CI

The `image` job in `.github/workflows/mvp-ci.yml` builds the image and checks:

* it runs as UID 10001 and contains no working data;
* it starts and answers `/healthz` with `--read-only --cap-drop ALL
  --security-opt no-new-privileges`, with only `/tmp` and `/state` (`ZF_STATE`)
  mounted as tmpfs, the seed data mounted read-only, and writes to `/state`
  succeed while writes to `/app` and `/` fail;
* a Trivy scan fails the job on any HIGH or CRITICAL finding that has a fix
  available (`ignore-unfixed`). Unfixed findings in the pinned Debian base are
  not blocked, so they are visible in a local `trivy image` run but not
  gated. The fix for a fixable OS package is the `apt-get upgrade` in the
  Dockerfile, never an ignore file;
* an SPDX SBOM (`zavaforward-mvp-sbom` artifact) is generated and uploaded.

Actions are pinned by commit SHA. The workflow result on GitHub is what proves
these checks; running the same commands locally is only a preview. Document
files default to `ZF_STATE/docs`, or set `ZF_DOC_DIR`; the app writes nowhere
else. The SQL Server integration job is not part of this job.

## Tests

```bash
cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -v
(cd ../orchestrator && PYTHONPATH=../core/tests python3 -m unittest discover -s tests -v)
```

The tests also cover the SQL store (including `test_sqlreads.py`), documents, ledger, role matrix, workflows, auth and time capture. They use small fixtures and a generated 60,000-case dataset, and need no
private data. The AI tests use a scripted model or the template path (no network).

Browser check (needs python3 playwright and chromium, and the built dataset):
`python3 src/api/checks/browser_check.py` (the dataset at `ZF_DATA`).
