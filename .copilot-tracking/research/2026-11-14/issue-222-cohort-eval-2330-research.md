---
description: "Primary research artifact for Issue #222 pre-live owner-approval boundary (OQ-018) and synthetic non-fairness disclaimer"
---
<!-- markdownlint-disable-file -->

# Task Research: issue-222-cohort-eval-2330

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-14                                                               |
| Researcher / agent | RPI Agent (`rpi-research`)                                               |
| Status             | Complete                                                                 |
| Artifact path      | .copilot-tracking/research/2026-11-14/issue-222-cohort-eval-2330-research.md |

## Research Brief

* What to research: Existing cohort and missing-data evaluation record implementation (`src/core/src/zava_forward/core/cohort_eval.py`, related RAI/prioritisation evaluation modules, and `src/api/src/zava_forward/api/server.py`) and how pre-live owner approval (`OQ-018`) and synthetic non-fairness disclaimers (`owner_approval_status`, `lawful_analysis_fields_approved`, `synthetic_not_fairness_evidence`) are enforced across runtime/API payloads and evaluation exports.
* Why it matters: Issue #222 requires cohorts, lawful analysis fields, and thresholds to be owner approved before live use (`OQ-018`) and synthetic results to be explicitly blocked from serving as fairness evidence or activating live prioritisation without dated human owner approval.
* Audience or intended use: Engineering implementation (`rpi-plan`, `rpi-implement`, `rpi-review`) and human reviewer verification.
* Scope: `src/core`, `src/agents` (if coupled), `src/api`, and existing evaluation documentation/tests.
* Non-goals: Fabricating owner approval for `OQ-018`, introducing live production demographic data, pushing to remote, or running unfocused full-gate checks outside the Focused tier.
* Criteria: Verify all six Issue #222 acceptance criteria invariants and identify exact schema/API gaps for `owner_approval_status`, `lawful_analysis_fields_approved: bool`, and `synthetic_not_fairness_evidence: True` + non-fairness provenance notice.
* Requested outputs: Convergence recommendation with exact code locations, contracts, and test targets.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                  |
|--------------------------------------|--------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How do `cohort_eval.py`, related evaluation modules, and `server.py` expose and enforce `OQ-018` owner approval (`owner_approval_status`, `lawful_analysis_fields_approved`) and `synthetic_not_fairness_evidence`, and how are all Issue #222 invariants verified? |
| Codebase scope                       | `src/core/`, `src/api/`, `src/agents/`, `docs/reference/research/evaluation/`                          |
| External scope                       | none                                                                                                   |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/cohort_eval.py`, `src/api/src/zava_forward/api/server.py`, `src/core/tests/test_cohort_eval.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`, `docs/reference/research/evaluation/cohort-evaluation-review-pack.md` |
| Initial external candidate areas     | none                                                                                                   |
| Research posture                     | focused                                                                                                |
| Posture provenance                   | caller-specified (bounded internal task with named source targets and Focused tier)                    |
| Explicit limits / deadline           | Focused validation tier; local commit only (no push)                                                   |
| Posture-specific completion basis    | focused scope and materiality                                                                          |
| Edits allowed during research?       | no, research-only                                                                                      |
| Resolved evidence root               | `.copilot-tracking/`                                                                                   |
| Known constraints / excluded sources | Do not claim OQ-018 is closed (`Refs #222`); synthetic runs remain non-fairness evidence.              |

## Extension Provenance and Participation

| Name | Kind | Status | Provenance / Scope |
|---|---|---|---|
| `.github/copilot-instructions.md` | Instruction | Selected | Repository rules, Focused validation tier, legal/regulatory/RAI boundaries, branch/commit rules |
| `rpi-research` | Skill | Selected | Three-wave (`Wider`, `Deeper`, `Contrarian`) primary artifact protocol |
| `RPI Researcher` | Subagent | Skipped (inline fallback) | Bounded internal scope across 6 tightly coupled modules fit direct inline verification without subagent latency |

## Cycle 1 Execution

### Wave 1: Wider

* Mapped the end-to-end cohort and missing-data evaluation pipeline across `src/core`, `src/agents`, and `src/api`:
  * Core evaluator: `src/core/src/zava_forward/core/cohort_eval.py` (`RECORD_VERSION = "cohort-missing-data-evaluation-v1"`) computes paired cohort denominators, errors, exclusions, review burden, Wilson 95% intervals, seeded-defect reconciliation, threshold blockers, and live-approval guards (`C1`, `C2`, `C3`).
  * Supporting core primitives: `src/core/src/zava_forward/core/rai_release.py` provides canonical SHA-256 `digest`, `named`, and `named_human` (`C4`); `src/core/src/zava_forward/core/paired_equity.py` evaluates deterministic single-factor pairs (`C5`).
  * Offline cohort runners & AI harness: `src/agents/src/zava_forward/agents/cohort_ranking_eval.py` (`C6`) and `src/agents/src/zava_forward/agents/cohort_ai_eval.py` (`C7`) evaluate 48 paired constructed cases across four factor dimensions (`sensor_completeness`, `support_need`, `source_completeness`, `appointment_history`); `src/agents/src/zava_forward/agents/ai_eval.py` (`cohort_report()`, `C8`) embeds deterministic ranking cohort results into `run_eval()["cohorts"]`.
  * HTTP API & export surfaces: `src/api/src/zava_forward/api/server.py` serves `GET /api/ai/report` (`C9`), which embeds `evaluation.cohorts` from `ai_eval.run_eval()`, and `src/api/tests/test_role_endpoint_inventory.py` (`C10`) enforces complete role-matrix registration for every `/api/...` route in `server.py`.
  * Reference governance baseline: `docs/reference/research/evaluation/cohort-evaluation-review-pack.md` (`C11`) and `src/agents/evals/cohort_manifest_draft.json` (`C12`) confirm `OQ-018` remains open for owner approval of cohorts, lawful analysis fields, and thresholds, and that synthetic exercises are never fairness evidence.

### Wave 2: Deeper

* Inspected `cohort_eval.evaluate(...)` (`src/core/src/zava_forward/core/cohort_eval.py:165-336`, `C3`) against every Issue #222 invariant and new requirement:
  * **Already implemented and tested invariants** (`src/core/tests/test_cohort_eval.py:14-247`, `C13`; `src/agents/tests/test_cohort_ranking_eval.py:32-270`, `C14`; `src/agents/tests/test_cohort_ai_eval.py:25-115`, `C15`):
    1. Paired constructed cohorts across sensor completeness, source completeness, accessibility/contact (`support_need`), and appointment history are evaluated against expected-outcome manifests.
    2. Seeded unjustified exclusion and deprioritisation defects are detected (`expected_defect_missed`, `unjustified_exclusion`, `unjustified_deprioritisation`).
    3. Per-cohort counts (`n`, `missing`, `excluded`), errors, review burden, and Wilson 95% uncertainty intervals reconcile (`sum(n + missing) == total_cases`, `0 <= low <= rate <= high <= 1`).
    4. Small (`0 < n < min_sample`) or empty (`n == 0`) cohorts remain `sufficient: False` with `insufficient_sample` blockers.
    5. Threshold breaches (`error_threshold_exceeded`, `exclusion_threshold_exceeded`, `review_burden_threshold_exceeded`, `subgroup_error_gap_exceeded`) block activation pending named human disposition and are never averaged across subgroups.
  * **Gaps identified for Requirement 2 (`OQ-018` pre-live owner-approval boundary & non-fairness provenance)**:
    1. `cohort_eval.evaluate(...)` (`C3`) does not expose `owner_approval_status`, `lawful_analysis_fields_approved: bool`, `lawful_analysis_fields`, `live_activation_allowed: bool`, `synthetic_not_fairness_evidence: True`, or `non_fairness_provenance_notice`.
    2. `cohort_eval._live_gaps(...)` (`src/core/src/zava_forward/core/cohort_eval.py:92-107`, `C2`) requires `expires` > `now` and `named_human(...)`, but does not accept/validate explicit ISO approval dates (`approved_at` / `approved_on`) when `expires` is absent or reject malformed `approved_at` strings, and `cohort_eval.py` provides no canonical `export_record(...)` helper enforcing these non-fairness and pre-live owner-approval invariants on exported records.
    3. `ai_eval.cohort_report()` (`src/agents/src/zava_forward/agents/ai_eval.py:601-612`, `C8`) strips approval/provenance metadata down to a minimal summary without `owner_approval_status`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`, or the offline AI priority cohort record (`cohort_ai_eval.run("faithful")`).
    4. `GET /api/ai/report` (`src/api/src/zava_forward/api/server.py:902-932`, `C9`) exposes `evaluation.cohorts` without a top-level `cohort_evaluation` export envelope or dedicated manager-only export endpoint (`GET /api/ai/cohort-evaluation`) carrying full `cohort_eval.export_record(...)` payloads for deterministic ranking and AI priority tasks.

### Wave 3: Contrarian

* Challenged proposed approval-status and fairness rules against existing regression tests and bypass vectors:
  1. **Fictional owner token bypass**: `rai_release.NON_HUMAN_TOKENS` (`src/core/src/zava_forward/core/rai_release.py:13-25`, `C4`) blocks `"agent"`, `"system"`, `"bot"`, `"ai"`, etc., but does **not** include `"fictional"`, `"placeholder"`, `"mock"`, or `"synthetic"`. Thus `"Data lead (fictional)"` from `cohort_eval_fixture.py` (`C16`) would pass `named_human(...)` if paired with a future `expires` timestamp! A dedicated `_named_real_human_owner(...)` check in `cohort_eval.py` must reject fictional/placeholder/mock/synthetic tokens in addition to `named_human(...)` so developer fixture strings can never establish dated human owner approval or pass `live=True`.
  2. **Backward-compatibility constraint on offline `fairness_evidence` and `HUMAN` fixture**:
     * `src/core/tests/test_cohort_eval.py:241-246` (`C13`) sets `m["synthetic"] = False` with `cohort_eval_fixture.approved(m)` (undated fictional fixture) in offline `evaluate(m, clean_observed(m))` (`live=False`) and asserts `fairness_evidence` is `True` when measured and `False` when unmeasured (`[]`). Meanwhile, `live=True` (`src/core/tests/test_rai_threshold_live_approval_guard.py:31-51`, `C17`) tests `HUMAN = {"cohorts_owner": "Priya Shah, Data Lead", "lawful_fields_owner": "Tom Reed, DPO", "thresholds_owner": "Amina Okafor, RAI Owner", "expires": NOW + 3600}` with `now=NOW` and expects `blockers == []` and `activation_allowed == True`.
     * Resolution: Keep offline `activation_allowed` and offline `fairness_evidence` backward-compatible with `C13` & `C17` while introducing explicit `owner_approval_status` (`"unapproved"` when no approval or unbound/invalid/expired approval is supplied; `"pending_owner_approval"` when an undated, fictional, or synthetic-manifest approval fixture is supplied; `"approved"` only when `not synthetic`, bound `manifest_digest`, valid thresholds, non-empty lawful analysis fields, real named human owners for all three roles, and a valid approval date via ISO/epoch `approved_at`/`approved_on` or verified unexpired `expires > now`), `lawful_analysis_fields_approved: bool` (`owner_approval_status == "approved"`), `live_activation_allowed: bool` (`False` unless `owner_approval_status == "approved"`, `lawful_analysis_fields_approved` is `True`, no `_live_gaps` exist, and no undispositioned blockers remain), `synthetic_not_fairness_evidence: True`, and `non_fairness_provenance_notice: str`. On `live=True`, enforce `owner_approval_status == "approved"` and `lawful_analysis_fields_approved == True` so fictional, undated, expired, or synthetic runs always fail closed with `activation_allowed == False` and `fairness_evidence == False` whenever `synthetic` is `True` or `live=True` fails owner approval.
  3. **Shared environment editable-install hazard**: Python's user site-packages in this shared VM points `zava_forward.*` to `/home/azureuser/source/ama/src/...` rather than this worktree. Validation commands must set explicit worktree-relative `PYTHONPATH` (`src:tests`, `../core/src:src:tests:../core/tests`, `../core/src:../agents/src:src:tests:../core/tests:../agents/tests`) without running global/user `pip install -e` that would mutate shared environment state.

## Evidence Log

| ID | Location | Finding |
|---|---|---|
| `C1` | `src/core/src/zava_forward/core/cohort_eval.py:16-33` | Defines `RECORD_VERSION = "cohort-missing-data-evaluation-v1"`, `OQ_018_GAP`, and `MEASUREMENT_BLOCKERS`. |
| `C2` | `src/core/src/zava_forward/core/cohort_eval.py:51-108` | `manifest_digest`, `approve`, `_thresholds_approved`, and `_live_gaps` check bound digests, threshold bounds, `named_human`, and `expires > now`, but do not expose `owner_approval_status` or reject fictional tokens or malformed `approved_at` dates. |
| `C3` | `src/core/src/zava_forward/core/cohort_eval.py:165-336` | `evaluate(...)` builds per-cohort counts, Wilson intervals, defects, and threshold blockers, returning `record_hash` over canonical JSON without `owner_approval_status`, `lawful_analysis_fields_approved`, `synthetic_not_fairness_evidence`, or `non_fairness_provenance_notice`. |
| `C4` | `src/core/src/zava_forward/core/rai_release.py:13-80` | `NON_HUMAN_TOKENS` blocks agent/system/bot tokens in `named_human(value)`, but omits `"fictional"`, `"placeholder"`, `"mock"`, and `"synthetic"`. |
| `C5` | `src/core/src/zava_forward/core/paired_equity.py:1-120` | Deterministic single-factor paired contrast evaluator; separate from versioned `cohort_eval` records. |
| `C6` | `src/agents/src/zava_forward/agents/cohort_ranking_eval.py:1-215` | 48-case paired ranking cohort runner across `sensor_completeness`, `support_need`, `source_completeness`, and `appointment_history`; intentionally omits approval so runtime runs stay blocked under `OQ-018`. |
| `C7` | `src/agents/src/zava_forward/agents/cohort_ai_eval.py:1-165` | 48-case paired AI priority cohort runner (`faithful`, `biased`, `unavailable`); verifies manual ranking invariance when AI is unavailable and detects all 3 seeded exclusions in `biased`. |
| `C8` | `src/agents/src/zava_forward/agents/ai_eval.py:601-612` | `cohort_report()` feeds `run_eval()["cohorts"]` and `GET /api/ai/report`, currently omitting `owner_approval_status`, `lawful_analysis_fields_approved`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`, and AI priority offline cohort evaluation details. |
| `C9` | `src/api/src/zava_forward/api/server.py:902-932` | Manager-only `GET /api/ai/report` returns `evaluation`, `live`, `registry`, and `consumption`. |
| `C10` | `src/api/tests/test_role_endpoint_inventory.py:15-80` | Asserts every `/api/...` route in `server.py` appears in `GET_ENDPOINTS` or `POST_ENDPOINTS` with verified role permissions. |
| `C11` | `docs/reference/research/evaluation/cohort-evaluation-review-pack.md:1-90` | Confirms `OQ-018` pre-live owner approval requirement for cohorts, lawful analysis fields, and thresholds, and non-fairness status of synthetic runs. |
| `C12` | `src/agents/evals/cohort_manifest_draft.json:1-40` | Confirms draft v0.2.0 status (`UNAPPROVED`, `is_synthetic: true`, `fairness_evidence: false`, `OQ-018` open). |
| `C13` | `src/core/tests/test_cohort_eval.py:14-247` | Exercises reconciliation, Wilson intervals, seeded defects, subgroup threshold blocking without averaging, digest binding, and line 246 offline non-synthetic `fairness_evidence` invariant. |
| `C14` | `src/agents/tests/test_cohort_ranking_eval.py:32-270` | Exercises 48-case paired deterministic ranking cohorts, `--defects` detection, negative-control rankers, and unapproved default blocking. |
| `C15` | `src/agents/tests/test_cohort_ai_eval.py:25-115` | Exercises `faithful`, `biased`, and `unavailable` AI priority cohort runs. |
| `C16` | `src/core/tests/cohort_eval_fixture.py:1-120` | Shared fixture using fictional undated owners (`"Data lead (fictional)"`, `"DPO (fictional)"`, `"RAI owner (fictional)"`). |
| `C17` | `src/core/tests/test_rai_threshold_live_approval_guard.py:18-90` | Exercises `live=True` guards with `HUMAN` (`expires: NOW + 3600`, `now=NOW`, `synthetic=False`). |

## Synthesis and Convergence Recommendation

### Accepted Recommendation

1. **Core evaluation record & export contract (`src/core/src/zava_forward/core/cohort_eval.py`)**:
   * Bind optional `lawful_analysis_fields` into `manifest_digest(manifest)` when present in `manifest`, and validate declared `lawful_analysis_fields` (defaulting to declared `dimensions` keys when omitted; blocking with `unapproved_lawful_analysis_fields` if explicitly empty or containing blank/non-string items).
   * Add dated real-human owner approval validation: require bound `manifest_digest`, valid thresholds, non-empty lawful analysis fields, real named human owners (rejecting `NON_HUMAN_TOKENS` plus `"fictional"`, `"placeholder"`, `"mock"`, `"synthetic"`), and a valid approval date (`approved_at` or `approved_on` as valid ISO-8601 date/datetime or finite positive epoch `<= now`, or verified unexpired finite `expires > now` when `now` is provided; plus unexpired `expires > now` whenever `expires` is present).
   * Expose on every `cohort_eval.evaluate(...)` record (included inside canonical `record_hash`):
     * `owner_approval_status`: `"approved"` only when `not synthetic` and dated real-human owner approval for cohorts, lawful analysis fields, and thresholds holds; `"pending_owner_approval"` when an approval mapping is present (such as undated/fictional fixtures or synthetic manifests) without live dated owner sign-off; `"unapproved"` by default when no approval mapping is present or when unbound, invalid, non-human, or expired.
     * `lawful_analysis_fields`: list of declared lawful analysis field/dimension names.
     * `lawful_analysis_fields_approved`: `bool` (`True` iff `owner_approval_status == "approved"`).
     * `live_activation_allowed`: `bool` (`True` iff `not synthetic`, `owner_approval_status == "approved"`, `lawful_analysis_fields_approved`, no `_live_gaps`, and either no blockers or human-dispositioned non-live-gap blockers).
     * `synthetic_not_fairness_evidence`: `True` (explicit policy & provenance invariant flag).
     * `non_fairness_provenance_notice`: explicit human-readable notice citing `OQ-018` that synthetic or owner-unapproved cohort runs are offline engineering checks only, are not fairness evidence or live fairness clearance, and cannot activate live prioritisation without dated owner approval of cohorts, lawful analysis fields, and thresholds.
   * Enforce on `live=True`: emit live-gap blockers (`constructed_thresholds_live`, `live_approval_not_named_human`, `live_approval_undated`, `live_approval_expired`, `unapproved_lawful_analysis_fields`) whenever `owner_approval_status != "approved"` or `not lawful_analysis_fields_approved`, ensuring `activation_allowed` and `fairness_evidence` are `False`.
   * Add `cohort_eval.export_record(record)` to validate and package canonical evaluation exports fail-closed (verifying `record_hash` integrity and refusing tampered flags where `synthetic=True` or `owner_approval_status != "approved"` claims `fairness_evidence=True` or `live_activation_allowed=True`).
2. **Agents cohort report & CLI export propagation (`src/agents/src/zava_forward/agents/ai_eval.py`, `cohort_ranking_eval.py`, `cohort_ai_eval.py`)**:
   * Propagate `record_version`, `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`, `authority_gap`, and `ai_priority_cohort_evaluation` (summary from `cohort_ai_eval.run("faithful")`) in `ai_eval.cohort_report()`, preserving all existing keys required by `test_ai_eval.py`.
   * Route `cohort_ranking_eval` and `cohort_ai_eval` `--json` outputs through `cohort_eval.export_record(...)`.
3. **API runtime & export endpoints (`src/api/src/zava_forward/api/server.py`)**:
   * Include `"cohort_evaluation"` (containing `export_record` payloads for both deterministic `ranking` and `ai_priority` tasks plus top-level `owner_approval_status`, `lawful_analysis_fields_approved`, `synthetic_not_fairness_evidence: True`, `non_fairness_provenance_notice`, `live_activation_allowed: False`) in `GET /api/ai/report`, and expose manager-only `GET /api/ai/cohort-evaluation` (registered in `test_role_endpoint_inventory.py`) for direct evaluation export retrieval without triggering full AI evaluation scenarios.
4. **Tests & Documentation**:
   * Add focused unit and API tests in `src/core/tests/test_cohort_eval.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`, `src/agents/tests/test_ai_eval.py`, `src/api/tests/test_ai_tasks.py`, and `src/api/tests/test_role_endpoint_inventory.py`, and update `src/core/README.md`, `src/agents/README.md`, and `src/api/README.md`.

### Rejected Alternatives

* **Mutating offline `activation_allowed` or offline `fairness_evidence` on undated fictional `cohort_eval_fixture.approved(m)`**: Rejected because `src/core/tests/test_cohort_eval.py:14-246` (`C13`) explicitly uses `approved(m)` to exercise offline disposition/measurement mechanics while `live=True` (`C17`) and `live_activation_allowed` + `owner_approval_status` + `lawful_analysis_fields_approved` cleanly enforce the pre-live `OQ-018` boundary without breaking existing offline mechanics tests.
* **Running `pip install -e` in the shared Python environment**: Rejected because user site-packages is shared across worktrees on this host; explicit worktree `PYTHONPATH` isolates validation safely.

## Decisions, Risks, and Readiness

* **Current decisions**: Converged on surgical schema/enforcement additions in `cohort_eval.py`, propagation in `ai_eval.py` and cohort runners, and export exposure in `server.py` (`GET /api/ai/report` and manager-only `GET /api/ai/cohort-evaluation`).
* **Unresolved decisions / open items**: `OQ-018` itself remains an open human owner governance decision by design (`Refs #222`, not `Closes #222`).
* **Further research needed**: None; Cycle 1 saturated all target modules and test invariants.
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`

