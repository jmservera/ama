<!-- markdownlint-disable-file -->
# RPI Plan Critique: Meaningful Human-Review Effectiveness Gate and Automation-Bias Harness (#223)

## Metadata

* Task ID: 223-human-review-effectiveness-2305
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver locally verifiable GitHub Issue #223 ("Meaningful human-review effectiveness test") acceptance criteria in `src/core` without modifying `pyproject.toml`, workflow YAML, `provenance-register.json`, or `src/agents`, validated exclusively via `cd /home/azureuser/source/ama-demo-wt/feat-223-human-review-effectiveness-2305/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*223*.py' -v`, and preserving `OQ-017` fail-closed live governance (`Refs #223`).
* Research and evidence considered: .copilot-tracking/research/2026-11-14/human-review-effectiveness-223-2305-research.md, .copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md, .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md, src/core/src/zava_forward/core/ai_tasks.py, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/gates.py, src/core/src/zava_forward/core/rai_release.py, src/core/src/zava_forward/core/controls.py.
* Decisions, dependencies, and acceptance criteria considered: Issue #223 criteria 1 through 5 (`AC-1` through `AC-5`), `FR-223-01` through `FR-223-04`, `NFR-223-01`, `NFR-223-02`, `OQ-017` provisional authority boundary, pure-Python synthetic scenario embedding (`C7`), and strict `mypy` typed boundary wrappers (`C8`).
* Assessment boundary: Evaluates plan and phase-details credibility, runtime API compatibility, type-safety contracts, and gate-bypass completeness against the supplied research and `src/core` modules. Does not inspect unreferenced modules outside the supplied inputs or evaluate live human reviewer trials excluded under `OQ-017`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-223-01 / AC-1 / P01-T02 | Partial | Defect taxonomy (`wrong`, `stale`, `unsupported`, `incomplete`) and semantic discrepancy checks are well structured, but `P01-T02` targets a non-existent `GateResult(gate, status, reasons, missing_authority)` signature (`PC-001`) and misstates `ai_tasks` field/hash contracts (`PC-002`). |
| FR-223-02 / AC-2 | Partial | `Store.review_ai` retains `resolved_by` and `review_evidence`, but `compared` keys are `ai`/`workflow` (not `ai_text`/`workflow_text`), edited text is `override_text` (not `final_text`) (`PC-002`), and unreasoned `accept` on valid controls omits `reason` and reviewer-verified `source` (`PC-003`). |
| FR-223-03 / AC-3 / P01-T01 / P02-T01 | Partial | Workflow-only pairing across `summary` and `message` covers effort and detection metrics, but offline `Store.ai_run` falls back to `template` unless seeded and `Store.review_ai` raises `PermissionError` on `source == "ai"` without a matching `release_current` seam and same-user reviewer identity (`PC-002`). |
| FR-223-04 / AC-4 / P03-T01 | Partial | Automation-bias confidence contrast is well designed, but allowing unreasoned `accept` on valid controls lets default acceptance + `verified == True` pass (`PC-003`), and `named_human`/`is_memory_reference` miss `"TBD"` and conversational memory phrases assumed by `P03-T01` (`PC-004`). |
| AC-5 / P02-T02 | Covered | `blank_worksheet()`, `score_human_session()`, and duplicate-rejecting `pool_human_sessions()` cleanly separate synthetic harness outputs from `OQ-017` human trial evidence once `PC-002` same-user `Store` seeding is applied. |
| NFR-223-01 / NFR-223-02 / C7 / C8 | Covered | Pure-Python embedded synthetic fixtures in `tempfile.TemporaryDirectory` and narrow `Any`-typed `Store`/`ai_tasks` adapters avoid `provenance-register.json`, wheel-packaging, and `pyproject.toml` drift. |

## Verdict

* Verdict: Revise
* Rationale: Overall architecture, pure-Python synthetic scenario design, and `OQ-017` governance boundaries are strong, but four concrete contract mismatches against `gates.py`, `store.py`, `ai_tasks.py`, `rai_release.py`, and `controls.py` (`PC-001` through `PC-004`) would cause immediate `mypy --strict` / runtime failures and leave a default-acceptance provenance gap unless corrected in the plan and phase details before implementation. All four findings are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Critical]: `human_review_gate` targets a non-existent `gates.GateResult` signature and omits `GateRule` effective-date semantics

* Related IDs: FR-223-01, AC-1, AC-4, C5, P01-T02, P03-T01
* Evidence: src/core/src/zava_forward/core/gates.py (lines 24-96), .copilot-tracking/research/2026-11-14/human-review-effectiveness-223-2305-research.md (line 57), .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md (lines 91, 102-104)
* Concern: `P01-T02` specifies `GateResult(gate, status, reasons, missing_authority)` returning list-valued `reasons` and `missing_authority`. In `src/core/src/zava_forward/core/gates.py`, `GateResult` is a frozen dataclass `(gate: str, outcome: str, reason: str, owner: str, correction: str, rule: GateRule | None = None)` where `PASS = "pass"`, `FAIL = "fail"`, `UNKNOWN = "unknown"`, `reason` must be a non-blank `str`, and there are no `status`, `reasons`, or `missing_authority` attributes. Additionally, `gates.check(rule, True, ..., on=...)` returns `UNKNOWN` whenever `rule.effective_date > (on or date.today().isoformat())`, which will trip if `effective_date` is set to a simulated November 2026 date while the host clock is earlier and `on` is omitted.
* Impact: Implementing `P01-T02` as written immediately fails `python3 -m mypy` (`strict = true`) and raises `TypeError` at runtime on every gate call, or spuriously returns `UNKNOWN` when `effective_date` exceeds host `date.today()`.
* Smallest useful change: Revise `FR-223-01` and `P01-T02` to construct `gates.GateRule(gate="human_review_effectiveness", source=..., effective_date=..., version="1", reviewer=...)` and `gates.GateResult(gate=..., outcome=PASS|FAIL|UNKNOWN, reason=..., owner=..., correction=..., rule=...)` (encoding specific failure codes and `OQ-017` authority gaps in `reason`, `owner`, and `correction`, or exposing a companion structured evaluation record alongside `GateResult`), and pass an explicit `on` date (or past/effective ISO date) so `gates.check` / `transition_allowed` behaves deterministically regardless of host wall-clock date.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-223-01` in `.copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md` and `P01-T02` in `.copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md` matching `gates.GateRule` and `gates.GateResult(gate, outcome, reason, owner, correction, rule)` plus explicit `on` / `effective_date` handling.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Offline `Store.ai_run` / `Store.review_ai` integration omits `release_current`, same-user ownership, record field names, and role-scoped `source_labels`

* Related IDs: FR-223-01, FR-223-02, FR-223-03, AC-1, AC-2, AC-3, AC-4, C3, C4, P01-T01, P01-T02, P02-T01, P02-T02
* Evidence: src/core/src/zava_forward/core/store.py (lines 72-94, 861-880, 1214-1215), src/core/src/zava_forward/core/ai_tasks.py (lines 58-129, 232-285, 345-397), src/core/src/zava_forward/core/controls.py (lines 13-14), .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md (lines 70, 106-116, 174-198)
* Concern: Five runtime mechanics in `store.py` and `ai_tasks.py` contradict the phase details:
  1. Offline `Store(data_path)` leaves `store.ai.configured == False` (causing `Store.ai_run` to emit `source="template"`) and defines `Store.release_context(...) -> None` (`store.py:82-94`), causing `Store.review_ai` (`ai_tasks.py:366-369`) to raise `PermissionError("Release changed; use the ordinary case controls.")` on every `"accept"` or `"edit"` when `rec["source"] == "ai"`.
  2. `ai_tasks.review` (`ai_tasks.py:354-355`) enforces `rec["user"] == user["email"]`; running `Store.ai_run(author, ...)` and `Store.review_ai(reviewer, ...)` with distinct users (`P02-T01`, `P02-T02`) raises `PermissionError("This AI output was made for someone else.")`.
  3. `Store.review_ai(self, user, rec_id, action, reason="", text=None)` (`store.py:1214`, `ai_tasks.py:348,384-392`) takes `(user, rec_id, action, reason, text)`, truncates `reason` to 300 chars, stores edited text in `rec["override_text"]` (not `final_text`), and writes `rec["review_evidence"]["compared"]` with keys `{"ai", "workflow"}` (not `{"ai_text", "workflow_text"}`).
  4. `source_labels(case, reason_ok)` (`ai_tasks.py:58-87`) formats labels as `Stage: ...`, `Safety issue: ...`, `Funding: ...`, `Extra support: ...` (not `[[Case ...]]` outside `Case history YYYY-MM-DD`), drops `summary` bullet lines whose citations do not all resolve (`bullets=True` in `store.py:877`), and includes `Extra support: <adjustment>` only when `projection.can_see_reason(user)` is `True` (`controls.RESIDENT_VIEW_ROLES` excludes `"Neighbourhood Officer"` and `"Finance Analyst"`).
  5. `ai_tasks.source_hashes(store, user, case_ids)` requires 3 arguments rather than `ai_tasks.source_hashes(case)` (`P01-T02`), and pre-review case mutation sets `rec["status"] = "Hold"` (`ai_tasks.HOLD`) without `review_evidence` and raises `ValueError`, which `P01-T02` would misclassify as `UNKNOWN` rather than `FAIL` (`stale_case_sources`).
* Impact: Without aligning to these exact `Store` and `ai_tasks` contracts, seeded `summary` bullets will drop or fail `verified == True`, `Store.review_ai` will raise `PermissionError` during `evaluate_panel` and `score_human_session`, field lookups (`final_text`, `ai_text`, 1-arg `source_hashes`) will fail, and `HOLD`/`QUARANTINED` records will return `UNKNOWN` instead of `FAIL`.
* Smallest useful change: Update `P01-T01`, `P01-T02`, `P02-T01`, and `P02-T02` to: (a) bind a deterministic offline `store.ai.run` responder plus matching synthetic `release` / `release_context` on the harness `Store` and run `Store.ai_run` under the reviewing user's account; (b) use `Store.review_ai(user, rec_id, action, reason, text)` (`<= 300` chars), `rec["override_text"]` / `rec["shown_output"]`, and `review_evidence["compared"]["ai" | "workflow"]`; (c) use exact `source_labels` syntax on every `summary` bullet and choose roles whose `can_see_reason` visibility matches cited labels (e.g., `Retrofit Coordinator` and `Resident Liaison Officer` as authorised roles, and `Retrofit Programme Manager` or `Grants and Evidence Officer` with non-reason-gated citations for `unauthorised_competent`); and (d) treat `rec["status"] in (HOLD, QUARANTINED)` as `FAIL` and recompute post-review hashes via `ai_tasks.source_hashes(store, reviewer_user, rec["case_ids"])` (or `source_snapshot_hashes` with matching `reason_ok`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01`, `P01-T02`, `P02-T01`, and `P02-T02` in `.copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md` (and corresponding `FR-223-01`/`FR-223-02` wording in the plan) reflecting exact `Store`/`ai_tasks` signatures, field keys, role visibility, `HOLD` status handling, and harness release binding.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Allowing unreasoned `accept` on non-discrepant proposals lets default acceptance + citation validity pass and leaves provenance incomplete

* Related IDs: FR-223-01, FR-223-02, FR-223-04, AC-2, AC-4, P01-T02, P02-T01, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md (lines 75-86, 108-115), .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md (lines 109-115, 190-196), src/core/src/zava_forward/core/ai_tasks.py (lines 345-393)
* Concern: `P01-T02` requires `len(reason.strip()) >= authority.min_reason_chars` and a resolving case `source_labels` citation only for `disposition in ("edit", "reject")` or proposals flagged by `inspect_case_discrepancies`. Consequently, on the two valid control scenarios (`S-223-07`, `S-223-08`) -- or on any subtle defect not caught by heuristic text rules -- `default_accept` and `citation_only` calling `Store.review_ai(user, rec_id, "accept")` with `reason=""` and zero source verification will receive `PASS` from `human_review_gate`. Simultaneously, `competent` accepting valid controls with `reason=""` leaves `reviewer_reason` blank and cites no source on 25% of reviewed records, contradicting `FR-223-02` ("Every reviewed scenario record exposes complete `reviewer`, `source`, and `reason` provenance fields") and Issue #223 criteria 2 and 4 ("Reviewer, source, and reason are retained" and "Default acceptance and citation validity alone cannot pass").
* Impact: Default rubber-stamp acceptance combined with `verified == True` passes `human_review_gate` on non-flagged proposals (`gate_passed_count > 0` for `default_accept` and `citation_only`), weakening the structural control against automation bias and breaking 100% `reviewer`/`source`/`reason` retention for `competent`.
* Smallest useful change: Require every `human_review_gate` pass -- including `action == "accept"` -- to provide a substantive (`>= authority.min_reason_chars`, `<= 300` chars), non-memory `reviewer_reason` citing at least one verified case `source_labels` key (`Store.review_ai` already accepts and persists `reason` on `"accept"`). Have `competent` supply a source-grounded verification reason when accepting valid controls (`gate_passed_count == 8`, `retained_evidence_complete == True`), while `default_accept`, `citation_only`, and unverified `automation_bias` acceptances pass blank or citation-badge-only reasons and fail `human_review_gate` (`gate_passed_count == 0` for `default_accept` and `citation_only`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-223-01`, `FR-223-02`, `AC-4`, `P01-T02`, and `P02-T01` requiring substantive case-source-cited `reviewer_reason` across all gate-passing dispositions (`accept`, `edit`, `reject`) and asserting `gate_passed_count == 0` for `default_accept` and `citation_only`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `rai_release.named_human` and `controls.is_memory_reference` have narrower token coverage than assumed in research and `P03-T01`

* Related IDs: FR-223-01, AC-4, C5, P01-T02, P03-T01
* Evidence: src/core/src/zava_forward/core/rai_release.py (lines 42-69), src/core/src/zava_forward/core/controls.py (lines 48-53), .copilot-tracking/research/2026-11-14/human-review-effectiveness-223-2305-research.md (lines 58-59), .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md (lines 103-107, 277-279)
* Concern: `P03-T01` asserts that `human_review_gate` rejects `"TBD"` via `named_human` and conversational chat-memory reasons via `controls.is_memory_reference`. In `rai_release.py`, `named()` blocks only `{"unknown", "unavailable", "none", "unapproved"}` and `NON_HUMAN_TOKENS` covers `{"system", "agent", "bot", "automation", "automated", "copilot", "assistant", "ai", "llm", "service"}`, so `named_human("TBD")`, `named_human("pending")`, `named_human("unassigned")`, `named_human("workflow")`, and `named_human("model")` all return `True`. Likewise, `controls.MEMORY_REF` matches only `CM-<12+ hex>`, `memory:<non-space>`, and `chat-memory`, not conversational phrases such as `"earlier in chat"` or `"the assistant said"`.
* Impact: Relying solely on `rai_release.named_human` and `controls.is_memory_reference` will allow placeholder identities (`"TBD"`, `"pending"`) in `resolved_by` or `AuthorityPolicy.approved_by` and conversational memory justifications to slip past `human_review_gate`, causing planned `P03-T01` adversarial tests to fail.
* Smallest useful change: Specify in `P01-T02` and `P03-T01` that `human_review_effectiveness` combines `rai_release.named_human(...)` with an explicit placeholder/automation token denylist (`tbd`, `todo`, `pending`, `unassigned`, `placeholder`, `workflow`, `model`, `n/a`) and combines `controls.is_memory_reference(reason)` with conversational chat/assistant-memory phrase refusal, testing both canonical (`CM-...`, `memory:...`, `chat-memory`) and conversational memory inputs.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T02` and `P03-T01` in `.copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md` specifying the supplemental placeholder-identity and conversational-memory checks alongside `rai_release.named_human` and `controls.is_memory_reference`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Pure-Python embedded synthetic fixtures (`ZF-223-A`, `ZF-223-B`, `DEFAULT_SCENARIOS`) executed inside `tempfile.TemporaryDirectory` cleanly avoid unregistered `src/core/evals/` provenance failures (`C7`) and wheel `package-data` gaps without touching `pyproject.toml`.
* Narrow typed adapter wrappers around legacy untyped `Store` and `ai_tasks` (`C8`) preserve full `mypy --strict` compliance across `human_review_effectiveness.py` and `test_human_review_effectiveness_223.py`.
* Multi-task pairing (`summary` and `message`) against `Store.ai_run(..., mode="workflow")`, combined with blind `blank_worksheet()`, `score_human_session()`, duplicate-rejecting `pool_human_sessions()`, and `live=True` fail-closed `OQ-017` enforcement, honestly separates deterministic engineering proof from live human-trial governance (`Refs #223`).
* Residual risk (explicitly accepted within engineering scope): Real participant review timing, human error distributions, and competent-review role delegations remain open governance items under `OQ-017` until named human authority holders approve live thresholds and execute blind human sessions.

## Questions or Blocking Evidence Gaps

* None. All four findings are fully resolved by the supplied `src/core` source evidence and require no user input or external research.

## Limitations

* Assessment is bounded to the supplied planning, research, and five `src/core` modules (`ai_tasks.py`, `store.py`, `gates.py`, `rai_release.py`, `controls.py`); mixed-in helpers (`GovernanceMixin.verify_audit`, `projection.can_see_reason`) were assessed strictly from their imported call sites in `store.py`, `ai_tasks.py`, and `controls.py`.
* Validation commands were not executed during critique because `human_review_effectiveness.py` and `test_human_review_effectiveness_223.py` have not yet been created.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md` and `.copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md` to apply `PC-001` through `PC-004`, record their dispositions in `Critique Disposition`, mark the plan `Ready`, and proceed to `rpi-implement` without another critique pass.
* User response required: No
