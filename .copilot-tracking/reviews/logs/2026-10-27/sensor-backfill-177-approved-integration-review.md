<!-- markdownlint-disable-file -->
# Review: Approved sensor backfill integration

## Scope and Evidence

* Task ID: 177-approved-integration-2026-10-27
* Review date: 2026-10-27
* Assessed implementation commit: 263e1dbfddd0587528c37dca5b8abb9697208dc9
* Review scope: complete integrated implementation diff from 864a502126ee0dfedf13eaf54f08a10f2339279c through 263e1dbfddd0587528c37dca5b8abb9697208dc9, including completed P01-P03, dependencies, tests, documentation, critique dispositions and acceptance qualifications. P04 publication gates remain separate.
* Branch: feat/sensor-backfill-177.
* Worktree: /home/azureuser/source/ama-wt/issue-177-backfill.
* Assessment count: one original independent Review; no nested agents, fixes or second Review.
* Plan: .copilot-tracking/plans/2026-10-27/sensor-backfill-177-approved-integration-plan.md
* Details: .copilot-tracking/details/2026-10-27/sensor-backfill-177-approved-integration-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/sensor-backfill-177-approved-integration-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/sensor-backfill-177-approved-integration-changes.md
* Research: .copilot-tracking/research/2026-10-27/sensor-backfill-177-approved-integration-research.md

## Opening Review State

* Goal: one independent post-implementation assessment of approved source,
  canonical IDs, composed behavior and aggregate evidence.
* Evidence readiness: P01-P03 markers and artifacts reconciled; full core,
  static/types, actual sensor SQL and every-row full-stock results available.
* Acceptance basis: current owner decisions and plan, PC-001 through PC-004
  dispositions, explicit daily/public-fixture/scientific boundaries.
* First comparison boundary: complete implementation diff against supplied
  base 864a502126ee0dfedf13eaf54f08a10f2339279c, preserving original
  historical critique and Review. This is a fixed source boundary, not a
  claim that the moving origin/main still equals that base.
* Read-only boundary: only this canonical Review record may be written;
  no source, plan, changes, critique or issue/PR mutation.
* Initial blockers: none to source Review. Sole scoped gate not run yet;
  exact-head publication receipt and hosted checks cannot be inferred.

## Execution Status

* Review execution status: Complete.
* Review execution evidence: the full runtime diff, changed tests/configuration,
  component documentation, knowledge-base continuation, current task artifacts,
  child ancestry and accessible external validation evidence were compared.
  One bounded, output-free adversarial probe confirmed RV-001.
* Implementation execution status: Partial across the full plan. P01-P03
  execution and aggregate evidence are present; P04-T01 is delivered by this
  record. P04-T02 has not run. Review completion does not mean implementation
  acceptance or publication completion.
* Write boundary: only this record was edited. The pre-existing modified
  continuation state file was neither changed nor reconciled by this reviewer.
  No GitHub operation, install, cleanup, gate, commit or publication was run.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01 / P01-T01 | Approved climate delivery at 09ea9e23 | Reconciled | Real 2023-2024 paired acquisition, strict core adapter and explicit synthetic-demo approval; no repeated year. |
| P02 / P02-T01 | Canonical identity delivery at 6fc8d0fe | Reconciled | Canonical export keys, compact fault-safe sensor namespace, separate store availability and retained independent controls. |
| P03 / P03-T01 | Parent integration and normal child merges | Reconciled | All five exact child source heads are ancestors; integrated opt-in model and retained legacy path are visible in source. |
| P03 / P03-T02 | Aggregate validation and pre-Review reconciliation | Reconciled with RV-001 | Actual scale and regression evidence support the exercised paths; the composed loader's pre-replay budget guard has an untested defect. |
| P04 / P04-T01 | Independent Review pending at assessed commit | Delivered by this record | Parent owns later marker/state reconciliation; no source or planning changes made here. |
| P04 / P04-T02 | Pre-Review remaining work | Not executed, correctly open | Original Review evidence commit, authorized archive/clean, sole scoped gate, receipt assessment and publication remain. |
| Follow-Up Items | Scientific, regional, private-register and real monitoring limitations | Reconciled | Excluded from bounded demo acceptance; distinct follow-up owner/action below. |

The plan's original Implement handoff and changes record's "in progress" header
are stage/history prose, not claims that P04 passed. Checked P01-P03 markers,
phase-index statuses, latest changes closeout and unchecked P04 markers form a
credible current review boundary. No historical adverse outcome was reclassified
as a new failure.

## Completed Work Assessment

| Scope | Files | Completion evidence and assessment |
| --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/synthetic/climate_history.py; src/core/tests/test_climate_history.py; docs/reference/research/climate-paired-source-178/ | Strict JSON/numeric/unit/hash/UTC alignment, Magnus consistency, record-derived bounds and exact covered subsampling. Read-only validation accepted all 17,544 committed hourly pairs. NASA remains a separate 2023 sensitivity input. Provenance explicitly admits unavailable exact provider revision and unverified underlying production/legal terms. |
| P02-T01 | src/core/src/zava_forward/core/synthetic/sensor_identity.py; src/core/src/zava_forward/core/synthetic/sensor_stock.py; src/core/src/zava_forward/core/sensor_consumer.py; src/core/tests/test_sensor_stock.py; src/core/tests/test_sensor_consumer.py | Eleven-character sensor keys derive from the complete canonical ID; duplicate sensor hashes stop generation. Home keys remain case/Unicode-preserving and <=128 UTF-16 units. Consumer availability is explicitly <=64 units on both stores, with no case creation, aliasing or control grant. Actual SQL/API evidence includes the inherited canonical tests. |
| P03-T01 | src/core/src/zava_forward/core/synthetic/indoor_projection.py; src/core/src/zava_forward/core/synthetic/retrofit_effects.py; src/core/src/zava_forward/core/synthetic/household_conditions.py; src/core/src/zava_forward/core/synthetic/sensor_backfill.py; src/core/src/zava_forward/core/synthetic/sensor_faults.py | Explicit dated multiplier, household setpoint and moisture/ventilation feed a separately versioned composition. No empty-history inference or legacy enum coercion. Legacy equation/RNG regression coverage remains. Analysis observations omit fault truth; deterministic gzip and input/model fingerprints are present. Actual consumer processing follows reconstructed-byte verification, except the resource-bound defect RV-001 occurs before that verification. |
| P03-T02 | src/core/tests/test_historical_backfill.py; other changed component tests; external aggregate evidence | Seven composed tests cover field effects, exact activation, unrelated-home neutrality, exclusions, deterministic compression, provenance, consumer replay and tampering refusal. These do not cover a forged homes_covered value under a small replay budget. The successful full-stock evidence remains valid for its declared inputs; RV-001 does not contradict those run results. |
| Documentation/configuration | src/core/README.md; docs/reference/README.md; docs/reference/log.md; docs/reference/research/iot-sensor-analytics-research-plan.md; src/core/pyproject.toml | Current continuation distinguishes historical component delivery from integrated behavior and preserves old outcomes. Index/log/synthesis reconcile actual evidence and limitations. The mypy override is restricted to calls from the new aggregate test module into existing untyped generator APIs. No application dependency was added. |

Normal merge ancestry was checked for:

* Climate: 09ea9e23f1634d593ebd2dacf1b1f7fe78925c1b.
* Identity: 6fc8d0fef27839f720ddbbb1c13c91a1ca52c128.
* Projection: c74a1015bf5f6f0af10c002faada72c50b4364b1.
* Retrofit: c969eae53d3d348cbe68f1f95ce90159cea7fed2.
* Household: e0491c441de0386cec5077e3c9e5e34ccbe1787a.

All five are ancestors of the assessed head. Merge history retains the
projection, retrofit, household, identity and climate integration commits.
Overlapping README sections remain, explicitly labelled as original independent
delivery boundaries before the new integrated section.

## Implementation-Time Plan and Detail Update Assessment

| Area | Update, rationale and trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01/P02 execution ownership | Split climate and identity into independent whole phases for disjoint worktrees | Current markers/details/dependencies agree. Historical PC phase labels remain explicitly historical; no requirement or owner decision was dropped. |
| P03 dependency refinement | Composition and already-delivered child merges could proceed against the agreed ClimateHistory.series/manifest seam while actual acquisition continued | Changes record and plan both preserve final climate merge/aggregate validation dependency on completed P01. Final implementation uses the agreed seam and real source; no unsupported source fallback appears. |
| PC-001/PC-002 identity qualification | Resolve existing SQL case ceiling and fault-prefix interaction without shared-schema expansion | Plan acceptance/details and actual consumer code agree on 128-unit export versus 64-unit available cases, and 11+9-character fault IDs. Independent consent/calibration/clock/order checks remain. |
| PC-003 composition | New explicit composed projection instead of placing arbitrary effects in a construction whitelist | Versioned parameters, input fields, aggregate tests and manifest agree. This is the approved synthetic integration, not physics calibration. |
| P03 scale/cadence | Generated public stock, deterministic compression, measured hourly estimate and complete 730-day daily run | Approved current plan and research already authorize this boundary. No private-register equivalence or billion-row hourly execution is claimed. |
| PC-004 documentation | Preserve original evidence and reconcile the existing synthesis/index/log before Review | Final assessed candidate contains the required durable continuation. Historical source/identity blockers are prospective history, not unresolved owner decisions for this approved demo. |

The significant decisions are supported by owner-approvals-2026-10-27-b and
the current plan/details. No new decision gap requiring rpi-plan or new material
source-evidence gap requiring rpi-research was identified. The one original
Complete / Revise critique remains unchanged; its direct planner dispositions
precede the affected approved implementation. No renewed critique is inferred.

## Critique and Material Revision Assessment

| Finding | Disposition assessed | Result |
| --- | --- | --- |
| PC-001 High | Full canonical export domain separated from exact available-case domain; unchanged shared case schema; explicit unsupported legacy SQL-column failure | Addressed for bounded demo. Tests cover 64/65/128 units, case/Unicode, absent homes and independent controls; 45 actual SQL/API tests passed in the supplied log. No universal 128-unit SQL case admission claim. |
| PC-002 Medium | Compact key reserves UNMAPPED- namespace and collision detection | Addressed. Real packet/consumer test asserts UNMAPPED, not IDENTITY; canonical valid admission/replay remains separately tested. |
| PC-003 High | Explicit multiplier and household condition composition, separate legacy equation and fingerprinting | Addressed. Field-effect, low combined-loss, dated boundary, no-history/other-home, exclusion and legacy coverage are present. RV-001 is a separate loader budget defect, not an unresolved composition decision. |
| PC-004 Medium | Durable continuation in synthesis, index and append-only log | Addressed in the assessed candidate. Original outcomes and production/legal limits are retained. |

No evidence of continuing affected work against an undispositioned significant
decision was found. New Review findings are not used to rewrite the critique's
original outcome or create another assessment.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Route |
| --- | --- | --- | --- |
| Production physical/source/regional qualification and real monitoring approval | Synthetic-demo authorization does not establish physical calibration, region-wide representativeness, underlying legal qualification, device mappings or real resident authority | Future production/monitoring work owner to obtain named technical, legal/compliance and resident/operational approval before any activation | Distinct follow-up; not a new active Pxx task or a defect in the approved demonstration. |
| Exact private-register equality and full-hourly/diurnal-scale acceptance | Private inputs are expressly excluded; the selected full-stock exercise is daily, with hourly capacity estimated separately | Owner to scope any future authorized data comparison or higher-cadence validation separately | Preserve as explicit acceptance limitations, not invented deferred approval or new current implementation scope. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Composed replay budget trusts manifest home count before regenerating the supplied stock

* Related scope: P03-T01/P03-T02; bounded-memory/output replay and rejection of
  invalid inputs before mutation.
* Evidence: src/core/src/zava_forward/core/synthetic/sensor_backfill.py:466-480.
  load_with_consumer reads homes_covered from the unverified manifest and checks
  max(homes * days * 1440 // cadence, len(stock.rows)) against max_rows.
  It does not first require homes to equal the supplied selection's actual
  granted sensor count. write then uses the actual stock, not that manifest
  count, to regenerate the complete snapshot. Only afterward do
  _compare_snapshot and the expected["rows"] guard run. In contrast, the legacy
  _verify_snapshot checks the actual granted count before write at lines 532-539.
* Reproduction: an output-free, read-only probe supplied two explicitly synthetic
  granted homes, manifest homes_covered=1, days=1, cadence_minutes=60 and
  max_rows=24. Path.read_text was mocked with that manifest; TemporaryDirectory
  was replaced by nullcontext, and write was intercepted before generation.
  The interceptor printed
  "REPLAY_ENTERED declared_rows=24 actual_rows=48 max_rows=24".
  No output, SQL, consumer processing or real temporary directory was created.
* Impact: an inconsistent/tampered manifest can trigger replay output far above
  the caller's explicit row budget before it is refused. At the exercised
  60,000-home, 730-day hourly size, lowering the untrusted homes_covered value
  can admit nominal regeneration of 1,051,200,000 rows under the default
  2,000,000-row cap. This defeats the resource guard and can exhaust local
  storage/CPU; it does not demonstrate unauthorized consumer admission.
* Severity rationale: Medium, a reproducible resource-bound correctness defect
  in an explicit verified-loader safeguard. No remote exploit, actual disk
  exhaustion or corrupted SQL result is asserted.
* Destination: later rpi-implement on the accepted current direction.
* Smallest useful next action: validate the manifest's home count against the
  supplied selection before write and bound replay from the actual granted
  sensor count and requested slots, retaining metadata/row and fault safeguards.
  Add a bounded regression asserting write is not called for under-reported
  counts, with normal/zero-granted behavior and existing replay still covered.
  Keep the original Review outcome; do not run another Review.

Severity summary: 0 Critical, 0 High, 1 Medium, 0 Low. This is the complete
substantive finding set for the assessed boundary.

## Defects

* RV-001: composed-loader pre-replay row budget can be bypassed by inconsistent
  manifest metadata. Route to later rpi-implement; unresolved at this head.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 Medium | rpi-implement | Active parent to correct actual-stock replay budgeting and add the pre-write refusal regression | Implementation defect within approved scope, not an owner decision or research gap. |

Later implementation of this finding does not require another Review. This
original assessment remains attached to its exact assessed head.

## Residual Work

* Distinct production/monitoring qualification follow-up above remains outside
  this synthetic exercise.
* Full-hourly validation and exact excluded-private-register equality are not
  results of this task and must not be represented as passed acceptance.
* P04 publication is remaining active plan work, not a newly invented defect or
  an outside-scope follow-up.

## Blockers and Remaining Work

* Source acceptance/readiness blocker: unresolved RV-001 at the assessed head.
* Publication blocker: P04-T02 gate and publication sequence have not run.
  The pre-existing modified state and this untracked Review record also mean
  this worktree is not an exact clean gate candidate.
* Moving base: local origin/main resolved during Review to
  2e031c89a18ce1ceb3de4fda014fddcb90231fda, one commit beyond the supplied
  864a502126ee0dfedf13eaf54f08a10f2339279c boundary. This Review did not fetch,
  rebase or silently change its source comparison. The publication owner must
  fetch and bind the actual then-current main in the authorized gate/receipt
  sequence. No receipt against either base exists or is implied here.
* After later implementation, the parent must reconcile original evidence/state,
  commit with the required authenticated noreply identity/trailer, and use the
  authorized finite archive/restore-verified cleanup before the one foreground
  --changed --lock-timeout 0 parent gate with a fresh external output directory.
  The scoped owner instruction supersedes --all; this Review ran neither.
* Official partial-scope receipt verification against the fetched current main,
  independent exact-head administrative receipt assessment, normal publication
  and passing applicable hosted checks remain mandatory. No parent ready
  transition, merge, issue acceptance or closure is authorized by this record.
* Any later correction/commit/source/base/input change requires evidence bound
  to the resulting candidate. Do not treat this implementation-head assessment
  or a historical receipt as a gate for changed bytes. Do not repeat this Review.

## Validation Evidence

External evidence root:
/mnt/ama-rpi-gates/177-approved-integration-20261027/.
These files are evidence inputs, not reviewer write targets.

| Check | Status | Evidence and scope |
| --- | --- | --- |
| Complete implementation diff and git diff --check 864a502..263e1db | Passed in Review | All changed runtime modules, tests/configuration and current related documentation inspected; no diff whitespace error. |
| Five git merge-base --is-ancestor checks | Passed in Review | Each exact supplied child source head is retained at assessed HEAD; no squash ancestry substitution. |
| Full core unittest discovery | Passed, existing run inspected | core-unit.log: Ran 1427 tests in 311.378s; OK (skipped=186). Skips remain explicitly outside passing execution; no suite rerun or benchmark rerun here. |
| Core Ruff/format/mypy | Passed as supplied implementation evidence | Changes record reports complete Ruff, 100-file format and 153-source mypy passes. Separate raw static-check logs were not present in the supplied evidence root; not independently re-executed or upgraded to gate evidence. |
| Existing task-owned sensor_sql_check.py harness | Passed, existing run inspected | sensor-sql.log: actual loopback SQL/API run, 45 tests in 16.351s, OK, owned container removed. This is not an RPI gate or a claim that every optional SQL test in the full unit suite ran. |
| Seven aggregate composition tests and 12 climate adapter tests | Passed in supplied implementation/full-suite evidence | Test methods inspected for asserted semantics, including actual consumer replay/tampering refusal and climate structure/hash/time/unit failures. Not independently rerun. |
| Full-stock generator and every-row/ID reconciliation | Passed, existing evidence inspected | scale-summary.json and full-stock/manifest.json: 60,000 generated public homes, 730 days, 1440-minute cadence, 43,800,000 rows, everyrow/everyID flags true, 6,000 explicit synthetic measures, 703,111,263 compressed reading bytes; 60 shards. No expensive regeneration or 43.8-million-row re-scan here. |
| Scale provenance binding | Passed in Review | Read-only import of exact local source recomputed sha256:7a4179b6720337eac04dcbfa59c7f36f6efef24d75c946879e11898f2bd5e893, matching summary and manifest. Manifest byte SHA-256 6625698566e3a7b8ca4a7efc38d870edf629f97cb0a4c23dd0e87ece8acc16d4 matches summary; source input hash af76a90414d9ad8f19dacc95a38f06d4c4321a91bdf030ba231558c42506051e agrees with pinned source and manifest. |
| Climate read/coverage | Passed in Review | Exact assessed core source accepted retained raw/metadata and returned 17,544 genuine hourly pairs for 2023-2024; scale window is 2023-01-02 through 2025-01-01 exclusive, exactly 730 days. No source download or new terms verification. |
| Actual-source seed/fault replay | Passed, existing evidence inspected | reproducibility-summary.json: four generated homes, two days, hourly cadence; every same-seed file identical, changed seed changes readings; separate truth, outlier/duplicate/gap rates each 0.1. Not a full-hourly estate run. |
| Pre-generation volume estimates | Passed, existing evidence inspected | hourly-estimate.json: 1,051,200,000 rows, 158.0 bytes/CSV row, 154.68 GiB; daily-estimate.json: 43,800,000 rows, 6.45 GiB. Both sampled 20 homes, exclude SQL/index overhead and are estimates, not actual hourly storage results. |
| RV-001 bounded no-write semantic probe | Defect confirmed in Review | Actual assessed load_with_consumer reached intercepted write for 48 nominal actual rows under max_rows=24 after trusting a 24-row manifest count. All output/temporary-directory/SQL effects were prevented by mocks. |
| Independent fresh unit/static/SQL suite execution | Not run | Existing logs are sufficient to assess their declared coverage; no expensive repeat was authorized or needed. The permitted home venv initially imported the climate child worktree and lacked revision_sources(composed=...). That read-only probe failed; no test result was claimed from it. Subsequent read-only probes explicitly selected src/core/src, verified __file__ in this assessed worktree, and disabled bytecode with PYTHONDONTWRITEBYTECODE=1 and -B. No install or candidate cache write. |
| Sole scoped RPI gate, final receipt and hosted checks | Not run / not assessed | P04 publication work intentionally remains. No fabricated gate result, full-tier claim, skip token, cleanup or cloud fallback. |

Scale reading SHA-256 from the retained evidence is
d07715c8b55fc4e0b6d771472f6f823110fe7b39ed47eab370ef7daf4d98bc41.
Normalized stock SHA-256 is
2802547013b069c6e3917d987e1bfcd3d9b758dae4e75a48a2b6381838cd98b2;
generated CSV SHA-256 is
91d2ae3f15e1f2d501faa7d9d24430263bc823a8179a40a016e7555ccb417dc7.
No exact ID-set comparison against private material was performed or inferred.

The integrated full diff adds five test modules and 39 test methods, including
the three already-delivered child component modules (13 methods). The approved
continuation's climate/identity/aggregate work adds two modules and 26 methods,
within its four-module/45-method allocation. No test method removal was found;
existing stock identity/revision expectations changed for the intentional
compact-ID/helper contract, not to conceal a failing assertion.

## Outcome

* Outcome: Not accepted.
* Rationale: source evidence broadly conforms to the owner-approved synthetic
  integration and resolves PC-001 through PC-004, but the reproduced Medium
  replay-budget defect RV-001 materially contradicts the loader's bounded
  reconstruction safeguard. The assessed head is not ready for publication.
* Review execution is Complete independently of that adverse outcome.
  Implementation execution across the whole plan remains Partial because P04
  gate/publication is unperformed. Successful existing core/SQL/scale runs are
  retained; they are neither erased by this finding nor treated as sufficient
  acceptance of the untested adversarial path.
* Bounded daily/public-fixture exercise, sampled hourly replay and synthetic
  source approval are justified qualifications of the current plan, not new
  failures for absent physical, regional, full-hourly or private-stock proof.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement, RV-001 | Active parent to correct actual-stock pre-replay budgeting and retain targeted evidence; no second Review. |
| Decision gap or invalid assumption | None identified | Approved direction and direct PC dispositions remain sufficient. |
| Material research gap | None for the bounded demo | Do not reopen already approved source terms as a new Review failure. |
| Non-blocking residual work | Distinct production/monitoring qualification follow-up | Future named technical/legal/compliance/resident and operational owners before activation. |
| Remaining active plan work | P04-T02 | Parent owns evidence commits, authorized clean, one scoped gate, verified receipt/exact-head administrative assessment and truthful hosted publication. |

* Assessed head: 263e1dbfddd0587528c37dca5b8abb9697208dc9.
* Assessed base: 864a502126ee0dfedf13eaf54f08a10f2339279c.
* Review execution: Complete.
* Outcome: Not accepted.
* Findings: one Medium, RV-001; no Critical/High/Low findings.
* Blockers: RV-001 and unperformed P04 publication prerequisites.
* No source fixes, plan/state changes, GitHub writes, gate execution or nested
  delegation occurred in this Review.
