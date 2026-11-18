---
title: "RPI Plan Critique: Management Views AI Consumption Economics (Issue #100)"
description: "Single-pass independent critique of candidate plan and phase details for Issue #100"
ms.date: 2026-11-15
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-100-mgmt-tokenomics
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the unticked Tokenomics Acceptance Criterion of Issue #100 on branch feat/insight-100-mgmt-tokenomics targeting feat/demo-164-chat-grounding-provenance-0900 (PR #1641) at the Focused validation tier without pushing; ensure management views include ai_consumption_economics with explicit integer denominators (proposal_count, accepted_outcome_count, metered_call_count, unmetered_call_count) and report "Unknown" (never 0 or 0.0) whenever no price source (price_source_configured=False / OD-51 open) or no accepted-outcome count (accepted_outcome_count == 0) exists; add src/core/tests/test_management_tokenomics_invariant_100.py and src/api/tests/test_management_tokenomics_api_100.py; update src/core/README.md and src/api/README.md; pass ruff check, mypy, and unittest in src/core and src/api.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-research.md, .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-plan.md, .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md, and cited codebase contracts in src/core/src/zava_forward/core/ai_consumption.py, src/core/src/zava_forward/core/assistants.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/ai_tasks.py, src/core/src/zava_forward/core/insights.py, src/core/src/zava_forward/core/progress.py, src/core/src/zava_forward/core/coordinator.py, src/core/src/zava_forward/core/store.py, src/api/src/zava_forward/api/progress.py, src/api/src/zava_forward/api/server.py, and existing tests cited in C16 through C20.
* Decisions, dependencies, and acceptance criteria considered: Keep BRD OD-51 open by default; preserve Consumption.report() and exact 5 top-level keys on GET /api/ai/report (C16, C17); preserve repeat-read determinism, CSV round-trip equality, read-only _db_seq() invariance, and content-free privacy canary guarantees (C18, C19, C20); keep web UI files under src/api/src/zava_forward/api/web/ unchanged; lock test file additions to at most 2 with zero removals.
* Assessment boundary: Evaluates completeness, contract fidelity, existing-test compatibility, and implementation readiness of P01 through P04 against supplied research, caller requirements, and cited source/test contracts. Does not execute runtime builds or broaden scope beyond the supplied Issue #100 tokenomics delta.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 (RPI loop, branch, Focused tier, no push) | Covered | Plan Metadata, User Decisions and Requirements, and P04-T01 preserve Focused tier and local-only commit scope. |
| Caller Req 2 & FR-1 (explicit integer denominators) | Partial | Four explicit denominators are specified, but P01-T01 deduplication uses record_id / unhashed IDs instead of SHA-256 reference(rec["id"]) and misses consumption_report-only and publish-held fallback edge cases (PC-003). |
| Caller Req 3 & FR-2 (BRD Required Management Views wiring) | Partial | All six HTTP surfaces are identified while preserving C16/C17 shapes, but coordinator.read calls progress.report directly without store wiring, and unbounded/HTTP priced-state mechanics are underspecified (PC-002, PC-004). |
| Caller Req 3 & FR-3 ("Unknown" fail-closed cost invariants) | Partial | Top-level unpriced and zero-accepted-outcome invariants are solid, but per-capability cost allocation and per-capability zero-accepted-outcome rules when overall accepted_outcome_count > 0 are omitted (PC-005). |
| NFR-1 & NFR-2 (determinism, read-only SQL, content-free typing) | Partial | Repeat-read and canary rules are addressed in principle, but P01-T01 catches nonexistent ConsumptionUnavailable, omits port.sql checks, and risks BEGIN IMMEDIATE write-locking under store.lock (PC-001). |
| P01 / P01-T01 (tokenomics.py core synthesis) | Partial | Needs fixes for PC-001 (DispatchHeld, port.sql, read-only SQL access), PC-002 (unbounded billing and store-level opt-in governance hook), PC-003 (output digest deduplication), and PC-005 (per-capability cost rules). |
| P02 / P02-T01 (core management view wiring) | Partial | coordinator.py must pass store.ai_consumption_economics(...) into progress.report(...) rather than relying on progress.report's empty default (PC-002). |
| P02 / P02-T02 (api.progress.dashboard wiring) | Partial | Recommendations store timestamp key created (including date-only and naive ISO strings), not created_at/at, and synthetic-only / explicit-vs-default date range parity needs specification (PC-004). |
| P03 / P03-T01 & P03-T02 (core and API invariant tests) | Partial | P03-T02 promises HTTP tests for priced-without-accepted-outcomes and priced-with-accepted-outcomes across all six endpoints, which requires the non-monkeypatched store/period contract in PC-002. |
| P04 / P04-T01 (README updates and Focused validation) | Covered | Covers src/core/README.md, src/api/README.md, ruff check, bare mypy in each package, and unittest discovery matching .github/workflows/src-ci.yml. |

## Verdict

* Verdict: Revise
* Rationale: The architectural split (new pure core tokenomics.py module, preserving Consumption.report() and the 5 top-level keys on GET /api/ai/report) is well-grounded in C1 through C20, but five concrete codebase-contract mismatches in P01, P02, and P03 would cause immediate existing-test regressions, silent zeroed denominators on /api/coordinator, double-counted unmetered calls on metered SQL stores, or blocked HTTP priced-state tests unless corrected in the plan and phase details before implementation. All five findings are direct planner corrections requiring zero user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Nonexistent ConsumptionUnavailable exception, missing port.sql guard, and BEGIN IMMEDIATE lock hazard in store_ai_consumption_economics

* Related IDs: NFR-1, P01, P01-T01, P02-T01, P03-T01, C8, C17, C20
* Evidence: .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md (P01-T01 item 2); src/core/src/zava_forward/core/ai_consumption.py lines 424 and 461-476; src/core/src/zava_forward/core/assistants.py lines 1100-1117 and 1217-1237; src/core/src/zava_forward/core/sqlstore.py lines 255-259; src/api/tests/test_ai_consumption_api.py lines 2079-2165
* Concern: P01-T01 specifies catching ConsumptionUnavailable while reading ledger._read(db) inside a transaction. In src/core/src/zava_forward/core/ai_consumption.py, ConsumptionUnavailable does not exist; Consumption._read(db) raises ai_consumption.DispatchHeld ("meter-capacity-reached" or "meter-evidence-invalid") or json.JSONDecodeError / ValueError. In addition, test_ai_consumption_api.py tests GET /api/ai/report under both DispatchHeld holds and patch.object(assistants, "sql", False) ("schema-unavailable") while self.store.ai.consumption remains attached on self.store.ai, and Assistants.transaction() executes BEGIN IMMEDIATE + COMMIT on a new assistant_connection(), acquiring a SQLite write lock while Store.stats(), Store.progress_report(), coordinator.read(), and api.progress.dashboard() already hold store.lock.
* Impact: Referencing ai_consumption.ConsumptionUnavailable raises AttributeError, failing to catch DispatchHeld or check port.sql crashes GET /api/ai/report (via s.ai_live_report(u) in server.py line 969) during existing test_ai_consumption_api.py hold and schema-unavailable tests, and calling port.transaction() (BEGIN IMMEDIATE) inside store.lock creates avoidable write-lock contention on read-only endpoints.
* Smallest useful change: Specify in P01-T01 and P02-T01 that store_ai_consumption_economics snapshots recommendations under store.lock, checks bool(getattr(port, "sql", False)) and getattr(port, "schema_error", None) is None before touching SQL, reads assistant_events on a short-lived read-only connection (plain SELECT + close without BEGIN IMMEDIATE, outside store.lock when called from Store entrypoints or without write locks), and catches (ai_consumption.DispatchHeld, ValueError, KeyError, TypeError, OSError, RuntimeError) to fail closed to price_source_configured=False, coverage="ledger-hold" (or "unavailable" when port.sql is False), and "Unknown" cost fields.
* Action owner: planning_parent
* Exact resolving evidence: P01-T01 and P02-T01 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md name ai_consumption.DispatchHeld (not ConsumptionUnavailable), guard on getattr(port, "sql", False) and schema_error, and specify read-only SELECT access without BEGIN IMMEDIATE write-locking.
* Decision route: Direct planner correction (no user decision required)

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Missing store wiring in coordinator.read and unspecified priced-state / unbounded-billing path for HTTP management endpoints

* Related IDs: FR-1, FR-2, FR-3, P01-T01, P02-T01, P02-T02, P03-T02, C8, C11, C12, C13, C15
* Evidence: .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md (Test Ownership and Coverage Lock, P01-T01, P02, P02-T01, P03-T02); src/core/src/zava_forward/core/coordinator.py lines 182-190; src/core/src/zava_forward/core/ai_consumption.py lines 1389-1399; src/api/src/zava_forward/api/server.py lines 942-972
* Concern: First, coordinator.read(...) calls progress.report(selected, as_of=..., start=..., cohort=..., scenario=None, audit_intact=intact) directly rather than Store.progress_report(...). P02 only instructs coordinator.py to expose rep["ai_consumption_economics"] without passing store.ai_consumption_economics(...) into progress.report(...), which causes /api/coordinator to fall back to progress.report's empty default (zero proposals, calls, and outcomes) even when the store has live records. Second, P03-T02 requires exercising all six HTTP endpoints across priced-without-accepted-outcomes and priced-with-accepted-outcomes states over App + SqlStore, yet (a) none of the five HTTP-facing views pass od_51_status, components, or quality_floor_status and no opt-in store governance hook is defined, (b) Consumption.report matches billing records strictly on r["start"] == begin and r["end"] == finish whereas Store.stats(), Store.ai_live_report(), and Store.progress_report(..., start=None) omit start and/or end, and (c) server.py line 969 calls s.ai_live_report(u) without forwarding explicit ?start=&end=&as_of= query bounds on GET /api/ai/report (and server.py is omitted from Canonical production targets).
* Impact: GET /api/coordinator silently reports zero denominators regardless of store state; unbounded endpoints (/api/stats, /api/stats?report=progress without start, /api/ai/report["live"]) can never reconcile a ledger billing record; and P03-T02 cannot test priced HTTP states across all six endpoints without brittle monkeypatching.
* Smallest useful change: Revise P01-T01, P02-T01, P03-T02, and Test Ownership and Coverage Lock so that: (1) coordinator.read passes ai_consumption_economics=store.ai_consumption_economics(start=query.get("start"), as_of=query.get("as_of")) into progress.report(...) and exposes it at top level; (2) store_ai_consumption_economics reads an optional, default-absent store governance config (for example store.data.get("tokenomics_governance") or store._tokenomics_governance, defaulting to od_51_status="open" so runtime OD-51 remains open unless explicitly configured by an authorised caller/test); (3) summarize_ai_consumption_economics defines exact billing reconciliation both for explicit [start, end) windows and for unbounded/half-bounded reads (reconciling complete, non-overlapping single-currency ledger billing record(s) covering every cohort call in the effective window with zero uncovered calls); and (4) if GET /api/ai/report?start=...&end=...&as_of=... should scope live["ai_consumption_economics"] when explicit query bounds are provided, add src/api/src/zava_forward/api/server.py to Canonical production targets (forwarding explicit query start/end/as_of only when present so parameterless live_report remains wall-clock-free).
* Action owner: planning_parent
* Exact resolving evidence: Updated P01-T01, P02-T01, P03-T02, and Test Ownership and Coverage Lock in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md (and matching summary in .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-plan.md) specify coordinator.read's store.ai_consumption_economics(...) call, the default-open store governance hook, deterministic unbounded billing reconciliation, and explicit server.py target disposition.
* Decision route: Direct planner correction (no user decision required)

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Ledger output ID hashing mismatch (reference(rec["id"]) vs record_id) and double-counting on consumption_report-only or publish-held fallback records

* Related IDs: FR-1, FR-3, P01, P01-T01, P03-T01, C8, C11, C15
* Evidence: .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md (P01-T01 item 1); src/core/src/zava_forward/core/ai_consumption.py lines 56-59, 1070-1072, and 1440-1525; src/core/src/zava_forward/core/ai_tasks.py lines 237 and 399-412; src/core/src/zava_forward/core/store.py lines 1814 and 1839-1853; src/core/src/zava_forward/core/chat_panel.py lines 820-823
* Concern: P01-T01 deduplicates recommendations against ledger records using meter_root / envelope.meter_root or "record_id recorded as ledger output". Persisted items in store.data["recommendations"] store their identifier under "id" (not "record_id"), and Consumption.output hashes that identifier via ai_consumption.reference(output) (SHA-256 hex digest) before storing r["output"]. Additionally, Consumption.report() returns only a single cohort SHA-256 digest rather than individual root IDs (so calling summarize_ai_consumption_economics with consumption_report + recommendations and ledger_records=None has no root set for deduplication), publish-held fallbacks in ai_tasks.py and store.py rewrite rec["source"] = "template" while retaining meter_root, and chat_panel.py records non-proposal metered ledger outputs with eligible=False.
* Impact: Matching raw record_id/id strings misses ledger output events, falsely classifying metered recommendations as unmetered_call_count > 0 (poisoning price_source_configured to False and double-counting proposal_count and accepted_outcome_count). Likewise, publish-held metered fallbacks or eligible=False chat ledger outputs can skew proposal_count or unmetered_call_count unless explicitly classified.
* Smallest useful change: Specify in P01-T01 that: (1) recommendation deduplication extracts root = rec.get("meter_root") or (rec.get("envelope") or {}).get("meter_root") and hashed_id = ai_consumption.reference(rec["id"]) (when isinstance(rec.get("id"), str) and rec["id"]) to match ledger reserved.root and output.output; (2) when consumption_report is supplied without ledger_records, recommendations carrying a valid 64-hex meter_root are treated as covered by consumption_report rather than unmetered; (3) metered records downgraded to source="template" on publish hold count their metered call in metered_call_count (never workflow_only_excluded_count, unmetered_call_count, or accepted_outcome_count); and (4) ledger roots with output.eligible is False (such as chat turns or held fallbacks) count in metered_call_count, never in accepted_outcome_count, with an explicit rule on whether proposal_count counts all metered call roots or only proposal-bearing roots + AI recommendations.
* Action owner: planning_parent
* Exact resolving evidence: P01-T01 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md specifies SHA-256 reference(rec["id"]) matching, consumption_report-without-ledger_records root handling, publish-held metered fallback handling, and eligible=False ledger output classification.
* Decision route: Direct planner correction (no user decision required)

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Recommendation timestamp key mismatch (created vs created_at/at) and synthetic/date-filter determinism in api.progress.dashboard

* Related IDs: FR-2, NFR-1, NFR-2, P02, P02-T02, P03-T02, C14, C18
* Evidence: .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md (P02-T02); src/api/src/zava_forward/api/progress.py lines 215-242 and 252-335; src/core/src/zava_forward/core/ai_tasks.py line 237; src/core/src/zava_forward/core/store.py line 1794; src/api/tests/test_progress_dashboard.py lines 72-95 and 545-592
* Concern: P02-T02 instructs api.progress.dashboard to filter recommendations by parsing ISO created_at / at timestamps when present, or including un-timestamped recommendations only when query has no explicit date filter. In the codebase, recommendations store their creation timestamp under "created" (for example "2026-09-01" date-only in test_progress_dashboard.py line 81, naive ISO seconds in store.py line 1794, and UTC ISO in ai_tasks.py line 237) and review timestamp under "resolved_at", never "created_at" or "at". Moreover, test_progress_dashboard.py injects non-synthetic ("REAL", is_synthetic=False) and unmarked-case ("MIXED", ZF-5) recommendations to verify synthetic-only isolation on /api/progress, and changing inclusion rules based on whether query had explicit start/end parameters would make dashboard(store, user, {}) disagree with dashboard(store, user, {"start": [default_start], "end": [default_end]}) for the exact same resolved [start, end] dates.
* Impact: Parsing created_at/at treats every stored recommendation as un-timestamped, miscounts window-scoped proposals/outcomes on GET /api/progress, risks admitting non-synthetic records into the synthetic-only progress dashboard, and creates inconsistent results between implicit and explicit [start, end] queries.
* Smallest useful change: Update P02-T02 to parse recommendation timestamps from created (and resolved_at when created is absent, normalizing date-only YYYY-MM-DD and timezone-naive ISO strings to UTC deterministically without depending on whether start/end were implicit or explicit in query), apply the same synthetic-case admission rule used by zava_forward.api.progress (or explicitly document synthetic-only recommendation filtering for /api/progress), and bound ledger calls to [start 00:00:00Z, (end + 1 day) 00:00:00Z) with as_of=(end + 1 day) 00:00:00Z.
* Action owner: planning_parent
* Exact resolving evidence: P02-T02 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md specifies parsing created / resolved_at (handling date-only and naive UTC ISO formats), uniform [start, end] filtering regardless of implicit vs explicit query parameters, and synthetic-record admission alignment with test_progress_dashboard.py.
* Decision route: Direct planner correction (no user decision required)

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Unspecified per-capability cost allocation and zero-accepted-outcome invariant when overall accepted_outcome_count > 0

* Related IDs: FR-2, FR-3, P01-T01, P03-T01, C1, C3, C6, C7, C8
* Evidence: .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-plan.md (FR-2, FR-3); .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md (P01-T01 items 1 and 3); src/core/src/zava_forward/core/ai_consumption.py lines 210-252 and 1389-1439
* Concern: P01-T01 specifies per-capability cost fields when not price_source_configured and when overall accepted_outcome_count == 0, and specifies top-level cost formulas when price_source_configured is True and overall accepted_outcome_count > 0, but omits how by_capability[cap]["token_cost"], by_capability[cap]["total_cost_of_ai"], and by_capability[cap]["cost_per_accepted_outcome"] are computed when price_source_configured is True and overall accepted_outcome_count > 0. In ai_consumption.py, billing and other_tca_components are cohort/budget-level rather than per-capability, and in a multi-capability cohort one capability can have accepted_outcome_count == 0 while another has accepted_outcome_count > 0.
* Impact: Without an explicit per-capability rule, an implementer may either divide by zero / emit "0" on a zero-accepted capability inside a positive cohort (violating assert_tokenomics_invariants and NFR-017) or invent arbitrary multi-capability TCA splits prohibited by C7.
* Smallest useful change: Specify in P01-T01 (and test in P03-T01) that for each capability in by_capability: (1) whenever cap["accepted_outcome_count"] == 0, cap["cost_per_accepted_outcome"] and cap["token_cost_per_accepted_outcome"] (if present) strictly equal "Unknown" even if overall accepted_outcome_count > 0; and (2) when price_source_configured is True, per-capability token_cost and total_cost_of_ai are populated only when attributable without invented splits (for example single-capability reconciled cohort, or exact reconciled zero-variance per-call charge attribution for token_cost while multi-capability unallocated total_cost_of_ai / cost_per_accepted_outcome fails closed to "Unknown" unless single-capability or explicitly allocated), and never emit 0, 0.0, "0", "0.0", or None.
* Action owner: planning_parent
* Exact resolving evidence: P01-T01 and P03-T01 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md state the exact per-capability attribution rule and per-capability accepted_outcome_count == 0 -> "Unknown" invariant.
* Decision route: Direct planner correction (no user decision required)

## Strengths and Residual Risk

* Strong contract preservation against C16 through C20: Keeping Consumption.report() and the 5 top-level keys of GET /api/ai/report untouched while surfacing ai_consumption_economics across Store.stats (/api/stats), Store.progress_report (/api/stats?report=progress and /api/cases.csv?report=progress), coordinator.read (/api/coordinator), api.progress.dashboard (/api/progress), and ai_tasks.live_report (/api/ai/report["live"]) avoids breaking existing API schema tests while covering every management surface.
* Comprehensive fail-closed zero protection: Explicitly guarding the reconciled billed == Decimal("0") + accepted_outcome_count == 0 edge case and sanitizing alert owners against "@" or whitespace directly addresses C8 and C20 privacy/zero-fabrication hazards.
* Clean test ownership lock: Adding exactly two dedicated test suites (test_management_tokenomics_invariant_100.py in src/core/tests/ and test_management_tokenomics_api_100.py in src/api/tests/) with zero test removals aligns directly with caller requirements and repository CI structure.
* Accepted residual risk: BRD OD-51 remains intentionally "open" by default in runtime state until owner approval of live tariffs, spend ceilings, and alert owners; default runtime payloads will therefore report "Unknown" cost fields by design while priced states are proven via explicit configured governance/ledger fixtures in tests.

## Questions or Blocking Evidence Gaps

* None. All required evidence is present in the workspace and supplied research; zero user decisions are needed.

## Limitations

* Critique is static and read-only; validation commands (ruff check, mypy, unittest) were not executed during plan critique and remain gated in P04-T01 and rpi-review.

## Recommended Next Action

* Highest-impact finding: PC-001 (paired with PC-002 and PC-003 in P01-T01 and P02-T01)
* Action owner: planning_parent
* Smallest next action: Apply PC-001 through PC-005 directly to .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-plan.md and .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md, record their disposition in the plan's Critique Disposition table, and finalize the plan for rpi-implement without another critique pass.
* User response required: No
