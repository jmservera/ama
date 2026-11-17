<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #134 Profile Journey Contract and Connected Same-Home Journey Acceptance

## Metadata

* Task ID: issue-134-same-home-walk-0018
* Task slug: issue-134-same-home-walk-0018
* Related plan: .copilot-tracking/plans/2026-11-15/issue-134-same-home-walk-0018-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-134-same-home-walk-0018-research.md

## Phase Index

| Phase ID | Name                                                                     | Status | Detail sections                  |
|----------|--------------------------------------------------------------------------|--------|----------------------------------|
| P01      | Core Connected Same-Home Journey Contract Validators                     | Ready  | P01, P01-T01                     |
| P02      | Specialist Screen Continuity and Connected Journey Acceptance Tests      | Ready  | P02, P02-T01, P02-T02, P02-T03   |
| P03      | Canonical UX Profile Journey Contract Reference and Knowledge Base Index | Ready  | P03, P03-T01                     |
| P04      | Focused Validation, Guardrail Verification, and Review-Aligned Closeout  | Ready  | P04, P04-T01                     |

## Test Ownership and Canonical Targets

* Canonical production targets:
  * `src/core/src/zava_forward/core/profile_journey_contract.py`
  * `src/api/src/zava_forward/api/web/role-screens.js`
  * `docs/reference/research/ux/profile-journey-contract.md`
  * `docs/reference/README.md`
  * `docs/reference/log.md`
* Generated targets: `none` (`scenario-manifest.json` untouched because `role_screens_browser_check.py` is unchanged).
* Exact test removals: `none`.
* Maximum new test files: `1` (`src/api/tests/test_same_home_profile_journey_acceptance.py`), plus strengthening existing `src/core/tests/test_profile_journey_contract.py`.
* Semantic vs regression coverage:
  * Semantic coverage: `test_profile_journey_contract.py` tests core invariant functions (`check_shared_facts`, `check_vulnerability_redaction`, `check_handover_dependencies`, `check_next_action_continuity`, `validate_same_home_walk`) across positive Store state transitions and negative mutations; `test_same_home_profile_journey_acceptance.py` tests full-stack HTTP API + resident preview + Node `role-screens.js` same-home transitions and contractor redaction.
  * Regression coverage: `test_perspective_walkthroughs.py`, `test_journey_acceptance.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_live_doc_links.py`, `test_content_standard.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_role_screens_connected_journey.py`, `test_role_screens_same_home_identity.py`, `test_role_screens_stage_map_focus.py`, `test_connected_home_check.py`, `test_scenario_manifest.py`, and `test_needs_inventory.py`.

<!-- rpi:phase id=P01 -->
## P01: Core Connected Same-Home Journey Contract Validators

### Context

`src/core/src/zava_forward/core/profile_journey_contract.py` currently validates only single-perspective five-element records (`ELEMENTS`, `validate`, `gaps`). Issue #134 requires code-testable connected same-home walkthrough invariants across the six staff profiles, contractor views, and resident portal (`C4`, `C7`, `C9`-`C12`, `C14`, `C15`).

### Intent

Provide pure, deterministic, fully typed validators and a `Store` multi-profile bundle projector in `profile_journey_contract.py` while keeping `ELEMENTS`, `validate`, and `gaps` backward-compatible.

### Boundaries

* Included: `src/core/src/zava_forward/core/profile_journey_contract.py`.
* Excluded: Changing `perspective_walkthroughs.py` or `journey_acceptance.py` status registers (`elements_met` must stay `0`, `passed` must stay `[]`).

### Likely Targets

* `src/core/src/zava_forward/core/profile_journey_contract.py`: Add connected same-home constants, four invariant checkers, `project_same_home_bundle`, and `validate_same_home_walk`.

### Dependencies

* None.

### Validation Expectations

* `mypy` passes cleanly on `src/core`; `test_profile_journey_contract.py`, `test_perspective_walkthroughs.py`, and `test_journey_acceptance.py` pass.

### Completion Evidence

* `profile_journey_contract.py` exports typed invariant checkers and passes unit and static type checks.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement same-home shared-facts, redaction, handover-dependency, and next-action continuity validators in `profile_journey_contract.py`

#### Context

Research `C4`, `C7`, `C9`-`C12`, `C14` and Critique `PC-001`, `PC-002`, `PC-004` established the exact projection shapes:
* Staff views (`Store.detail` -> `projection.redact_staff_detail`): nested `d["home"]["address"]` and `d["home"]["postcode"]`, `d["id"]`, `d["stage"]`, `d["measures"]`, `d["closed"]` (bool), `d["resident"]["adjustment"]` (literal for `projection.DEFAULT_REASON_ROLES` else `projection.REDACTED`), `d["handoff"]` (`state`, `confirmed_receiver=None` until accepted, `chase_owner`), `d["work"]` (`owner`, `reason`, `next_action` using `taskqueues.HELD` when free-text handoff/return actions are redacted for non-reason roles, `blockers`, `handoff` with `state` and `confirmed_receiver="Unknown"` until accepted), `d["quality"]`, and `d["quality_handover_blockers"]`.
* Contractor views (`projection.contractor_summary`, `projection.contractor_detail`, `Store.list_work_orders`, and staff-mediated `Store.work_order_job_pack` / `job_pack.build_job_pack`): nested `d["home"]["address"]` and `d["home"]["postcode"]`, `d["status"] == ("Completed" if closed else stage)`, `d["needs_notice"]` (bool), `d["named_contact"]`, `order["state"]` (`"Completed"` etc.), comma-joined or list `order["measures"]`, `job_pack.ACCESS_NOTICE` / `job_pack.ACCESS_NONE`, and `job_pack.ACKNOWLEDGED` (`"Receipt acknowledged - not accepted"`).
* Resident portal view (`resident_preview.resident_view(store, grant)`): nested `view["home"] = {"address", "town", "postcode"}`, `view["measures"]`, `(view["progress"], view["next_step"]) == resident_preview.STAGE_TEXT[stage]`, `"closed": "This case is recorded as closed."` iff `closed` is True (absent otherwise), `view["read_only"] is True`, `view["banner"] == resident_preview.BANNER`, and `"Consent and decisions"` in `view["unavailable"]`.
* Existing five-element contract: `ELEMENTS = ("entry", "evidence", "safe_endpoint", "recovery", "handoff")`, `validate(walkthrough)`, and `gaps(root: Path)`.

#### Intent

Preserve `ELEMENTS`, `validate(walkthrough)`, and `gaps(root)` unchanged and implement four composable finding functions plus `project_same_home_bundle` and `validate_same_home_walk`:

1. `check_shared_facts(case_id, staff_views, resident_view=None, contractor_view=None, contractor_orders=(), job_pack=None, sibling_ids=(), sibling_markers=()) -> list[str]`:
   * Requires all six `SIX_STAFF_PROFILES` to be present and agree on `id == case_id`, nested non-empty `home["address"]` and `home["postcode"]`, `stage`, normalized `measures` tuple, and `closed` bool.
   * Requires `resident_view` (when supplied) to carry matching `view["home"]["address"]`, `view["home"]["postcode"]`, normalized `view["measures"]`, `(view["progress"], view["next_step"]) == resident_preview.STAGE_TEXT[stage]`, and `view.get("closed") == "This case is recorded as closed."` iff `closed` is True else `"closed" not in view`.
   * Requires `contractor_view`, `contractor_orders`, and `job_pack` (when supplied) to carry `id`/`case_id == case_id`, matching `address` and `postcode` (`contractor_view["home"]`, `order["address"]`/`postcode` or `home`, `job_pack["home"]`), `contractor_view["status"] == ("Completed" if closed else stage)`, and measures subset/equality consistent with planned measures.
   * Scans serialized staff, resident, and contractor single-home views to ensure no `sibling_ids` or `sibling_markers` leak into the home's projected records.
2. `check_vulnerability_redaction(staff_views, contractor_views=(), resident_view=None, *, vulnerability_reason=None, private_markers=()) -> list[str]`:
   * When `vulnerability_reason` is non-empty: `REASON_STAFF_PROFILES` (`projection.DEFAULT_REASON_ROLES`) retain `resident["adjustment"] == vulnerability_reason`; `REDACTED_STAFF_PROFILES` (`Retrofit Coordinator`, `Quality Inspector`, `Grants and Evidence Officer`) and optional `Programme Support Officer` show `resident["adjustment"] == projection.REDACTED` (`"Extra support noted"`) and contain zero substring matches of `vulnerability_reason` or `private_markers`.
   * Contractor payloads (`contractor_summary`, `contractor_detail`, `work_orders`, `job_pack`) never contain keys `resident`, `contacts`, `hazards`, `safety_clocks`, `funding`, `finance`, `grants`, or `documents`, never contain `projection.REDACTED` (`"Extra support noted"`), `vulnerability_reason`, or `private_markers`, and when `vulnerability_reason` is active expose `needs_notice is True` (on summary/detail) or `job_pack.ACCESS_NOTICE` (on job pack) plus non-empty `named_contact`.
   * `resident_view` (when supplied) never contains `"Extra support noted"`, `"priority_support"`, `"Safeguarding"`, or staff-only `private_markers`.
3. `check_handover_dependencies(staff_views, *, work_orders=(), job_pack_receipt=None, audit_trace=None) -> list[str]`:
   * Inspects canonical staff home detail across `SIX_STAFF_PROFILES`:
     * No quality record in `d["quality"]` may be in `"Handed over"` state while an unreleased hazard (`any(not h.get("released") for h in hazards)`), unresolved stock query, unaccepted resident decision (`resident_decision != "Accepted"`), non-empty `quality_handover_blockers`, blank `accepted_by`, or self-acceptance (`accepted_by == submitted_by`) exists.
     * Unaccepted quality states (`"Submitted"`, `"Returned"`, `"Fixed, awaiting reinspection"`) or self-accepted `"Accepted"` (`accepted_by == submitted_by`) are reported if combined with `"Handed over"` or treated as handed over, even when `quality_handover_blockers == []` at `"Quality check"`.
     * Contractor `work_orders` with `state == "Completed"` or `job_pack_receipt` with `status == job_pack.ACKNOWLEDGED` (`accepted is False`) never establish quality `"Accepted"` or `"Handed over"` without independent quality `accepted_by != submitted_by`.
     * When `audit_trace` (`journey_trace`) is supplied: `order_findings` must be `[]`, `financial_closure` must be `"Not recorded"` when `handover == "Not recorded"`, and `user_validation` must equal `"not-established"`.
4. `check_next_action_continuity(transitions) -> list[str]`:
   * Accepts one or more ordered same-home transition snapshots (`{"staff_views": ..., "resident_view": ...}`).
   * At each transition: every staff profile in `SIX_STAFF_PROFILES` shares identical non-empty `work["owner"]`; `REASON_STAFF_PROFILES` share identical non-empty plain-language `work["next_action"]`; `REDACTED_STAFF_PROFILES` carry either that identical system-generated `work["next_action"]` or `taskqueues.HELD` (`"Held for roles with a recorded need"`) when free-text handoff/return next actions are held; and zero `work["next_action"]`, `work["reason"]`, or `work["blockers"][*]["next_action"]` strings match `BANNED_INTERNAL_TERMS` (`gate`, `gates`, `hold`, `holds`, `provenance`, `trace`, `traces`, `snapshot`, `snapshots`, `envelope`, `envelopes`).
   * Pending handoffs (`state` in `{"Offered", "Received", "Escalated"}`) keep `d["handoff"]["confirmed_receiver"] is None` and `work["handoff"]["confirmed_receiver"] == "Unknown"` with non-empty `chase_owner`; accepted handoffs (`state` in `{"Accepted", "Completed"}`) set `confirmed_receiver` to the proposed receiver.
   * When `resident_view` is present: `(resident_view["progress"], resident_view["next_step"]) == resident_preview.STAGE_TEXT[stage]`, `resident_view["next_step"]` matches zero `BANNED_INTERNAL_TERMS`, `resident_view["read_only"] is True`, `resident_view["banner"] == resident_preview.BANNER`, and `"Consent and decisions"` is in `resident_view["unavailable"]`.

#### Boundaries

* Included: Pure functions and `project_same_home_bundle` helper in `profile_journey_contract.py`.
* Excluded: Mutating `Store` state inside validators.

#### Likely Targets

* `src/core/src/zava_forward/core/profile_journey_contract.py`: Core contract module.

#### Dependencies

* Existing `projection`, `job_pack`, `taskqueues`, `resident_preview`, and `journey_trace` modules in `zava_forward.core`.

#### Validation Expectations

* `mypy` and `src/core` unit tests pass.

#### Completion Evidence

* Positive and negative unit tests in `test_profile_journey_contract.py` exercise every branch.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Specialist Screen Continuity and Connected Journey Acceptance Tests

### Context

Research `C13` found that `section.screen-evidence` (`Selected home ${c.id}`) in `role-screens.js` omits `Current owner` and `Next action` when a staff profile navigates across specialist screens on the same home. Critique `PC-005` established that `src/api/tests/test_same_home_profile_journey_acceptance.py` must exist on disk before `docs/reference/research/ux/profile-journey-contract.md` references it under `ControlClaimsMapToTests`.

### Intent

Complete selected-home plain-language next-action continuity in `role-screens.js` under AMA Web Development Guidance, strengthen `src/core/tests/test_profile_journey_contract.py`, and create `src/api/tests/test_same_home_profile_journey_acceptance.py`.

### Boundaries

* Included: `src/api/src/zava_forward/api/web/role-screens.js`, `src/core/tests/test_profile_journey_contract.py`, `src/api/tests/test_same_home_profile_journey_acceptance.py`.
* Excluded: Visual redesign, CSS changes, timer changes, new `.screen-record` panels, or `@unittest.skip` decorators.

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`
* `src/core/tests/test_profile_journey_contract.py`
* `src/api/tests/test_same_home_profile_journey_acceptance.py`

### Dependencies

* P01; loading `redesign-existing-projects` and `web-design-guidelines` + fetching canonical web-interface-guidelines source before editing `role-screens.js`.

### Validation Expectations

* `test_profile_journey_contract.py`, `test_same_home_profile_journey_acceptance.py`, `test_content_standard.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_role_screens_connected_journey.py`, `test_role_screens_same_home_identity.py`, `test_role_screens_stage_map_focus.py`, and `test_connected_home_check.py` pass.

### Completion Evidence

* `role-screens.js` reviewed against fetched `web-design-guidelines` rules with `file:line` findings; core and API acceptance tests pass.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Load web design skills and add selected-home plain-language next-action continuity in `role-screens.js`

#### Context

AMA Web Development Guidance requires loading `redesign-existing-projects` and `web-design-guidelines` and fetching the `web-design-guidelines` canonical rules before editing web files. `test_content_standard.py` (`C16`, `PC-003`) bans `gate`, `hold`, `provenance`, `trace`, `snapshot`, and `envelope` anywhere in `role-screens.js` (including comments), and `test_role_screens_conformance.py` (`C17`) guards classes, controls, and timers.

#### Intent

Load the required skills, fetch the current web-interface-guidelines source, and add inside `selected` (`section.screen-evidence`) right after `<p data-same-home="${c.id}">`:
`c.work?.next_action && h("p", { "data-same-home-next-action": c.id }, `Current owner: ${screenValue(c.work.owner)}. Next action: ${c.work.next_action}`),`
with zero `BANNED` words in code or comments, so staff specialist screens carry plain-language owner and next-action continuity (including `taskqueues.HELD` when free-text handoff actions are redacted for non-reason roles) across every same-home screen transition while contractor screens (where `c.work` is absent) and minimal mocks remain unaffected.

#### Boundaries

* Included: `src/api/src/zava_forward/api/web/role-screens.js` lines 145-153.
* Excluded: Any banned internal terms in code or comments; any CSS class not in `style.css`; any new `.screen-record` section.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`

#### Dependencies

* `redesign-existing-projects` and `web-design-guidelines` skill activation + `web_fetch` of canonical rules URL.

#### Validation Expectations

* All `role-screens.js` unit/conformance/copy test modules in `src/api/tests/` pass; `web-design-guidelines` review reports no violations.

#### Completion Evidence

* Node tests verify `data-same-home-next-action` across staff transitions and absence of internal staff `work` / vulnerability reason on `contractor-job-pack`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Strengthen `src/core/tests/test_profile_journey_contract.py` with multi-stage Store walkthrough and negative invariant tests

#### Context

`src/core/tests/test_profile_journey_contract.py` currently tests `ELEMENTS`, `validate`, and `gaps(root)` (`C19`, `PC-001`, `PC-002`, `PC-004`).

#### Intent

Keep all existing tests intact and add `ConnectedSameHomeContractTests`:
1. Drive a synthetic `Store` home (`ZF-1`) alongside a sibling home (`ZF-2` with distinct address, contractor, and markers) through:
   * Seeded resident vulnerability adjustment reason (`"Needs quiet knock and extra time at the door; sensory sensitivity"`) and private contact note.
   * Safeguarding hazard raised -> active stop verified -> independent restart recorded.
   * EPC stock conflict raised -> reconciled by independent staff actor.
   * Technical evidence, risk control, and independent design/coordination sign-offs recorded.
   * Resident measure scope and supplied `Accepted` decision recorded.
   * Cross-team handoff offered (`d["handoff"]["confirmed_receiver"] is None`, `work["handoff"]["confirmed_receiver"] == "Unknown"`, `taskqueues.HELD` on non-reason roles) -> accepted (`confirmed_receiver == receiver`).
   * Approved supplier onboarded, work order issued, staff-mediated job pack generated (`Store.work_order_job_pack`), contractor receipt acknowledged (`status == job_pack.ACKNOWLEDGED`, `accepted is False`), work order marked `state == "Completed"` (still not quality-accepted).
   * Quality submitted -> returned with defect -> remediation recorded -> independently reinspected and accepted (`accepted_by != submitted_by`) -> handed over with resident guidance.
   * Finance invoice matched, human disposition recorded, payment status updated, and case closed.
2. Capture `project_same_home_bundle` snapshots at each transition (including `resident_preview.resident_view(store, grant)`) and assert `validate_same_home_walk` passes with `ok is True`, `boundaries == {"human_approval": "not-established", "resident_approval": "not-established", "accessibility_walkthrough": "not-established"}`, `perspective_walkthroughs.check(root)["elements_met"] == 0`, and `journey_acceptance.check(root)["passed"] == []`.
3. Exercise negative mutations proving each checker fails deterministically on shared-fact mismatch/sibling leak, vulnerability redaction leak, handover dependency bypass (unreleased hazard, unaccepted/returned quality marked handed over, self-acceptance, work-order `Completed` / job-pack `ACKNOWLEDGED` treated as handed over, out-of-order `audit_trace`, fabricated `user_validation`), and next-action continuity violations (banned jargon, unconfirmed handoff receiver mismatch, resident `STAGE_TEXT` / `read_only` drift).

#### Boundaries

* Included: `src/core/tests/test_profile_journey_contract.py`.
* Excluded: Modifying `test_perspective_walkthroughs.py` or `test_journey_acceptance.py`.

#### Likely Targets

* `src/core/tests/test_profile_journey_contract.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `python3 -m unittest discover -s src/core/tests -p "test_profile_journey_contract.py" -v` passes.

#### Completion Evidence

* Unit test run output recorded in `.copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Create `src/api/tests/test_same_home_profile_journey_acceptance.py` for full-stack HTTP, `ResidentPreview` (`GET /resident/view`), and Node `role-screens.js` walkthrough verification

#### Context

`src/api` serves authenticated staff and contractor endpoints (`/api/cases/{id}`, `/api/workorders`, `/api/workorders/{id}/job-pack` in `STAFF_GET`, `/api/cases/{id}/home-case`), `ResidentPreview` (`resident_preview/app.py`) serves `GET /resident/view` over loopback `ThreadingHTTPServer` backed by disposable synthetic `grants.json` (`PC-001`), and `role-screens.js` renders specialist screens (`programme-queue`, `technical-queue`, `resident-choice`, `procurement-packages`, `quality-queue`, `finance-invoices`, `safety-lead`, `contractor-job-pack`) calling `workSummary` from `app.js` when `row.work` is populated (`PC-003`).

#### Intent

Create `src/api/tests/test_same_home_profile_journey_acceptance.py` with two test classes:
1. `SameHomeApiAndResidentPortalWalkTests`:
   * Configures a synthetic dataset (`ZF-1` + sibling `ZF-2` + vulnerability adjustment reason), instantiates the staff/contractor WSGI `App` AND a live loopback `ResidentPreview` server (`GET /resident/view` with `Host: 127.0.0.1:<port>` and disposable synthetic `grants.json`).
   * Authenticates as all 6 primary staff profiles, `Programme Support Officer`, assigned `Contractor`, and unassigned `Contractor`.
   * Walks `ZF-1` across transitions (pending handoff -> accepted handoff & work order & staff-fetched `/api/workorders/{id}/job-pack` -> quality acceptance, handover, and closure), verifying Contractor gets `403` on `/job-pack` and unassigned Contractor gets `403` on `/api/cases/ZF-1` and `0` work orders.
   * Passes live HTTP responses from all 6 staff profiles, assigned Contractor, staff-fetched job pack, and live `GET /resident/view` directly into `validate_same_home_walk(...)`, proving shared facts, sibling isolation, vulnerability redaction, handover dependencies, plain-language continuity, and `not-established` approval/AT boundaries.
2. `RoleScreensSameHomeWalkAndRedactionTests`:
   * Slices `workSummary` from `app.js` into Node `vm` and routes `api(...)` calls against live authenticated `App` responses for `ZF-1` and sibling `ZF-2` across `programme-queue`, `technical-queue`, `resident-choice`, `procurement-packages`, `quality-queue`, `finance-invoices`, `safety-lead`, and `contractor-job-pack`.
   * Verifies every staff screen renders `Same home: case ZF-1`, `data-same-home-next-action` with `Current owner` and plain-language `Next action` (`taskqueues.HELD` when free-text handoff action is held for redacted roles), and `Journey stages for ZF-1` carrying `case=ZF-1`.
   * Verifies `contractor-job-pack` renders `Needs notice`, `"The reason for any notice is not shared with contractors."`, `"Not shown for this role"`, omits `data-same-home-next-action` / internal staff `work`, and leaks zero occurrences of the raw vulnerability adjustment reason, `"Extra support noted"`, resident phone/email, or `ZF-2` sibling data.

#### Boundaries

* Included: `src/api/tests/test_same_home_profile_journey_acceptance.py`.
* Excluded: `@unittest.skip` decorators or Playwright browser daemon dependencies.

#### Likely Targets

* `src/api/tests/test_same_home_profile_journey_acceptance.py`

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* `PYTHONPATH=src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_same_home_profile_journey_acceptance.py" -v` passes.

#### Completion Evidence

* Full-stack HTTP + `ResidentPreview` + Node `role-screens.js` test run passes with `0` failures.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Canonical UX Profile Journey Contract Reference and Knowledge Base Index

### Context

With `test_same_home_profile_journey_acceptance.py` present on disk (`PC-005`), `docs/reference/research/ux/profile-journey-contract.md` can be published and verified immediately against `test_epic149_ux_journey_requirement_traceability.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`, and `test_live_doc_links.py` (`C20`, `C21`, `PC-004`).

### Intent

Publish `docs/reference/research/ux/profile-journey-contract.md` and update `docs/reference/README.md` and `docs/reference/log.md`.

### Boundaries

* Included: `docs/reference/research/ux/profile-journey-contract.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* Excluded: Rewriting prior `log.md` entries or editing `docs/case_study_48_original.md`.

### Likely Targets

* `docs/reference/research/ux/profile-journey-contract.md`
* `docs/reference/README.md`
* `docs/reference/log.md`

### Dependencies

* P01, P02 (including `test_same_home_profile_journey_acceptance.py` on disk).

### Validation Expectations

* `test_epic149_ux_journey_requirement_traceability.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`, and `test_live_doc_links.py` exit `0`.

### Completion Evidence

* Traceability and link suites pass with zero findings.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Author `docs/reference/research/ux/profile-journey-contract.md` and update `docs/reference/README.md` and `docs/reference/log.md`

#### Context

`test_epic149_ux_journey_requirement_traceability.py` resolves requirement IDs against `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/prds/proper-warm-retrofit-programme-demonstrator.md`, and `docs/brds/agentic-retrofit-programme-brd.md`, checks that every named `test_*.py` module exists and runs with zero skips, and rejects premature conformance claims (`PC-004`, `PC-005`).

#### Intent

Create `docs/reference/research/ux/profile-journey-contract.md` with YAML frontmatter (`title`, `description`, `ms.date: 2026-11-15`, `ms.topic: reference`), no H1, `*` unordered lists, plain ASCII punctuation, no em dashes, and no bolded-prefix list items, covering:
1. Five-element profile journey contract (`ELEMENTS = ("entry", "evidence", "safe_endpoint", "recovery", "handoff")`) across the 11 PRD perspectives (`AC-034`–`AC-043`, `FR-003`, `FR-004`, `FR-011`, `FR-012`, `FR-014`–`FR-017`, `FR-034`, `FR-035`, `FR-045`, `FR-048`, `FR-049`, `NFR-001`, `NFR-009`, `NFR-018`, `SA-001`–`SA-008`).
2. Connected same-home journey invariants across the six staff profiles (`Retrofit Programme Manager`, `Retrofit Coordinator`, `Resident Liaison Officer`, `Building Safety Liaison`, `Quality Inspector`, `Grants and Evidence Officer`), `Contractor` view, and resident portal (`shared facts`, `vulnerability redaction`, `handover dependencies`, `plain-language next-action continuity`).
3. Code-testable evidence mapping (`test_profile_journey_contract.py`, `test_same_home_profile_journey_acceptance.py`, `test_role_screens_connected_journey.py`, `test_role_screens_same_home_identity.py`, `test_perspective_walkthroughs.py`, `test_journey_acceptance.py`, `test_resident_preview.py`, `test_resident_preview_api.py`).
4. Explicit non-equivalence boundaries: automated checks leave `perspective_walkthroughs.check(root)["elements_met"] == 0` and `journey_acceptance.check(root)["passed"] == []` and do not establish live human approval, resident consent, user walkthrough sign-off (`#155`, `OD-38`), or assistive-technology acceptance (`#151`).
Update `docs/reference/README.md` and append a dated entry to `docs/reference/log.md`.

#### Boundaries

* Included: `docs/reference/research/ux/profile-journey-contract.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* Excluded: Rewriting earlier `log.md` entries.

#### Likely Targets

* `docs/reference/research/ux/profile-journey-contract.md`
* `docs/reference/README.md`
* `docs/reference/log.md`

#### Dependencies

* P02-T02 and P02-T03.

#### Validation Expectations

* `test_epic149_ux_journey_requirement_traceability.py` and `test_live_doc_links.py` exit `0`.

#### Completion Evidence

* Both traceability and link test suites pass with the new file indexed and logged.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Focused Validation, Guardrail Verification, and Review-Aligned Closeout

### Context

The caller specifies the Focused validation tier (`mypy`, `ruff check .`, `ruff format --check .`, targeted unit tests in `src/core` and `src/api`, plus `test_scenario_manifest.py` and `test_needs_inventory.py`), AMA Web Development Guidance review of changed web files, and a clean local commit with privacy-safe repository-local `user.email` and `Co-authored-by` trailer without pushing (`PC-005`, `PC-006`).

### Intent

Verify zero type, lint, formatting, unit-test, traceability, link, content-standard, role-screen conformance, or manifest regressions, complete `rpi-review`, and create the final local commit preserving `6efbf1d` with a clean working tree.

### Boundaries

* Included: Local focused validation commands across `src/core`, `src/api`, and `docs/`, plus post-`rpi-review` local Git commit.
* Excluded: `git push` or remote PR mutation.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md`

### Dependencies

* P01, P02, P03.

### Validation Expectations

* Every command exits `0`, and `git status --short` is empty after the post-`rpi-review` local commit.

### Completion Evidence

* Exact commands and exit codes captured in `.copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Execute focused validation suite and record verification outputs

#### Context

All code, web copy, UX reference documentation, and unit tests must pass repository static checks and targeted regression suites (`PC-005`, `PC-006`).

#### Intent

Run:
1. `mypy` across `src/core` and `src/api` (including modified/new modules and tests).
2. `ruff check .` and `ruff format --check .`.
3. `src/core` tests: `test_profile_journey_contract.py`, `test_perspective_walkthroughs.py`, `test_journey_acceptance.py`, `test_journey_trace.py`, `test_resident_preview.py`, `test_live_doc_links.py`.
4. `src/api` tests: `test_same_home_profile_journey_acceptance.py`, `test_resident_preview_api.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`, `test_content_standard.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_role_screens_connected_journey.py`, `test_role_screens_same_home_identity.py`, `test_role_screens_stage_map_focus.py`, `test_role_screens_tensions_same_home.py`, `test_connected_home_check.py`, `test_scenario_manifest.py`, `test_needs_inventory.py`.
5. Refresh and verify `role-screens.js` against `web-design-guidelines`.
6. After `rpi-review` persists `.copilot-tracking/reviews/2026-11-15/issue-134-same-home-walk-0018-review.md` and finalizes session state, configure repository-local `user.email` as `{id}+{login}@users.noreply.github.com` from `gh api user` and create a single clean local commit (`Refs #134`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`) on `feat/ux-134-same-home-walk-0018` preserving commit `6efbf1d` without pushing.

#### Boundaries

* Included: Focused tier checks and post-review local commit.
* Excluded: `git push`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-134-same-home-walk-0018-changes.md`

#### Dependencies

* P01, P02, P03.

#### Validation Expectations

* `0` errors / `0` test failures.

#### Completion Evidence

* Recorded command transcript summary in the changes artifact.

#### Unresolved Items

* None.
