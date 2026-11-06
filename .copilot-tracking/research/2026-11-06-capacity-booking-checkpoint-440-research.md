---
title: Capacity booking checkpoint research (Refs #440 #82 #81)
description: Prospective research for the eleventh stabilization checkpoint after PR 1229 merged into the lifecycle parent
ms.date: 2026-11-06
ms.topic: reference
---

Research disposition: executed inline (focused documentation tier). Planning Readiness: Ready.

## Scope and pins (freshly fetched 2026-11-06, verified)

* Child branch `docs/capacity-booking-checkpoint-440` at governance target `feat/discovery-assurance-integration-123` `a97bea15318307aacf60ed1690d054d32417c23e`, tree `7995337ffe41a01d250c2c4856e48b5f08d45b82`; ignored-clean on entry.
* Lifecycle SOURCE `feat/controlled-lifecycle-integration-81` `af891a5cccf730ccf61e670f312b7674218dbe4b`, tree `cb8a3d463b0f1d31d1a5de0d1e1a2e68de7ebc8e`. PR 1229 MERGED 2026-11-06T03:10:17Z (merge commit equals this head). The parent also holds #1226 (`cd271cfa5`) and #1228 (`d4d33c7ec`, rule provenance wording).
* Main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, unchanged. All three pins equal the supplied values; nothing changed.
* Issues 82, 81, 440, 144, 80 and 79 read live: all OPEN. #82 criteria: three of four unchecked (only the safety-hold criterion is ticked). #440 criteria 7 and 8 (triage; genuine RPI artifacts) remain unticked in the live body.
* Heavy holder per task: original 79 r9 (PID 2560481, `/tmp/g79-pub-r9-1106`). This session takes no lock and runs no heavy work.

## Source read (git diff of #1229, 23 files, +519/-16; whole parent over main 48 files, +1200/-25)

* `gates.py`: `CAPACITY_RULE` (effective 2026-11-06, version 1, reviewer is the unreviewed marker; source cites PRD FR-008 as governing plus FR-016, exercise fixture); `capacity_gate(state, reason)`: True gives Pass, False gives Fail, None gives Unknown; `CapacityGateError(ValueError)` keeps the ValueError text and carries `state` and `result`. `QUALITY_RULE.source` now cites PRD FR-008 and FR-017 (#1228), which resolves the provenance ambiguity disclosed by the tenth checkpoint.
* `procurement.py`: capacity checks raise `CapacityGateError`: deficit and date-outside-period carry `False` (Fail); absent evidence, legacy or unverified capacity, changed source/scope/contract, lost authorised acceptor, authority change and the absent single appointed order carry `None` (Unknown). `require_booked_capacity` returns a Pass result only after the resident clear; capacity remains last.
* `appointments.py`: `_appointment_assessment` returns the status plus a capacity error only when it is the sole missing item; `require_appointment_commitment` rethrows structurally as `CapacityGateError` only then; mixed failures stay a plain `ValueError`.
* Pass is server-internal, not newly persisted or API-exposed (no API or store schema file changed).

## Light observation (read-only research evidence, before this plan)

* Immutable export: `git archive` of `af891a5cc` paths `src/core` and `src/agents` into new external `/tmp/l440af891/src` (path refused if existing).
* Environment: existing 440-owned venv `/tmp/ama-main-440-ui-cache-wave3-venv` (the #82 venv was not used or mutated), `env -i`, bytecode off, external TMPDIR, no network use, no installation.
* Import provenance proved: `gates`, `procurement`, `appointments`, `quality` and the fixture module `test_gates` resolve under `/tmp/l440af891/src/src/core/...`; `CapacityGateError` present.
* `unittest tests.test_gates tests.test_quality_procurement tests.test_hazard_referral` exit 0 captured directly: 193 tests in 65.9 s, OK, 1 skip (attributed by source reading to the single `skipTest` "JSON-only separate-file audit ordering", not shown by the non-verbose log). No `__pycache__` created. Log `/tmp/l440af891/out/run.log` sha256 `3fd61476e1c5ceb642590380499abe252872fe825855adce3734bb568edab9e6`. The traceback in the log is an injected-fault test's expected output. The earlier tenth run had 183 tests; the +10 are the new gate and capacity cases.
* Supplied hashes matched the files: receipt `/tmp/g82-cap-r3-1106/receipt.json` `eb1cd5ed...a0bc`; SQL log `/tmp/g82-cap-r3-1106/0176-mssql.log` `51953f94...5e1c`; contents not re-adjudicated and the SQL log not read or rerun. Root session files under `77149bdf-...` were not read.

## Document identities (equal to main)

* BRD 0.21.0 draft blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 in-review blob `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0003 blob `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006 blob `956da1a3b804c803041fe2e8a312bd9f400273ae`. Draft and in-review are not approval.
* Requirement qualification: PRD FR-008 governs gates (AC-010, AC-011, AC-067, AC-144 mapped, acceptance not run); PRD FR-016 is the provider-package and capacity record; FR-017 is quality disposition; BRD FR-008 is a different requirement.

## Evidence classification candidates

* Local observed: pins, issue states, source read, 193-test light run, supplied hash matches.
* Coordinator-supplied (not independently reproduced): candidate 272146 FULL receipt (17 groups, 205 commands, no group skip; the native zero-nonzero assertion was false and is qualified in the #82 comment: 13 expected nonzero probes individually read); SQL 296 total, 295 executed, 1 JSON-only skip, 5 new capacity cases passed; hosted 10 checks success; published and local functional approval with 0 findings; human boxes unchecked.
* Implemented-unverified: SQL Server, browser and full gate at parent `af891a5cc` (tree equality is not a run); other gate families; integrated parent FULL.
* Unknown: named rule review for the capacity and quality exercise rules. Blocked: any heavy work while 79 r9 holds.

## Owner comparison and recommendation candidate

* No new defect or necessary refactor was confirmed. The inherited Low RV-C1 future-ordering caveat is not a current defect. No issue is proposed. Owners: #82 (remaining families, rule review), #81, #80, #144, #79, #440.
* Recommendation: continue; no fix or pivot. Whole 81, 82 and 440 stay open; no tick.
