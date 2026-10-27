---
title: IoT consumer final-candidate plan critique
ms.date: 2026-10-27
---

## Metadata

* Task ID: 110 / iot-consumer-110.
* Critique date: 2026-10-27.
* Plan: .copilot-tracking/plans/2026-10-27/iot-consumer-110-plan.md.
* Phase details: .copilot-tracking/details/2026-10-27/iot-consumer-110-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one final-candidate critique; no additional pass.

## Inputs and Criterion Boundary

* Caller direction: deliver #110/#184 and children #185-#189 in one PR from
  prepared feat/iot-consumer-110. ADR 0003 authorizes source engineering in the
  Free/B1 envelope and existing ama scope, not deployment. No Azure operations,
  secrets, private datasets or uv; local tests only.
* Supplied research:
  .copilot-tracking/research/2026-10-27/iot-consumer-110-research.md, including
  C1-C6/W1-W5 and its explicitly failed routed-property lookup.
* Read the named issue bodies, required repository context, ADR 0003 dated
  authorization, infra/README.md IoT contract, PRD AC-066, existing IoT synthesis,
  core composition guide, SensorIngestion, SensorConsumer, sensor_stock,
  sensor_backfill, sensor_faults and existing sensor integration tests.
* Dependencies: merged infrastructure and historical generator are available
  source contracts; P02 depends on P01 and P03 on both. #186 is already delivered.
  #185 credential operations, #188 actual Hub/Azure SQL evidence and #189 actual
  headroom/alert verification remain owner-operated and deferred.
* Test ownership: at most two new modules,
  src/core/tests/test_sensor_stream.py and src/api/tests/test_iot_stream.py;
  no test removals. All proposed cases below belong in those modules or reuse
  existing suites; no additional test module is requested.
* Validation authorization: at most one --changed gate, heavy-lock timeout zero,
  never --all. This narrower authorization controls command selection; it does
  not turn an unavailable or failing gate into a passing publication receipt.
* Boundary: assess implementation credibility, identity authority, durable SQL
  ordering, replay identity, bounded lifecycle and evidence/publication claims.
  This is not live transport acceptance, legal approval or an implementation
  review. The only authored file is this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #110 identity and no public endpoint; C1-C3; P02-T01 | Partial | Explicit activation and API ownership are sound; routed SDK property contract is unresolved, PC-001 |
| #110 durable append and replay; P02-T01 | Partial | Existing SQL receipt/commit boundary is sound; partition checkpoint/restart behavior is unspecified, PC-002 |
| #184/#185 synthetic identity and credentials; P02-T01 | Partial | Per-device X.509 and owner deferrals are credible; unmapped injection conflicts with identity fence, PC-004 |
| #186 shared schema and cadence; P01-T01 | Covered | Canonical observation required, 480-minute default explicit, already delivered status preserved |
| #187 replay, controls and failures; P01-T01/P02-T01 | Partial | Seed/origin and pause/deadline intentions are sound; lifecycle and exact replay-mode details need PC-003/PC-005 |
| #188 union, seam and restart; C4-C6; P01-T01/P03-T01 | Partial | Local SQLite boundary and live deferral are honest; generator-mode witness needs PC-005 |
| #189 quota/run limits; P01-T01/P02-T01 | Partial | Declared headroom/owner/alert and finite counts are sound; transport waits can outlive pacing deadline, PC-003 |
| Local tests, two-module limit, documentation; P03-T01 | Covered | Appropriate existing suites, static checks, index/log and issue-specific evidence |
| Single Review and constrained gate/publication; P03-T01 | Partial | No repeated Review or full gate requested; failed/busy gate must block publication, PC-006 |
| Live AC-066, OD-43 and owner operations | Covered | Explicitly deferred; no mock, source-only infrastructure or SQLite result can satisfy these gates |

## Verdict

* Verdict: Revise.
* Severity summary: four High, two Medium; no Critical or Low findings.
* Rationale: the overall architecture and local-only scope are credible, but the
  transport authority and restart/lifecycle contracts are not precise enough to
  implement safely without new assumptions. All six findings are direct
  corrections within confirmed user direction; none requires a new user choice.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Resolve the routed SDK identity contract before implementing its fence

* Related IDs: #110, #185, C1, W3/W4, P02-T01.
* Evidence: phase-details lines 41-54 require pinned SDKs and Hub connection
  metadata but do not name the SDK accessor, AMQP key/type or origin predicate.
  The research Evidence Log explicitly records failed retrieval of routed Python
  property placement. infra/README.md:3111-3143 requires the dedicated custom
  Event Hub, not the built-in endpoint. The local import probe found
  azure.eventhub and azure.iot absent; azure.identity is present.
* Concern: a property name alone does not establish whether the custom endpoint
  presents it as an annotation, system property or application property, nor how
  bytes/string values are represented. A fabricated EventData dictionary can
  accidentally prove an invented contract. The phrase "wrong-origin identity"
  also lacks an exact check and its trust assumptions.
* Impact: valid routed traffic could be rejected, or caller-controlled metadata
  could be mistaken for authenticated Hub identity and bind another sensor/home.
* Smallest useful change: add a bounded dependency/API-contract prerequisite to
  P02. Select exact versions, verify the corresponding SDK accessor/key/value
  representation using supplied W3/W4 and installed SDK source after authorized
  dependency changes, and record which routing properties are Hub-set and why
  the configured dedicated endpoint is trusted. Define conflict/missing/type
  handling and permitted decoding explicitly; do not guess aliases or use
  application home/device claims as fallback. Keep actual routing unproved.
* Action owner: planning parent; API implementer supplies the SDK witness.
* Exact resolving evidence: revised P02 details name the pinned versions,
  accessor/key types, origin trust boundary and rejection rules, with a precise
  SDK/source pointer. src/api/tests/test_iot_stream.py uses actual EventData/AMQP
  representation for a positive case and missing, conflicting, wrong-type,
  spoofed-application-property and wrong-configured-origin cases. Record any
  remaining actual-routing verification as deferred, not passed.
* Decision route: Direct planner correction. Missing SDK evidence is a bounded
  prerequisite, not authorization for Azure activity or a user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Define partition checkpoint persistence and the restart position

* Related IDs: #110 idempotency, #188 rerun, P02-T01, P03-T01.
* Evidence: phase-details lines 50-52 specify SQL-before-checkpoint and original
  identities on retry but no checkpoint store, starting position, inclusive
  behavior or partition serialization. SensorConsumer.process at
  src/core/src/zava_forward/core/sensor_consumer.py:557-640 reconciles durable
  outcomes; its _write boundary commits before a successful public return.
  SensorIngestion consumes finite batches with acknowledged-prefix reporting.
* Concern: checkpoint ordering alone does not define recoverability across a
  fresh SDK client. An in-memory/no-store checkpoint can disappear; an implicit
  latest start can miss earlier events. Concurrent callbacks within one partition
  can checkpoint a later offset beyond a failed earlier event.
* Impact: SQL idempotency cannot recover messages that are never redelivered.
  A restart demonstration could pass using a test that manually resubmits rows
  while the real receiver resumes past the failure.
* Smallest useful change: choose and document either a supplied durable
  checkpoint abstraction or an explicit bounded retained-history replay policy
  with a deterministic start and SQL deduplication. No new cloud service is
  needed. Require serial SQL/checkpoint processing per partition, monotonic
  successful offsets and no checkpoint advancement beyond a failed event.
  Specify checkpoint-write failure and restart behavior, including the case
  where SQL committed but the checkpoint did not.
* Action owner: planning parent and API implementer.
* Exact resolving evidence: revised P02 restart/partition contract plus tests in
  src/api/tests/test_iot_stream.py that construct a new receiver, preserve only
  the chosen durable state, and resume after accepted SQL, durable DQ, SQL
  failure, uncertain commit and checkpoint failure. Assert actual SQLite row/DQ
  counts and no skipped failed offset or duplicate insert. Include two
  partitions to distinguish partition-local ordering from global offsets.
* Decision route: Direct planner correction within the existing local adapter
  scope; durable Azure checkpoint operations remain deferred if selected.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Make the run deadline cover SDK operations and cancellation

* Related IDs: #187, #189, P01-T01, P02-T01.
* Evidence: plan lines 63-67 promise runtime at most 3600 seconds, finite rate,
  no autonomous reconnect and cleanup. Phase-details lines 30-32 only bind
  pacing/pause to the monotonic deadline; lines 50-52 require terminating receive
  and closing resources but specify no API mode, operation timeout, SDK retry
  flags or callback-to-runner failure channel.
* Concern: connect, idle receive, send, checkpoint and shutdown can wait outside
  the pacing loop. "Cancel/close" does not explain how a failed callback stops a
  receive loop that catches callback exceptions, or how cancellation interacts
  with an in-flight SQL operation. Default reconnect/retry settings are not
  explicitly overridden.
* Impact: a nominally finite simulator can remain connected or continue sending
  after stop/deadline. Cancellation could acknowledge an event before its SQL
  outcome is known or leak clients and secret-bearing exception context.
* Smallest useful change: define the sync/async runner strategy, bounded
  connect/send/idle/checkpoint/cleanup waits, explicit SDK reconnect/retry
  settings, and a first-failure channel that stops callback admission and the
  receive runner. Define a finite cleanup allowance within the declared total
  bound. Do not treat cancellation of a task/thread as cancellation of a SQL
  commit: uncertain outcomes must retain identities and remain uncheckpointed.
  Cover normal completion, external stop, timeout and cancellation separately.
* Action owner: planning parent and API implementer.
* Exact resolving evidence: revised lifecycle state/timeout contract, with
  src/api/tests/test_iot_stream.py cases for blocked connect/send, idle receive,
  callback failure caught by the fake SDK, checkpoint failure, cancellation
  during SQL and bounded cleanup. Assert no later send/checkpoint, exact
  resource cleanup including owned credentials, sanitized error output and
  disabled SDK reconnect. Core deterministic pacing tests remain in the one
  allocated core module.
* Decision route: Direct planner correction. No owner decision is needed to
  enforce the already required finite-run boundary.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Reconcile the unmapped fault with strict device-to-sensor binding

* Related IDs: #110 visible unmapped DQ, #185 identity, #187 faults, P01-T01/P02-T01.
* Evidence: phase-details lines 33-34 require forced AC-066 faults while lines
  46-49 require one selected device/sensor/home and rejection of identity
  mismatch before SQL. src/core/src/zava_forward/core/synthetic/sensor_faults.py:
  139-140 implements unmapped by changing sensor_id to "UNMAPPED-" plus its
  original ID. Existing test_sensor_consumer.py proves this reaches UNMAPPED
  under direct SQL admission.
* Concern: sending that existing fault through the normal device binding makes
  it an identity mismatch, stopping before owned SQL DQ. Relaxing the fence
  based on a fault label or application home claim would instead weaken the
  authority boundary. The plan currently promises both outcomes without a path.
* Impact: the required fault exercise either cannot complete as claimed or
  introduces an unintended bypass allowing a device to name other sensors.
* Smallest useful change: explicitly choose a trusted synthetic-only fault
  binding established before receive, such as a separate explicitly configured
  device mapped to its exact intentionally unmapped compact sensor and same
  granted stock home, while leaving that sensor absent from SQL controls.
  Otherwise classify the normal-device mutated-ID case as a transport refusal
  and defer its routed SQL-DQ proof. Never use payload fault/truth markers to
  authorize an exception. Preserve one exact binding per device.
* Action owner: planning parent; core/API implementer owns paired test coverage.
* Exact resolving evidence: revised fault/binding table distinguishes normal,
  deliberately unmapped and spoofed devices. The API test module proves the
  selected path and unchanged SQLite property/audit state; a normal device
  claiming another or UNMAPPED sensor still stops without checkpoint. If the
  routed DQ case is deferred, the #110/#187 criterion map says so explicitly.
* Decision route: Direct planner correction using already permitted synthetic
  configuration or honest deferral; no device provisioning is authorized.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Bind the replay witness to a specific existing model and packet boundary

* Related IDs: #186 schema, #187 seed reproduction, #188 seam, C4/C5, P01-T01.
* Evidence: phase-details lines 25-34 require "existing backfill generator" and
  complete-origin suffix equality. src/core/README.md:2261-2318 distinguishes
  legacy and approved composed generation, whose manifest binds climate,
  measures, model versions and stock. sensor_backfill.readings defaults to
  legacy reading-v1 with injected_fault; _series and sensor_faults.observation
  produce the canonical consumer form in selected modes. sensor_faults.packets
  has independent seeded two-row state, requires even clean counts and can
  reverse, omit, duplicate or move observation timestamps.
* Concern: matching seed/origin alone does not choose between legacy and composed
  histories or define packet-aligned replay. Filtering a faulty stream only by
  observed_at can change suffix membership when skew moves timestamps, reorder
  an out-of-order packet or restart packet RNG. A self-comparison of the new
  stream generator would not prove equality with existing backfill.
* Impact: the local zero-difference seam criterion can pass vacuously while
  emitted observations differ in schema, values, units or replay membership from
  the selected historical model.
* Smallest useful change: identify supported model mode(s) and bind the complete
  run descriptor to the stock selection, seed, original window/cadence, model
  versions, explicit climate/measures when applicable and fault configuration.
  Specify canonical observation conversion and replay selection by stable
  nominal slot/packet identity, not mutated timestamp alone. Define odd-window
  behavior for the three-per-day default rather than padding silently.
* Action owner: planning parent and core implementer.
* Exact resolving evidence: revised P01 descriptor/selection contract and tests
  in src/core/tests/test_sensor_stream.py compare against the existing generator
  and packet functions, not only the new generator. Cover nonzero/odd suffix
  boundaries, skew, reversed/duplicate/gap packets and the declared model mode.
  API SQLite tests compare union IDs, units, timestamps and numeric overlap
  against that same witness; unsupported modes are explicitly excluded, and
  actual statistical/live Azure handover proof remains deferred.
* Decision route: Direct planner correction; choosing a bounded supported
  existing mode or documenting an unsupported mode is not a new physics claim
  or permission to access private data.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Make failed or unavailable gates a stop before push

* Related IDs: P03-T01, one-PR publication, user-constrained local gate.
* Evidence: plan P03 says a busy heavy lock means "skip and disclose".
  Phase-details lines 69-71 say disclose busy/missing prerequisites followed by
  push and PR creation, without a conditional stop. Repository publication
  instructions require a valid exact-candidate receipt and immediate pre-push
  verification; missing prerequisites block publication. The caller authorizes
  at most one --changed run with timeout zero and expressly forbids --all.
* Concern: the handoff can be read as permission to publish after the sole gate
  attempt is busy, missing prerequisites or failing. Disclosure is not gate
  satisfaction. A later source/evidence commit also invalidates an earlier
  candidate receipt.
* Impact: the implementation could exceed its publication authority even while
  accurately reporting that validation did not pass.
* Smallest useful change: make push/PR conditional on the authorized scoped gate
  passing and receipt verification against the fetched current main and final
  candidate. Busy/missing/failing means retain committed work and report blocked
  publication, with no second gate or --all fallback. Preserve original Review
  outcomes and record correction evidence without another Review. Any later
  invalidating change stops publication until separately authorized.
* Action owner: planning parent.
* Exact resolving evidence: revised P03 includes an explicit pass/blocked branch,
  exact-head/base receipt verification and no retry/full-gate fallback. The
  changes record subsequently captures the actual single attempt and either a
  verified receipt plus eligible publication or a truthful blocked closeout.
* Decision route: Direct planner correction. Existing user direction resolves
  command scope; a blocked gate does not require inventing broader permission.

## Strengths and Residual Risk

* API-owned adapters, core-owned pure replay and no new HTTP route preserve the
  existing separation and avoid startup cloud activation.
* SQL already provides durable accepted/rejected receipts, owned DQ and exact
  replay reconciliation. Reuse this rather than introduce new ingestion rules.
* Synthetic stock selection, independent consent/calibration, available cases
  and human/resident boundaries remain intact.
* Actual credential issue/rotation/teardown, private routing, Azure SQL restart,
  actual quota/spend/alerts and registered real AI evidence remain deferred.
  These are accepted scope exclusions, not findings requiring cloud work.
* B1/one unit and the dedicated Event Hub are already selected within the
  approved source scope. No new tier, owner appointment or deployment decision
  is requested. Budgets remain alerts rather than hard spending stops.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents direct plan revision.
* Routed SDK representation needs the bounded PC-001 witness before its
  implementation contract can be treated as verified. This is not a reason to
  expand research or perform live routing in this task.

## Limitations

* No implementation exists for the planned adapters in the assessed candidate.
  No tests, gate, Azure command or SDK installation was executed by this critique.
* Named issue bodies were read, but stale "not started" prose does not override
  merged repository evidence. No issue status was changed.
* No fresh external documentation retrieval was performed; supplied W3-W5 are
  research pointers, not independent proof of exact routed SDK field placement.
* Existing untracked plan/research/session files belong to the parent. They were
  not changed, moved, staged or committed. No additional agent was launched.

## Recommended Next Action

* Highest-impact finding: PC-001, routed SDK identity authority.
* Action owner: planning parent.
* Smallest next action: revise P02 with the explicit SDK-contract prerequisite
  and fail-closed binding rules, then disposition all six findings in the plan
  and details before advancing to implementation.
* User response required: No.
* Do not request or run another final-candidate critique.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/iot-consumer-110-plan.md](.copilot-tracking/plans/2026-10-27/iot-consumer-110-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/iot-consumer-110-phase-details.md](.copilot-tracking/details/2026-10-27/iot-consumer-110-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-27/iot-consumer-110-research.md](.copilot-tracking/research/2026-10-27/iot-consumer-110-research.md) | Supplied evidence and deferred live gates |
| [.copilot-tracking/reviews/plans/2026-10-27/iot-consumer-110-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/iot-consumer-110-plan-critique.md) | This single Complete / Revise critique |

## Next Steps

The active planning parent corrects and dispositions PC-001 through PC-006
directly, finalizes the plan without another critique, then continues the
confirmed ordered RPI loop within its existing authorization. No user action is
required for these corrections. An unavailable or failing authorized gate blocks
publication rather than authorizing a second attempt, --all or Azure fallback.
