<!-- markdownlint-disable-file -->
# Current-Source Assessment Table: issue #126 eleven residuals and eleven unassessed checks

## Status and Boundary

* Assessed 2026-11-17 by native RPI worker `rpi-126-residual-assessment` (model label asserted: claude-sonnet-5.5), local-only, read-only source assessment. It is an evidence candidate, not an approval, closure, acceptance, release, legal or privacy decision.
* Assessed source: commit `01baf8d3df86a28f754da8545d0e8f12012bf350`, tree `d10bd7a918779f770da471fd3c54d8a61e14883e`. This is the declared parent topic `feat/demo-164-chat-grounding-provenance-0900` head (PR #1641, open, not main). PR #1812 commit `755371d2cf09d4680b2b675d0152dbdecb905a89` is an ancestor of this commit and is not on main.
* Main `f1df574bba2b94cd83bb2a783079ec94cd584c90` is separate provenance and is neither this assessment's source nor an acceptance basis. Nothing here claims parent code is on main.
* Baseline distinction: the original report `docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md` (baseline `1cb398c7b90bec05a5700008a97d0cfac494144a`, owner acceptance 2026-10-15 for baseline and remediation planning only) is preserved unchanged. "Baseline" fields below quote it; "HEAD" fields are this assessment. DOWNGRADED means a verified residual, not closure; no row is treated as closed.
* Accountable roles are proposed (residuals, from the report remediation checklist) or inferred (unassessed rows, by this assessment from the report handoff). No person is named, no delegation is accepted and no approval is recorded by this table.
* Vocabulary (register `RAI_TIERS`): `implemented/source-tested`; observed (= `deployed-observed`); `proposed`; `insufficient`; independently accepted (= `independent-acceptance`). Observed and independently accepted are unavailable for all 22 rows: no external, deployed, human, witnessed or qualified-owner evidence exists in the repository.
* Tier rule: `implemented/source-tested` only where the engineering gap named in the baseline finding has a directly relevant executed and passed test at HEAD and the remaining open items are human, qualified or actual-environment gates; `proposed` where only a candidate or proposed control exists; otherwise `insufficient`. A narrow source-tested component is listed separately and does not raise the tier.

## Summary

| Tier at HEAD | Count | IDs |
| --- | --- | --- |
| implemented/source-tested (component, not closed) | 1 | GOVERN-AUDIT-02 |
| observed | 0 | none |
| proposed | 1 | MN-4.1 |
| insufficient | 20 | T-RAI-001, T-RAI-002, MEASURE-01, GOVERN-AUDIT-01, MAP-01, MAP-02, MAP-04, MN-3.2, MN-4.3, GOVERN-AUDIT-04, GOVERN-AUDIT-05, MAP-05, MEASURE-02, MEASURE-03, MEASURE-04, MN-2.3, T-RAI-005, EU-COND-01, EU-COND-02, EU-COND-04 |
| independently accepted | 0 | none |

Closed findings: 0 of 22. Qualified human, DPO/Legal, real-model, witnessed-restore and EU-applicability evidence is absent for every row.

## Commands Run (tests, executed once each)

Environment for both batches: run from `/tmp`, `env -i` with only PATH, HOME, TMPDIR and ZF_DATA under the evidence root `.../evidence-126-assess/run/`, `PYTHONDONTWRITEBYTECODE=1`, and `PYTHONPATH=<worktree>/src/{core,agents,api}/src:<worktree>/src/{core,agents,api}/tests`. Own-source import was proven first: `zava_forward.core.governance` and `zava_forward.agents.chat_eval` resolved to the worktree and `zava_forward.api` listed the worktree path first. Installed distributions `0.1.0` in site-packages are shadowed; nothing was installed. No `ZF_*MSSQL*` variable was set, so opt-in SQL Server tests skipped.

* Batch A (evidence id `A`): `python3 -m unittest -v test_governance test_rai_release_invalidation test_rai_threshold_live_approval_guard test_recovery test_paired_equity test_cohort_eval test_monitoring_coverage test_human_review_effectiveness_223 test_heldout_eval`. Result: exit 0, `Ran 251 tests in 6.996s`, `OK (skipped=18)`. Log SHA-256 `8fd8668b01bd4b624a26c464556d819b8a58ff3a81f772f869afcc9ba869e0cc` (`evidence-126-assess/run/batchA.log`).
* Batch B (evidence id `B`): `python3 -m unittest -v test_assistants test_assistant_release test_rai_harm_threshold_incident test_restart_audit test_chat_eval`. Result: exit 0, `Ran 270 tests in 89.068s`, `OK (skipped=67)`; the skipped tests are the opt-in SQL Server classes. Log SHA-256 `0235f289a27ca362c526de903685c07c200ca992d846f93de336536a7d7daee4` (`evidence-126-assess/run/batchB.log`).
* Test paths: `test_governance`, `test_rai_*`, `test_recovery`, `test_paired_equity`, `test_cohort_eval`, `test_monitoring_coverage`, `test_human_review_effectiveness_223`, `test_heldout_eval` are under `src/core/tests/`; `test_assistants`, `test_assistant_release`, `test_rai_harm_threshold_incident`, `test_restart_audit` under `src/api/tests/`; `test_chat_eval` under `src/agents/tests/`.
* Unperformed: `test_data_protection`, `test_ai_register_completeness`, `test_source_monitor`, `test_ledger_digest_blob`, `test_regulatory_privacy`, `test_challenges`, every opt-in SQL Server, browser, container, Azure, real-model, human-study and full-suite run (cap of two batches; boundary). Source-test claims below cite only tests that executed and passed in A or B; skipped or unrun tests support nothing.

## Version Evidence (applies to all rows unless a row says otherwise)

* Task id/version and release version: none recorded. No approved task or release version exists in source or repository records; the registry and evaluation versions below are related version evidence only and are not substituted for approvals.
* Related version evidence: `ai_registry.REGISTRY_VERSION = "2026-10-15.1"` (`core/ai_registry.py:17`); `rai_release.EVALUATION_VERSION = "task-release-evaluation-v1"` (`core/rai_release.py:12`); PRD `0.21.0` unsigned (`docs/prds/zava-forward-retrofit-programme-demonstrator.md`, ms.date 2026-10-25); distributions `0.1.0` (`src/*/version.py`).
* The register contract (`core/governance.py:147-167`) requires `source_commit`, `task_id`, `task_version`, `release_version` or an explicit nonapplicability reason; this table records equivalent context but writes nothing to the register.

## Residuals (11)

Paths: `core/` is `src/core/src/zava_forward/core/`, `agents/` is `src/agents/src/zava_forward/agents/`. Blob identities: see the Blob Index.

### T-RAI-001 Legacy input minimization differs

* Baseline: PARTIAL, MEDIUM, CONFIRMED (information disclosure residual). Role (proposed): Digital / task owners / DPO-Legal.
* HEAD code: `core/assistants.py:148` (`ROLE_WITHHELD_OUTPUT`), `core/assistants.py:286` (`projection.can_see_reason` role need), `core/export_fields.py:36` (`chat_case`), `core/export_fields.py:88` (`prompt_case`), `core/data_protection.py:1135` (`validate_task_payload`).
* HEAD tests (executed, passed, B): `test_assistants.ContractTests.test_exact_source_role_matrix_and_no_cross_audience_leaks`. `core/data_protection.py` tests unperformed.
* Version evidence: none recorded (task/release); no EU nexus claimed.
* Result: closed assistant projections and role-scoped sources are source-tested. Task-specific necessity of legacy shared facts and content-bearing uploads is not established by this evidence; `export_fields.py` constrains field shape, not semantics (project RAI review F07).
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: DPO/Legal necessity decision per task and field; run `test_data_protection` and legacy-path inventory when a further bounded batch is authorised.

### T-RAI-002 Resolution is not source/factual verification

* Baseline: PARTIAL, MEDIUM, CONFIRMED (tampering integrity residual). Role (proposed): Task owners / Assurance / Digital.
* HEAD code: `core/assistants.py:3680` (`review(... source_verified ...)`), `core/chat_panel.py:542` (`parse_reply` allowed ids).
* HEAD tests (executed, passed, B): `test_assistants.ReviewTests.test_verification_requires_explicit_true_and_same_reviewer`, `test_assistants.ReviewTests.test_material_only_staleness_accept_reject`, `test_assistants.HumanReviewMechanics.test_automation_bias_negative_control_false_attestation_is_not_semantic_truth`.
* Result: explicit same-reviewer verification and staleness gates are source-tested; the negative-control test itself shows a false attestation is not semantic truth, so the residual is unchanged.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: independently labelled critical-defect detection by real reviewers (human sessions) and actual-model evidence.

### MEASURE-01 Citation validity is not factual correctness

* Baseline: PARTIAL, MEDIUM, DOWNGRADED. Role (proposed): Task owners / Data and Performance / Assurance.
* HEAD code: `core/chat_panel.py:534` (`unsupported_claims`), `agents/chat_eval.py:403-420` (known-gap handling), `agents/chat_eval.py:610` (`unsupported_claim_withheld`).
* HEAD tests (executed, passed, B): `test_chat_eval.GoldenRunTests.test_unsupported_claim_with_a_valid_citation_is_withheld`.
* Result: the baseline draft-fixture gap (unsupported reason accepted) is now withheld by a deterministic token check for the named scripted scenario. This is not semantic entailment, not a held-out or actual-model result.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: authorised actual-model held-out evaluation bound to frozen versions (see MEASURE-02).

### GOVERN-AUDIT-01 Whole-system accountability incomplete

* Baseline: PARTIAL, LOW, DOWNGRADED. Role (proposed): Product owner / Digital.
* HEAD code: `core/ai_registry.py:5` (docstring: no accountable individual, delegation or approval recorded), `core/ai_registry.py:26-34` (`DEMO_ACTIVATION`: demo-only, DPO/Legal review outstanding), `core/ai_registry.py:51` (`AUTHORITY_STATES` all unknown), `core/rai_release.py:22` (`AUTHORITY_GAP`).
* HEAD tests: `test_ai_register_completeness` unperformed; related register behaviour `test_governance.EvidenceRegister.test_all_tiers_and_explicit_owner_unknown_are_claims` executed and passed (A) shows owner stays unknown.
* Result: registry and bounded activation exist; accountable individuals and signed policy ownership are not recorded. The `DEMO_ACTIVATION` demo-only owner string is a demonstrator scope decision recorded in source, not a recorded acceptance of this residual.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: personal owner/delegate acceptance recorded by those owners.

### GOVERN-AUDIT-02 Approved model-change binding unproved

* Baseline: PARTIAL, MEDIUM, DOWNGRADED. Role (proposed): Digital / Product owner.
* HEAD code: `core/assistant_release.py:85` (`invalidate_changed`), `core/assistant_release.py:102` (`invalidation_cause`), `core/rai_release.py:13` (`CHANGE_TRIGGERS`: intended_use, model, prompt, policy, data, evidence, permissions), `core/rai_release.py:12` (`EVALUATION_VERSION`).
* HEAD tests (executed, passed): `test_rai_release_invalidation.Invalidation.test_each_material_change_revokes_and_records_trigger` (A), `test_rai_release_invalidation.Invalidation.test_failed_audit_write_rolls_back_revocation_and_denies` (A), `test_assistant_release.TaskReleaseRecord.test_actual_prompt_change_invalidates_each_retained_route` (B).
* Version evidence: related only (`task-release-evaluation-v1`); no approved task/release version.
* Result: material model/prompt/policy/data/evidence/permission changes revoke the retained release and are audited at source-test level. A human approval of any change or release is not evidenced.
* Tier: implemented/source-tested (change-binding control only; human approval absent). Not closed; operational and qualified acceptance remain.
* Missing evidence and resume condition: named owner acceptance of release/change authority and a version-bound actual release record.

### MAP-01 Ranking impact evidence and ownership

* Baseline: PARTIAL, LOW, DOWNGRADED. Role (proposed): Asset / Data and Performance.
* HEAD code: `core/ranking.py:74-75` (`_support` is true only for "Yes", so "Unknown" sorts with "No"), `core/ranking.py:119-127` (`reasons` adds `support_unknown` human-review reason), `core/paired_equity.py:203` (`predeclared_cohorts`).
* HEAD tests (executed, passed, A): `test_paired_equity.PairedEquityTests.test_ai_task_paired_evaluation_and_transparent_non_ai_comparison`.
* Result: the source ordering behaviour behind the baseline residual is still present at HEAD (read, not exercised by a test in this batch). Constructed paired checks exist but are not ranking-owner sign-off.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: ranking-owner signed policy/version/hash and accepted impact of missing or unknown data.

### MAP-02 Staff processing and future live transition

* Baseline: PARTIAL, MEDIUM, DOWNGRADED. Role (proposed): Product owner / DPO-Legal / Record owners.
* HEAD code: `core/data_protection.py:52` (`synthetic_resident_does_not_exempt_actual_staff`), `core/data_protection.py:92-98` (staff identity data class), `core/data_protection.py:439` (`register_report`), `core/staff_intake.py:1`.
* HEAD tests: unperformed (`test_data_protection` not run in the two-batch cap).
* Result: the register states actual staff processing is not exempted by constructed residents; source documents it as reference-only, not DPO/Legal approval. No row of this assessment verified it by test.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: DPO/Legal decision on actual staff data now and future resident processing separately; execute `test_data_protection` in a later authorised bounded batch.

### MAP-04 Participation, competence and benefit unproved

* Baseline: PARTIAL, LOW, DOWNGRADED. Role (proposed): Resident Engagement / Assurance.
* HEAD code: `core/human_review_effectiveness.py:96` (`AuthorityPolicy`), `core/human_review_effectiveness.py:141` (`ReviewScenario`), `core/cohort_eval.py:1` (OQ-018 note).
* HEAD tests (executed, passed, A): `test_human_review_effectiveness_223.HumanReviewEffectiveness223Tests.test_competent_panel_detects_all_defects_retains_evidence_and_compares_effort`, `...test_live_mode_fails_closed_until_named_human_oq017_approval`.
* Result: the harness and fail-closed live gate are source-tested with constructed scenarios; no accessible direct participation, realistic competence or benefit measurement exists.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: human sessions (accessible resident/frontline participation) under a separate authorised protocol.

### MN-3.2 Lifecycle monitoring and release invalidation

* Baseline: PARTIAL, MEDIUM, DOWNGRADED. Role (proposed): Model-service owner / Product owner.
* HEAD code: `core/assistant_release.py:85-110`, `core/rai_release.py:13-20`, `core/ai_registry.py:17`.
* HEAD tests (executed, passed): `test_rai_release_invalidation.Invalidation.test_each_material_change_revokes_and_records_trigger` (A), `test_assistant_release.TaskReleaseRecord.test_actual_prompt_change_invalidates_each_retained_route` (B), `test_chat_eval.GoldenRunTests.test_changed_versions_require_renewed_threshold_evidence` (B).
* Result: release invalidation on changed versions is source-tested. Accepted retirement review is not evidenced.
* Tier: insufficient (invalidation present; retirement review acceptance absent). Not closed.
* Missing evidence and resume condition: named model-service owner retirement and model-change review record.

### MN-4.1 Owned AI harm monitoring unproved

* Baseline: PARTIAL, MEDIUM, DOWNGRADED. Role (proposed): Product owner / Digital.
* HEAD code: `core/monitoring_coverage.py:22-27` (INSTALLED/CANDIDATE/GAP and owner role labels), `core/monitoring_coverage.py:171` (`coverage_gaps`), `core/monitoring_coverage.py:203-206` (INSUFFICIENT/BLOCKED/WITHIN/BREACH), `core/rai_metrics.py:110` (`reconstruct`).
* HEAD tests (executed, passed): `test_monitoring_coverage.IndicatorTests.test_breach_requires_owned_incident` (A), `test_monitoring_coverage.DeclarationTests.test_bot_and_fictional_approvers_block_live_indicator_and_ai_limits` (A), `test_rai_harm_threshold_incident.HarmThresholdIncident.test_approved_threshold_breach_needs_a_named_incident_owner` (B).
* Result: monitoring register, never-green evaluator and constructed thresholds exist; thresholds, owners and windows are constructed or proposed roles, not approved.
* Tier: proposed. Not closed.
* Missing evidence and resume condition: owner-approved harm, disparity and review-burden thresholds and windows; installed alerts evidenced from the deployed environment (not performed here).

### MN-4.3 Incident communication and restart assurance

* Baseline: PARTIAL, MEDIUM, DOWNGRADED. Role (proposed): Digital / Incident and restart owners.
* HEAD code: `core/restart_authority.py:194` (`validate_restart_authority`), `core/restart_authority.py:319` (`ensure_distinct_restart_actor`), `core/rai_release.py:28` (`AUTHORITY_ROLES`).
* HEAD tests (executed, passed): `test_governance.JsonGov.test_breach_pauses_scope_until_authorised_restart` (A), `test_governance.JsonGov.test_breach_names_restart_authority_and_blocks_automatic_restart` (A), `test_monitoring_coverage.IndicatorTests.test_breach_requires_owned_incident` (A); the `SqlGov` counterparts ran on the local SQLite store only.
* Result: breach pause, named restart authority and automatic-restart refusal are source-tested. Accepted incident-wide suspension and restart exercise are not evidenced.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: appointed named incident and restart holders (`AUTHORITY_GAP`) and a witnessed restart exercise.

## Unassessed Checks (11)

The accountable roles in this section are inferred by this assessment and are not accepted delegations.

### GOVERN-AUDIT-04 Privacy and retention authority

* Baseline: NOT_ASSESSED. Role (inferred): DPO-Legal / Digital.
* HEAD code: `core/data_protection.py:1` (docstring: recorded references are not DPO or Legal approval; no retention schedule set), `core/data_protection.py:1342` (`RightsRequestLedger`), `core/recovery.py:53` (`erase_resident`).
* HEAD tests (executed, passed, A): `test_recovery.RecoveryTests.test_erasure_survives_restore_of_an_older_backup`. `test_data_protection`, `test_regulatory_privacy` unperformed.
* Result: local erasure and rights-ledger machinery exist; DPO/Legal authority, processor and transfer terms, retention periods and effective erasure/restore are unverified.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: DPO/Legal decision record; witnessed erasure/restore reconciliation.

### GOVERN-AUDIT-05 Operational acceptance differs from exercise authority

* Baseline: NOT_ASSESSED. Role (inferred): Named operational owners (Product owner / Digital).
* HEAD code: `core/rai_release.py:22-34` (`AUTHORITY_GAP`, `AUTHORITY_ROLES`), `core/rai_control_plane.py:214` (`validate_live_task_approval`), `core/ai_registry.py:51` (`AUTHORITY_STATES` unknown).
* HEAD tests (executed, passed): `test_rai_threshold_live_approval_guard.LiveReleaseApprover.test_blank_missing_or_system_approver_fails_live` (A), `test_human_review_effectiveness_223.HumanReviewEffectiveness223Tests.test_live_mode_fails_closed_until_named_human_oq017_approval` (A).
* Result: live activation needs named-human approval at source level; no version-specific operational acceptance or delegation is recorded.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: owners personally record version-specific acceptance and delegations.

### MAP-05 Legal scope and currentness

* Baseline: NOT_ASSESSED. Role (inferred): Legal / DPO.
* HEAD code: `core/lawstore.py:1` (versioned dated law store, "nothing here is legal advice"), `core/source_monitor.py:1` (offline discovery, never legal approval), `core/ai_registry.py:133` (`reliance_review` requirement); `docs/reference/regulatory/README.md` reviewed update 2026-11-01 (Legal and DPO decision record `Pending`).
* HEAD tests: unperformed (`test_source_monitor` not run).
* Result: dated local snapshots and drift detection exist as engineering aids; no current UK/EU legal refresh or Legal decision is recorded.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: dated Legal currentness review and official-source check recorded by Legal.

### MEASURE-02 Real-model quality and calibration

* Baseline: NOT_ASSESSED. Role (inferred): Task owners / Data and Performance / Assurance.
* HEAD code: `core/heldout_eval.py:229` (`approve_manifest`), `core/heldout_eval.py:260` (`check_heldout_freeze`), `core/heldout_eval.py:615` (`check_prompt_tuning_isolation`).
* HEAD tests (executed, passed): `test_heldout_eval.HeldoutEvalTest.test_freeze_rejects_heldout_overlap_with_prompt_tuning_or_calibration_splits` (A), `test_rai_threshold_live_approval_guard.LiveCohortThresholds.test_constructed_manifest_is_rejected_even_with_named_approval` (A), `test_chat_eval.GoldenRunTests.test_actual_model_dispatch_is_gated_by_the_authorisation` (B).
* Result: freeze/isolation machinery and authorisation gate are source-tested with constructed fixtures. No actual-model, held-out, independently labelled evaluation was run (none authorised).
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: authorised finite actual-model evaluation on a human-approved frozen split.

### MEASURE-03 Fairness and accessible challenge evidence

* Baseline: NOT_ASSESSED. Role (inferred): Ranking owner / Resident Engagement / Assurance.
* HEAD code: `core/cohort_eval.py:1` (synthetic results never fairness evidence, OQ-018), `core/paired_equity.py:203`, `core/challenges.py:1`.
* HEAD tests (executed, passed, A): `test_cohort_eval.CohortEvalTests.test_clean_run_is_ready_but_never_fairness_evidence`, `test_cohort_eval.CohortEvalTests.test_default_unapproved_and_fictional_offline_records_enforce_oq018_boundary`. `test_challenges` unperformed.
* Result: constructed cohort controls are source-tested and explicitly not fairness evidence; no population, comprehension or non-digital challenge usability evidence exists.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: accessible representative human research and ranking-owner acceptance of cohort evidence.

### MEASURE-04 Reviewer effort and incremental benefit

* Baseline: NOT_ASSESSED. Role (inferred): Task owners / Assurance.
* HEAD code: `core/human_review_effectiveness.py:96-141`, `core/monitoring_coverage.py:286` (`REVIEW_EFFORT_STAGES`; corrected after Review finding 1, original line 162 cited `REQUIRED_CRITERIA`, which has no review-effort criterion).
* HEAD tests (executed, passed, A): `test_human_review_effectiveness_223.HumanReviewEffectiveness223Tests.test_competent_panel_detects_all_defects_retains_evidence_and_compares_effort`, `test_monitoring_coverage.DeclarationTests.test_all_registered_task_declarations_cover_harm_and_complete_review_effort`.
* Result: effort comparison is source-tested against constructed sessions; actual preparation, verification, correction and re-review effort and benefit are unmeasured.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: authorised human effort study compared with manual/template handling.

### MN-2.3 Retention, reset and disaster recovery

* Baseline: NOT_ASSESSED. Role (inferred): Digital / DPO-Legal / Record owners.
* HEAD code: `core/recovery.py:53` (`erase_resident`), `core/recovery.py:69` (`reapply_deletions`), `core/recovery.py:85` (`backup`), `core/ledger_digest_blob.py:1` (immutable blob digest verification).
* HEAD tests (executed, passed, A): `test_recovery.RecoveryTests.test_erasure_survives_restore_of_an_older_backup` (local SQL-store backup/restore double). `test_ledger_digest_blob` unperformed.
* Result: erasure survives restore of an older local backup; no witnessed backup restore, erasure reconciliation, deployed retention lock or disaster-recovery proof exists.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: independently witnessed restore under named retention and reset authority (Azure/SQL; not performed).

### T-RAI-005 Operational and model-integrity assurance

* Baseline: NOT_ASSESSED. Role (inferred): Digital / Incident and restart owners / Model-service owner.
* HEAD code: `core/rai_metrics.py:110`, `core/monitoring_coverage.py:171-210`, `core/rai_control_plane.py:214`.
* HEAD tests (executed, passed): `test_rai_harm_threshold_incident.HarmThresholdIncident.test_approved_threshold_breach_needs_a_named_incident_owner` (B), `test_monitoring_coverage.IndicatorTests.test_breach_requires_owned_incident` (A).
* Result: constructed monitoring and incident-owner controls exist; no evidence located for training/checkpoint integrity, provider operations, deployed monitoring or reviewer effectiveness (not exhaustively searched beyond the listed modules).
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: deployed monitoring evidence, provider operational attestation and review-effectiveness human evidence.

### EU-COND-01 Territorial scope and legal currentness

* Baseline: NOT_ASSESSED. Role (inferred): Legal / DPO with Product owner.
* HEAD code: `core/governance.py:115-121` (`RAI_EU_CONDITIONAL`, `RAI_CONDITIONAL_EU_ASSURANCE`), `core/governance.py:244` (`_rai_view`), `core/ai_registry.py:48,133`; `docs/reference/regulatory/README.md` 2026-11-01 update (decision `Pending`).
* HEAD tests (executed, passed, A): `test_governance.EvidenceRegister.test_live_use_blocked_dispatch_disabled_and_conditional_eu_guards`.
* Applicability: not established; nonapplicability not recorded; the guard keeps the finding NOT_ASSESSED and EU assurance conditional on qualified review.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: dated qualified Legal applicability review (territory, market, output-use facts).

### EU-COND-02 Actual influence and actor roles

* Baseline: NOT_ASSESSED. Role (inferred): Legal / DPO with Product owner.
* HEAD code and tests: as EU-COND-01 (`core/governance.py:115-121`, `244`; same executed test in A).
* Applicability: not established; provider/deployer/model-supplier roles, material influence and profiling facts not recorded.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: qualified actor-role and influence review.

### EU-COND-04 Operational assurance remains unproved

* Baseline: NOT_ASSESSED. Role (inferred): Legal / DPO / Assurance.
* HEAD code and tests: as EU-COND-01; supporting `test_human_review_effectiveness_223...test_live_mode_fails_closed_until_named_human_oq017_approval` (A).
* Applicability: not established.
* Tier: insufficient. Not closed.
* Missing evidence and resume condition: representative quality, fairness, oversight and monitoring evidence, plus applicability review.

## Cross-Row Limits

* Source tests prove narrow constructed behaviour at HEAD on the local JSON/SQLite doubles; they do not prove deployed effectiveness, semantic quality, fairness, legal compliance, recovery, resident comprehension or human oversight.
* No register write, tick, signature, threshold, target or source-current outcome was synthesised. The issue #126 checkboxes are not ticked or closed by this table.
* Full tier, native-host, real AI, SQL, Azure and qualified-human acceptance remain required for any application or release claim and are not supplied here.

## Blob Index (git blob ids at HEAD `01baf8d3`)

| Path | Blob |
| --- | --- |
| core/assistants.py | `98c3fa6d0969263ca91948b3016ba2a805d7c824` |
| core/export_fields.py | `6815bc24b8fda540b52624554d1e3c302d6df174` |
| core/data_protection.py | `521ab4f246abcd2cd42a7fe34cb49597d4247f3f` |
| core/chat_panel.py | `4357465f667927854e998009e1602410cdce0a1a` |
| core/ai_registry.py | `8c7c90c83c2ba388ff89b501598d622df887e725` |
| core/assistant_release.py | `8f0f50177d3afc8045a38bb7eee2face57f26f0b` |
| core/rai_release.py | `5e3c97a0ac3b5d8d7c01ae3c684c7c5ee203e385` |
| core/rai_control_plane.py | `fe376e51510049857bb09591166b89ff4fe65427` |
| core/rai_metrics.py | `dec9336465627b0e9de9a9db6798a51d4ce83d5e` |
| core/monitoring_coverage.py | `3a2010d7c026aa778c55d6c0e2647b4643e389d8` |
| core/restart_authority.py | `6562fb88189a214cb77e58bfe80b67db700ad14d` |
| core/recovery.py | `1b4b3e62b3fe8a606403683c66740a6303c2d2bd` |
| core/ledger_digest_blob.py | `ce61e8103443c14873cb8209a9ff331a7679ac23` |
| core/ranking.py | `7fcf49eb3aadb882504f838dcb84280580b0ebfe` |
| core/paired_equity.py | `7de27ed79bee103b8972383e8810cf8b2b384b5a` |
| core/cohort_eval.py | `4c6b7e9e23db5137ed74ff3a1bf701d2c48822f8` |
| core/heldout_eval.py | `f2d9000746141ac3140424deefbffe93e15f7aec` |
| core/human_review_effectiveness.py | `25fb74cab7ab3836d234e2a66aa01abe014a4d52` |
| core/lawstore.py | `bd222d3cb5f664de29a427589169dffe838ba4f9` |
| core/source_monitor.py | `294c99dc25dfabd8a57d2f32c4f8116a45d75ade` |
| core/governance.py | `38d3bd8615ad353fc099e009eb35baf6701492a2` |
| core/staff_intake.py | `3de31ca27b08ec4de0aa37affd54a2cd9a39ee53` |
| core/challenges.py | `613d484f31349c3aa7955607d7a0dba6c93fe58d` |
| agents/chat_eval.py | `2ffffe26bd3b04c32dc60197409c995aeb4a7c8b` |
| src/core/tests/test_governance.py | `79ce33234979323648e95be6b5aef7390f423eb8` |
| src/core/tests/test_rai_release_invalidation.py | `1ca9d5e767fe361356dcf4ebcc80cec09e418310` |
| src/core/tests/test_rai_threshold_live_approval_guard.py | `f769f383c646e8bab84703f3112378c5880291ad` |
| src/core/tests/test_recovery.py | `f4810ebc19d4483379ab4b36e45f8f55767d15f0` |
| src/core/tests/test_paired_equity.py | `0dfca4913889ab19fe52394b142b788c57877c9d` |
| src/core/tests/test_cohort_eval.py | `da6c7669d5571a260d14cc4e4376f520d037cffb` |
| src/core/tests/test_monitoring_coverage.py | `d65a2ed6581c3be08630684953bd5d8ca66d3bc1` |
| src/core/tests/test_human_review_effectiveness_223.py | `379b71ddb73af386bb408b2fcf84ce668101af1b` |
| src/core/tests/test_heldout_eval.py | `2c82683bae9b0d8de218ba50f4d845151899354a` |
| src/api/tests/test_assistants.py | `fc057d725e0a4937cc5c04b8c1355343fb77786f` |
| src/api/tests/test_assistant_release.py | `0ce099bb15dec8f05b9f50834183a24ca214048f` |
| src/api/tests/test_rai_harm_threshold_incident.py | `a0ac9a3bef8354a4f70287df7eaf5556c4b6bf7a` |
| src/api/tests/test_restart_audit.py | `6899c6544ed8de9f13f4f055874b2b8db504223b` |
| src/agents/tests/test_chat_eval.py | `ec5e78fcac69287a2d43621fc4879d439fcf504e` |
| docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md | `c578d69a68805a2362026a77d4eb6b18b076ed19` |
| docs/reference/regulatory/README.md | `164f7233491bff818dd656d0052685553c69ca65` |
| docs/case_study_48_addendum.md | `6cf511f7cc007959b2d4cf5efaf221a7d73803de` |
| docs/prds/zava-forward-retrofit-programme-demonstrator.md | `5aec7dfa0a6100d28f4a55126259af8119a84a06` |

## Restart Follow-Up Update (2026-11-17, additive; original text above unchanged)

Task `issue-126-restart-followup`, start commit `23eca3a5551fe355969f07651660d1b2ce40ae5c`, tree `27c0c2d9bb39746b016b669a59c63a4ac07ea154`. Source files are identical to the assessed `01baf8d3` (the only differences are the eight `.copilot-tracking/*/2026-11-17/` parent files), so the original "HEAD" source claims stand. The original Review is preserved unchanged and is not re-run or amended; this section is not a qualified acceptance, closure, approval or release claim.

### Deferred six-module batch (batch C, executed once)

* Basis: `src/core` is the documented component directory (`src/core/README.md`, source-monitor section). The orchestrator `src/orchestrator/tests/test_source_monitor.py` is a different module (tests `zava_forward.orchestrator.source_monitor`) and was not run; the MAP-05 row cites `core/source_monitor.py`.
* Environment: external venv with `pip install` of a `git archive` staging copy of `src/core` (outside the candidate), after a probe in the empty venv reported `ModuleNotFoundError: No module named 'zava_forward'`. Installed module files for the six modules plus `ai`, `lawstore`, `rulecards`, `rule_engine`, `ledger` were SHA-256 matched to the start-commit blobs and lie under the venv (`own-source-proof.txt`, `ALL_MATCH_AND_UNDER_VENV True`). Run from `src/core` with `env -i` (PATH, HOME, TMPDIR, ZF_DATA only, all external), `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=<worktree>/src/core/tests`; no `ZF_*MSSQL*`, model or credential variable.
* Command: `python -m unittest -v test_data_protection test_ai_register_completeness test_source_monitor test_ledger_digest_blob test_regulatory_privacy test_challenges`.
* Result: exit 0, `Ran 125 tests in 1.272s`, `OK`, 0 skipped, 0 failures, 0 errors. Per module: data_protection 32, ai_register_completeness 5, source_monitor 29, ledger_digest_blob 22, regulatory_privacy 18, challenges 19. Log SHA-256 `b2ffa2db3661bdf7dc271b868626b50744c5c40db368fdaedc4b7d302b95fcf9` (external `evidence-restart-126/run/batchC.log`).
* Qualification: the run used stdlib JSON/SQLite doubles and an in-module fake immutable blob transport (`test_ledger_digest_blob`). It is local synthetic execution, not SQL Server, Azure, real-model, human or deployed evidence. The batch had no skip; SQL Server opt-in classes elsewhere were not run and stay unproven.

### Per-row qualified disposition changes (7 of 22 rows; tiers unchanged for all 22)

No tier is raised: each baseline gap named in the row still has a human, DPO/Legal or actual-environment item open, and the added tests do not cover the semantic gap the row states. Counts remain 1 implemented/source-tested, 1 proposed, 20 insufficient, 0 observed, 0 independently accepted, 0 closed.

| ID | Executed and passed in batch C (source-observed, synthetic) | Disposition change | Still absent |
| --- | --- | --- | --- |
| T-RAI-001 | `test_data_protection`: `test_declared_fields_only_with_type_and_length`, `test_unknown_task_denied_with_manual_path`, `test_user_permission_never_establishes_task_necessity_or_bypasses_bounds`, `test_whole_system_task_manifests_cover_all_seven_plus_legacy_tasks` | "`test_data_protection` unperformed" replaced by source-tested payload-bounds and manifest evidence; remains insufficient | DPO/Legal necessity decision per task and field |
| GOVERN-AUDIT-01 | `test_ai_register_completeness`: `test_every_feature_carries_the_required_fields`, `test_incomplete_entry_is_reported`, `test_run_of_unregistered_feature_makes_no_model_call` | "unperformed" replaced by source-tested register completeness; remains insufficient | Personal owner/delegate acceptance |
| MAP-02 | `test_data_protection`: `test_subject_populations_separate_staff_tenant_review_fixtures_and_future_residents`, `test_nothing_is_approved_by_default`, `test_synthetic_refs_do_not_count_and_values_not_echoed`; the `synthetic_resident_does_not_exempt_actual_staff` symbol is not named by a passed test, so it stays read-only | "unperformed" replaced by population-separation and no-default-approval tests; remains insufficient | DPO/Legal decision on actual staff data now and future resident processing |
| GOVERN-AUDIT-04 | `test_data_protection`: `test_rights_ledger_never_represents_local_deletion_as_provider_erasure`, `test_rights_ledger_persists_across_sqlite_sqlstore_reopen`; `test_regulatory_privacy`: `test_unknown_periods_do_not_imply_approval_or_disposal`, `test_exact_due_boundary_is_simulated_review_not_deletion`, `test_every_retention_class_is_in_the_dpia_draft` | "unperformed" replaced by source-tested local rights-ledger and no-implied-retention-approval behaviour; remains insufficient | DPO/Legal decision record, processor/transfer terms, witnessed erasure/restore |
| MAP-05 | `test_source_monitor` (core, 29 tests): `test_detection_is_idempotent_unverified_and_does_not_change_law_or_cards`, `test_approval_needs_owner_provenance_complete_impact_and_card_approval`, `test_runtime_citation_gate_rejects_missing_partial_unreviewed_and_historical` (local SQLite double) | "unperformed" replaced by source-tested offline detection that stays unverified until an owner approves; remains insufficient | Legal currentness review and official-source check |
| MEASURE-03 | `test_challenges` (19 tests): `test_staff_route_needs_named_staff_and_non_digital_channel`, `test_owner_and_next_update_are_mandatory`, `test_only_named_owner_resolves_with_evidence` | "unperformed" replaced by source-tested challenge routing with a named owner and a non-digital staff channel; remains insufficient. This is route mechanics, not usability, comprehension or fairness evidence | Accessible representative human research, ranking-owner acceptance |
| MN-2.3 | `test_ledger_digest_blob` (22 tests, fake immutable blob transport): `test_retention_lock_rejects_short_or_boolean_days_and_missing_policy`, `test_verify_detects_corrupt_remote_anchor_stale_current_head_and_unlocked_blob_headers` | "unperformed" replaced by source-tested retention-lock posture checks against a fake transport; remains insufficient | Witnessed restore under named retention authority; deployed WORM lock (Azure) |

The other 15 rows are unchanged by batch C. T-RAI-005, MEASURE-02, MEASURE-04 and the EU rows keep the parent text.

### Low evidence-quality gaps (parent Review findings 2-4)

* MAP-01 test linkage (finding 2): the cited `test_paired_equity.PairedEquityTests.test_ai_task_paired_evaluation_and_transparent_non_ai_comparison` is context only. It runs the ranking function indirectly through a signed policy (so `_support` can be called), but it does not assert the `support_unknown` reason code or that "Unknown" sorts with "No"; no test run so far asserts that behaviour (corrected after the follow-up Review, which found the earlier "does not exercise `_support`" wording overstated). Existing candidate tests, listed but not run and not written for this assessment: `src/api/tests/test_ranking_policy.py` and `src/agents/tests/test_cohort_manifest_draft.py` (binding `ties_with_no_adds_support_unknown_reason`). MAP-01 stays insufficient and the source ordering stays "read, not asserted by an executed test".
* MN-3.2 tier rationale (finding 3): MN-3.2 stays insufficient while GOVERN-AUDIT-02 is source-tested because the table's tier rule requires a directly relevant passed test for the baseline gap. GOVERN-AUDIT-02's baseline gap is the change binding, which the invalidation tests exercise. MN-3.2's baseline gap also includes model retirement and change review; no executed test covers retirement detection or a retirement review, and no named human review exists. The invalidation tests are therefore partial, relevant to MN-3.2 but not sufficient to meet the rule.
* Retained verifier (finding 4): the original inline checks (69 path:line, 44 symbols, 38 blobs, 27 test ids) were not retained and cannot be reproduced exactly. A reconstructed external verifier, not the original, is retained at `evidence-restart-126/verify/verify_table_refs.py` (SHA-256 `2807748302e94fe4f94b8f386d2e59684546a544a160a22c525de0c8db629cd5`) with its output next to it; its results are recorded in the follow-up changes record and are distinct from the parent's historical counts. Parent batch A/B logs were inaccessible to that confined follow-up worker (not lost; see "Retention Correction (2026-11-17)" below), so that follow-up checked test ids from those batches for existence in the test sources only, not for a passed result in a log.

### Retention Correction (2026-11-17)

* Superseded claim: the earlier wording of the paragraph above, "Parent batch A/B logs were not retained at the original location", and the same wording in the restart follow-up Review (info finding 2). Those records are preserved unchanged. Inaccessible to a confined worker is not the same as missing or not retained.
* Directly observed by the correction worker (copies in its own run root, `evidence-retention-correction-1455/run/`): `batchA.log` SHA-256 `8fd8668b01bd4b624a26c464556d819b8a58ff3a81f772f869afcc9ba869e0cc`, ending `Ran 251 tests in 6.996s`, `OK (skipped=18)`; `batchB.log` SHA-256 `0235f289a27ca362c526de903685c07c200ca992d846f93de336536a7d7daee4`, ending `Ran 270 tests in 89.068s`, `OK (skipped=67)`. Both hashes equal those recorded in "Commands Run" above.
* Coordinator-reported, not directly observed by the worker: both files exist at the original host-only path `/mnt/tmp/ama-run-74bd1fe9-126-assess-20261117T1305/evidence-126-assess/run/` with the same SHA-256 values. The worker did not access that run root.
* These are historical logs from the earlier assessment, not newly executed tests. Their aggregate results do not by themselves verify individual test ids; the restart follow-up's existence-only check of test ids is unchanged and no per-id log verification was performed here.
* Unchanged: the original inline verifier remains unrecovered; the reconstructed verifier is a different helper with its name-only/class-membership limitation. No row disposition, MAP-01 semantic qualification, skipped SQL or telemetry coverage, evidence limit, or RAI, DPO, Legal or human approval boundary changes.

### Unchanged boundary

Qualified owner, DPO, Legal, Finance, real-model, witnessed-restore, Azure and EU-applicability evidence and approvals remain absent for every row. The issue #126 checkboxes are not ticked or closed.
