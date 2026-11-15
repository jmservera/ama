---
title: "RPI Plan Critique: nomination-challenge-130-2142"
description: "Single-pass credibility critique of candidate RPI plan and phase details for Issue 130 locally verifiable controls in src/core"
ms.date: 2026-11-14
---

## Metadata

* Task ID: nomination-challenge-130-2142
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/nomination-challenge-130-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the four locally verifiable acceptance criteria of Issue #130 (`FR-037`, `AC-065`, `RULE-005`) in `src/core` on branch `feat/safety-130-nomination-challenge-2142`, and verify from `src/core` with bare `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v` without altering SQL DDL or shared site-packages.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/nomination-challenge-130-2142-research.md, .copilot-tracking/plans/2026-11-14/nomination-challenge-130-2142-plan.md, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md, src/core/src/zava_forward/core/nomination_route.py, src/core/src/zava_forward/core/resident_decisions.py, src/core/src/zava_forward/core/challenges.py, src/core/tests/test_nomination_route.py, src/core/tests/test_resident_decisions.py
* Decisions, dependencies, and acceptance criteria considered: Preserve `Store` and `SqlStore` JSON body schema (`cases.body`) without DDL changes; preserve shared user site-packages; keep `OD-41`, `OD-42`, and `src/api` UI authoring forms out of scope (`Refs #130`); reuse `challenges.ChallengeRegister`, `challenges.stamp_assurance`, and `workflows.raise_hazard`; satisfy all four locally verifiable criteria plus strict `mypy`, `ruff`, and bare `unittest discover` gates.
* Assessment boundary: Evaluates completeness, type and runtime correctness, backward compatibility with existing `test_resident_decisions.py` invariants, `Store`/`SqlStore` parity (`validate_sql` replay and retention deletion), and test-isolation safety across the supplied artifacts and five referenced `src/core` files. Does not evaluate out-of-scope `src/api` templates, live MSSQL infrastructure gates, or governance ratification of `OD-41` and `OD-42`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Criterion 1 (`FR-037`, `AC-065`, `C1`..`C3`) | Partial | Pre-review readiness and `nomination_acknowledge` are planned, but `version` transition, existing-owner `_owner_rights`, `.casefold()` role-label comparison, and `SqlStore` `validate_sql` fixture persistence need explicit specification (`PC-004`). |
| Criterion 2 (`FR-037`, `FR-043`, `RULE-005`, `C6`..`C8`) | Partial | Resident and representative raising on `nomination_correct` and `challenge_open` are planned, but `_raiser` delegating directly to `authority_for` fails on multi-measure cases (`versions[-1]`), `delete_resident_records` leaks `representative_ref` on `affected_challenges` (`PC-002`), and `challenge_trail` misses live resolved `affected_challenges` outcomes (`PC-005`). |
| Criterion 3 (`FR-037`, `FR-052`, `AC-065`, `C8`, `C9`) | Partial | Dependent re-review via `re_review_set` and default `re_review` backward compatibility are planned, but `Node = tuple[str, str, str]` clashes with integer `record_version` / `expected_version` under `mypy --strict` and runtime `<=`, and caller `dependencies` lack fail-closed validation (`PC-001`). |
| Criterion 4 (`FR-037`, `AC-065`, `C4`, `C5`, `C10`) | Covered | Fail-closed `#85` routing across `nomination_record`, `nomination_acknowledge`, `nomination_review`, `nomination_correct`, and `challenge_open` (including explicit `None`) is covered; retain `"endpoint"` and `HAZARD_INTAKE_ROUTE` keys (`PC-005`). |
| `P01` (`P01-T01`, `P01-T02`) | Partial | Module boundary and store parity strategy are sound; requires targeted contract fixes in `PC-001`, `PC-002`, `PC-004`, and `PC-005`. |
| `P02` (`P02-T01`, `C11`, `C12`, `D1`) | Partial | Bare `unittest discover` worktree bootstrap and `Store`/`SqlStore` acceptance scenarios cover all four criteria, but unconditional `sys.modules` eviction breaks class identity in multi-file `unittest discover` runs (`PC-003`) and `SqlStore` unready fixtures must be durably saved (`PC-004`). |

## Verdict

* Verdict: Revise
* Rationale: The architecture, scope boundaries, and four-criterion coverage in `nomination_route.py`, `resident_decisions.py`, and `test_nomination_route.py` are well-structured, but five concrete specification defects (`PC-001` through `PC-005`, including a `mypy --strict` / `TypeError` mismatch on `Node` versions and a broken multi-measure `authority_for` assumption) would cause implementation or regression failures unless corrected in the plan details before coding. All five findings are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Node version type mismatch and unvalidated dependency inputs in re_review_set and _res_nomination_correct

* Related IDs: `FR-037`, `FR-052`, `AC-065`, `C8`, `C9`, `C11`, `P01-T01`, `P01-T02`, `P02-T01`
* Evidence: src/core/src/zava_forward/core/challenges.py:16, src/core/src/zava_forward/core/nomination_route.py:85-95, src/core/src/zava_forward/core/resident_decisions.py:1241-1278, src/core/tests/test_nomination_route.py:60-70, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:107, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:148
* Concern: `challenges.py:16` defines `Node = tuple[str, str, str]` and `ChallengeRegister.dependents` sorts `set[Node]` lexicographically. However, `P01-T01` specifies comparing integer `review["record_version"]` (`1`, `2`, ...) via `record_version <= corrected[2]` where `corrected[2]` is `str` (such as `"v1"` in `test_nomination_route.py:61`), and `P01-T02` calls `nomination_route.re_review_set(("nomination", record["id"], body["expected_version"]), parsed_deps, record)` where `body["expected_version"]` is `int`. Additionally, `P01-T01` renames `re_review_set`'s `"review_versions"` output key (`nomination_route.py:90`, `test_nomination_route.py:68`) to `"dependent_review_versions"` without noting the lockstep change, and `P01-T02` does not specify fail-closed `ValueError` validation for malformed caller-supplied `dependencies` payloads or version-token normalization (`"1"` vs `"v1"`).
* Impact: Causes immediate `mypy --strict` failure in `nomination_route.py`, raises runtime `TypeError` (`int <= str` or mixed-type tuple sorting) when `re_review_set` or `_res_nomination_correct` runs with `dependencies`, and allows malformed `dependencies` inputs to raise unhandled `KeyError`/`TypeError` exceptions.
* Smallest useful change: Update `P01-T01`, `P01-T02`, and `P02-T01` so `Node` elements are strictly `tuple[str, str, str]` with canonical normalized version strings (for example `f"v{expected_version}"` or normalized string tokens), `re_review_set` parses integer suffixes from `corrected[2]` (`"v1"` or `"1"`) before bounding integer `record_version <= cutoff`, `_res_nomination_correct` validates optional `dependencies` strictly and raises `ValueError` on malformed shapes or blank elements, and `dependent_review_versions` key naming is aligned across `nomination_route.py`, `resident_decisions.py`, and `test_nomination_route.py`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01`, `P01-T02`, and `P02-T01` sections in `.copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md` specifying `str`-typed `Node` version normalization, integer cutoff parsing in `re_review_set`, fail-closed `dependencies` validation, and aligned return keys.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Multi-measure representative check via authority_for inspects only versions[-1] and retention deletion leaks representative_ref on affected_challenges

* Related IDs: `FR-037`, `FR-043`, `RULE-005`, `C6`, `C7`, `P01-T02`, `P02-T01`
* Evidence: src/core/src/zava_forward/core/resident_decisions.py:44-45, src/core/src/zava_forward/core/resident_decisions.py:257-270, src/core/src/zava_forward/core/resident_decisions.py:1020-1033, src/core/src/zava_forward/core/resident_decisions.py:1173-1190, src/core/tests/test_resident_decisions.py:2542-2575, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:147
* Concern: `P01-T02` directs `_raiser` to validate confirmed `Communicate` authority "via `authority_for` across the case's measures", but `authority_for` (`resident_decisions.py:1023-1028`) hardcodes `a = versions[-1]` and fails whenever `a["measure"] != measure` (a contract relied upon for `authority_version` pinning in `test_resident_decisions.py:2566-2568`). When a representative has authorities recorded for two measures (for example `Confirmed` `Communicate` on `Loft insulation` followed by `Works decision` on `Cavity wall`), looping `authority_for` across `case_measures(c)` rejects every measure because `versions[-1]` belongs to `Cavity wall`. Furthermore, `P01-T02` stores `**raiser` (`raised_by`, `representative_ref`) on `affected_challenges`, which is outside `RESIDENT_FIELDS` (`resident_decisions.py:44-45`) and survives `delete_resident_records` (`resident_decisions.py:1173-1190`); unlike `service_requests` (`line 1186`), `delete_resident_records` does not scrub `representative_ref` from `affected_challenges`.
* Impact: Valid confirmed representatives on multi-measure cases are falsely rejected on `nomination_correct` and `challenge_open` (Acceptance Criterion 2), and personal `representative_ref` identifiers persist in `affected_challenges` after resident retention deletion.
* Smallest useful change: Specify in `P01-T02` that `authority_for` remains unchanged for measure-scoped actions, while `_raiser` strips and validates non-blank `representative_ref` and checks the latest recorded authority entry per measure (`[v for v in versions if v.get("measure") == m][-1]`) against all `authority_for` invariants (non-expired retention, `status == "Confirmed"`, `"Communicate" in tasks`, matching `current_context(c, m)` revision, matching `resident_safe_contact` and `len(resident_contact_history)`, and `authority_date <= k.today() < review_date`) so revoked/superseded versions on a measure never pass while valid authority on another measure succeeds; also scrub `challenge.pop("representative_ref", None)` across `c.get("affected_challenges", [])` inside `delete_resident_records`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T02` and `P02-T01` sections in `.copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md` specifying per-measure latest-entry `Communicate` validation in `_raiser` and `representative_ref` scrubbing in `delete_resident_records`.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Unconditional sys.modules eviction in test_nomination_route.py splits class identities during multi-file test discovery

* Related IDs: `C11`, `C12`, `D1`, `P02`, `P02-T01`
* Evidence: src/core/tests/test_nomination_route.py:1-7, src/core/tests/test_resident_decisions.py:21-25, .copilot-tracking/research/2026-11-14/nomination-challenge-130-2142-research.md:104, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:162, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:202
* Concern: `P02` and `P02-T01` instruct `tests/test_nomination_route.py` to clear cached `zava_forward*` modules from `sys.modules` unconditionally before importing `zava_forward.core`. During a full-suite `unittest discover -s tests` run (where `test_ai_tasks.py` through `test_m*.py` import `ConflictError`, `GateError`, `Store`, `SqlStore`, `SupersessionBinding`, and `ResidentCommittedError` before `test_nomination_route.py` is imported), unconditional `sys.modules` eviction reloads `zava_forward.core.*` as second class objects, breaking `isinstance` and `assertRaises` checks in sibling test modules.
* Impact: Introduces cross-module class-identity regressions in full `src/core` discovery runs and CI gates even when the single-file `'test_*nomination*.py'` selector passes.
* Smallest useful change: Specify in `P02` and `P02-T01` that `test_nomination_route.py` prepends `<worktree>/src/core/src`, `<worktree>/src/core/tests`, and `<worktree>/src/agents/src` to `sys.path` if not already leading, and evicts `zava_forward*` entries from `sys.modules` only when a loaded `zava_forward*` module `__file__` or namespace `__path__` resolves outside `<worktree>/src`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P02` and `P02-T01` bootstrap specification in `.copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md` requiring conditional foreign-origin eviction rather than unconditional `sys.modules` deletion.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Unspecified version progression, existing-owner authorization, and SqlStore replay setup for nomination_acknowledge

* Related IDs: `FR-037`, `AC-065`, `C1`, `C3`, `P01-T01`, `P01-T02`, `P02-T01`
* Evidence: src/core/src/zava_forward/core/resident_decisions.py:481-500, src/core/src/zava_forward/core/resident_decisions.py:517-528, src/core/src/zava_forward/core/resident_decisions.py:582-601, src/core/tests/test_resident_decisions.py:265-271, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:102, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:142-144, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:208
* Concern: `P01-T02` checks `expected_version` in `_res_nomination_acknowledge` via `_version(body, record)` (`resident_decisions.py:481`) without defining: (1) whether `record["version"]` increments or stays constant (if incremented after a review, `_review_current` at line 527 flips false; if left constant, duplicate stale calls at the same `expected_version` are not optimistic-version fenced on JSON `Store`, and `P02-T01` leaves `nomination_review`'s subsequent `expected_version` ambiguous); (2) authorization when `record.get("owner")` already has `"Known"` identity (`_owner_rights` required to prevent unauthorized owner overwrite) versus when missing or `"Unknown"` (initial owner assignment allowed for authorised intake staff); and (3) `SqlStore` test setup in `P02-T01`, where mutating `store.cases` only in memory (as in `test_resident_decisions.py:267`) fails when `validate_sql` (`resident_decisions.py:595-599`) replays `_res_nomination_acknowledge` against the SQLite `cases.body` row. In addition, `P01-T01` should compare `owner["name"]` against `owner.get("role")` using stripped `.casefold()` to match `_person` (`resident_decisions.py:499`).
* Impact: Risks version/review-currency mismatches, unauthorized overwrite of an already-assigned referral owner, or `SqlStore` `validate_sql` replay failures during `P02-T01`.
* Smallest useful change: Update `P01-T01`, `P01-T02`, and `P02-T01` to specify stripped `.casefold()` role-label rejection in `missing_before_review`, `_owner_rights` enforcement in `_res_nomination_acknowledge` whenever `_identity_status(record.get("owner")) == "Known"` (with `challenges.protected_snapshot` non-retaliation check), an explicit `record["version"]` transition rule (for example incrementing `version` while refusing post-review acknowledgement unless re-review is triggered, or keeping pre-review version rules explicit with matching `expected_version` in `P02-T01`), and persisted `store.save()` / `reseed()` unready-referral fixtures for `SqlStore` tests.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01`, `P01-T02`, and `P02-T01` details in `.copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md` recording explicit `version` rules, existing-owner `_owner_rights` checks, `.casefold()` role-label comparison, and persisted `SqlStore` test fixtures.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Backward-compatible key contracts and live resolved-challenge lookup in HazardRouted and challenge_trail

* Related IDs: `FR-037`, `FR-043`, `AC-065`, `C4`, `C8`, `P01-T01`, `P01-T02`
* Evidence: src/core/src/zava_forward/core/nomination_route.py:16-21, src/core/src/zava_forward/core/nomination_route.py:63-88, src/core/src/zava_forward/core/resident_decisions.py:72-75, src/core/src/zava_forward/core/resident_decisions.py:561-566, src/core/src/zava_forward/core/resident_decisions.py:1259-1261, src/core/src/zava_forward/core/resident_decisions.py:1625-1641, src/core/tests/test_nomination_route.py:51-58, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:101, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:105, .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md:149
* Concern: Three contract mismatches appear across `P01-T01` and `P01-T02`: (1) `P01-T01` replaces `"endpoint"` in `HAZARD_INTAKE` / `HazardRouted.route` with `"endpoint_template"` and omits re-exporting `HAZARD_INTAKE_ROUTE` in `resident_decisions.py`; (2) `P01-T01` changes `challenge_trail(record)["original_account"]` from `str | None` (`nomination_route.py:68`, `test_nomination_route.py:53`) to a nested dictionary instead of preserving `"original_account"` alongside structured `"original"` metadata; and (3) `_res_nomination_correct` (`resident_decisions.py:1261`) copies the linked `affected_challenges` entry at correction time (typically while `status == "Open"` and `resolution is None`), so calling `nomination_route.challenge_trail(record)` in `followup_view(case)` without passing `case.get("affected_challenges")` omits the challenge reviewer (`resolution.recorded_by`) and `resolution.outcome` recorded later via `challenge_resolve`.
* Impact: Breaks callers or tests reading `route["endpoint"]`, `resident_decisions.HAZARD_INTAKE_ROUTE`, or string `trail["original_account"]`, and omits resolved formal challenge reviewer/outcome details from `record["challenge_trail"]`.
* Smallest useful change: Retain `"endpoint"` in `HAZARD_INTAKE` and `HazardRouted.route` (re-exporting `HAZARD_INTAKE_ROUTE = nomination_route.HAZARD_INTAKE` in `resident_decisions.py`), keep `"original_account"` as `str | None` alongside `"original"` metadata in `challenge_trail`, and accept optional `challenges: Iterable[Mapping[str, Any]] = ()` in `challenge_trail` (passed `case.get("affected_challenges", ())` from `followup_view`) so linked formal challenges expose current `status` and `resolution` reviewer/outcome alongside the correction snapshot.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` and `P01-T02` details in `.copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md` retaining `"endpoint"`, `HAZARD_INTAKE_ROUTE`, and `"original_account"` and passing `case.get("affected_challenges", ())` to `challenge_trail`.
* Decision route: Direct planner correction (no user decision required).

## Strengths and Residual Risk

* Strong architectural separation: Keeping `nomination_route.py` pure and strictly typed while delegating transactional JSON/SQL persistence (`_operation` and `validate_sql`) to `resident_decisions.py` avoids unnecessary SQL DDL changes and preserves optimistic `rowversion` concurrency.
* Contrarian regression awareness: The plan explicitly preserves `test_resident_decisions.py`'s case-key isolation invariant (`after.pop("nomination_records") == before`) and default `correction["re_review"]` dictionary shape when `dependencies` are omitted (`C9`, `D5`).
* Fail-closed hazard boundary: Catching explicit `hazard_concern=None` as well as truthy non-`False` values across all five nomination and challenge actions (`D2`, `C4`, `C5`) ensures unknown hazard states route immediately to `#85` (`raise_hazard`) with zero nomination queue items or state mutations.
* Accepted out-of-scope residual risk: Governance ratification of `OD-41` and `OD-42` and interactive `src/api` authoring forms remain outside this `src/core` slice, properly reflected by keeping Issue #130 open with `Refs #130`.

## Questions or Blocking Evidence Gaps

* None. All five findings are resolvable directly from the supplied codebase and specification artifacts without additional research or user decisions.

## Limitations

* Critique was bounded strictly to the supplied tracking artifacts and the five referenced `src/core` source and test files without modifying files outside `.copilot-tracking/reviews/plans/2026-11-14/nomination-challenge-130-2142-plan-critique.md` or executing test mutations.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for `PC-001` through `PC-005` in `.copilot-tracking/plans/2026-11-14/nomination-challenge-130-2142-plan.md` and `.copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md`, record critique dispositions, and finalize the plan to `Ready` for `rpi-implement` without another critique pass.
* User response required: No
