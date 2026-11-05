---
title: Lifecycle quality-gate checkpoint research (Refs #440 #82 #81)
description: Prospective research for the tenth stabilization checkpoint after PR 1226 merged into the lifecycle parent
ms.date: 2026-11-05
ms.topic: reference
---

Research disposition: executed inline (focused documentation tier). Planning Readiness: Ready.

## Scope and pins (fetched, verified)

* Documentation target and child base: `feat/discovery-assurance-integration-123` `1faadaa3e75d3b4003319fde0491473fa1a87dee`, tree `678085a22e982a438fd275701f1e686bb212f258`. Child branch `docs/lifecycle-quality-checkpoint-440` at the same commit, ignored-clean before any artifact.
* Lifecycle SOURCE parent `feat/controlled-lifecycle-integration-81` `cd271cfa54216fbc2ae7d59a63ac8068f372d697`, tree `6bc669420643d524402b3b26ef325aae3a65b53a` (PR 1226 merged 2026-11-05T23:01:10Z; tree equals reviewed child `10161ecb`).
* Main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, unchanged. Three separate pins. Governance runtime and unmerged 144, 79, 80, 96, 185, 188 and 1204 work are excluded from lifecycle and main acceptance.
* Issues read live: 82, 81, 440, 144 and 80 are all OPEN. #82 has three of four criteria unticked.

## Source read (git diff main..cd271cfa, one commit, 28 files, +682/-10)

* `gates.py`: new `QUALITY_RULE` (reviewer is the `_UNREVIEWED` marker, so no named approval) and `quality_gate`: Pass only with no gaps, Unknown for an unreadable record, Fail with reason "Checks without evidence".
* `quality.py`: `evidence_gaps` returns `None` for malformed stored items, checklist name or measure; `handover_blockers`, accept and handover use the gate; the independence check, resident clear and safety clear are retained; a corrupted in-progress record may be replaced only by a quality role (owner decision 2026-11-05).
* `store.py`: `require_quality_evidence` raises `GateError` with reason, owner and next action.
* Requirement qualification: PRD FR-008 is the controlled-transition gate requirement; BRD FR-008 is a different requirement (material change invalidates downstream approvals). PRD FR-007 forbids bulk quality acceptance. Both documents are draft or in-review (BRD 0.21.0 draft blob `34d88395`, PRD 0.21.0 in-review blob `c788b917`, ADR 0003 blob `d6064539`, ADR 0006 blob `956da1a3`), identical to main.

## Light observation performed during research (recorded honestly)

Before any pack, index or log edit, as read-only research on an immutable export (not implementation):

* Export `git archive` of `cd271cfa` into new external `/tmp/l440cd271/src`; existing 440-owned venv `/tmp/ama-main-440-ui-cache-wave3-venv`, scrubbed env, bytecode off, external TMPDIR.
* Import provenance proved: `store`, `quality` and `gates` resolve under `/tmp/l440cd271/src/src/core/src/...`, `evidence_gaps` present.
* `unittest tests.test_gates tests.test_quality_procurement tests.test_hazard_referral` exit 0 (captured directly from the subprocess), 183 tests, 1 skip, 80.2 s, no `__pycache__` under the export. The output file is `/tmp/l440cd271/out/run.log` (sha256 `3b43f8b16bb79baf1e4298ee649e666a67ba8c2587bb69c13f8c1706342b88e0`). The traceback text in the log is an injected-fault test's expected logged error, not a failure.
* Skip reason is not yet attributed; it is recorded as unattributed unless the log shows it.
* The supplied receipt `/tmp/g82-measure1-1105/receipt.json` exists and its sha256 equals the supplied `ba37e035...f57` (hash verified; contents not re-adjudicated).
* No lock, service, SQL Server, browser, Docker, scanner or cloud use. #144 owns heavy resources.

## Evidence classification candidates

* Local observed: 183-test light run on the cd271cfa export; receipt hash match; git identities; issue states.
* Supplied, not independently reproduced: child 10161 full receipt (17 groups, 205 commands, 192 exit 0, 13 probe exit 1 inspected), SQL 291 total/290 executed/1 JSON-only skip, hosted 10 checks, functional approve with 0 findings over 28 sections.
* Implemented-unverified: SQL store behaviour at parent `cd271cfa` (tree equality is not a run), other capacity, authority, finance and eligibility gate families.
* Unknown: named rule review for `QUALITY_RULE` (unreviewed exercise rule).
* Deferred: remaining #82 family implementation; blocked: any heavy gate while #144 holds exclusive resources.

## Owner comparison

No new defect was found, so no issue is proposed. Owners: #82 (gates family and rule review), #81 (epic), #80 (Excel, unmerged), #144 (heavy owner), #440 (this checkpoint series).

## Recommendation candidate

Continue: no fix or pivot needed. Remaining #82 work and expansion proceed after coordinator consumption; no closure or ticks.
