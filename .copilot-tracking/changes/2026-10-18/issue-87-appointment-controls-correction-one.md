<!-- markdownlint-disable-file -->
# Issue 87 correction ONE

## Metadata and Authorization

* Date: 2026-10-18; session b9f13d51-f8d3-4fc5-80bb-0e255ec31995.
* Scope: one coherent implementation cycle for all RV-001 through RV-007.
* Starting HEAD: 49d3d663a95714d0b90e8795c8ea3f4ade2a92c2.
* Original source: 22c98267ae6da365d6a2d9fceed7113c8f4578ea.
* Base and freshly checked origin/main: 99056cae7bc679d2ace3e42c75f28577cfce8887.
* Branch: feat/appointment-commitment-controls-87; initially clean; no remote PR.
* Authority: coordinator instruction at 2026-10-18T01:37Z authorizes correction
  ONE for all seven findings. This worker owns source/tests/docs and evidence
  only; coordinator owns subsequent identity/commit/push/PR judgment. This worker
  performs no branch switch/rebase/commit/push/PR/merge/issue closure.
* Original Review remains Complete / Not accepted; no second Review/self-Pass.
* Frozen critique SHA256:
  044c3b5b9399522993ddb81ba4f90fe0f8a708960cc812169f306f29e80f7396.
* Frozen Review SHA256:
  b0759a56265e8f82a5db71a99443736e07cec597b0e5e17bcc2d9a7f1e6cba4b.

## Execution Status

Complete implementation of RV-001 through RV-007 as one coherent correction
batch, now source commit0830f7c339fe9b5fa936cda849f14edc5a0e3624. No known
in-scope implementation blocker remains. Parent
coordinator did not implement source. No policy/research decision is inferred.
Implementation evidence is not independent acceptance; original Review remains
Complete / Not accepted. No second Review, critique or self-Pass was run.

Validation ran on starting HEAD49d3d663 plus the correction before commit; the
identical source/docs tree is now pinned by the source commit above.
Base/origin-main remains99056cae. SHA256 of
`git diff 49d3d663 -- src docs` is
`2a7ee976ce7556663a453cb8bb54021975b8d6515a793f5fd4a4549f20bac16d`.
Tracking receipt reconciliation is outside that source/docs patch fingerprint.

## Approved Scope and Validation

One coherent correction batch: committed-response serialization before headers,
role-sensitive appointment projections, threshold-change atomic evaluation,
bounded textual competence source, ended withdrawn appointments, selected-slot
display and manual draft protection. Failing-first evidence for each finding,
then exact targeted local/domain/HTTP regressions, actual SQL configuration/
outcome/closure races, actual browser keyboard/draft/date behavior, configured
static checks and final source-context hardened image as affected.

Web rules must be freshly fetched before edits and the changed-web guideline
check; retain Fluent/native/WCAG/plain-language baselines, no visual overhaul.
No weakening of capacity/resident/safety/quality/finance/event/audit/committed
outcome guards. Same-case explicit human closure alone resets; no new policy,
live approval/private inputs/spend/cloud integrations. Stop exact owned SQL.

## Findings and Evidence

Failing-first evidence executed on the original source before correction:

* Core selector: existing JsonFlows/SqlFlows methods
  `test_bundle_needs_explicit_agreement_and_scoped_competence`,
  `test_configuration_evaluates_existing_active_counts_once`,
  `test_withdrawn_appointment_is_ended_and_history_retained`,
  `test_appointment_reads_apply_existing_resident_evidence_roles`.
  8 tests, 8 failures, zero skips, 1.813s. Respectively whitespace accepted,
  count5/threshold4 task absent, Withdrawn still Committed, private closure and
  circumstances present in serialized QUIL work-order payload. RV-002/003/004/005.
* Actual HTTP selector: ProcurementApi and JsonProcurementApi
  `test_response_only_encoder_failure_is_truthful_for_confirmation_and_closure`,
  ProcurementApi bundle/withdrawal tests: 4 tests, 5 failing assertions,
  zero skips, 3.643s. Response-only predicate tests dictionaries with
  `work_orders[0].appointment_control`, never persistence serialization.
  Actual confirmation returned400 without committed outcome; whitespace offer
  returned200; withdrawal projected Committed. RV-001/004/005.
* Actual local Chromium, existing procurement browser check extended:
  first run timed out waiting for selected `1 Jan 2099 / Morning` on the new
  Offer, without legacy Booked. Second isolated draft reproduction skipped only
  the date assertion (`ZF_APPOINTMENT_REPRO=draft`), typed a threshold draft,
  activated the safe-contact link by keyboard with a cancellation handler.
  No dialog occurred; the route replaced the form and its input locator timed
  out. Both failures are real browser execution, RV-006/007.
* Corrections now include pre-header response encoding, explicit actor-sensitive
  resident/reason projection, strict competence text, Ended withdrawal,
  atomic configuration evaluation of stored active eligible events and all
  affected case rowversions, current localized slot and draft/context retention.
  Existing JSON/SQLite core101 and API18 initially passed; added configuration
  races5 passed. New API canary fixture initially had a misplaced append causing
  SyntaxError; fixed before further execution. These are interim, not final gates.

Historical SQL61/browser/image receipts are not corrected-source results.

## Per-finding Correction Results

* RV-001, addressed: `server.py` JSON-serializes AND UTF8-encodes the response
  inside the post-COMMIT guard before `_send` can send headers. A response-only
  encoder fault now produces409 with `outcome: committed` and explicit
  reload/reconcile guidance. No network recovery is promised after bytes sent.
  The shared HTTP test
  `test_response_only_encoder_failure_is_truthful_for_confirmation_and_closure`
  faults only the returned work-order dictionary, not persistence serialization,
  and proves durable confirmation/closure, one corresponding event, and an
  identical successful retry without duplication on JSON/SQLite and actual SQL.
  Initial failing-first confirmation returned400 despite durable success.
  Additional closure isolation replayed the pinned original server module
  IN MEMORY after edits: original response400/no committed marker with durable
  closure1; identical retry200/closure1. This is a pinned-original reproduction,
  not a claim that the closure isolation ran chronologically before editing,
  nor a rerun of the original Review. Corrected final HTTP tests exercise both.
* RV-002, addressed: direct domain summaries and HTTP work-order reads require
  the actual current registered actor. The existing resident-view AND
  recorded-reason entitlement is reused without broadened roles or a privileged
  default. Unrelated QUIL and assigned provider retain status/date/period/
  minimum necessary instructions, not household reasons, representative or
  confirmation sources, closure reasons/sources or investigation circumstances.
  Failing-first serialized QUIL payload contained private canaries.
  `test_appointment_reads_apply_existing_resident_evidence_roles` and
  `test_appointment_http_serialized_canaries_follow_existing_roles` now pass
  against actual serialized domain/HTTP payloads across JSON/SQLite/MSSQL.
  Authorized manager still sees evidence; direct-summary forged/current-user
  refusal, provider assignment, ordinary resident projection parity,
  `ZF_REASON_ROLES=""` and relevant audit/projection absence are covered.
* RV-003, addressed: configuration evaluates ALREADY eligible active counts
  atomically across all affected homes, capturing each SQL case dependency.
  `_evaluate_appointment_investigation` is shared with outcome processing.
  It creates at most one human task for the current closure boundary, records
  current config version/current eligible refs, never recounts or replays
  consumed events, and never resets an existing task.
  Failing-first count5/lowered threshold4 produced no task.
  `test_configuration_evaluates_existing_active_counts_once` now covers
  lowering, raising, retry, existing task, closed/reopened/consumed histories,
  and configuration invoked from a different home's order. Actual SQL covers
  BOTH config/outcome winners, BOTH config/human-closure winners, BOTH competing
  lower/higher version winners, and another eligible home's lifecycle race.
  Refusal/retry outcomes preserve atomic versions/tasks/events; no sanction,
  policy, consent or automatic consequence is inferred.
* RV-004, addressed: competence source passes existing bounded `text` validation,
  requiring a nonblank string of at most500 characters and exact work-order
  binding. Explicit bundle agreement remains independently necessary.
  Initial domain/HTTP whitespace source was accepted. Expanded
  `test_bundle_needs_explicit_agreement_and_scoped_competence` and
  `test_bundle_competence_http_requires_bounded_text_and_exact_scope` pass
  whitespace/empty/nontext/overlength/wrong-scope refusals and valid agreement
  on JSON/SQLite/MSSQL. No competence is inferred from an actor's role.
* RV-005, addressed: withdrawing an offered/confirmed order projects Ended,
  noncurrent historical-only slot, while retaining offer/confirmation history.
  Initial domain and HTTP returned Committed. Core
  `test_withdrawn_appointment_is_ended_and_history_retained` and HTTP
  `test_withdrawal_http_ends_current_appointment_for_staff_and_provider` now
  prove staff/provider projections and consequential booking/completion/advance
  refusals across JSON/SQLite/MSSQL. Actual provider browser also shows Ended
  with historical selected slot.
* RV-006, addressed: `appointmentSlot` uses existing localized `fmtDate` and
  shows selected date/period/instructions for current authorized staff/provider;
  Unknown and ended-history wording remain explicit. Initial actual browser
  failed selected-slot display before confirmation. Final actual browser
  confirms `1 Jan 2099 / Morning` on the NEW Offer, then provider Committed
  with those details BEFORE any legacy Booked record. Empty legacy visits are
  explicitly asserted; legacy booking does not mask this path.
* RV-007, addressed: manual appointment forms reuse `data-unsaved`, have a
  per-form identity and confirmed native reset/discard. In-app router cancellation
  restores the displayed URL and leaves DOM/draft/focus intact; beforeunload
  remains. Successful save clears only its own form. Refresh captures pending
  fields/checkboxes/open sections immediately before replacement, including
  edits while GETs were pending, and restores ORIGINAL offer/case dependencies
  rather than silently rebinding evidence to refreshed versions.
  Initial actual keyboard navigation discarded a draft without a dialog.
  Final actual keyboard cancellation preserves the safe-contact draft/URL;
  confirmation save leaves the threshold draft; another order's save leaves
  the first order's household draft; canceled discard preserves text and
  accepted discard clears only that form. Existing explicit closure checkbox,
  canceled/accepted closure and resident-update preservation still pass.

## Final Local Gates

Existing editable source distributions in `.venv` were used; no installs,
dependency changes, `uv`, private datasets or `PYTHONPATH=mvp` workaround.
All commands used project-local `.validation` as `TMPDIR` and
`PYTHONDONTWRITEBYTECODE=1`; test modules remain outside installed packages.

```bash
# From src/core
PYTHONPATH=tests ../../.venv/bin/python -m unittest \
  test_quality_procurement test_resident_decisions test_hazard_referral \
  test_finance_signoffs test_progress_event_capture test_buildings -q
# From src/api
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest \
  test_procurement_api test_resident_api test_hazard_api test_finance_match_api \
  test_workflows test_buildings test_mvp test_accessibility_baseline \
  test_design_system test_content_standard -q
# Configured gates from each component
../../.venv/bin/ruff check src tests
../../.venv/bin/ruff format --check src tests
../../.venv/bin/mypy
# API adds its existing checks directory to both ruff invocations.
node --check src/api/src/zava_forward/api/web/app.js
node --check src/api/src/zava_forward/api/web/ops.js
```

* Core:336 run,277 pass,59 existing skips,61.916s.
* API/web:93 run,92 pass,1 existing skip,42.838s.
* Configured core ruff/format/mypy passed:69 formatted files,123 mypy files.
* Configured API ruff/format/mypy passed:23 formatted files,56 mypy files.
* Both JS syntax checks passed. Final exact-tree static rerun passed after
  the last draft-capture/provider loopback test refinement.
* Expected injected recovery errors log stack traces in passing tests; they
  are not hidden suite failures. No retained neighboring assertions were weakened.
* Interim failures corrected within this SAME correction cycle: misplaced
  synthetic API fixture append caused SyntaxError; browser save assertion
  initially raced asynchronous refresh; a non-function `wait_for_function`
  expression was rejected by CSP and replaced with a function, not weakened CSP;
  initial configured lint/format/mypy failures were corrected. Initial
  JSON/SQLite101/API18/config-races5 and first actual SQL73 were interim,
  superseded by final gates above/below. No new tooling dependency was installed.

## Actual Owned SQL Server

Executed the existing canonical
`python -m unittest test_mssqlstore.MssqlProcurement test_mssqlstore.MssqlProcurementApi -q`
with the existing API/core/agents test paths and installed `.venv`.
Its inherited shared core and API tests include all the new regressions.
Bounded project-local launcher provisioned a uniquely labelled, loopback-only
`mcr.microsoft.com/mssql/server:2022-latest` instance, memory3g, disposable DB,
random in-memory password; inspected ownership before start and removed exactly
that container/database in `finally`, immediately after each run.

| Run | Owned container and label suffix | Loopback | Ephemeral DB | Result |
| --- | --- | --- | --- | --- |
| Interim | `zf-issue87-correction1-mssql-395076a0d0`, `ama.task=issue87-correction1-395076a0d0` | `127.0.0.1:32799` | `issue87_correction1_395076a0d0` |73/73,0 skips,82.359s |
| Final expanded races | `zf-issue87-correction1-mssql-9a50b2c1d7`, `ama.task=issue87-correction1-9a50b2c1d7` | `127.0.0.1:32800` | `issue87_correction1_9a50b2c1d7` |75/75,0 skips,78.111s |

Final includes config/outcome/closure/version BOTH winner orders, other-case
lifecycle dependency and retained current authority/source/scope/offer/capacity,
pending-audit rollback, post-COMMIT/retry and closure/reopen races. Serialized
privacy and response-only HTTP encoder faults run in canonical SQL API class.
Final exact-label/name inspection found no task containers; unrelated existing
stopped containers were left untouched. Old historical SQL61 is not reused.

## Actual Browser and Bounded Guideline Check

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests \
  .venv/bin/python src/api/checks/procurement_browser_check.py
```

Final actual local Chromium passed after the last test change. Both independent
staff/provider contexts block non-loopback requests. No page errors or external
requests. Covers required source-backed capacity/quota/delegation checks,
keyboard package creation/save, provider read/write denial, Unknown/Offer/
Committed, new-flow selected slots, Ended history, missing-offer refusal,
separate manual confirmations, draft/navigation/unrelated-save cancellation,
explicit human closure/update preservation and320/390/1280px reduced-motion
reflow. It does not establish resident usability or WCAG acceptance.

Required `web-design-guidelines` and `redesign-existing-projects` were loaded.
COMPLETE fresh source fetched before edits and REFRESHED after final web edit:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Both changed web files were read for integration and checked against all fetched
rule families. Fluent2/native controls, existing focus/skip/live regions,
noncolour statuses, plain ASCII/sentence-case content, reduced motion, safe
contact/provider redaction and manual approval boundaries take precedence over
conflicting generic typography/Title Case recommendations. No redesign.

The required source-format findings below distinguish correction-hunk checks
from inherited out-of-scope file findings; this is not a second RPI Review:

### src/api/src/zava_forward/api/web/app.js

* src/api/src/zava_forward/api/web/app.js:145 - correction guard pass: keyboard
  canceled navigation preserves URL/DOM/draft; existing beforeunload retained.
* src/api/src/zava_forward/api/web/app.js:64 - inherited sign-in inputs lack
  meaningful names; email input lacks explicit spellcheck suppression.
* src/api/src/zava_forward/api/web/app.js:1274 - inherited funding list renders
  up to150 rows without virtualization.

### src/api/src/zava_forward/api/web/ops.js

* src/api/src/zava_forward/api/web/ops.js:112 - correction selected-slot pass:
  localized date, period/instructions, Unknown and historical-ended states.
* src/api/src/zava_forward/api/web/ops.js:136 - correction draft pass: native
  labelled forms and per-form values/context survive unrelated refresh.
* src/api/src/zava_forward/api/web/ops.js:277 - correction discard/save pass:
  keyboard-operable native actions, cancellation and dirty-state protection.
* src/api/src/zava_forward/api/web/ops.js:259 - inherited appointment source/code
  inputs lack explicit spellcheck suppression; numeric input helper lacks
  explicit inputmode.
* src/api/src/zava_forward/api/web/ops.js:272 - inherited non-auth selects lack
  explicit autocomplete suppression.

No new correction-hunk guideline defect was found. Inherited metadata/list
findings are disclosed, not silently fixed outside this authorized batch.
No media/image/hydration/new-animation/theme or gesture surface was introduced;
their rules do not imply an unperformed whole-app conformance assessment.

## Fresh Source-context Image and Hardened Runtime

```bash
docker build -f src/api/Dockerfile \
  -t zf-issue87-api:correction1-b9f13d51 src
```

Final rebuild succeeded against latest application source, not the historical
image. Manifest list:
`sha256:1db7a8d46d9168a4e3adfef451756fc903d6b397e49b051bd41793b569d6e7f4`.
Owned runtime `zf-issue87-correction1-api-831de1df80`,
label `ama.task=issue87-correction1-api-831de1df80`,
`http://127.0.0.1:32801`, was responsive and tested with:

* UID/GID10001, installed site-packages wheel, no source-checkout import.
* `--read-only --cap-drop=ALL --security-opt=no-new-privileges`.
* All five capability sets0, NoNewPrivs1, root write refused.
* Writable `/state` tmpfs `rw,nosuid,nodev,uid=10001,gid=10001`;
  read-only synthetic fixture/docs mount, SQLite/password auth, no private data.
* Actual health/login/current Committed order/manual human closure/identical
  retry exactly once/outstanding resident update/app and served JS hashes pass.
* Served `app.js` SHA256
  `ba3632a14b57ff05a5cb8d93476ed26b14a6522cba80c4d9a37df240e290adee`.
* Served `ops.js` SHA256
  `d28b705ffa88f386cb1b23ca4db9be93dd09d2bcbc6ea2fee3a4f12d0e466cd3`.
  Both match the current source exactly.

Exact owned container/tmpfs and copied synthetic fixture removed immediately.
Local built image and pre-existing `.venv` may remain; no idle3GB container.

## Integrity, Documentation and Handoff

Directly related core/API guides, existing resident-journey synthesis/reference
index and APPEND-ONLY reference log updated. Relative target/anchor and diff
review performed; no repository-wide documentation build exists. Prior reference
log411582 bytes remain an exact prefix. Original case and memory unchanged.
Parent state file untouched by worker; SHA256
`07b1bc85774a85d4cbe398025ec9a16b343ac76a52ab10ffe68e2424ebf62870`.
Frozen original Review/critique hashes match Metadata exactly, including adverse
Not accepted outcome. Plan/details/current changes/routing reconciled without
rewriting historical SQL61/browser/image receipts or inventing a new source SHA.
`git diff --check` passed. Project-local `.validation` scripts/logs/synthetic data
removed after transcription; no secrets/data/logs are included in delivery.

Human limitations remain explicit: synthetic engineering validation only, no
independent corrected-head acceptance, resident validation, WCAG certification,
live policy, regulatory/legal/professional approval, procurement allocation,
real contact, cloud/IAM/spend or service activation. Works consent, appointment-
specific representative authority, actual home/scope/order/date/period/current
capacity and ALL #90 checks remain; quota is per home/work-order/package period,
not weekly slots. #88 updates/remedies, #85 urgent response, #91 quality, #102
events, #101 coordinator and #117 rescans are not weakened. No #92/389 blanket
hold or inferred legal clearance. Only explicit supplied human closure of the
underlying same home case resets its active count; task/order/remedy completion
does not. History/config/refs remain; reopening cannot replay consumed events.

Next action belongs to coordinator: assess this coherent correction evidence
and handle any authorized identity/commit/publication. Worker stops here, with
RV-001 through RV-007 addressed and no independent acceptance verdict.

## Parent Delivery Reconciliation

Parent verified the exact source/docs patch fingerprint and served app.js/ops.js
hashes against the completed receipt, clean diff, frozen Review/critique hashes,
unchanged memory/original specification and fresh origin/main at the pinned base.
No second source Review or coordinator source implementation occurred.
All seven findings have implementation/reproduction evidence in this one cycle;
the latest explicit coordinator instruction therefore permits normal own-branch
publication. This is a delivery decision, not independent correctness acceptance
or a replacement of the original Not accepted verdict.

| Exact issue AC | Correction implementation evidence, not independent acceptance |
| --- | --- |
| AC1 offer versus commitment | Existing separate confirmations retained; withdrawn state Ended, selected localized slot visible before confirmation, response-only committed truth and current actor projections tested. |
| AC2 no bundle safety delay | Nonblank bounded exact-scope competence required; explicit agreement retained; independent hazard regression selection passed. |
| AC3 constraints/options/deferral/pause | Existing household/owner persistence retained, serialized role canaries exclude protected reasons, keyboard navigation cancellation and unrelated-save draft retention exercised. |
| AC4 configurable human investigation only | Existing strict default-five sixth-event rule retained; lowering evaluates already eligible active cases atomically with dedup/version/history/closure boundaries; actual SQL both-winner races passed. |

No known unresolved original RV finding is reported by the source owner.
Inherited guideline findings and human/live/UX acceptance limits above remain
explicitly outstanding and are not silently treated as conformant. An unrelated
issue122 SQL container observed during parent cleanup verification was untouched;
no issue87 owned runtime remains. Final publication identifiers are recorded
after source is pinned and remote creation succeeds, not invented beforehand.

## Publication Receipt

Normal push of the coherent correction succeeded under the latest explicit
coordinator authorization. Source commit:
0830f7c339fe9b5fa936cda849f14edc5a0e3624. Main pull request:
https://github.com/jmservera/ama/pull/397. PR body uses Refs87, names parent81,
retains the original Not accepted verdict and distinguishes fresh correction
evidence from independent acceptance and historical receipts.

Fresh authenticated identity was jmservera, id8036360; repository-local privacy
address 8036360+jmservera@users.noreply.github.com was used for author and committer
with Conventional Commit and Copilot co-author trailer. Origin/main was checked
at pinned99056cae immediately before push; no main advance/rebase/force was used.
Follow-on commit reconciles delivery artifacts only, not validated source/docs.
No merge, issue close, automatic live action or second Review occurred. PR checks
are external follow-on evidence, not a substitute for the executed local gates.

## Later Correction-TWO Clarification

The coordinator-supplied external evidence later found a nondeterministic wait
in the browser check and a stale coupled public fixture digest. Earlier observed
results above remain unchanged; they do not prove deterministic synchronization
or independently establish later-step coverage at every run. The separate
correction-two receipt records exact form-replacement synchronization and actual
complete later provider selected-date/Committed/Ended and unrelated-order/draft
execution, including a final-byte complete run. Both named digest tests and all
19 coupled tests pass. Full-core discovery was also executed, but existing
generator output guards reject mandated project-local scratch (1048 run,
32 error records over 23 methods, 114 skips). No green full-core, rerun SQL75/
image, second Review or independent acceptance is implied.
