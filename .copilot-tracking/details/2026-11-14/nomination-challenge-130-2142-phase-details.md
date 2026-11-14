---
title: "RPI Phase Details: nomination-challenge-130-2142"
description: "Evidence-backed phase and task implementation details for Issue 130 controls in src/core"
ms.date: 2026-11-14
---

## Metadata

* Task ID: nomination-challenge-130-2142
* Task slug: nomination-challenge-130-2142
* Related plan: .copilot-tracking/plans/2026-11-14/nomination-challenge-130-2142-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/nomination-challenge-130-2142-research.md, docs/brd/business-requirements.md, docs/prd/product-requirements.md

## Phase Index

| Phase ID | Name                                                            | Status | Detail sections        |
|----------|-----------------------------------------------------------------|--------|------------------------|
| P01      | Core Nomination, Challenge, Re-Review, and Hazard Domain Controls | Ready  | P01, P01-T01, P01-T02  |
| P02      | Worktree-Isolated Bare Test Suite and Verification Gate         | Ready  | P02, P02-T01           |

<!-- rpi:phase id=P01 -->
## P01: Core Nomination, Challenge, Re-Review, and Hazard Domain Controls

### Context

Research (`C1`..`C10`) established that `resident_decisions.py` already implements `nomination_record`, `nomination_correct`, `nomination_review`, `challenge_open`, and `challenge_resolve`, and the worktree holds an initial untracked draft of `nomination_route.py`, but five concrete gaps remain: whitespace/role-label bypasses in pre-review readiness (`C1`), missing pre-review acknowledgement/owner completion action for unready referrals (`C3`), duplicate `HazardRouted` definitions and silent bypass on explicit `hazard_concern=None` or during `nomination_review` (`C4`, `C5`), missing `raised_by`/`representative_ref` support on `challenge_open` plus unstripped/single-entry lookup in `_raiser` (`C6`, `C7`), and disconnected `nomination_route.re_review_set`/`challenge_trail` helpers (`C2`, `C8`, `C9`).

### Intent

Deliver complete, single-source domain enforcement in `nomination_route.py` and `resident_decisions.py` across all four target Issue #130 acceptance criteria while preserving existing `Store` and `SqlStore` schemas and regression contracts.

### Boundaries

* Included: `src/core/src/zava_forward/core/nomination_route.py` and `src/core/src/zava_forward/core/resident_decisions.py`.
* Excluded: `sqlstore.py`, `mssqlstore.py`, `challenges.py`, and `src/api/*`.

### Likely Targets

* `src/core/src/zava_forward/core/nomination_route.py`: canonical strict-typed rules and `HazardRouted`.
* `src/core/src/zava_forward/core/resident_decisions.py`: store-backed resident actions and projections.

### Dependencies

* None.

### Validation Expectations

* `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` pass in `src/core`.

### Completion Evidence

* Clean diff in `nomination_route.py` and `resident_decisions.py` with zero lint or strict type errors.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden `nomination_route.py` strict-typed rules and unified `HazardRouted`

#### Context

`nomination_route.py` is checked under `mypy` `strict = true` (`C11`). It currently lacks `HazardRouted`, treats whitespace-only strings as truthy (`C1`), omits `representative_ref`, `channel`, `challenged_review`, `rationale`, and `evidence_ref` in `challenge_trail` (`C8`), and does not bound `dependent_review_versions` or normalize graph edge inputs (`C8`).

#### Intent

Make `nomination_route.py` the complete, self-contained, strictly typed domain module for Issue #130.

#### Boundaries

* Included:
  * `HAZARD_ROUTING_MESSAGE`, `HAZARD_INTAKE` (retaining `"endpoint": "/api/cases/{case_id}/hazard-raise"` alongside `"route": "independent_hazard_intake"`, `"issue": "#85"`, `"queue_item_created": False`, `"immediate": True`), and `HazardRouted(ValueError)` carrying `self.route = hazard_routing(True, case_id=case_id)`.
  * `missing_before_review(record)` checking stripped non-empty `owner["name"]` (rejecting `owner["name"].strip().casefold() == owner.get("role", "").strip().casefold()` when `role` is a string), stripped non-empty `acknowledgement["reference"]`, and stripped non-empty `non_digital_route`; `require_ready_for_review(record)` raising `ValueError`.
  * `hazard_routing(hazard_concern, *, case_id=None)` returning `None` only when `hazard_concern is False` and returning the `#85` route mapping otherwise (keeping `"endpoint"` and adding `"action": f"/api/cases/{case_id}/hazard-raise"` when `case_id` is supplied, else `"/api/cases/{case_id}/hazard-raise"`).
  * `challenge_trail(record, challenges=())` preserving `"original_account"` as `str | None` alongside structured `"original"` (`reported_subject_ref`, `account`, `source`, `channel`), `"competing_evidence"` (`version`, `reported_subject_ref`, `account`, `source`, `channel`, `raised_by`, `representative_ref`, `challenge_id`, `challenged_review`, and live `challenge_resolution` / `challenge_status` resolved from `challenges` when `challenge_id` matches), and `"reviews"` (`record_version`, `reviewer`, `outcome`, `rationale`, `evidence_ref`, `competing_evidence_versions`, `stale_from_version`).
  * `re_review_set(corrected, dependencies, record)` accepting strictly typed `Node = tuple[str, str, str]`, parsing an optional positive integer version cutoff from `corrected[2]` (`"v2"` or `"2"`) when `corrected[0] == "nomination"` so integer `record_version <= cutoff` filters safely under `mypy --strict`, computing deterministic transitive `dependents` via `ChallengeRegister(dependencies=dependencies).dependents(corrected)`, returning both `"review_versions"` and `"dependent_review_versions"`, and setting `automatic_acceptance=False`, `automatic_sanction=False`, `priority_changed=False`, `consent_changed=False`.
* Excluded: Direct `Store` or SQL I/O inside `nomination_route.py`.

#### Likely Targets

* `src/core/src/zava_forward/core/nomination_route.py`: full module refinement.

#### Dependencies

* `src/core/src/zava_forward/core/challenges.py` (`ChallengeRegister`, `Node`).

#### Validation Expectations

* `python3 -m mypy` (`strict = true`) and `python3 -m ruff check .` pass with zero warnings.

#### Completion Evidence

* All exported symbols in `nomination_route.py` are strictly typed and exercised by unit and store tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Integrate `nomination_route` across `resident_decisions.py` actions and read views

#### Context

`resident_decisions.py` owns transactional resident mutations (`_operation`) for both `Store` and `SqlStore`, subject to strict backward-compatibility invariants (`C9`: `_res_nomination_correct` must not mutate case keys outside `nomination_records`, and default `correction["re_review"]` must preserve exact keys `required`, `automatic_acceptance`, `automatic_sanction`, `dependent_review_versions` when `dependencies` are not supplied).

#### Intent

Wire all nomination and challenge write/read paths in `resident_decisions.py` through `nomination_route` while closing every contrarian gap (`D2`..`D5`).

#### Boundaries

* Included:
  * Re-export `HAZARD_ROUTING_MESSAGE = nomination_route.HAZARD_ROUTING_MESSAGE`, `HAZARD_INTAKE_ROUTE = nomination_route.HAZARD_INTAKE`, and `HazardRouted = nomination_route.HazardRouted`.
  * Update `_refuse_hazard(c, body, *, required=False)` so when `required` is true or `"hazard_concern" in body`, `nomination_route.hazard_routing(body.get("hazard_concern"), case_id=c.get("id"))` raises `HazardRouted(HAZARD_ROUTING_MESSAGE, case_id=c.get("id"))` whenever the flag is not `False` (catching explicit `None`, `True`, strings, numbers).
  * Apply `_refuse_hazard` across `_res_nomination_record` (`required=True`), `_res_nomination_acknowledge` (optional), `_res_nomination_review` (optional), `_res_nomination_correct` (optional), and `_res_challenge_open` (optional).
  * Add `"nomination_acknowledge"` to `RESIDENT_ACTIONS` and `INTAKE_ACTIONS` (`_res_nomination_acknowledge`): requires `appointment_evidence_visible`, enforces `_owner_rights(self, user, record)` whenever `_identity_status(record.get("owner")) == "Known"` (allowing initial owner assignment when missing or `"Unknown"`), refuses post-review acknowledgement once a current un-staled review exists (`ValueError`), checks `expected_version` via `_version(body, record)`, increments `record["version"] = record["version"] + 1` under `challenges.protected_snapshot(c)` / `stamp_assurance`, records named `_intake_owner`, staff-recorded `acknowledgement` (`delivery="Not verified by this system"`), staffed `non_digital_route`, `next_update`, appends prior route snapshot to `acknowledgement_history` when present, and preserves `original` unchanged.
  * In `_res_nomination_review`, enforce `nomination_route.require_ready_for_review(record)` and `_identity_status(record.get("owner")) == "Known"` before allowing review.
  * Keep `authority_for` unchanged for measure-scoped bindings; fix `_raiser(c, extras)` to strip `representative_ref`, reject expired retention (`retention_schedule(c)["expired"]`), inspect the latest recorded entry per measure in `c["representative_authorities"][ref]` (`[v for v in versions if v.get("measure") == m][-1]`), and require at least one case measure whose latest entry has `status == "Confirmed"`, `"Communicate" in tasks`, matching `current_context(c, m)` revision, matching `resident_safe_contact` and `len(resident_contact_history)`, and `authority_date <= k.today() < review_date`; enable optional `("hazard_concern", "raised_by", "representative_ref")` on `_res_challenge_open`, store `**raiser` on the created `affected_challenges` entry, and scrub `challenge.pop("representative_ref", None)` across `c.get("affected_challenges", [])` inside `delete_resident_records`.
  * In `_res_nomination_correct`, accept optional `dependencies` (validated fail-closed with `ValueError` into `dict[Node, list[Node]]` of normalized 3-string `Node` tuples, normalizing integer nomination versions as `f"v{n}"`), call `nomination_route.re_review_set(("nomination", record["id"], f"v{body['expected_version']}"), parsed_deps, record)`, keep default `re_review` dict keys (`required`, `automatic_acceptance`, `automatic_sanction`, `dependent_review_versions`) unchanged when `dependencies` is omitted, and attach `"dependents": [dict(kind=nk, id=ni, version=nv) for nk, ni, nv in re_review["dependents"]]` when `dependencies` is supplied.
  * Delegate `nomination_follow_up` missing-check to `nomination_route.missing_before_review(record)` and attach `record["challenge_trail"] = nomination_route.challenge_trail(record, case.get("affected_challenges", ()))` inside `followup_view(case)`.
* Excluded: Changing `priority_correction_lookup` SQL queries or mutating non-`nomination_records` keys during `nomination_correct`.

#### Likely Targets

* `src/core/src/zava_forward/core/resident_decisions.py`: targeted edits in `_refuse_hazard`, `_raiser`, `nomination_follow_up`, `followup_view`, `_res_nomination_record`, `_res_nomination_acknowledge`, `_res_nomination_correct`, `_res_nomination_review`, and `_res_challenge_open`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Existing `tests.test_resident_decisions` (`JsonResidentDecisions` and `SqlResidentDecisions`) passes 100%, and new nomination/challenge/hazard edge cases pass on both stores.

#### Completion Evidence

* Clean diff in `resident_decisions.py` verified against JSON and SQLite stores.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Worktree-Isolated Bare Test Suite and Verification Gate

### Context

The mandatory verification command runs `python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v` from `src/core` without `PYTHONPATH` (`C12`). Because `.local` has an editable install pointing to `/home/azureuser/source/ama/src/core/src`, `test_nomination_route.py` must bootstrap `<worktree>/src/core/src` (plus `tests` and `../agents/src`) onto `sys.path` and conditionally evict `zava_forward*` modules from `sys.modules` only when a loaded module `__file__` or namespace `__path__` resolves outside `<worktree>/src` (preserving class identities during full-suite multi-file discovery per `PC-003`).

### Intent

Ensure `'test_*nomination*.py'` exercises both pure `nomination_route` domain functions and real `Store`/`SqlStore` persistence across all four acceptance criteria, while passing `mypy --strict`, `ruff check .`, `ruff format --check .`, and adjacent regression suites.

### Boundaries

* Included: `src/core/tests/test_nomination_route.py` and `src/core/tests/test_resident_decisions.py` (0 test removals; up to 12 focused tests in `test_nomination_route.py` and up to 3 focused tests in `test_resident_decisions.py`).
* Excluded: Modifying `/home/azureuser/.local/lib/python3.12/site-packages` or `pyproject.toml`.

### Likely Targets

* `src/core/tests/test_nomination_route.py`: worktree `sys.path` bootstrap, pure domain tests, and JSON `Store` + SQLite `SqlStore` acceptance tests.
* `src/core/tests/test_resident_decisions.py`: focused coverage for `nomination_acknowledge`, explicit `hazard_concern=None`, and resident/representative `challenge_open`.

### Dependencies

* P01-T01, P01-T02.

### Validation Expectations

* Exact mandatory command:
  `cd /home/azureuser/source/ama-demo-wt/feat-130-nomination-challenge-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v`
* Regression verification:
  `cd /home/azureuser/source/ama-demo-wt/feat-130-nomination-challenge-2142/src/core && PYTHONPATH=src:tests:../agents/src python3 -m unittest tests.test_resident_decisions tests.test_challenges tests.test_hazard_referral tests.test_taskqueues`

### Completion Evidence

* Zero errors across `mypy`, `ruff check`, `ruff format --check`, bare `unittest discover` on `test_*nomination*.py`, and targeted store regression suites.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Bootstrap worktree `sys.path` and expand `test_nomination_route.py` and `test_resident_decisions.py`

#### Context

`test_nomination_route.py` is the canonical file matched by `'test_*nomination*.py'` and is type-checked under `mypy` `strict = true` (`C11`, `C12`).

#### Intent

Provide self-contained, strict-typed unit and `Store`/`SqlStore` acceptance tests in `test_nomination_route.py` plus focused complementary assertions in `test_resident_decisions.py`.

#### Boundaries

* Included:
  * Worktree `sys.path` bootstrap at top of `test_nomination_route.py` with conditional foreign-origin `sys.modules` eviction (`PC-003`), `# noqa: E402` on post-bootstrap imports, and an explicit assertion that `nomination_route` and `resident_decisions` loaded from this worktree's `src/core/src`.
  * Pure `NominationRouteUnitTests` covering `missing_before_review` (including whitespace and `.casefold()` role-label rejection), `require_ready_for_review`, `hazard_routing` (`False` vs `True`/`None`/`"yes"`), `challenge_trail` (retaining `"original_account"` string plus live resolved challenge outcomes), and `re_review_set` (string `Node` versions, integer `record_version` cutoff, transitive graph vs unrelated nodes).
  * Store-backed `JsonNominationChallengeRouteTests` and `SqlNominationChallengeRouteTests` exercising:
    1. Pre-review refusal when named owner, acknowledgement, or non-digital route is missing (persisted durably via `store.save()` / seed before `SqlStore` `validate_sql` replay per `PC-004`), followed by `nomination_acknowledge` (bumping `version` to `2`) and independent `nomination_review` (`expected_version=2`).
    2. Resident and confirmed-representative (`Communicate` authority, including multi-measure cases where another measure's authority was recorded later per `PC-002`) `nomination_correct` and `challenge_open` retaining original account, competing evidence, reviewer, and outcome, rejection of unconfirmed/wrong-task representatives, and `representative_ref` scrubbing in `delete_resident_records`.
    3. Correction staling prior nomination reviews and exact transitive dependent decisions (`dependencies` with fail-closed invalid-input rejection per `PC-001`) and `challenge_resolve("Correction recorded")` staling dependent priority recommendations while preserving prior versions, unrelated decisions, priority order, and consent (`automatic_acceptance=False`, `automatic_sanction=False`).
    4. Immediate `HazardRouted` (`#85`, `queue_item_created=False`) across `nomination_record`, `nomination_acknowledge`, `nomination_review`, `nomination_correct`, and `challenge_open` (including `True` and explicit `None`) with zero nomination queue items or audit mutations, paired with independent `store.raise_hazard` verification.
* Excluded: Unrelated test suites outside `src/core/tests`.

#### Likely Targets

* `src/core/tests/test_nomination_route.py`
* `src/core/tests/test_resident_decisions.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Both the bare verification command and the targeted `Store`/`SqlStore` regression suites exit `0`.

#### Completion Evidence

* Recorded command outputs in `.copilot-tracking/changes/2026-11-14/nomination-challenge-130-2142-changes.md`.

#### Unresolved Items

* None.
