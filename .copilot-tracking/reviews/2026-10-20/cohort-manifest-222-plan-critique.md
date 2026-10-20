<!-- markdownlint-disable-file -->
# RPI Plan Critique: cohort-manifest-222

## Metadata

* Task ID: 222
* Critique date: 2026-10-20
* Plan: .copilot-tracking/plans/2026-10-20/cohort-manifest-222-plan.md
* Phase details: .copilot-tracking/details/2026-10-20/cohort-manifest-222-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context: preparation-only, wholly synthetic, UNAPPROVED manifest and human protocol for jmservera/ama#222; no evaluator, runtime, models, participants, live data, threshold approval or ticked AC.
* Research and evidence considered: .copilot-tracking/research/2026-10-20/cohort-manifest-222-research.md; spot-verified against src/core/src/zava_forward/core/ranking.py, src/core/src/zava_forward/core/stock.py, src/agents/evals/registry.json, src/agents/tests/test_eval_registry.py, src/agents/src/zava_forward/agents/ai_eval.py (build_case), src/agents/pyproject.toml, .github/workflows/mvp-ci.yml, docs/reference/README.md, and the #222 issue body (six ACs).
* Decisions, dependencies, acceptance: owner decision 2026-10-20; #108 (open) and #174 (closed); plan AC-P1..AC-P3; issue AC1..AC6.
* Assessment boundary: plan-level credibility only. No implementation exists. Issue comments and PRD line cites were not re-fetched; they are taken from research.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| C3 registry rule | Covered | test_eval_registry requires every src/*/evals/*.json to be registered, version equal to file `version`, contains_real_data false. Plan FR-6 matches. |
| C5/C6 ranking Unknown | Covered | ranking.py `_support` is `support_status == "Yes"`; Unknown sorts with No; `reasons` adds support_unknown. Claim true. |
| C7 invariance | Covered | ranking reads only hazards, resident support, days_in_stage, stage, id. Sensor and appointment fields are ignored. |
| C9 build_case | Covered | No sensor field; build_case also writes phone, postcode, email fields (fictional constants). |
| Issue AC1 paired cohorts | Partial | Factor families named; no minimum scenario inventory or per-factor coverage rule (PC-004). |
| Issue AC2 seeded defects | Partial | Only C6 is evidence-backed; other SD-xx are undefined (PC-004, PC-005). |
| Issue AC3 reconciliation | Partial | Arithmetic over invented counts proves nothing real (PC-006). |
| Issue AC4 small samples | Covered | Zero denominator, small, missing-label scenarios planned. |
| Issue AC5 no averaging | Covered | Threshold-averaging seed planned. |
| Issue AC6 owner approval | Covered | Owner checklist and unresolved decisions. |
| Oracle and leakage | Partial | PC-001, PC-002. |
| Test ownership and gate | Partial | PC-003, PC-007, PC-008. |

## Verdict

* Verdict: Revise
* Rationale: The design is bounded and the cited code facts hold. Several substantive gaps would let a draft be read as an oracle or held-out set, pre-judge an owner decision, or leave acceptance traceability and test ownership under-specified. All are planner-correctable before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Co-located expected outcomes contradict the held-out and leakage protocol

* Related IDs: FR-1, FR-2, P02 held-out custody, G2, research Risks
* Evidence: Plan FR-2 puts scenarios and expected outcomes in one committed JSON; P02 says "manifest IDs only in prompts; expected outcomes withheld until freeze". src/agents/evals/registry.json already labels the golden sets development evidence.
* Concern: A repo-resident file holding both scenarios and agent-authored expected outcomes is by construction a development/authoring set that any agent or prompt can read. The pack cannot also claim it as the held-out set or describe a withholding the file itself defeats.
* Impact: Leakage and oracle inference; weakens W1/W3 independence criteria.
* Smallest useful change: State in manifest (`role`: "authoring-draft-not-held-out"), registry purpose and pack that this file is never the held-out set; the held-out set must be authored later by a named custodian outside the repo; add a test assertion on that field and that no expected outcome is labelled "ground truth", "gold" or "oracle".
* Action owner: planning parent
* Exact resolving evidence: plan FR-1/FR-8 and P02 text updated; manifest field and test assertion listed in details P01-T03.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Expected-difference pair for support-Unknown pre-judges an owner decision

* Related IDs: FR-2, FR-3, P01-T01, research C6, Unresolved Decisions
* Evidence: ranking.py `_support` / stock.py `support_status`; research lists "defect or accepted policy" as owner-only; policy v1.0.0 is an unsigned draft.
* Concern: Encoding "expected difference" for Unknown vs No asserts the agent's view of correct behaviour as the expected outcome, and ranking.py currently produces the opposite. Seed SD for C6 would read as a confirmed defect.
* Impact: Approval inference; a later evaluator would score current code as failing against an unapproved label.
* Smallest useful change: Record C6 as a pair with two alternative expectations (A: current policy behaviour, B: candidate correction), each `proposal`, `owner_decision_required` true, no pass/fail expectation until the owner chooses; mark the seed "candidate, unconfirmed".
* Action owner: planning parent (owner disposition stays with the policy owner)
* Exact resolving evidence: FR-3 and P01-T01 revised; checklist item for C6 in the pack.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Registry has no status field, so DRAFT relies on prose; "owner Unassigned" and version style may read as sanctioned

* Related IDs: FR-6, AC-P2, research C2/C3
* Evidence: src/agents/evals/registry.json entries (owner and purpose strings only); test_eval_registry checks id, path, version, owner, purpose, contains_real_data only.
* Concern: Nothing machine-enforced in the registry marks the entry draft; the plan relies on the new test, which does not run if deselected. `used_by` listing the review pack (a Markdown file) is inconsistent with existing entries that list code/tests.
* Impact: Registered datasets sit beside approved evidence; consumers could treat it as approved.
* Smallest useful change: Keep registry schema unchanged (test ownership) but fix purpose wording ("DRAFT, UNAPPROVED, NOT EXECUTED, not held-out, not fairness evidence") and the new test cross-checks registry purpose against the manifest literals; list only the new test in `used_by` or state why the pack is included.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 and FR-8 text; test asserts registry-manifest consistency.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: No acceptance traceability matrix from AC1-AC6 to manifest elements, and no minimum inventory

* Related IDs: FR-2..FR-5, FR-7, FR-8, P01-T01, issue AC1-AC6
* Evidence: Plan lists factor families and seeds in prose; "CM-P01..." has no count; "Done when FR-1 to FR-5 hold" is circular.
* Concern: Doneness cannot be judged; FR-7 traceability is only in the pack, not checkable against the manifest. The AC2 "all seeded defects" has one evidence-backed seed.
* Impact: Under- or over-building; reviewer cannot confirm coverage.
* Smallest useful change: Add to details a table AC1..AC6 -> manifest keys -> minimum structural content (at least one pair per factor family; at least one seed per defect class; named insufficient cases) and have the test assert each AC key is referenced by at least one element. Label counts structural, not targets.
* Action owner: planning parent
* Exact resolving evidence: details table; test asserts per-AC reference.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Pair factors not all distinguishable by current code; cohort definition risks sensitive-attribute implication

* Related IDs: FR-2, P01-T01, research C7/C9, OQ-018
* Evidence: ranking.py and build_case: only support/adjustment, hazards, days, stage drive ranking; no sensor or appointment fields exist on cases; `adjustment`, `priority_support`, `preferred` are the only accessibility/contact proxies.
* Concern: Sensor and appointment pairs are invariance-only for ranking, and AI-task expectations are "to be labelled", so many pairs carry no usable expected outcome. Cohort arms for accessibility need are special-category-adjacent; the plan does not say arms are abstract placeholders rather than proposed cohorts.
* Impact: Pre-empts OQ-018 field and cohort choice; empty-looking scenarios.
* Smallest useful change: Use neutral arm labels (arm-A/arm-B) with a `cohort_definition: "placeholder, not an approved cohort or lawful field"` note; mark AI-task expected outcome `unlabelled` explicitly and state which factors map to existing case fields vs not yet representable.
* Action owner: planning parent
* Exact resolving evidence: FR-2 and P01-T01 text; pack checklist item for OQ-018.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Reconciliation and denominators are invented arithmetic that may be mistaken for results

* Related IDs: FR-4, FR-8, AC3
* Evidence: research C1, C4 (no cohort labels in fixtures; no harness cohort report); no evaluator is in scope.
* Concern: Per-arm counts and errors with no producer can only be hand-authored; the test then checks the author's own arithmetic.
* Impact: Looks like evidence; tautological test.
* Smallest useful change: Name them `illustrative_reconciliation_template` values, state the test checks internal consistency only and that real reconciliation needs the later evaluator; keep numbers out of the proposals unless labelled.
* Action owner: planning parent
* Exact resolving evidence: FR-4/FR-8 wording and manifest field name.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Test ownership and gate wiring underspecified

* Related IDs: FR-8, NFR-3, P04, AC-P1
* Evidence: .github/workflows/mvp-ci.yml runs `unittest discover` for src/api and src/orchestrator with PYTHONPATH to agents/tests; src/agents/pyproject.toml pins ruff 0.17.1; P04 says "the core test selector used by the gate" without naming it; test_eval_registry reaches the repo root via parents[3].
* Concern: Not stated how the new module is discovered in CI (src/agents job or only the api discover), the exact commands, or that Ruff config applies. A test reading the review pack in docs/ also couples an agents test to a KB path not shipped in the agents image (README says evals/fixtures are not shipped).
* Impact: Test may never run in CI or break when paths move; ownership ambiguous.
* Smallest useful change: In details name the exact commands (`cd src/agents && python3 -m unittest test_cohort_manifest_draft test_eval_registry -q` plus ruff check from src/agents), confirm the CI job that discovers it, and keep the pack-AC check to a path-relative read with a clear failure message, or drop it and verify the pack by the link/ASCII check. Keep one module, removals none.
* Action owner: planning parent
* Exact resolving evidence: details P04 command list; one run output at implementation.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Test heuristics are brittle or ineffective ("no approval wording", personal-data patterns)

* Related IDs: FR-8
* Evidence: Plan requires `requires_approval` and "approval requirement" wording in the manifest itself, so a naive approval-word ban conflicts.
* Concern: Define exactly: forbid `status` values other than the literals, forbid "approved"/"held-out"/"ground truth" unless inside a negation field, scoped to the JSON only. Personal-data check should cover email, phone-like and UK postcode patterns with a fixed allow-list for the harness fictional constants if reused.
* Impact: False failures or hollow checks.
* Smallest useful change: Specify the assertions in details P01-T03.
* Action owner: planning parent
* Exact resolving evidence: assertion list in details.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-009 -->
### PC-009 [Low]: Scope creep and placement details

* Related IDs: FR-9, P02, P03, plan metadata
* Evidence: docs/reference/research/evaluation/ does not exist; docs/reference/README.md has "Research Syntheses" at line 390; src/agents/README.md pointer is requested.
* Concern: A new KB subfolder for one page needs index placement-rule justification; "review burden and uncertainty plan", "held-out label protocol" and "quality-threshold proposals" are requested by the owner, but the plan's extra items (separate pointer README edit plus a new folder) add surface. Plan status "ready" while critique disposition is pending.
* Impact: Minor surface growth; index mismatch.
* Smallest useful change: Place the page in an existing folder (for example docs/reference/research/) or justify the new folder against the index rules; set plan status to "revise after critique" until the disposition is recorded; record the C6 and PC dispositions in the plan.
* Action owner: planning parent
* Exact resolving evidence: plan updated path and status; index row text.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-010 -->
### PC-010 [Low]: Proposed numeric targets lack a rule for what counts as a proposal and who may revise

* Related IDs: FR-5, NFR-1
* Evidence: Plan FR-5 requires `proposals` with rationale.
* Concern: No required keys or "source of rationale" (invented vs cited) are given, so a reviewer cannot tell a sector-derived figure from an arbitrary one.
* Smallest useful change: Require per proposal `value`, `rationale`, `basis` ("invented" or a cited local source), `requires_approval` true, `approver_role` unassigned; test asserts the keys.
* Impact: Invented numbers look authoritative.
* Action owner: planning parent
* Exact resolving evidence: FR-5 text and test assertion.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Code claims C3, C5-C7, C9 verified; option A reuses registry and avoids new services.
* Non-goals, unticked ACs, "Refs #222" and local-first publication are clear.
* Residual risk: all expected outcomes remain agent-authored; accepted only if the pack states so.

## Questions or Blocking Evidence Gaps

* None blocking. Owner decisions (C6 disposition, cohorts, thresholds, labeller) remain open by design.

## Limitations

* Issue comments, PRD line numbers and governance.py line cites not re-fetched or fully re-verified; no implementation to test.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: direct revision of plan FR-1/FR-6/FR-8 and details P01-T03/P02 for PC-001 to PC-010, record dispositions in the plan, finalize without another critique
* User response required: no

## Referenced Artifacts

| Artifact | Description |
|----------|-------------|
| [.copilot-tracking/plans/2026-10-20/cohort-manifest-222-plan.md](.copilot-tracking/plans/2026-10-20/cohort-manifest-222-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-20/cohort-manifest-222-phase-details.md](.copilot-tracking/details/2026-10-20/cohort-manifest-222-phase-details.md) | Phase details |
| [.copilot-tracking/research/2026-10-20/cohort-manifest-222-research.md](.copilot-tracking/research/2026-10-20/cohort-manifest-222-research.md) | Research |

## Next Steps

No user action required. Dispatching planning parent revises directly (no further critique).
