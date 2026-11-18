<!-- markdownlint-disable-file -->
# Task Research: issue #126 residual and unassessed-check source assessment

## Status

* Phase: Research (opened 2026-11-17 13:09Z; witness `research-open` seq 2 recorded before substantive source searches; the opening artifact text is preserved at `evidence-126-assess/research-opening-snapshot.md`)
* Research disposition: executed (read-only repository inspection; no external, cloud or private data)
* Planning Readiness: Ready
* Task: `issue-126` / `issue-126-residual-source-assessment`; state `.copilot-tracking/rpi-sessions/2026-11-17/issue-126-residual-source-assessment-state.json`

## Scope and Lineage

* Issue #126 snapshot, parent and PR #1812 pins: caller-supplied evidence under `evidence-126-assess/` (`issue-source.json`, `parent-source.json`, `pr1812-source.json`).
* Assessed source: worktree HEAD `01baf8d3df86a28f754da8545d0e8f12012bf350`, tree `d10bd7a918779f770da471fd3c54d8a61e14883e`, branch `docs/rai-residual-source-assessment-126`. It is the declared parent topic `feat/demo-164-chat-grounding-provenance-0900` head (PR #1641, OPEN, not main).
* PR #1812 commit `755371d2cf09d4680b2b675d0152dbdecb905a89` (tree `22bb382c784222b600e828c001d441f596c9db3d`) is an ancestor of HEAD (`git merge-base --is-ancestor` confirmed). It merged into the parent only.
* Main `f1df574bba2b94cd83bb2a783079ec94cd584c90` is separate provenance. It is not this assessment's source and not an acceptance basis. `git merge-base HEAD origin/main` is `61e1917dd075a8307f0fd436c42cc41f47906846`.
* Original baseline: `RAI_BASELINE = 1cb398c7b90bec05a5700008a97d0cfac494144a` (`src/core/src/zava_forward/core/governance.py`), report `docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md`, owner acceptance 2026-10-15 for baseline and remediation planning only. Report-accepted pre-annotation commit `cf6a5c18d984951a9522d664b8e7c4676492a93e`.
* Whole-project later review `docs/reference/research/rai/project-rai-review.md` (baseline `9bfed51863b05a25e9939d82504c576524688e14`, 2026-10-28) is separate prior evidence and not this score.

## Canonical Sources Read

* `docs/case_study_48_original.md`, the RAI release-position parts of `docs/case_study_48_addendum.md`, `docs/reference/memory.md` (context only), the project RAI review, and the 2026-10-14 RAI report (framework tables, remediation checklist, human-review handoff).
* `governance.py` register contract: `RAI_RESIDUALS`/`RAI_UNASSESSED` (11 + 11), `RAI_TIERS` (implemented/source-tested, deployed-observed, proposed, insufficient, independent-acceptance), `RAI_ASSESSMENT_FIELDS` (source_commit, task_id, task_version, release_version, nonapplicability_reason), `RAI_CLAIM_FIELDS`, `RAI_EU_CONDITIONAL`, `RAI_AFFECTED_DISPATCH`, `PRD_QUALITY_REVIEW`, `PRD_OWNER_ACCEPTANCE`.
* PR #1812 changes and review (`.copilot-tracking/changes/2026-11-15/governance-126-rai-prd-separation-changes.md` and review log): runtime PRD-separation, EU applicability guards and documentation reconciliation. Its validation ran on its own head, not on this HEAD, and it produced no per-ID disposition table.

## Findings

* F1: the register can hold per-ID claims, but the repository holds no committed per-ID current-source disposition table with blob identities, version evidence and accountable roles. This task addresses that gap (issue criteria "Track all eleven..." and "fresh current-source assessment" were restored to unchecked on 2026-11-16).
* F2: version evidence at HEAD: all five `src/*/version.py` are `0.1.0` (distribution version, not a task/release version); `ai_registry.REGISTRY_VERSION = "2026-10-15.1"`; `rai_release.EVALUATION_VERSION = "task-release-evaluation-v1"`; PRD `0.21.0` (unsigned, ms.date 2026-10-25). No approved task or release version is recorded. Rows take registry/evaluation versions where relevant and state "none recorded" otherwise.
* F3: relevant current modules (under `src/core/src/zava_forward/core/` unless noted): `assistants.py`, `export_fields.py`, `chat_privacy.py`, `data_protection.py`, `ai_registry.py`, `assistant_release.py`, `rai_release.py`, `rai_control_plane.py`, `rai_metrics.py`, `monitoring_coverage.py`, `restart_authority.py`, `recovery.py`, `ledger_digest_blob.py`, `ranking.py`, `paired_equity.py`, `cohort_eval.py`, `heldout_eval.py`, `human_review_effectiveness.py`, `challenges.py`, `lawstore.py`, `source_monitor.py`, `regulatory_eval_gates.py`, `regulatory_privacy.py`, `governance.py`; `src/agents/src/zava_forward/agents/chat_eval.py` and related held-out modules.
* F4: module docstrings state the evidence limits: `data_protection.py` ("recorded references are not verified DPO or Legal approval ... Constructed fixtures are the only data permitted to reach a model"), `ai_registry.py` ("no accountable individual, delegation or approval is recorded"), `monitoring_coverage.py` ("Indicator evaluation never reports green"), `cohort_eval.py` ("Synthetic results are never fairness evidence (OQ-018)"), `recovery.py` (local store backup/erase/reapply, not witnessed restore).
* F5: own-source import paths proven from `/tmp` with `PYTHONPATH=<worktree>/src/{core,agents,api}/src` plus test directories: `zava_forward.core.governance`, `zava_forward.agents.chat_eval` and `zava_forward.api` resolve to the worktree. Installed `zava-forward-{core,agents,api} 0.1.0` also exist in site-packages and are shadowed by PYTHONPATH; no install is needed.
* F6: the accountable-role vocabulary for residuals comes from the report remediation checklist (roles, not named people). For unassessed rows the report's human-review handoff supplies roles; the role mapping for those eleven is this assessment's inference and is labelled so.
* F7: no human, real-model, witnessed-restore, privacy/legal or EU-applicability evidence exists in the repository for any of the 22 IDs, so no row can be observed or independently accepted from repository evidence alone.

## Constraints and Boundary

* RPI assessment files only under `.copilot-tracking/`; no application, test, SQL, config, gate, agent or policy edit; no new test files.
* At most two bounded test batches; no full suites, SQL/browser/container/Azure; no private default `ZF_DATA`.
* No signatures, thresholds or source-current outcomes synthesised; disposition vocabulary follows `RAI_TIERS`; the original adverse report is unchanged.

## Selected Approach

One assessment table artifact (`.copilot-tracking/changes/2026-11-17/issue-126-residual-source-assessment-table.md`) of 22 rows with baseline status/verdict, current assessed commit, blob identities (`git rev-parse HEAD:path`), version evidence, code and test references, command/result or unperformed status, accountable role, disposition, and missing evidence with resume condition. One critique of the plan, one Review restricted to the 22 rows.

## Planning Readiness

Ready: sources, boundary, vocabulary and test import path are established; no blocker.

## Follow-Ups (current)

* Human, DPO/Legal, real-model, witnessed-restore and EU-applicability evidence per row (listed as resume conditions in the table).
* Publication or PR of this candidate requires separate authorisation; none is given here.
