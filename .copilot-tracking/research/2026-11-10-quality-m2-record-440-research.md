<!-- markdownlint-disable-file -->
# Research: #440 Quality-M2 current-main qualification record

Written 2026-11-10T01:06Z (readback `date -u`). Task `440-quality-m2-record`, branch `docs/demo-quality-m2-440-1110`, Refs #440 (criteria 6 evidence part only), #1288, #891, #184. Documentation-only checkpoint; no source, test, config, schema or workflow change. Planning Readiness: Ready. Research disposition: executed (new reading of the merged records and the external H2 raw evidence; no heavy check).

## Trigger and scope

* Trigger: merged #1331 (Quality retained-sensor evidence and guarded AI request path). Since then #1339 (witnessed transport-attempt accounting, replaces the envelope heuristic of the first #891 correction), #1341 (importer refusal CLI, unrelated surface) and #1342 (tracking-only H0/H1/H2 evidence) merged.
* Runtime proof already executed (H0, H1 adverse; H2 confirmed) and is tracked in merged records. The canonical dated evidence-pack record was still due. This task updates `docs/architecture/cutover-evidence-pack.md` in place, the reference index and the append-only log. It repeats no consumed finance #1234 checkpoint and creates no duplicate evidence page.
* Excluded: aftercare PR 1338 (open, base `feat/demo-quality-workflows-89-1109`), parent epic #149 (open), #132 and #1238 shared hooks, any live Azure, model or human acceptance.

## Source identities (read with Git, 2026-11-10)

| Item | Identity |
| --- | --- |
| Current `origin/main` (fetched) and this branch start | `32221a8459ff5c42d45be1dd86adccb5fcb4c1d6`, tree `74107550f69ce77108f15961d16e1e80f363338d`; PR 1342 squash |
| Quality merge, PR 1331 | `1b7a1719bee088ce2823bff45242e319bc928295` at 2026-11-09T22:47:40Z (final head `f995774ca2415f6ae8903b6f45683dd55432eff1`) |
| Accounting merge, PR 1339 | `ddeebd01694ddb46b456451d9ac6390347e51aaa` at 2026-11-10T00:17:56Z (head `1692b2315b59b6275a35a467af366c47ae72dfaa`) |
| Importer merge, PR 1341 | `5318f738f6bc58a10a9d4df1ca18ae51c1547a79` at 2026-11-10T00:54:31Z (head `80cc8363c64b61c0f7599732de892f9256f1c31c`) |
| Tracking merge, PR 1342 | `32221a8459ff5c42d45be1dd86adccb5fcb4c1d6` at 2026-11-10T01:01:55Z (head `d41195a274b921e320f94b65e8483b6022103c85`, tree `05e57c5b1af3151cbb972178785a63e190c73dc5`) |
| H2 observed source (external worktree) | merge `5d0460dd6c05312d0a905e69774d561c7ab8fc59`, tree `230c976d5ceaedea7515683f1746f685cc71d096`: main `ddeebd01` plus tracking-only records; dirty 2 (tracking timestamp corrections) |
| H0/H1 observed source | `a8593a7a8` (before #1339; the H0 record excluded "unmerged 891", which was true then) |

Git read-only comparison, all by `git diff` and `git rev-parse`:

* `git diff --stat ddeebd016 HEAD -- src infra tools .github`: six files only, all importer (`__main__.py`, `exceptions.py`, `mapping.py`, README, one new test) plus `.github/rubric/scores/latest.json` (bot score data). Zero bytes in `src/core`, `src/api`, `src/agents`, `src/orchestrator`, `infra`, `tools` or workflows.
* `git diff 5d0460dd6 HEAD -- src infra tools .github`: the same six files. The subtree ids of `src/core` (`7a83bae4adfa`), `src/api` (`ea090b15e073`) and `src/agents` (`db7717006298`) are identical at `ddeebd016`, `5d0460dd6` and HEAD.
* No Core, API or Agents file imports `zava_forward.importer`; core imports neither agents nor api; agents import neither api, orchestrator nor importer (grep counts 0). PR 1341 is therefore a separate surface that cannot alter the Quality path by import.
* Consequence: the H2 observation applies to an identical Core/API/Agents source tree at current main. It is a dated local observation of that identical surface, not a new runtime, Azure or hosted observation. No relevant code drift was found, so no acceptance is stopped for drift.

Hosted coverage read with `gh pr checks` (not rerun): PR 1339 head `1692b2315`: src-core, src-api, src-agents, src-orchestrator, src-importer and mssql all pass. That head's tree is not the merged tree: it differs from `ddeebd016` in `src/core/src/zava_forward/core/resident_decisions.py` and its test (the independently merged #1332 landed after the branch point). PR 1341 head `80cc8363c` likewise differs from `5318f738f` in the #1339 files (`ai.py`, `chat.py`, their tests, README). `gh run list --commit` shows no hosted `src-ci` run for the exact merged trees (merges to main ran only the rubric scorer and a skipped what-if). So an exact-head hosted success for current main is unobserved and is not claimed. The hosted `mssql` job selects `test_mssqlstore`, `test_lawstore`, `test_assistants.Mssql*` and `test_resident_aoai_sql`; it selects no `test_quality_sensors*` class (`.github/workflows/src-ci.yml`, `mssql` job), so the Quality SQL contracts are local-only evidence.

## Documents (blob ids unchanged since the previous checkpoint; draft is not approved)

BRD 0.21.0 `draft` `34d88395`; PRD (Zava Forward) 0.21.0 `in-review` `c788b917`; PRD (proper-warm) 0.13.0 `in-review` `f7f9b767`; case study original `0aec2d80`; addendum `28c19242`; ADR 0001 `d42fa5c4` Proposed; 0002 `cbe21530` (only the staff identity and role decision is owner-accepted, 2026-10-24); 0003 `d6064539` accepted with amendment (2026-10-15); 0004 `9406c2e7` accepted (2026-10-15); 0005 `4d610335` accepted for synthetic development only (2026-10-16); 0006 `956da1a3` accepted (2026-10-15); 0007 `abb21088` Proposed, not accepted (2026-11-04); parity matrix `91b5d33d` proposal for owner review. No statement in any of them is promoted by this task.

## Requirement trace inputs (document-qualified, no cross-document ID joins)

* PRD FR-050 (simulated humidity and temperature observations, deterministic review signals that can only create a human condition-review task); BRD FR-048 (consented in-use monitoring retained with provenance and calibration status). BRD FR-050 is opt-in chat memory, a different requirement: the document numbers collide, so every ID is document-qualified.
* PRD FR-008 and AC-010/011 (deterministic gates before controlled transitions; bulk or AI actions never approve); FR-017 and AC-020/042 (independent per-measure quality-disposition record, not established by an advisory display); FR-044 (real AI in accepted builds, assistance optional, manual completion never depends on model availability); NFR-017 with AC-109/110 (AI consumption bounds and metering; BRD NFR-012); FR-003/FR-072 and AC-144 (server-enforced roles); PRD CON-009 (accepted exercise build needs actual Azure hosting, real SQL state and a registered real AI task); FR-051/FR-053 and OQ-017 (RAI release, suspension and restart authority, unassigned).
* PRD AC-066 requires actual IoT Hub, Azure SQL after restart and a real AI task; its status is "Not run". The #1288 criterion 8 live walkthrough is the same kind of evidence and is unticked.

## What the merged work implements (read from the merged change records and README, spot-checked at HEAD)

* Retained read model and UI: `core/sensor_view.py` (bounded, permission-projected readings: Quality Inspector and Retrofit Programme Manager only), `Assistants.sensors` with API `GET /api/cases/{id}/sensors`, `web/assistants.js`, `web/ops.js`.
* Quality capture and flag: `core/assistants.py` captures the identical reading IDs the UI shows, cites them as `sensor:{sensor_id}:{reading_id}`, and a proactive current returned finding that cites a reading is an `review-suggested` flag, unapproved, requests human review and approves nothing.
* Sensor consent: control index in `core/sensor_consumer.py`, withdrawal withholds values, citations, derived output and flags; SQL guard triggers, dispatch hold and per-attempt gate before the first byte; an absent or unreconciled index fails closed.
* Transport and bounds: `core/ai_transport.py`, `core/ai.py`, `core/ai_consumption.py`; real-provider simulation route is code-off; private captured readings are never given to a real AI by the Agents worker or API composition (E2 tests); manual route remains when AI, store or release is unavailable.
* #1339: `ai.py` `DispatchWitness`, `count_dispatches()`; the chat adapter reports calls from the witnessed transport hand-off, not an envelope heuristic; unwitnessed providers are an unverified assumption of one. #891 criterion 2 (the token, cost, privacy, retention and refusal conjunction) stays unticked.

## Runtime evidence (external, VM-local) read for this task

The raw H2 bundle is VM-local under the coordinator session files (`logs-h2-matching-context-1110/sql-run/`, `merged-sql-proof-1109/`); it is not committed and not repeated here beyond identities and values. Read in full: `meta.txt`, `server-version.txt`, `image-id.txt`, both exit files, `h2.stderr.txt`, `existing.stderr.txt`, `container-cleanup.txt`, `SHA256SUMS`, `h2.json` (hash recomputed here: `1285e610f60ea9595b4de48a3af8de55eb4d4d872692352ef8bb328bebbc44e6`, equal to the declared value), `sql-run-h2.sh`.

| Fact | Value |
| --- | --- |
| Admission | one `flock -n /tmp/ama-rpi-heavy.lock`, exit 0, 2026-11-10T00:23:08Z, no queue or retry |
| Server and image | SQL Server 2022 RTM-CU27-GDR 16.0.4305.5 (Linux, container, 127.0.0.1 only, removed on exit); image `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`; Python 3.12.3 |
| Harness and wrapper | `harness_h2_matching_context.py` `698c13ec...f96ac4`; `sql-run-h2.sh` `68851d83...2940fe` (not shipped; the wrapper's own exit would not prove child results, so child exit files were read) |
| H2 test, process 1 | exit 0, Ran 1, OK, 0 skips, 3.693 s |
| Existing selectors, process 2 | exit 0, Ran 30, OK, `skipped=1` ("the cross-process SQLite withdrawal is SQLite-only", not waived), 29 pass, 70.884 s. Not 30 SQL passes |
| H2 verdict fields | `verdict` confirmed; `b_differs_on` and `c_differs_on` empty; `releases_equal_baseline`, `releases_unchanged_throughout`, `durable_unchanged`, `first_provider_counters_unchanged` all true; 47 recorded steps; 11 synthetic `assistant_releases` rows unchanged; `fx-quality-evidence` active revision 1 |
| Equality across first, B and C | flag `review-suggested`, `ready`, actionable, no release denial; cited IDs `sensor:SENS-SYN-1:LIVE-SENS-SYN-1-20261109T2350Z` and `sensor:SENS-SYN-1:R-ZF-1-000`; five reading pairs for Quality Inspector and Retrofit Programme Manager; seven other role labels (including Unknown) refused; same binding digest `b4791e0c22b1f1be`; task state and body digest equal |
| Independence | B and C: distinct store, provider and service objects (flags in `independence_B/C`); counters 0 calls and 0 prompts before and after; first provider 1 call, 1 prompt |
| Limits | same-process reopen, not an OS or VM restart; no peer in H2, so no H2 bytes or bytes-saved claim; synthetic `CapturingProvider`, not a model; truncated 16-hex fingerprints, not cryptographic byte identity |

The independent bounded assessment of the H2 publication (verdict approve, zero findings, with required erratum) was read from the coordinator files `independent-1288-h2-matching-context-1110/`; its reviewer did not recompute hashes, and neither it nor this task read H2 as authority evidence.

## Errata the canonical record must carry (originals unchanged)

* Merged H2 research/review/changes and the coordinator handoff state "Excluded: unmerged 891 work". For source `ddeebd01` that is wrong: #891 (the #1339 accounting correction) is included. It was true for the H0/H1 base `a8593a7a8`. The H2 review's literal sentence is superseded here, not rewritten.
* The H2 research mentioned a TLS peer and expected 0 bytes; the applied plan amendment and actual harness have no peer. No H2 byte measurement exists.
* The merged SQL-proof review overstates "30 existing tests ok": it is 29 pass and 1 SQLite-only skip, and its "before meter and token" wording must be read with the changes record (the real `Ai` path reserves the meter and token before the transport fence by design).
* Timestamps: H2 prospective commit `32a54b5ba` readback 00:22:17Z; SQL admission 00:23:08Z on 2026-11-10 (not 23:23:08 on 2026-11-09).

## Gaps found and deduplication (searched open issues with `gh issue list --search`)

| Gap | Existing owner | New issue |
| --- | --- | --- |
| H0 default-provider `release-denied` and H1 revoke of the active synthetic release row after the A-variant, which call revoked is unestablished, intended-or-defect unclassified; H2 did not reproduce it under the matching context | #1288 (E11 spent, E12 and E13 unused; no source fix authorised) with #107 as the release machinery parent | none: no search hit is a dedicated issue, but classification needs the owner to authorise a read-only diagnostic first, so no defect is asserted |
| Quality MSSQL classes not in hosted CI | #440 later criteria and #1288 | none proposed; recorded as a local-only evidence limit |
| Chat receipt provenance for the unwitnessed fallback (R4/PC-002); test hygiene N1/N2; fence-withdrawal and error-type pins (now pinned in C2) | #891 | none |
| No exact-head hosted run for the merged trees | #440 | none |
| Actual UI-to-model autonomous Quality proof; IoT Hub transport; release owner, budget and role decisions (OQ-017) | #1288 criterion 8, #184, #891 criterion 2 | none; owner decisions are not invented |
| OS or VM process restart persistence; Azure SQL | #1288, #440 | none |
| Cross-process SQLite withdrawal test is SQLite-only | accepted by design, recorded | none |

The $700 five-minute synthetic transport authority in #184 is not a paid-model grant (#1288 body, "Existing authority and evidence boundary").

## Planning Readiness

Ready. Constraints for the plan: pure documentation; one new section in the evidence pack; index paragraph; one log entry; frozen local candidate; no push, PR, issue or board write; no raw logs committed; original adverse H0/H1 records, the H2 records and all earlier pack sections unchanged; no document approval; whole-epic closure holds.
