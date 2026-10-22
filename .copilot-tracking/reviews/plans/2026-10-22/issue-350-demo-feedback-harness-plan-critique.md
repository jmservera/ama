<!-- markdownlint-disable-file -->
# RPI Plan Critique: Offline demo-feedback acceptance harness (Refs #350)

## Metadata

* Task ID: issue-350-demo-feedback-harness
* Critique date: 2026-10-22
* Plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-harness-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-harness-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: single final-candidate critique; offline harness for the #350 owner-feedback minimum; reuse runtime schemas with no invented API shapes; redirect, denial or asset existence never counts as success; four states pass/fail/blocked/not-run; no broad catches; ownership limited to tools/check-demo-feedback.py, tools/test_check_demo_feedback.py and own .copilot-tracking files.
* Research and evidence considered: .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-harness-research.md (not re-read in full; plan citations C1-C16 spot-checked through source), plus source: src/core/src/zava_forward/core/{projection,taskqueues,store,ranking,ledger}.py, src/api/src/zava_forward/api/{server,workbench,auth}.py, tools/rpi-checks.py.
* Decisions, dependencies, and acceptance criteria considered: plan User Decisions and Requirements, Functional and Non-Functional Requirements, Acceptance Criteria, P01-P03 task details.
* Assessment boundary: plan claims about identifiers, imports and response shapes were checked against current source in this worktree. Not executed: no imports run, no tests, no gate. src/core/ai.py was not read beyond grep hits.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Import identifiers (projection.STAFF_ROLES, CONTRACTOR, me_payload, NOTE_HELD; ranking.CURRENT; taskqueues.contract; workbench.navigation; Store.REC_LABEL) | Covered | All exist. REC_LABEL is a class attribute at store.py:757 ("AI suggestion, not approved"). `workbench` imports only typing, projection, workflows.MANAGER_ROLES: no import-time side effects. `zava_forward.api` has no `__init__.py` (namespace package): fine. `ranking.CURRENT` is loaded from policy files at import (ranking.py:60-61), read-only. |
| `/api/me` shape (P01-T02, FR me_contract) | Covered | server.py:366-372 matches plan: me_payload + account{name,email,provider} + map{tiles,attribution} + navigation + work_queues for non-contractors. |
| Case write/reload (FR case_write_reload) | Partial | POST `/api/cases/{id}/call` and log_call exist (server.py:915, store.py:481); `/api/audit-check` returns ledger.verify_entries report (intact, entries, head). See PC-003, PC-004. |
| ai_evidence (FR ai_evidence) | Partial | rec fields match store.py:~820-850 and `_rec_view`; endpoint wrapping unspecified. See PC-001. |
| baseline_distinction | Covered | page_cases `total` = len(_filtered), which excludes closed cases for non-closed views (store.py:255). |
| Overall verdict rule (P01-T01) | Partial | Self-contradictory. See PC-002. |
| NFR quality gates / P03 | Partial | See PC-005. |
| Ownership and no-edit constraints | Covered | Only two tools files plus tracking; no shared file edits. |

## Verdict

* Verdict: Revise
* Rationale: The runtime identifiers and the `/api/me` and call/audit contracts the plan relies on are real, and the safety posture (offline, bounded loader, denial never success) is credible. Four substantive gaps remain that an implementer would otherwise resolve by guesswork: the AI evidence endpoint envelope, a contradictory overall-verdict rule, self-declared persistence/identity markers that can make a pass look stronger than its proof, and an undefined Ruff scope. All are planner-correctable; none needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `ai` evidence slot does not say which endpoint response it holds, and the two real shapes differ

* Related IDs: FR ai_evidence; P01-T02 evidence slots (`ai.status/body`)
* Evidence: src/api/src/zava_forward/api/server.py:407-408 (`GET /api/ai/priority` returns `{"recommendation": <rec view or None>}`); server.py:887-888 (`POST /api/ai/priority` returns the rec view directly); store.py:861 (`latest_priority` may return None).
* Concern: The plan lists record fields (source, model, validated, release, label, ...) but not whether the body is the GET envelope, the POST record, or both, nor how `recommendation: null` is classified. A checker written to the POST shape rejects a real GET capture and vice versa, which is exactly the "invented API shape" risk. The real POST path is a paid AI call, so a capture of it is the spend event; the plan must state which is accepted.
* Impact: Wrong envelope gives false `fail` or a misread pass; null recommendation could be mis-scored.
* Smallest useful change: Specify `ai.body` as the `GET /api/ai/priority` envelope `{"recommendation": rec}` (and optionally accept the bare POST record by explicit rule); define `recommendation: null` as `not-run` (no recommendation recorded), non-200 as `fail`. Also state that `mode == "ai"` is true for template fallback too (store.py: `mode` is "workflow-only" only for the workflow-only reason), so `source == "ai"` plus `fallback_reason` absence is the real discriminator, and that `status == "Quarantined"` is the late-result state.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 and the ai_evidence FR name the endpoint/envelope and the null, quarantined and template fallback classifications, with a P02 test for each built from `Store._rec_view`-shaped output or the same field list.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Overall-verdict rule contradicts itself and makes the exit-0 and pass paths dead or untestable

* Related IDs: FR report model (exit codes); P01-T01 Context; Acceptance Criteria 1
* Evidence: P01-T01 Context first states "all required checks pass with origin deployed-capture gives pass" then states a deployed-capture overall pass is "never produced while any gap exists" (spend_bound and admin_account always `not-run`). Plan FR 2 says exit 0 only for overall `pass`, and also that overall pass is unreachable.
* Concern: Two incompatible rules for the same case, an `authenticity: unverified-by-harness` field that belongs only to the unreachable branch, and an exit code (0) that can never occur. "mixed pass and not-run gives blocked" also conflicts with "not-run gaps are non-gating" wording.
* Impact: An implementer must pick one; tests asserting "pass for each check and the overall cap" become ambiguous; a future maintainer could make overall `pass` reachable without an explicit decision.
* Smallest useful change: Replace with one table: any fail gives fail; else any blocked gives blocked; else all measurable checks pass with gaps listed gives `blocked` (reason "gaps: spend_bound, admin_account"); all not-run gives not-run. Drop the unreachable pass branch, keep exit 0 documented as reserved/unreachable in this slice, and keep `authenticity` as a top-level field on every report. State that per-check `pass` is the testable pass surface.
* Action owner: planning parent
* Exact resolving evidence: P01-T01 Context contains a single non-contradictory rule table and the FR no longer describes a reachable overall pass; P02-T01 asserts the rule table rows.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Self-declared markers (`origin`, `synthetic`, `restart_between_write_and_read`, `image.reference`) can turn operator assertion into a pass; the plan does not bound that

* Related IDs: FR image_identity, case_write_reload; Acceptance Criteria 3; user requirement "never count denial/assertion as success"
* Evidence: plan evidence slots are harness-defined (the runtime has no restart, origin or image field; server.py exposes none), and P01-T01 allows `origin` to be either value, set by whoever writes the bundle.
* Concern: A bundle author can set `origin: deployed-capture` and `restart_between_write_and_read: true` without any capture. The plan caps fixture origin but does not cap these claims, and does not say the bundle schema is harness-owned rather than runtime-derived.
* Impact: A per-check `pass` for persistence and image identity can be read as deployed proof. This is the main overclaim risk for #350.
* Smallest useful change: (a) State the bundle schema is a harness-owned evidence envelope, not a runtime schema (runtime bodies inside it are unchanged). (b) Make every per-check `pass` reason and the report carry `authenticity: unverified-by-harness`; (c) require persistence evidence to be corroborated by runtime-observable data already in the plan (after-restart detail shows the contact, ledger entries increased and head changed) and say the restart flag alone is never sufficient; (d) require a capture timestamp and source URL/host fields only as recorded context, never gating.
* Action owner: planning parent
* Exact resolving evidence: plan FR and Non-Goals text states the envelope is harness-owned and that pass is "consistent with supplied evidence", and a P02 test shows restart flag true with an unchanged after-detail is not `pass`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Case write/reload and `/api/me` rules omit checks that real source permits, and one stated rule is unverified

* Related IDs: FR me_contract, case_write_reload; P01-T02
* Evidence: store.py:481-493 (`log_call` truncates outcome to 80 chars, defaults channel "Phone", stores `at/purpose/direction/by`, `outcome` projected through `status_only` for roles without need: projection.py:102-103, outcome returns NOTE_HELD unless it is an APPOINTMENT_STATUS value); store.py:355-358 (`counts` keys mine, hazards, ...); projection.py:192-195 (staff `user` is the full user dict; contractor `user` is name/role/contractor only); server.py:366.
* Concern: (1) The plan says contacts +1 "with the exact outcome", but only APPOINTMENT_STATUS strings or empty survive projection for some roles; a free-text outcome read back by such a role will be NOTE_HELD. The plan treats that as `blocked` but never says how to tell it from a genuine mismatch (compare against `projection.NOTE_HELD` before comparing outcome). (2) The evidence must say whose role captured the after-detail; otherwise outcome comparison is meaningless. (3) Outcomes over 80 characters are truncated by log_call, so the exact-match rule must compare the truncated value. (4) `me_contract` does not say what is checked for staff `counts` and `staff` (shape of counts keys, `staff` a list) while it checks contractors strictly; and `navigation equal to workbench.navigation(user)` uses the captured `user`, which for contractors is a reduced dict: confirm navigation(user) works with it (it uses `user["role"]` and `projection.allowed`, so it does).
* Impact: False `fail` or false `blocked` on legitimate captures; missed drift in staff payload.
* Smallest useful change: Add to details: compare after-outcome to `outcome[:80]`; if after-outcome equals `projection.NOTE_HELD` then `blocked`; require `case_write.role` or reuse `me.body.user.role`; add staff `counts` (mapping with int values) and `staff` (list) checks, or state explicitly they are unchecked.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 details list these rules and P02-T01 has tests for truncation, NOTE_HELD and staff counts type.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Quality-gate claims are underspecified: Ruff scope/config for tools/, the unittest invocation, and the "no broad catch" self-check

* Related IDs: NFR quality gates; P02-T01 validation; P03-T01
* Evidence: tools/rpi-checks.py:424-425 and 1084-1085 run `ruff check .` and `ruff format --check .` only with each project's cwd (src/<project>), whose pyproject.toml files carry the Ruff config (src/agents/pyproject.toml:22+); tools/ has no pyproject. The plan's CI-pinned Ruff is 0.17.1 (rpi-checks.py:468). tools/test_rpi_checks.py is the only tools test in the gate matrix (rpi-checks.py:47, 95).
* Concern: "new files pass Ruff" has no defined command, config or version, so the claim cannot be reproduced, and the gate never lints the new files, so a green gate says nothing about them. `python -m unittest tools.test_check_demo_feedback` relies on tools being an importable namespace package from repo root, and the hyphenated script is loaded via importlib; neither is shown to work. There is also no stated check that implies "no broad catches".
* Impact: Unverified lint/format status is reported as a quality pass; a later reviewer cannot reproduce it.
* Smallest useful change: In P03 and P02 specify exact commands: `python -m ruff check tools/check-demo-feedback.py tools/test_check_demo_feedback.py` and `ruff format --check` with ruff==0.17.1 and an explicit `--select`/`--line-length` or `--isolated` choice recorded in the changes record; run unittest as `python -m unittest tools.test_check_demo_feedback` from root (or `python tools/test_check_demo_feedback.py`) and record which one worked; add a grep-based review step that the script contains no `except Exception`/bare `except`. State plainly in the PR that the gate does not exercise the new files.
* Action owner: planning parent
* Exact resolving evidence: P02/P03 detail sections contain these commands and the PR-body disclosure sentence; the changes record later captures their outputs.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: ImportError handling conflicts with the "no evidence means every check not-run" rule and imports a heavy module for one constant

* Related IDs: P01-T02 Context; FR CLI acceptance
* Evidence: store.py:1-27 (importing `Store` imports ~25 modules including documents scanner, ai and mixins; no import-time writes seen, but ranking policy files are read at import). `Store.REC_LABEL` is a plain string constant.
* Concern: Plan says an ImportError makes the whole run `blocked`, but with no `--evidence` it also says every check is `not-run`, overall exit 3 with no file access. Module-level imports precede argument parsing in any natural layout. Importing all of `store` merely to read one label also couples the checker to unrelated modules' import health.
* Impact: Ambiguous exit code in a missing-package environment; fragile dependency surface.
* Smallest useful change: State that imports are attempted lazily after argument parsing and only when evidence is present; with no evidence, exit 3 regardless of installability. Keep `Store.REC_LABEL` (it is the real constant) but note the import cost and that no instance is created.
* Action owner: planning parent
* Exact resolving evidence: P01-T01/T02 specify import timing and a P02 test running the no-evidence path with the runtime modules blocked from import (e.g. patched `sys.modules` entry set to None) yielding exit 3.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Critique Disposition table is `pending`; "Planning status: ready" precedes disposition

* Related IDs: Plan Critique Disposition, Task Metadata
* Evidence: plan Critique Disposition row "pending / open".
* Concern: Substantive only because the plan must record each PC finding's disposition before implementation starts; leaving it pending lets implementation begin with open findings.
* Impact: Findings above could be silently dropped.
* Smallest useful change: After applying PC-001 to PC-006, record each finding with Applied/Rejected and response; no second critique is needed.
* Action owner: planning parent
* Exact resolving evidence: Disposition table has one row per PC-001..PC-006 with a disposition and response.
* Decision route: direct planner correction

## Strengths and Residual Risk

* All named imports and identifiers exist as described; importing `zava_forward.api.workbench` has no side effects.
* `/api/me` composition, `/api/cases?view=all` open-only total, call and audit-check endpoints match plan text.
* Fixture-origin cap, bounded loader, specific exceptions and ownership limits satisfy the caller requirements.
* Residual (accepted by design): spend_bound and admin_account stay `not-run`, so no overall pass; #349, #360 and the #350 criteria remain unmet.

## Questions or Blocking Evidence Gaps

* None that need a user answer.

## Limitations

* No code was executed; src/core/ai.py release shape was inferred from store.py release_current (id, version, digest strings) rather than a full read; the research file was spot-checked only via source.

## Recommended Next Action

* Highest-impact finding: PC-001 (ties with PC-002)
* Action owner: planning parent
* Smallest next action: apply PC-001 to PC-006 as direct corrections in the plan and details, then record dispositions (PC-007); no further critique.
* User response required: no
