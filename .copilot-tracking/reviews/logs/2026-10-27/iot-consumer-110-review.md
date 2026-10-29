---
title: IoT consumer and synthetic streaming Review
description: One independent complete-candidate RPI Review, preserving defects and deferred acceptance
ms.date: 2026-10-27
---

## Scope and Evidence

* Task: #110 with #184 and #185-#189, iot-consumer-110.
* Review date: 2026-10-27.
* Repository and branch: jmservera/ama, feat/iot-consumer-110.
* Comparison base and current HEAD: 09099ecd1a66ee9d37ad993707d1f2eda07cdfd4.
* Boundary: the entire supplied working candidate, not merely tracked diff
  output. Nine modified tracked files and eleven untracked files were inspected,
  including this pre-existing opening record, the original critique, session
  state, both new source modules and both new test modules.
* Acceptance basis: current P01-P03 and task markers, original critique
  PC-001-PC-006 and their recorded dispositions, issue bodies retrieved
  read-only with gh, ADR 0003's source authorization, existing ingestion,
  synthetic selection/backfill contracts and PRD AC-066.
* Existing project context: original case study, addendum, knowledge-base index,
  owner memory and housing-association primer. Memory is context, not evidence.
* Authority: exactly one independent post-implementation Review; only this file
  may change. No source, plan, details, changes, critique, research, session
  state, issue or remote mutation. No nested agent, Azure operation, credential
  or private-data access, dependency installation, uv, deployment or gate run.
* Parent-reported test evidence is assessed as reported evidence, not silently
  relabelled as independently rerun validation.

## Opening Review State

* Interpreted goal: assess implementation against issue criteria, approved
  architecture and the six direct critique dispositions, without implementing.
* Scope: complete candidate against the supplied base, including untracked
  implementation and original RPI evidence.
* Readiness at opening: source and reported local validation available;
  live acceptance and publication evidence unavailable.
* First comparison: synthetic replay and async SDK/SQL recovery boundaries,
  followed by tests, dependencies, documentation and criterion/status claims.
* Acceptance basis: current P01-P03, ADR 0003 and PC-001-PC-006 dispositions.
* Read-only boundaries: every file except this canonical Review record;
  no second Review or nested assessment.
* Initial blockers: full live acceptance and final-publication gates remain
  unproven. They do not prevent a credible source Review.

## Execution Status

* Review execution status: Complete.
* Implementation execution status: Partial overall. P01/P02 source and local
  validation were executed; P03 publication and live acceptance are not complete.
* Evidence: all named artifacts and complete candidate categories compared;
  three bounded independent exact-source probes executed locally without SDK
  connections, package installation, cache writes or persistent scratch files.
* Assessment count: exactly one Review. The original critique remains Revise.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Shared seasonal replay, nominal-slot faults, bounds and pacing | Partial | Model/suffix behavior agrees; actual send-rate enforcement and descriptor identity have RV-001/RV-002 defects |
| P02 / P02-T01 | Explicit async SDK adapters, binding fence and SQL recovery | Partial | No-store retained-history restart agrees; construction failure escapes the promised lifecycle/error boundary, RV-003 |
| P03 / P03-T01 | Local checks, READMEs and knowledge-base updates | Reconciled for executed scope | Checklist remains unchecked; independent Review now exists, publication is still pending |
| Critique Disposition | Six direct compatible corrections | Reconciled as decisions | Application does not itself prove every corrected invariant; see findings |
| Follow-Up Items | #185, #188, #189 and OD-43 remain deferred | Reconciled | Distinct owner actions below; none is silently promoted into an active completed task |

The changes record retains stale introductory "Pending" wording under P02 and
P03, and the plan's Handoff still names the earlier advance to Implement.
The detailed validation/pre-Review reconciliation, phase index and session
active_phase=Review make the current state interpretable. These dated handoff
remainders are not evidence of live completion or permission to publish.
Later continuation should use the current phase/status evidence and this record,
not the earlier handoff sentence.

## Completed Work Assessment

| Marker | Files | Change and rationale | Evidence and assessment |
| --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/synthetic/sensor_stream.py; src/core/tests/test_sensor_stream.py | Reuses existing seasonal backfill with faults disabled before canonical conversion; bounded synthetic selections and per-slot transforms | Six tests exercise origin suffixes, odd windows, faults, budget and pacing; replay comparison uses the existing generator, not only self-comparison. RV-001/RV-002 remain |
| P02-T01 | src/api/src/zava_forward/api/iot_stream.py; src/api/tests/test_iot_stream.py | Dedicated endpoint, managed-identity receive, per-device X.509 publish, independent binding and SQL admission | Seventeen reported local tests; actual EventData construction with fake transport and constructed SQLite. Source has no HTTP/startup activation. RV-003 remains |
| P03-T01 | src/api/pyproject.toml; src/api/requirements.in; src/api/requirements.txt; src/core/pyproject.toml | API owns pinned SDK and async identity transport dependencies; narrow existing-style untyped-call overrides | All pre-existing lock pins preserved; sixteen transitive/direct additions, hashed blocks present; TOML parses. Parent reports hashed installation dry-run and pip check passed |
| P03-T01 | src/api/README.md; src/core/README.md | Documents callable activation, retention limit, cancellation uncertainty, supported model and local commands | Generally faithful; rate-cap and descriptor guarantees are stronger than behavior, RV-001/RV-002 |
| P03-T01 | docs/reference/research/iot-sensor-analytics-research-plan.md; docs/reference/README.md; docs/reference/log.md | Extends existing synthesis, index and append-only log with issue-by-issue delivered/deferred evidence | No fabricated issue closure, deployment or operational acceptance. Rate-cap claim needs RV-001 correction |

The scope adds exactly two owned test modules, removes no existing test and
changes no workflow/check name. Packaging stays under src with no legacy
PYTHONPATH workaround. No infrastructure, schema, resident consent or
professional approval authority is broadened.

## Implementation-Time Plan and Detail Update Assessment

| Area | Update and reason | Evidence / decision | Reconciliation and assessment |
| --- | --- | --- | --- |
| P02 / PC-001 | Pins Event Hubs 5.15.1 and IoT device 2.14.0; byte-keyed application-property decoding under a Hub-only sender boundary | Recorded installed-SDK witness and tests using actual EventData objects; actual routing deferred | Compatible source correction. SDK accessor behavior is not evidence that Azure emits the constructed property shape |
| P02 / PC-002 | Removes warning-only no-store checkpoint call; fresh receivers start at "-1" without a checkpoint store | Recorded SDK witness; source/test restart contract | Reconciled. SQL is the durable state; retention expiry and poison-envelope limits are explicit |
| P02 / PC-003 | Async deadlines, reserved cleanup, retry flags and shielded threaded SQL | Source, cancellation/timeout tests and explicit uncertainty narrative | Compatible correction, not rollback or hard thread-cancellation proof; RV-001/RV-003 expose remaining lifecycle/control defects |
| P01/P02 / PC-004 | Normal-device UNMAPPED mutation is refused; separately installed exact unmapped binding supplies SQL DQ | Source binding check and constructed-SQLite UNMAPPED test | Reconciled without payload-granted exception or new provisioning authority |
| P01 / PC-005 | Legacy seasonal model only; full-origin generation, nominal-slot slicing and deterministic fault transforms | Independent generator comparison; odd/nonzero suffix tests | Compatible bounded model choice, not a composed-model claim. Descriptor remains incomplete, RV-002 |
| P02 dependencies | Explicit aiohttp==3.14.5 after missing async transport witness | Parent reports dependency failure/probe, manifest/lock update and successful no-network transport open/close | Necessary API-owned dependency; no unrelated pin changes observed |
| P03 / PC-006 | Conditional publication, one authorized changed-gate attempt, no fallback | Current plan/details and user constraints | Failure/busy/unavailable is blocked publication, not a receipt. A scoped pass still cannot establish missing repository-wide final-publication requirements |

No material new product, tier, deployment, credential or physics authority is
inferred from these updates. The direct corrections preserve the supplied user
direction; no new divergent owner decision was required before local source
work. The preserved critique was not relabelled Pass or rerun. Its unresolved
implementation consequences are routed here rather than rewriting the critique.

## Critique and Material Revision Assessment

* PC-001: explicit metadata accessor/key/type handling implemented; wrong
  namespace, device, sensor/home, aliases, byte-key annotation conflict and
  absent auth are locally covered. The trust boundary requires the actual
  dedicated namespace to have no other sender; Activation is a declaration,
  not verification. Actual Hub emission and role propagation remain deferred.
* PC-002: no checkpoint update exists. Fresh receiver replay is explicit and
  SQL accepted/DQ receipts are durable before success. Constructed restart
  tests retain SQL state, including lost acknowledgement. Their fake two-
  partition delivery is sequential, not actual partition/load-balancing proof.
* PC-003: receive completion/failure signaling, deadlines, external stop,
  shielded SQL uncertainty and bounded cleanup are materially implemented.
  Cancellation can leave SQL settling after return; no rollback is claimed.
  The caller must keep the store alive. Cooperative fake cancellation is not
  proof of termination of every real SDK/internal worker. RV-003 is a concrete
  resource-construction/error-boundary gap.
* PC-004: normal spoofed/mutated identity fails before SQL; independently
  configured unmapped binding produces owned UNMAPPED DQ without a bypass.
* PC-005: selected model, stable observation conversion, full-origin RNG and
  nominal-slot fault replay are supported by local tests. The complete
  descriptor-to-selection binding is not implemented, RV-002.
* PC-006: publication remains conditional. No gate was run by this reviewer.
  The parent's at-most-one --changed authorization does not waive the complete
  live or repository final-publication gates.
* Dependent-work assessment: current artifacts record direct correction before
  implementation, not a new unaccepted divergent choice. Actual cloud work
  remains paused. Do not equate recorded disposition with defect-free execution.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment and distinct route |
| --- | --- | --- | --- |
| #185 credential lifecycle | No enrollment, secret access or device deletion authorized | Named exercise credential owner: approve and perform issue, approved Key Vault storage/access, rotation/revocation and exact run-owned identity teardown | Open; distinct #185 follow-up, not a source defect or an active P02 completion claim |
| #188 live store/seam/restart | Fake SDK and constructed SQLite cannot prove actual private Hub-to-Azure SQL ingestion or durable live restart | Exercise operator and ingestion owner: obtain separate live authority, witness actual metadata/routing and SQL/restart, compare per-home handover to the approved model/tolerance | Open; distinct #188 acceptance follow-up; no Azure action authorized here |
| #189 operational quota/cost | Cost/alert/headroom references are caller declarations, not queried operational evidence | Exercise owner / budget operator: verify current currency, aggregate cap/headroom, consumed quota and active alerts before any live send | Open; distinct #189 operational follow-up. RV-001 separately addresses an implementation defect in local rate enforcement |
| OD-43 | Operational/legal/professional activation is outside synthetic source engineering | Existing accountable human governance owners: resolve and approve the operational gate through the established process | Open; distinct OD-43 follow-up, never auto-approved by agents or tests |

Related declared exclusions are also distinct: #187 live replay and the
#187/#188 composed-climate seam need a separately scoped model/acceptance
follow-up by the backfill/ingestion owners. They are honestly excluded from
the current legacy-model proof, not newly discovered implementation defects.
The changes record mirrors the main credential/live/budget deferrals; its
Amendments and Divergences also preserves composed-model deferral.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Rate reservation occurs before connection, not at actual send

* Related scope: P01-T01, P02-T01, #187/#189, PC-003.
* Evidence: src/core/src/zava_forward/core/synthetic/sensor_stream.py:223-233
  reserves next_send when pacing returns. In
  src/api/src/zava_forward/api/iot_stream.py:355-395, pacing precedes a possibly
  slow client.connect(), message preparation and the truth callback; there is
  no rate recheck immediately before send_message().
* Independent reproduction: exact candidate Pacer/RunBudget/Frame,
  HubPublisher and timeout/cleanup helpers were executed from parsed source
  with inert SDK replacements. At max_per_second=5, a 0.25-second fake initial
  connect followed by two burst frames produced an actual send interval of
  0.000133 seconds, rather than the required 0.2 seconds.
* Impact: connection/setup latency spends the reserved pacing interval; the
  next frame can be sent immediately after the first. The documented assertion
  that burst/speed never bypasses the rate cap is false at the transport send
  boundary. Bounded counts and total quota preflight do not fix send spacing.
* Destination: rpi-implement, within the accepted finite-run direction.
* Smallest useful next action: enforce the global send-rate budget at actual
  send-attempt admission after connection/setup, preserving model-time pacing,
  stop and the absolute deadline. Add delayed-connect and delayed-preparation
  regressions asserting actual send timestamps, including multiple devices.
  Reconcile the directly related README/synthesis claim if semantics change.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Replay descriptor does not bind the selected mutable model inputs

* Related scope: P01-T01, #187/#188, PC-005.
* Evidence: src/core/src/zava_forward/core/synthetic/sensor_stream.py:184-202
  records only selection.input_sha256 for stock identity.
  src/core/src/zava_forward/core/synthetic/sensor_stock.py:135-140 hashes the
  full clean register before slicing clean[:homes]; therefore this digest does
  not identify the selected subset. Selection.rows contains mutable dicts.
  replay() validates/copies the actual rows, but descriptor() neither hashes
  those current rows nor records their selected identities/count.
* Independent reproduction: exact select() and descriptor() definitions, with
  known valid synthetic fixture home IDs, produced equal descriptors for the
  same two-home register selected at homes=1 and homes=2. Mutating a selected
  row's building_form_osm also left its descriptor unchanged.
* Impact: different device/home sets or model-affecting stock inputs share the
  same purported reproducibility witness. A retained descriptor cannot uniquely
  establish the claimed original selection, even though fixed-input replay
  itself is deterministic. Frozen dataclass wrappers do not freeze row dicts.
* Destination: rpi-implement, not a new model-selection decision.
* Smallest useful next action: bind the descriptor to a validated snapshot of
  the selected canonical model inputs as actually used for replay, retaining
  any separate original-register digest. Add subset-collision and mutable-row
  regressions and keep descriptor/frame provenance consistent.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Receiver construction is outside owned cleanup and sanitized errors

* Related scope: P02-T01, PC-003, non-functional cleanup/error contract.
* Evidence: src/api/src/zava_forward/api/iot_stream.py:208-218 creates the
  owned ManagedIdentityCredential and EventHubConsumerClient before the
  try/finally beginning at the receive-wait boundary. A client-constructor
  failure cannot reach credential.close() or a fixed StreamError wrapper.
* Independent reproduction: exact HubReceiver.run() with an inert owned
  credential and a deliberately failing EventHubConsumerClient constructor
  raised RuntimeError rather than StreamError; credential.close await count
  was zero. No credential material or network was involved.
* Impact: an SDK initialization failure violates the promised fixed-error
  boundary and owned-resource cleanup discipline. Unexpected constructor
  diagnostics reach the caller unfiltered. This is separate from acknowledged
  send/SQL outcome uncertainty and does not claim an observed secret leak.
* Destination: rpi-implement, within the accepted adapter lifecycle.
* Smallest useful next action: include resource construction in ownership-aware
  error handling, close whichever resources were successfully constructed and
  sanitize SDK construction failures while preserving cancellation. Add tests
  for credential/client constructor failure and partial initialization.

## Defects

* RV-001: actual send-rate admission is not capped as documented.
* RV-002: replay provenance does not identify the actual selected inputs.
* RV-003: receiver partial construction bypasses cleanup/error handling.
* All three route once to later rpi-implement; none is fixed in this Review.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent / API-core implementer: enforce actual send spacing and regressions | Defect within accepted controls |
| RV-002 | rpi-implement | Parent / core implementer: bind selected snapshot and regressions | Defect within accepted reproducibility contract |
| RV-003 | rpi-implement | Parent / API implementer: cover partial construction lifecycle and regressions | Defect within accepted resource/error contract |

No new significant/divergent decision is identified for rpi-plan, and no new
source-blocking research question is substituted for the concrete defects.
Previously accepted live evidence gaps remain the distinct follow-ups above.
If later work changes the supported model or trust/restart direction rather
than fixing these defects, that new decision belongs to rpi-plan; this record
does not authorize it. Later implementation does not require another Review.

## Residual Work

* Distinct #185, #188, #189 and OD-43 follow-ups remain open as assessed above.
* Live/composed-climate replay remains outside the declared legacy witness.
* Whole AC-066 still requires actual Hub, Azure SQL persistence after restart
  and registered real-AI build acceptance. No fake transport, SQLite result,
  dependency probe or static check passes those requirements.
* #186 is already closed by #412; no new closure or reopening is requested.
  #110/#184/#185/#187/#188/#189 remain incompletely proven and should be
  referenced, not closed from this implementation.

## Blockers and Remaining Work

* Current candidate acceptance: blocked by RV-001/RV-002/RV-003.
* P03 remains open: parent owns later correction evidence, commit and any
  permitted gate/publication continuation; this Review changes no checklist.
* Publication: no final committed-candidate receipt or independent exact-head
  approval is present. Required repository final-publication and whole live
  acceptance gates remain unproven.
* The parent may attempt at most the separately authorized single --changed
  gate under lock timeout zero, after commit. This reviewer ran no gate.
  Busy, unavailable or failed means blocked; no second attempt or --all
  fallback is authorized. Even a scoped pass is not the complete local gate
  demanded by repository publication instructions and cannot waive it.
* Missing broader authority/evidence must remain a publication stop, not be
  resolved by fabricating status, changing protection or performing cloud work.
  Any later invalidating source/base/head/input change also invalidates an
  earlier receipt.

## Validation Evidence

| Command / evidence | Scope | Status | Result / limitation |
| --- | --- | --- | --- |
| git status --short; git diff against supplied SHA; untracked inventory; direct file reads | Complete candidate | Passed, independent | Base/branch confirmed; all tracked/untracked categories included |
| gh issue view for 110, 184, 185-189 | Issue acceptance and state | Passed, independent read-only | #186 closed; other supplied issues open. Stale issue "Not started" prose does not override merged source/ADR evidence |
| git diff --check | Tracked candidate | Passed, independent | No whitespace errors; not proof of untracked-source lint or runtime behavior |
| Standard-library lock inventory and TOML parsing | Changed manifests and hashed lock | Passed, independent | No existing pin changed/removed; sixteen added pins; every requirement block hashed; both TOMLs parse |
| PYTHONDONTWRITEBYTECODE=1 python3, exact-source AST/fake SDK probes | Rate, descriptor, receiver-construction boundaries | Defects reproduced, independent | RV-001: 0.000133-second send gap at five/second; RV-002: subset/mutation descriptor collisions; RV-003: raw constructor error, zero credential closes |
| Initial exact-source probe harness | Local probe setup | Failed, then corrected | Dataclass module registration missing in the in-memory harness; registered modules and reran successfully. Not an application/test failure |
| Installed-distribution availability probe | Review system interpreter | Unavailable | azure.eventhub, azure.iot.device and zava_forward core/API distributions absent; no parent /tmp environment used or dependencies installed by reviewer |
| Core configured Ruff/format and mypy | Core project | Passed, parent-reported | 102 formatted files; 155 typed source files; not independently rerun |
| Core test_sensor*.py | Core sensor suites | Passed with skip, parent-reported | 96 tests, one existing opt-in SQL Server skip; existing unclosed-file ResourceWarnings reported |
| Core test_historical_backfill.py | Backfill regression | Passed, parent-reported | Nine tests; not actual climate/live seam acceptance |
| API configured Ruff/format and mypy | API project | Passed, parent-reported | 48 formatted files; 90 typed source files |
| API full unittest discovery | API regression | Passed with skips, parent-reported | 1137 tests in 463.978 seconds; 314 opt-in/integration skips. This run preceded the final additional case/descriptor snapshot update |
| API final test_iot_stream + test_sensor_ingestion selector | Final focused adapter/ingestion scope | Passed, parent-reported | 62 tests including seventeen new transport tests; not a rerun of the full suite after final edits |
| tools/rename-zava-tests.py | Migration authoring regression | Passed after prerequisite recovery, parent-reported | Initial system run lacked declared PPTX/Pillow dependencies; declared requirements installed externally, then 25 passed |
| Hashed requirements dry-run, pip check, AioHttpTransport open/close | Dependency/runtime construction | Passed, parent-reported | No-network transport check, not token acquisition or endpoint acceptance |
| New documentation link/heading review | Added docs sections | Passed, parent-reported | Reviewer also compared changed claims with source; RV-001/RV-002 remain |
| Actual Hub, Azure SQL, credential lifecycle, active budgets, composed seam, OD-43 and whole AC-066 | Live/operational acceptance | Not run / deferred | Outside authorized local boundary, never counted passed |
| Changed/full gate, receipt verification, hosted checks and final exact-head assessment | Publication | Not run by reviewer / unproven | Parent-only constrained continuation; no receipt or publication permission inferred |

The independent probes compiled the named definitions from candidate ASTs;
they did not import installed application distributions or exercise actual
SDK implementations. The rate probe used a fake client with a delayed connect.
The descriptor probe used the exact stock select/hash logic and a stub
home-key predicate limited to two known valid synthetic fixture IDs; unrelated
model version constants were held identical. These limitations do not remove
the demonstrated control/identity collisions, and do not establish live SDK
representation, thread termination or SQL correctness beyond supplied evidence.

## Outcome

* Outcome: Not accepted.
* Severity: three Medium implementation findings; no Critical or High source
  defect asserted from the inspected evidence.
* Rationale: material accepted-direction invariants remain false: actual
  transport send spacing, complete replay-selection provenance and partial
  receiver construction lifecycle. Reported passing suites do not cover these
  counterexamples. This is not a rejection of the approved B1/ama direction.
* Scope distinction: the single Review is Complete; implementation/publication
  is Partial and whole live acceptance remains unproven.
* Preserve this adverse original outcome. Later correction/test evidence
  belongs in the appropriate later stage, not a rewritten or repeated Review.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Parent continues with RV-001-RV-003 and targeted regression evidence |
| Significant decision gap / invalid assumption | None identified for current source scope | No new owner choice needed to correct these defects |
| New material research gap | None added to current source scope | Existing actual-routing/live evidence gaps remain the explicit #188 follow-up |
| Non-blocking residual work | Distinct #185, #187/#188, #189 and OD-43 work | Existing credential, backfill/ingestion, budget and human governance owners |
| Publication evidence/authority | Parent-controlled blocked P03 continuation | Retain work without push/PR unless applicable gates and authority are satisfied |

* Review execution: Complete.
* Outcome: Not accepted.
* Validation coverage: independent full-boundary inspection and three bounded
  exact-source counterexamples; existing local checks credited as reported.
* Blockers: RV-001-RV-003, unproven final-publication requirements and separate
  live/operational acceptance. No cloud/gate execution authorized by this record.

## Compared Artifact Index

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/iot-consumer-110-research.md](.copilot-tracking/research/2026-10-27/iot-consumer-110-research.md) | Research evidence, trust assumptions and exclusions |
| [.copilot-tracking/plans/2026-10-27/iot-consumer-110-plan.md](.copilot-tracking/plans/2026-10-27/iot-consumer-110-plan.md) | Current requirements, markers and follow-ups |
| [.copilot-tracking/details/2026-10-27/iot-consumer-110-phase-details.md](.copilot-tracking/details/2026-10-27/iot-consumer-110-phase-details.md) | Per-phase implementation and validation contracts |
| [.copilot-tracking/reviews/plans/2026-10-27/iot-consumer-110-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/iot-consumer-110-plan-critique.md) | Original Revise critique, preserved |
| [.copilot-tracking/changes/2026-10-27/iot-consumer-110-changes.md](.copilot-tracking/changes/2026-10-27/iot-consumer-110-changes.md) | Reported implementation/validation and deferrals |
| [.copilot-tracking/rpi-sessions/2026-10-27/iot-consumer-110-state.json](.copilot-tracking/rpi-sessions/2026-10-27/iot-consumer-110-state.json) | Parent phase state, inspected not changed |
| [src/core/src/zava_forward/core/synthetic/sensor_stream.py](src/core/src/zava_forward/core/synthetic/sensor_stream.py) | Replay, descriptor, budget and pacer |
| [src/api/src/zava_forward/api/iot_stream.py](src/api/src/zava_forward/api/iot_stream.py) | Origin decoding, receiver/publisher and lifecycle |
| [src/core/tests/test_sensor_stream.py](src/core/tests/test_sensor_stream.py) | New core coverage |
| [src/api/tests/test_iot_stream.py](src/api/tests/test_iot_stream.py) | New transport/SQLite coverage |
| [src/core/pyproject.toml](src/core/pyproject.toml) | Core typing overrides |
| [src/api/pyproject.toml](src/api/pyproject.toml) | API dependency pins and typing overrides |
| [src/api/requirements.in](src/api/requirements.in) | Runtime lock inputs |
| [src/api/requirements.txt](src/api/requirements.txt) | Generated hashed lock |
| [src/core/README.md](src/core/README.md) | Core callable contract |
| [src/api/README.md](src/api/README.md) | Transport activation/recovery contract |
| [docs/reference/research/iot-sensor-analytics-research-plan.md](docs/reference/research/iot-sensor-analytics-research-plan.md) | Issue-by-issue synthesis and live deferrals |
| [docs/reference/README.md](docs/reference/README.md) | Knowledge-base index delta |
| [docs/reference/log.md](docs/reference/log.md) | Append-only knowledge-base log delta |
| [.copilot-tracking/reviews/logs/2026-10-27/iot-consumer-110-review.md](.copilot-tracking/reviews/logs/2026-10-27/iot-consumer-110-review.md) | This single independent Review |

## Next Steps

Parent continuation: route RV-001-RV-003 to later rpi-implement and preserve
this original Complete / Not accepted Review. Keep the four plan follow-ups
and related live/composed work distinct. Do not run another Review, infer issue
closure or publish from this verdict. The parent owns any separately authorized
single changed-gate attempt after commit; final-publication requirements and
live acceptance remain unproven and cannot be waived here.
