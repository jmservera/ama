<!-- markdownlint-disable-file -->
# RPI Plan Critique: Legacy AI usage attribution (Refs #432, first criterion)

## Metadata

* Task ID: legacy-ai-usage-attribution-432-1112
* Critique date: 2026-11-12
* Plan: .copilot-tracking/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan.md
* Phase details: .copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: one bounded offline slice under #432 criterion 1; no new dispatch, price or budget assumption, raw-case telemetry, resident-host change, push or model call; reuse wrappers and ledger; missing or invalid usage is Unknown; #116 owns new test modules; if already implemented report proof; at most six tests in existing test_ai_consumption_api.py; source change limited to statement order in Ai._request; one docs sentence plus log append.
* Research and evidence considered: .copilot-tracking/research/2026-11-12/legacy-ai-usage-attribution-432-1112-research.md; read-only checks of src/core/src/zava_forward/core/ai.py (_request, evidence, run), ai_consumption.py (complete_in), src/api/tests/test_ai_consumption_api.py, docs/reference/resources/ai-tokenomics.md, docs/reference/log.md.
* Decisions, dependencies, and acceptance criteria considered: plan Phase Checklist P01/P02, details P01-T01 to P02-T02, acceptance criteria and PYTHONPATH dependency.
* Assessment boundary: single pass, source read-only; no tests were run by the critique.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Stale-claim verification (C1-C4) | Covered | ai.py:200 sets receipt usage via ai_consumption.usage, then complete at :202; run merges receipt on every outcome. Claim confirmed. |
| Source-change limit | Partial | Reorder is confined to _request, but _request also serves evidence() (envelope is the receipt); blast radius is wider than the validation list (PC-001). |
| Six tests / no #116 duplication | Partial | No overlap map against existing tests (PC-002). |
| Settlement-failure test feasibility | Partial | Fault-injection mechanism and the second complete() in the except branch are unaddressed (PC-003). |
| Docs sentence and log | Partial | Wording scope (PC-004). |
| Critique disposition and status | Partial | Plan still says Pending (PC-005). |

## Verdict

* Verdict: Revise
* Rationale: The slice is credible and the stale-claim finding is source-true, but validation omits other callers of the changed function, the duplicate-avoidance mapping and the failing-first mechanism are unspecified, and wording scope needs bounding. All are planner-correctable.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Reorder also changes the evidence() path, which validation omits

* Related IDs: P01-T02, P02-T02, C1
* Evidence: src/core/src/zava_forward/core/ai.py:196-212 (_request, shared) and evidence() passing its envelope as receipt; test_ai_consumption_api.py:905-925 asserts envelope usage None on provider failure for the agent path; plan P02-T02 lists only test_ai_tasks and test_document_controls.
* Concern: Plan describes the reorder as legacy-only. The same statement order governs assistants/agents/simulation envelopes.
* Impact: A regression in the agent or simulation lanes could pass the planned targeted set.
* Smallest useful change: State the shared blast radius in P01-T02 and add the full existing test_ai_consumption_api module plus src/core/tests and src/agents/tests modules that exercise _request (for example test_ai_consumption*, test_ai_dispatch_marker, test_ai_input_bounds) to P02-T02, read-only, no edits to #116 modules.
* Action owner: planning parent
* Exact resolving evidence: P02-T02 names those modules and the changes record shows their results.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: No duplicate-avoidance map for the six cases

* Related IDs: P01-T01, caller requirement "if already implemented report proof"
* Evidence: existing tests at test_ai_consumption_api.py:455 (workflow-only route), :460 and :978 (legacy join, limits), :905-925 (provider failure, envelope usage None), :246-253 (envelope usage equals ledger tokens, agent path).
* Concern: Provider failure, workflow-only no dispatch and a generic envelope-equals-ledger assertion may already be proven; the plan asserts only that no legacy-path assertion exists, without a per-case table.
* Impact: Duplicate tests violate the caller rule and may overlap #116.
* Smallest useful change: Add a per-case table (case, existing coverage line or none, keep or drop); keep only cases uncovered on the legacy `briefing` path, retaining settlement failure and malformed/omitted usage as the likely gaps; record dropped cases as existing proof.
* Action owner: planning parent
* Exact resolving evidence: table in P01-T01 with line citations; kept cases at most six.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Failing-first settlement-failure mechanism is unspecified

* Related IDs: P01-T01, P01-T02, acceptance criteria
* Evidence: ai.py:200-209: on any exception the except branch calls complete(..., "provider-unavailable"); ai_consumption.py:766 returns if already completed, so a second complete only helps when the first did not persist.
* Concern: The plan does not say how complete is made to raise once (a one-shot fault on consumption.complete, not on the ledger store) nor what the second call does. A fault that persists makes the result untestable; one that raises after persisting makes it not the stated defect.
* Impact: The only test that fails before the fix may not exercise the defect, leaving the reorder unproven.
* Smallest useful change: Specify a one-shot wrapper on self.service.consumption.complete (raise on first call, delegate after), and the expected assertions: result usage None, ledger completed record with tokens None and outcome provider-unavailable, no output join. Require recorded failing-first output on unfixed source.
* Action owner: planning parent
* Exact resolving evidence: P01-T01 states the mechanism; changes record holds the failing run before and passing run after.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Docs wording must stay bounded and ASCII

* Related IDs: P02-T01
* Evidence: docs/reference/resources/ai-tokenomics.md lines 77-81; the plan says state that `run`/`look_at` return usage, but tests cover only the text-draft `run` path.
* Concern: The look_at claim is source-read only; the caller allows one sentence; the page is flagged pre-extension evidence.
* Impact: Overclaiming proof or a larger rewrite.
* Smallest useful change: One sentence, saying that `Ai.run()` and `look_at()` return provider usage through the receipt, validated, with the legacy text-draft join test-proven and look_at source-observed only; keep the chat host, price, cost and billing gaps; ASCII, no em dash; log append dated 2026-11-12 with no criterion tick.
* Action owner: planning parent
* Exact resolving evidence: git diff of the doc shows one sentence changed and one appended log entry.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Plan disposition and test-count ownership left open

* Related IDs: Critique Disposition, P01-T01
* Evidence: plan "Critique Disposition: Pending"; details say a fixture `response_usage` attribute is added.
* Concern: Disposition must be recorded after revision; the fixture edit and the six-test cap should be stated as inside existing test_ai_consumption_api.py only, with no new module.
* Impact: Ambiguity about ownership versus the #116 session.
* Smallest useful change: Record dispositions for PC-001 to PC-004 and state the file-ownership lock.
* Action owner: planning parent
* Exact resolving evidence: plan Critique Disposition lists each finding as applied.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Research correctly refutes the "discards usage" hypothesis from source and keeps the slice small, offline and non-priced.
* Residual risk accepted: real provider usage shapes are unobserved; only synthetic payloads.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* No tests executed; line numbers from the current worktree; issue #432 text was not re-read by the critique.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: apply PC-001 to PC-005 directly and finalize without another critique
* User response required: no

## Related Artifacts

| Path | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan.md](.copilot-tracking/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan.md) | Plan critiqued |
| [.copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md](.copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md) | Phase details critiqued |
| [.copilot-tracking/research/2026-11-12/legacy-ai-usage-attribution-432-1112-research.md](.copilot-tracking/research/2026-11-12/legacy-ai-usage-attribution-432-1112-research.md) | Supporting research |

## Next Steps

Return the verdict to the planning parent, which applies PC-001 to PC-005 directly and finalizes. No user action is required.
