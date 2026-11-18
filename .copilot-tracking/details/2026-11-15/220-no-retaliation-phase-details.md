<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #220 Criterion 5 — No Retaliation, Inferred Refusal or Delayed Hazard Response

## Metadata

* Task ID: issue-220-no-retaliation-2026-11-15
* Task slug: 220-no-retaliation
* Related plan: .copilot-tracking/plans/2026-11-15/220-no-retaliation-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/220-no-retaliation-research.md (`C1`-`C18`), `src/core/src/zava_forward/core/challenges.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/assistants.py`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js`

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Upgrade Core Challenge Safeguards, Reopen, Representative Metadata, and Assurance Contract | Complete | P01, P01-T01, P01-T02 |
| P02 | Enforce Store-Backed Case Challenge, Reopen, Representative, AI-Task/Form, and Immediate Hazard Routing | Complete | P02, P02-T01, P02-T02, P02-T03 |
| P03 | Add Assistant Proposal Challenge Route, HTTP API Endpoint, and Plain-Language Workbench Support | Complete | P03, P03-T01, P03-T02 |
| P04 | Deliver Core & API Test Suites, Update Module READMEs, and Pass Focused Tier Validation | Complete | P04, P04-T01, P04-T02, P04-T03 |

<!-- rpi:phase id=P01 -->
## P01: Upgrade Core Challenge Safeguards, Reopen, Representative Metadata, and Assurance Contract

### Context

`src/core/src/zava_forward/core/challenges.py` defines `ChallengeRegister`, `FORBIDDEN_ADVERSE_FIELDS`, `SAFEGUARDS`, `reject_adverse_mapping`, and `assert_no_adverse_challenge_effects` (`C1`, `C3`, `C4`). Currently it lacks `reopen`, representative submission metadata, explicit `non_retaliation_assurance` / `hazard_clock_preserved` outputs, and complete runtime checks for `no_access`, `withdrawn`, `negative_engagement`, `work_orders`/`packages`/`handoff`/`resident_update`, Awaab's Law 24h/7d/14d deadlines, `safeguarding` clocks, `awaiting_hazard_action`, and controlled independent hazard append verification.

### Intent

Make `challenges.py` the single typed source of truth for non-retaliation, non-refusal, non-closure, and statutory/emergency clock invariants as well as the canonical `non_retaliation_assurance` / `hazard_clock_preserved` contract.

### Boundaries

* Included: `src/core/src/zava_forward/core/challenges.py`.
* Excluded: Mutating `SAFEGUARDS` keys/values in a way that breaks `test_issue_220_challenge_route.py` (`shown["safeguards"] == SAFEGUARDS`), or using forbidden content-standard phrases.

### Likely Targets

* `src/core/src/zava_forward/core/challenges.py`: Safeguard constants, `build_non_retaliation_assurance`, `assert_no_adverse_challenge_effects`, `ChallengeRegister.submit`, `update`, `reopen`, `escalate`, `resolve`, `confirm_hazard_handoff`, and `view`.

### Dependencies

* None.

### Validation Expectations

* `mypy` (`strict = true`), `ruff check`, `ruff format --check`, `test_challenges.py`, and `test_issue_220_challenge_route.py` pass in `src/core`.

### Completion Evidence

* `build_non_retaliation_assurance`, expanded `FORBIDDEN_ADVERSE_FIELDS`, upgraded `assert_no_adverse_challenge_effects`, and `ChallengeRegister.reopen` + representative metadata are implemented and type-clean.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Expand adverse-effect invariants and build canonical `non_retaliation_assurance` helper

#### Context

Research `C3`, `C4`, `C10`, and `C12` show that `FORBIDDEN_ADVERSE_FIELDS` must cover `no_access`, `non_access`, `withdrawn_flag`, `negative_engagement`, `engagement_penalty`, `safeguarding_delay`, `safeguarding_clock_paused`, and `awaabs_clock_delayed` (without banning legitimate challenge outcome string `"withdrawn"` when used as a value), and `assert_no_adverse_challenge_effects` must inspect every priority, engagement/refusal, task-closure, and statutory/emergency clock surface.

#### Intent

Provide a deterministic runtime verifier `assert_no_adverse_challenge_effects(before_case, after_case, *, allow_new_independent_hazard: bool = False)` and a canonical `build_non_retaliation_assurance(*, hazard_concern: bool = False, independent_hazard_routed: bool = False) -> Record`.

#### Boundaries

* Included:
  * `build_non_retaliation_assurance` returning machine-checkable booleans (`priority_preserved: True`, `ranking_score_lowered: False`, `refusal_inferred: False`, `no_access_inferred: False`, `sanction_applied: False`, `withdrawn_inferred: False`, `negative_engagement_inferred: False`, `unrelated_work_items_closed: False`, `hazard_clock_preserved: True`, `awaabs_law_clocks_preserved: True`, `safeguarding_clocks_preserved: True`, `awaiting_hazard_action_preserved: True`, `hazard_concern_flagged: bool`, `independent_hazard_intake_routed: bool`, `waits_for_challenge_review: False`).
  * `assert_no_adverse_challenge_effects` verifying:
    1. `score` and `urgent` never lowered and `priority` unchanged;
    2. `reject_adverse_mapping` finds zero added/modified `FORBIDDEN_ADVERSE_FIELDS` anywhere outside legitimate challenge records;
    3. `closed`, `decision`, `measure_decisions`, and `resident` (including `consent`, `withdrawn`, `no_access`, `refusal`, `sanction`, `negative_engagement`, `opt_out`) are unchanged;
    4. Unrelated `tasks`, `returns`, `service_requests`, `work_orders`, `packages`, `handoff`, and `resident_update` are never closed, cancelled, withdrawn, or dropped (`allow_service_request_growth: bool = False` for `service_open` / `service_reopen` validation where existing items remain unclosed);
    5. `safeguarding` / `safeguarding_clocks` and `awaabs_law_clocks` are unchanged (never cleared, paused, or pushed later);
    6. Pre-existing `hazards[:len(before_hazards)] == before_hazards` (preserving every `aware_at`, `noticed`, `priority`, `released`, `hold`, `referred`, `repaired`, `response_due_at`, `investigation_due_at`, `summary_due_at`, `make_safe_due_at`, `resident_update_due_at`), `awaiting_hazard_action` count (`sum(1 for h in hazards if not h.get("released") and not h.get("referred"))`) never decreases, and when `allow_new_independent_hazard=False` no extra hazard entries appear, whereas when `allow_new_independent_hazard=True` any appended hazard entry has `released is False` and active hold (`hold.status == "Active"`).
* Excluded: Changing `SUBJECT_KINDS` or breaking existing `ChallengeSafeguardError` exception signatures.

#### Likely Targets

* `src/core/src/zava_forward/core/challenges.py`

#### Dependencies

* None.

#### Validation Expectations

* Existing tamper tests in `test_issue_220_challenge_route.py` and new tamper cases in `test_challenge_no_retaliation_220.py` raise `ChallengeSafeguardError`.

#### Completion Evidence

* `build_non_retaliation_assurance` and upgraded `assert_no_adverse_challenge_effects` pass `mypy --strict` and unit tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add `ChallengeRegister.reopen`, representative submission, and assurance fields on records and views

#### Context

`ChallengeRegister` (`C1`) currently blocks reopening a resolved challenge (`challenges.py:381-383`) and does not record representative/nominee submitters or `non_retaliation_assurance` / `hazard_clock_preserved`.

#### Intent

Add `ChallengeRegister.reopen(...)`, support `submitted_by` (`"resident"`, `"representative"`, `"nominee"`, `"third_party"`) + `representative_ref` on `submit`, `update`, and `reopen`, enrich `hazard_referral` with `independent_intake: True`, `waits_for_challenge_review: False`, and `hazard_clock_preserved: True` while preserving `received_on` across updates/reopens/escalations, and include `non_retaliation_assurance` + `hazard_clock_preserved: True` on all records and `.view(cid)`.

#### Boundaries

* Included: `ChallengeRegister.submit`, `update`, `reopen`, `review`, `escalate`, `resolve`, `confirm_hazard_handoff`, and `view` in `challenges.py`.
* Excluded: Reopening must never clear `self.stale` entries produced by an earlier `"corrected"` resolution until a separate human re-review occurs, and must preserve prior resolutions in `rec["previous_resolutions"]`.

#### Likely Targets

* `src/core/src/zava_forward/core/challenges.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `test_challenges.py` and `test_issue_220_challenge_route.py` pass unchanged; new `reopen` and representative tests in `test_challenge_no_retaliation_220.py` pass.

#### Completion Evidence

* `ChallengeRegister` supports full submit -> resolve -> reopen -> escalate -> resolve lifecycle with representative metadata, preserved hazard referrals, and `non_retaliation_assurance` / `hazard_clock_preserved`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Enforce Store-Backed Case Challenge, Reopen, Representative, AI-Task/Form, and Immediate Hazard Routing

### Context

`src/core/src/zava_forward/core/resident_decisions.py` implements store-backed challenge, nomination, representative-authority, and service-dispute actions shared by `Store` and `SqlStore` (`C2`, `C5`, `C6`, `C11`, `C14`, `C15`). It currently lacks `challenge_reopen`, `"Assisted visit"` / `"Trusted intermediary"` challenge channels, `submitted_by` / `representative_ref`, `hazard_concern` / `hazard_intake` immediate routing, `ai_task` and `form_review` challenge targets, runtime `assert_no_adverse_challenge_effects` enforcement, and `non_retaliation_assurance` / `hazard_clock_preserved`.

### Intent

Close all store-backed challenge and correction gaps in `resident_decisions.py` while keeping 100% backward compatibility with existing strict equality, schema-rejection, and SQL writer-fence tests.

### Boundaries

* Included: `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/ai_tasks.py`.
* Excluded: Running `ruff format` on ADR 0006-excluded legacy modules (`resident_decisions.py`, `sqlstore.py`, `mssqlstore.py`, `ai_tasks.py`), mutating `store.data["recommendations"]`, or changing `_res_nomination_record(hazard_concern=True)`'s intentional `ValueError` (`C14`).

### Likely Targets

* `src/core/src/zava_forward/core/resident_decisions.py`
* `src/core/src/zava_forward/core/sqlstore.py` (`PC-002`: `priority_correction` column & `_priority_correction_rows` matching `prior_correction_preserved`)
* `src/core/src/zava_forward/core/mssqlstore.py` (`PC-002`: `_priority_correction_rows` matching `prior_correction_preserved`)
* `src/core/src/zava_forward/core/ai_tasks.py` (`PC-003`: `review` rejecting `accept`/`edit` when `priority_challenge_state` reports `stale=True`)

### Dependencies

* P01.

### Validation Expectations

* `test_resident_decisions.py`, `test_issue_220_challenge_route.py`, `ruff check`, `ruff format --check`, and `mypy` pass in `src/core`.

### Completion Evidence

* `Store` and `SqlStore` enforce runtime non-retaliation/clock safeguards across all challenge, reopen, representative, AI-task/form, nomination, and service-dispute actions and emit `non_retaliation_assurance` / `hazard_clock_preserved`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add `challenge_reopen`, representative/nominee fields, and expanded non-digital channels

#### Context

Research `C2`, `C5`, and `C15` show `_res_challenge_*` validates exact field sets (`400` on unknown keys), `CHALLENGE_CHANNELS` omits `"Assisted visit"` and `"Trusted intermediary"`, and `challenge_reopen` is missing.

#### Intent

Expand `CHALLENGE_CHANNELS` to `("Digital", "Phone", "Letter", "In person", "Assisted visit", "Trusted intermediary")`, support optional `submitted_by` (`"The resident"`, `"Their representative"`, `"Nominee"`), `representative_ref` (required when `submitted_by != "The resident"`, capturing read-only `representative_authority_status` from `c.get("representative_authorities")` without inferring works consent or blocking safety/challenge intake), `hazard_concern` (`bool`), and `hazard_intake` (`dict`) on `challenge_open`, `challenge_update`, and new `challenge_reopen` (`RESIDENT_ACTIONS` + `FOLLOWUP_ACTIONS`), keeping unknown keys fail-closed (`ValueError`).

#### Boundaries

* Included: `_res_challenge_open`, `_res_challenge_update`, `_res_challenge_reopen`, `_res_challenge_escalate`, `_res_challenge_resolve`, `RESIDENT_ACTIONS`, `FOLLOWUP_ACTIONS`.
* Excluded: Accepting forged server-owned fields like `recorded_by`, `version`, or `status` (`C15`). When a challenge previously resolved with `"Correction recorded"` is reopened via `challenge_reopen`, move the prior resolution into `record["previous_resolutions"]` and record `prior_correction_preserved: True` so `priority_challenge_state` continues to keep dependent proposals marked stale until a fresh human review supersedes them!

#### Likely Targets

* `src/core/src/zava_forward/core/resident_decisions.py`

#### Dependencies

* P01.

#### Validation Expectations

* `test_resident_api.py:567` forged-field `400` tests continue to pass; reopen and representative flows work in both `Store` and `SqlStore`.

#### Completion Evidence

* `challenge_reopen` and representative/non-digital channels operate cleanly across JSON and SQLite stores.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Wire immediate independent hazard intake, runtime invariant guards, and audit/view assurance contract

#### Context

Research `C4`, `C9`, `C10`, `C11`, `C12`, and `C14` establish that standard challenges without `hazard_intake` must only mutate `c["affected_challenges"]` (`after.pop("affected_challenges"); after == before`), while `hazard_concern=True` must immediately record `hazard_referral` on the challenge record and, when `hazard_intake` (`{category, priority, source, aware_at, note?}`) is supplied, atomically append an active independent safety entry to `c["hazards"]` using the exact `raise_hazard` structure and `hazard.persist_event` audit contract without waiting for challenge review or altering any existing hazard clock.

#### Intent

Implement `_route_challenge_hazard(...)` (checking `getattr(getattr(self, "local", None), "resident_validation", None)` so detached `SqlStore` replay validation appends `h` in memory without re-emitting `hazard.persist_event`, resolving `PC-001`), update `priority_correction_lookup` plus `sqlstore.py` (`priority_correction` column projection and `_priority_correction_rows`) and `mssqlstore.py` (`_priority_correction_rows`) to include `prior_correction_preserved = true` (`PC-002`), wrap `_res_challenge_open`, `_res_challenge_update`, `_res_challenge_reopen`, `_res_challenge_escalate`, `_res_challenge_resolve`, `_res_nomination_record`, `_res_nomination_correct`, `_res_nomination_review`, `_res_service_open`, and `_res_service_reopen` in runtime `assert_no_adverse_challenge_effects` + `_ranking()` verification, store `non_retaliation_assurance` and `hazard_clock_preserved: True` on every `affected_challenges` record and `challenge_targets` entry, and include `non_retaliation_assurance=verified hazard_clock_preserved=true` in challenge audit detail strings.

#### Boundaries

* Included: `resident_decisions.py` challenge/nomination/service handlers and `followup_view`.
* Excluded: Projecting `challenge_non_retaliation` when `user is None` or `not projection.can_see_reason(user)` (because `test_resident_decisions.py:1920-1943` tests exact projection keys for unauthorized roles and `detail("ZF-1")` without user!). Specifically, expose `challenge_non_retaliation` inside each item of `challenge_targets` or on each `affected_challenges` record so `detail("ZF-1", cached)` and `detail("ZF-1")` keys remain 100% compatible with existing projection tests (`C11`)!
  * Note on `detail` top-level keys: Storing `non_retaliation_assurance` and `hazard_clock_preserved: True` on every `affected_challenges` record AND on every `challenge_targets` entry avoids adding unexpected top-level keys to `case` / `detail("ZF-1")` while exposing the contract directly in both stored records and `detail(cid, user)` views!

#### Likely Targets

* `src/core/src/zava_forward/core/resident_decisions.py`

#### Dependencies

* P01, P02-T01.

#### Validation Expectations

* `test_resident_decisions.py` (including lines `229`, `343`, `1615-1621`, `1894-1945`) and `test_issue_220_challenge_route.py` pass 100%.

#### Completion Evidence

* Runtime safeguard verification, immediate independent hazard intake, and audit/view `non_retaliation_assurance` / `hazard_clock_preserved` contract verified in `Store` and `SqlStore`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Extend `challenge_catalog` and staleness tracking to `ai_task` and `form_review` suggestions

#### Context

Closure Audit Batch 014 flagged wider assistant/form coverage (`C6`). Currently `challenge_catalog` and `_priority_record` ignore `kind == "ai_task"` recommendations (`ai_tasks.py:358`) and `c.get("forms", [])` extraction suggestions (`form_review.py:140-260`).

#### Intent

Allow `challenge_catalog`, `_priority_record`, `_dependency`, and `priority_challenge_state` to resolve:
1. Priority recommendations (`r.get("kind") != "ai_task"` with matching `case_id`),
2. Recorded `ai_task` recommendations (`r.get("kind") == "ai_task"` where `case_id in r.get("case_ids", [])`), and
3. Recorded `form_review` extraction records on `c.get("forms", [])` (proposal ID `f"form:{form['id']}"` or `form["id"]` when `proposal_kind="form_review"`),
computing deterministic `proposal_version`, `source_version`, `policy_version`, and `decision_version` without mutating `store.data["recommendations"]` or `c["forms"]`.

#### Boundaries

* Included: `challenge_catalog`, `_priority_record`, `_dependency`, and `priority_challenge_state` in `resident_decisions.py`.
* Excluded: Mutating stored `recommendations` or `forms` dictionaries on challenge open/resolve (`C11`).

#### Likely Targets

* `src/core/src/zava_forward/core/resident_decisions.py`
* `src/core/src/zava_forward/core/ai_tasks.py` (`PC-003`: guard `review` against accepting/editing `ai_task` proposals marked `stale` by `"Correction recorded"`)

#### Dependencies

* P02-T01, P02-T02.

#### Validation Expectations

* Existing priority suggestion catalog tests and new `ai_task` + `form_review` challenge/correction staleness tests pass in both `Store` and `SqlStore`.

#### Completion Evidence

* `ai_task` and `form_review` suggestions appear in `challenge_targets`, accept challenges/corrections/reopens across all channels, and reflect targeted `"Correction recorded"` staleness without altering priority, refusal, or hazard clocks.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Add Assistant Proposal Challenge Route, HTTP API Endpoint, and Plain-Language Workbench Support

### Context

SQLite `assistant_tasks` (`src/core/src/zava_forward/core/assistants.py`, `C7`) backs role-owned retrofit assistant proposals (`quality-evidence`, `retrofit-coordination`, `resident-communication`, etc.), exposed via `/api/assistants/proposals/...` in `src/api/src/zava_forward/api/server.py` (`C8`). Meanwhile `src/api/src/zava_forward/api/web/panels.js` (`C16`) renders `#affected-challenges` in the staff workbench (`web/role-screens.js` must not be modified).

### Intent

Provide full non-retaliatory challenge, update, reopen, escalation, resolution, and immediate independent hazard intake support on SQLite `Assistants` proposals and HTTP `/api/assistants/proposals/<tid>/challenge`, and update `web/panels.js` to support expanded non-digital channels, representative/nominee submission, safety-concern flag, challenge reopen, and plain-language assurance display.

### Boundaries

* Included: `src/core/src/zava_forward/core/assistants.py`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js`.
* Excluded: `src/api/src/zava_forward/api/web/role-screens.js` (strict non-modification rule), running `ruff format` on `assistants.py` or `server.py` (ADR 0006), or introducing any forbidden word in `web/panels.js` (`C17`).

### Likely Targets

* `src/core/src/zava_forward/core/assistants.py`
* `src/api/src/zava_forward/api/server.py`
* `src/api/src/zava_forward/api/web/panels.js`

### Dependencies

* P01, P02, and loading `web-design-guidelines` skill before editing `web/panels.js`.

### Validation Expectations

* `test_content_standard.py`, `test_resident_api.py`, `test_challenge_no_retaliation_220.py`, `test_challenge_no_retaliation_api_220.py`, `ruff check`, `ruff format --check`, and `mypy` pass across `src/core` and `src/api`.

### Completion Evidence

* Assistant proposals can be challenged, updated, escalated, resolved, and reopened via `Assistants.challenge` and `POST /api/assistants/proposals/<tid>/challenge` with verified non-retaliation and hazard-clock preservation, and `web/panels.js` passes all content-standard and guideline checks.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Implement `Assistants.challenge` and assurance projection in `assistants.py`

#### Context

`Assistants._view` (`assistants.py:1094-1146`) computes `stale`, `display_state`, `actionable`, `relied_on`, and `review_flag`, while `Assistants.review` (`assistants.py:2041-2109`) updates `assistant_tasks` with optimistic `revision` fencing and writes `assistant_events` (`C7`).

#### Intent

Add `Assistants.challenge(self, user, tid, body)`:
1. Authorizes staff user for the task's capability & `case_id` (`projection.can_see_reason(user)` required for challenge records) and validates `revision` (int matching `task["revision"]`, raising `ConflictError(tid)` on mismatch) and closed payload fields for sub-actions `open`, `update`, `reopen`, `escalate`, `resolve`.
2. Snapshots `before_case = deepcopy(self.store._case(task["case_id"]))` and `before_ranking = self.store._ranking()` before mutation.
3. Records the challenge lifecycle entry inside `stored["challenges"]` with `submitted_by`, `representative_ref`, `channel`, `target_kind` (`"proposal"`, `"source"`, `"policy"`), `owner`, `non_digital_route`, `next_update`, `hazard_referral` (when `hazard_concern=True`, `status="referred_on_receipt"`, `independent_intake=True`, `waits_for_challenge_review=False`), `non_retaliation_assurance`, and `hazard_clock_preserved: True`.
4. When `hazard_concern=True` and `hazard_intake` is supplied, routes immediate independent hazard intake onto the linked case via `self.store.raise_hazard(...)` without touching any existing hazard clock.
5. When resolved as `"Correction recorded"` (and kept across `reopen` via `prior_correction_preserved: True`), sets `stored["challenged_stale"] = dict(...)` so `_view` projects `body["stale"] = True`, `body["display_state"] = "stale"`, `body["actionable"] = False`, and `body["relied_on"] = False` until fresh human work/verification, while `"Explanation recorded"` leaves `stale` unchanged!
6. Runs `assert_no_adverse_challenge_effects(before_case, after_case, allow_new_independent_hazard=routed_hazard)` and verifies `self.store._ranking() == before_ranking`, strips transient `_view` keys (`non_retaliation_assurance`, `hazard_clock_preserved`, `review_flag`, etc.) before writing `stored` to `assistant_tasks.body` (`PC-004`), emits an `assistant_events` entry (`kind="challenge"`) and store audit event (`non_retaliation_assurance=verified hazard_clock_preserved=true`), and projects `non_retaliation_assurance` + `hazard_clock_preserved: True` in `_view` whenever `body.get("challenges")` is present while redacting free-text challenge notes (`WITHHELD_NOTE`) under `_withhold_sensors` (`PC-004`).

#### Boundaries

* Included: `src/core/src/zava_forward/core/assistants.py`.
* Excluded: Breaking existing `Assistants.detail` / `Assistants.review` keys when no challenges exist on a proposal, or leaking sensor-derived notes when monitoring consent is withheld.

#### Likely Targets

* `src/core/src/zava_forward/core/assistants.py`

#### Dependencies

* P01, P02.

#### Validation Expectations

* Existing assistant tests in `src/core/tests` and `src/api/tests` pass unchanged; new assistant challenge tests in `test_challenge_no_retaliation_220.py` and `test_challenge_no_retaliation_api_220.py` pass.

#### Completion Evidence

* `Assistants.challenge` and `_view` projection verified across SQLite `SqlStore`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Expose `/api/assistants/proposals/<tid>/challenge` in `server.py` and update `web/panels.js`

#### Context

`server.py:1145-1180` routes `/api/assistants/proposals/<tid>/review` with CSRF/role checks and ConflictError -> `409` / PermissionError -> `403` / ValueError -> `400` / KeyError -> `404` mapping (`C8`). `web/panels.js:430-575` renders `#affected-challenges`, exercised by `challenge_browser_check.py` (`C13`, `C16`) and scanned by `test_content_standard.py` (`C17`).

#### Intent

1. Load `web-design-guidelines` skill and fetch/apply its rules before editing `web/panels.js`.
2. In `server.py`, route `POST /api/assistants/proposals/<tid>/challenge` to `self.store.assistants.challenge(u, tid, body)` using the same auth, bounded-JSON, and HTTP status mapping as `/review`.
3. In `web/panels.js` (`renderChallengePanel`):
   * Allow optional inputs in `formFor` via a 4th tuple flag (`optional = true`) so `challenge_browser_check.py` (which fills the original 9 fields) continues to submit cleanly without touching new controls!
   * Expand channel options to `["", "Digital", "Phone", "Letter", "In person", "Assisted visit", "Trusted intermediary"]`.
   * Add `["submitted_by", "Submitted by", ["The resident", "Their representative", "Nominee"]]`, optional `["representative_ref", "Representative reference (if submitted for the resident)", null, true]`, and `["hazard_concern", "Safety concern mentioned in this request", ["No", "Yes - route urgent safety check separately now"]]` to `#challenge-open` (mapping `"Yes..."` to `hazard_concern: true` and omitting blank `representative_ref` when `submitted_by === "The resident"`).
   * Display plain-language non-retaliation & safety-clock confirmation on each recorded challenge (`Priority unchanged, no refusal or no-access recorded, and safety response times unchanged.` plus `Safety concern flagged for immediate separate safety action.` when `record.hazard_referral` is present).
   * When `record.resolution` is present on a recorded challenge, also render `formFor("challenge-reopen-" + record.id, "Reopen " + record.id + " with new supplied evidence", ...)` calling `action: "challenge_reopen"`!
   * Verify zero forbidden words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`, `human-approved`) appear anywhere in `web/panels.js`, and never edit `web/role-screens.js`.

#### Boundaries

* Included: `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js`.
* Excluded: `src/api/src/zava_forward/api/web/role-screens.js`.

#### Likely Targets

* `src/api/src/zava_forward/api/server.py`
* `src/api/src/zava_forward/api/web/panels.js`

#### Dependencies

* P03-T01 and `web-design-guidelines` skill activation.

#### Validation Expectations

* `test_content_standard.py`, `test_resident_api.py`, and `test_challenge_no_retaliation_api_220.py` pass; `web-design-guidelines` review of `web/panels.js` reports zero open violations.

#### Completion Evidence

* HTTP assistant challenge endpoint and updated `web/panels.js` verified.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Deliver Core & API Test Suites, Update Module READMEs, and Pass Focused Tier Validation

### Context

Prompt Objectives 3 & 4 and the Focused Tier validation rules require comprehensive core and API test suites in exact named files (`src/core/tests/test_challenge_no_retaliation_220.py` and `src/api/tests/test_challenge_no_retaliation_api_220.py`), directly related README updates, and clean `ruff`, `mypy`, and `unittest` runs via `pip`/`python3`.

### Intent

Author focused, high-signal tests proving every positive workflow and negative tamper/validation boundary across all entrypoints, update `src/core/README.md` and `src/api/README.md`, and run all Focused Tier checks to green.

### Boundaries

* Included: `src/core/tests/test_challenge_no_retaliation_220.py`, `src/api/tests/test_challenge_no_retaliation_api_220.py`, `src/core/README.md`, `src/api/README.md`.
* Excluded: Removing any existing tests (`removals = none`), adding more than the 2 planned test files (`max additions = 2`), using `uv`, or pushing to `origin`.

### Likely Targets

* `src/core/tests/test_challenge_no_retaliation_220.py`
* `src/api/tests/test_challenge_no_retaliation_api_220.py`
* `src/core/README.md`
* `src/api/README.md`

### Dependencies

* P01, P02, P03.

### Validation Expectations

* `ruff check`, `ruff format --check`, and `mypy` exit `0` in `src/core` and `src/api`.
* Focused and suite `unittest` runs exit `0` in `src/core` and `src/api` (including `test_content_standard.py`).

### Completion Evidence

* Recorded command exit codes and test counts in `.copilot-tracking/changes/2026-11-15/220-no-retaliation-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Create `src/core/tests/test_challenge_no_retaliation_220.py`

#### Context

Core test suite is type-checked under `mypy --strict` (`C18`) and must cover both JSON `Store` and SQLite `SqlStore` plus `ChallengeRegister` and `Assistants`.

#### Intent

Test:
1. `ChallengeRegister` submit/update/reopen/escalate/resolve across resident digital, staff non-digital, and representative/nominee channels, verifying preserved `"corrected"` staleness on reopen, receipt-dated `hazard_referral` (`received_on` never reset), and `non_retaliation_assurance` + `hazard_clock_preserved: True` on records and `.view()`.
2. `assert_no_adverse_challenge_effects` fail-closed `ChallengeSafeguardError` detection for every adverse mutation class: lowered `score`, cleared `urgent`, changed `priority`, injected `refusal` / `no_access` / `non_access` / `sanction` / `withdrawn_flag` / `negative_engagement`, mutated `resident` / `decision` / `measure_decisions`, closed `tasks` / `returns` / `service_requests` / `work_orders` / `packages` / `handoff` / `resident_update`, delayed/paused Awaab's Law 24h emergency or 7d/14d significant hazard clocks, reduced `awaiting_hazard_action`, and delayed/paused `safeguarding` clocks.
3. End-to-end JSON `Store` and SQLite `SqlStore` lifecycles (`challenge_open`, `challenge_update`, `challenge_reopen`, `challenge_escalate`, `challenge_resolve`, `nomination_record`/`nomination_correct`/`nomination_review`, `service_open`/`service_reopen`) across priority, `ai_task`, and `form_review` suggestions, resident/representative/nominee submitters, all 6 channels, active Awaab's Law 24h & 14d + safeguarding clocks, and immediate atomic `hazard_concern=True` + `hazard_intake` independent hazard routing + verified hash-chained audit trail.
4. SQLite `Assistants.challenge` (`open`, `update`, `reopen`, `escalate`, `resolve`) with immediate hazard routing, `"Correction recorded"` staleness (`actionable=False`, `stale=True`), sensor-consent withholding scrub, and `non_retaliation_assurance` / `hazard_clock_preserved: True`.

#### Boundaries

* Included: `src/core/tests/test_challenge_no_retaliation_220.py`.
* Excluded: Forbidden content-standard phrases anywhere in comments, docstrings, or test strings; all synthetic test strings prefixed with `SYN`.

#### Likely Targets

* `src/core/tests/test_challenge_no_retaliation_220.py`

#### Dependencies

* P01, P02, P03-T01.

#### Validation Expectations

* `python3 -m unittest tests/test_challenge_no_retaliation_220.py -v`, `ruff check`, `ruff format --check`, and `mypy` pass in `src/core`.

#### Completion Evidence

* Passing core test run and strict type-check output.

#### Unresolved Items

* None.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Create `src/api/tests/test_challenge_no_retaliation_api_220.py`

#### Context

API test suite runs against real HTTP `ThreadingHTTPServer` / handler dispatch (`test_resident_api.py` pattern) and is type-checked under `mypy --strict` (`C15`, `C18`).

#### Intent

Test over HTTP across `/api/cases/<cid>/resident`, `/api/cases/<cid>/followup`, `/api/assistants/proposals/<tid>/challenge`, `/api/cases/<cid>/hazard-raise`, `/api/cases/<cid>`, and `/api/audit`:
1. Digital, staff non-digital (`Phone`, `Letter`, `In person`, `Assisted visit`, `Trusted intermediary`), and representative/nominee challenge open -> update -> escalate -> resolve -> reopen flows against priority, `ai_task`, `form_review`, and SQLite assistant proposals.
2. Zero priority/ranking drop (`/api/cases` order and `score`/`urgent` unchanged), zero refusal/no-access/sanction/withdrawn/negative-engagement flags, zero unrelated task/service/handoff closures, and zero delay to active 24h Emergency / 7d / 14d Awaab's Law hazard clocks, `awaiting_hazard_action`, and safeguarding clocks.
3. Immediate independent hazard referral and atomic `hazard_intake` routing via HTTP challenge endpoints (`hazard_concern=True` + `hazard_intake`), confirming immediate active case hazard creation and `safety_emergency` / `safety_raised` audit entries without waiting for challenge review.
4. Machine-checkable `non_retaliation_assurance` and `hazard_clock_preserved: True` in HTTP responses, `GET /api/cases/<cid>`, `GET /api/assistants/proposals/<tid>`, and `GET /api/audit`, plus closed-schema `400` / `403` / `409` rejection tests and workbench `web/panels.js` static contract check.

#### Boundaries

* Included: `src/api/tests/test_challenge_no_retaliation_api_220.py`.
* Excluded: Modifying `web/role-screens.js` or using forbidden phrases.

#### Likely Targets

* `src/api/tests/test_challenge_no_retaliation_api_220.py`

#### Dependencies

* P01, P02, P03.

#### Validation Expectations

* `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests/test_challenge_no_retaliation_api_220.py tests/test_content_standard.py -v`, `ruff check`, `ruff format --check`, and `mypy` pass in `src/api`.

#### Completion Evidence

* Passing API integration test run and strict type-check output.

#### Unresolved Items

* None.

<!-- rpi:task id=P04-T03 -->
### P04-T03: Update `src/core/README.md` and `src/api/README.md` and execute Focused Tier validation

#### Context

AMA `<rules_for_code_changes>` requires updating directly related documentation and running the planned Focused Tier validation commands.

#### Intent

Update `src/core/README.md` and `src/api/README.md` with concise documentation of `challenge_reopen`, representative/nominee and AI/assistant/form challenge coverage, immediate independent hazard intake routing, and the `non_retaliation_assurance` / `hazard_clock_preserved` contract, then execute full Focused Tier validation across `src/core` and `src/api`.

#### Boundaries

* Included: `src/core/README.md`, `src/api/README.md`, validation runs.
* Excluded: Unrelated documentation or `.copilot-tracking/` references inside `src/` READMEs.

#### Likely Targets

* `src/core/README.md`
* `src/api/README.md`

#### Dependencies

* P04-T01, P04-T02.

#### Validation Expectations

* Editable installs verified via `pip` if needed; `ruff check`, `ruff format --check`, `mypy`, and full `unittest discover` suites pass in `src/core` and `src/api`; `git diff --name-only` confirms `src/api/src/zava_forward/api/web/role-screens.js` is unmodified.

#### Completion Evidence

* Clean command outputs captured in `.copilot-tracking/changes/2026-11-15/220-no-retaliation-changes.md`.

#### Unresolved Items

* None.
