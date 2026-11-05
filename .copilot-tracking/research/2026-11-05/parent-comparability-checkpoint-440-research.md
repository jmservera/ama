<!-- markdownlint-disable-file -->
# Research: parent-topic comparability stabilization checkpoint (#440, parent #123), 2026-11-05

Task slug `parent-comparability-checkpoint-440`. Research disposition: executed (bounded source, identity and light local observation). Planning Readiness: Ready.

## Scope and provenance

* Worktree `/home/azureuser/source/ama-wt/docs-parent123-checkpoint-wave2`, branch `docs/parent123-checkpoint-wave2`, start HEAD `ad1ee0264a381fb76de100417c535a4e194e2460` (tree `8052fa5d3248c9dc3a4f9cb8558ccfbfa65e360e`), clean, no ignored files at start. Declared target `feat/discovery-assurance-integration-123`: `git ls-remote` (read only) names `ad1ee026...`; the local ref of that name is stale at `3d7ad2fe`, so the pin is taken from the remote and the HEAD, not the local ref.
* Fresh `origin/main` `c6d5a8f3c3a35892322300be27b9747f7b11362d`, tree `876679c32ff8f8a3d35822d9e46d8b377ce15428`. Main to parent: parent is two commits ahead (#1211 `e546bf23`, #1212 `ad1ee026`) of merge base `3d7ad2fe`; main is one commit ahead (#1210, tooling only).
* Trigger: owner comment on the existing open recurring checkpoint #440 (parent #123): completed child wave #1211 and #1212 needs an affected-surface record before parent #123 closure or dependent cohort expansion. No duplicate issue.
* Read at start: `docs/case_study_48_original.md` and addendum (context), `docs/reference/README.md`, `docs/reference/memory.md` (context only), `docs/reference/method/tracking-retention-policy.md`, `src/core/README.md` paired_equity section, the prior fifth checkpoint in the evidence pack, the #128 research, changes, original review and published functional assessment (`issue-128-published-functional-assessment.json`).
* Excluded and not read: open unmerged #1203, #1205, #1141 and #1206 (all confirmed OPEN, `mergedAt` null); no private datasets; no remote mutation.

## Findings

* Parent-only versus main (blob identity): `paired_equity.py` parent `5aedcd7b`, main `d29768d5` (the unfixed blob of the original #128 reproduction); `test_paired_equity.py` parent `f9b07cb6`, main `432aef3e`; `src/core/README.md` parent `bb709453`, main `b5469625`. The comparability fix is therefore parent-topic only and main still admits a confounded pair.
* Unchanged between parent and main (same commit lineage, no diff): `journey_register.py` `92f75403`, `ranking.py` `052bc6b9`, `ranking_publication.py` `934ef16d`, `rai_release.py` `970678ca`, `cohort_eval.py` `60907194`, and their tests. The BRD (draft 0.21.0, `34d88395`), PRD (in-review 0.21.0, `c788b917`), ADR 0002 (Proposed, `cbe21530`) and ADR 0003 (`d6064539`) blobs are identical on both.
* Boundary map: `paired_equity` imports `journey_register` (`human_review_route`, rank effect `none`), `ranking.rank` (or an injected ranker) and `rai_release.digest` only. It does not import or call `cohort_eval`, `ranking_publication`, or the `rai_release` selection and invalidation functions. Consumers of `cohort_eval` are in `src/agents` (cohort ranking and AI evaluation) and of `ranking_publication` in `src/core/store` and `src/api/server`; those were not executed here. The paired diagnostic is a pure, constructed-fixture check; it is not wired into release admission, invalidation or the cohort approval manifest.
* Comparability change: predeclared fixture-local `CONTRASTS`, tuple-path `_flatten`, type-aware deep `_same`, `_comparability`, `invalid_pairs`, blockers `invalid_comparison:<reason>`; invalid pairs never count as tested or failed. All four historical holes (bool versus int, empty nested mapping, nested sequence type, dotted-key shadowing) are in the source and tests. The original NOT CLEAN review (2 Medium) and the correction-2 adverse findings stay separate, as does the later published exact-head functional assessment of #1211 (approve, 0 findings, bounded to the constructed diagnostic, reading only).
* Source inspection: no defect confirmed. Not claimed as defects: the reviewer's optional regression (seeded defect on a rejected pair), strict `type(a) is type(b)` also separating dict subclasses, and absence of wiring. These are observations, none reproduced as wrong behaviour.
* Environment finding: shared editable installs and `/tmp/rpi128-venv` resolve `zava_forward.core` through a namespace path whose first entries are other trees (`issue-128-comparability`, the primary checkout). The only candidate-bound observation therefore used the existing venv interpreter with explicit `PYTHONPATH` of this worktree's `src/core/src` and `src/core/tests`, plus an asserted `__file__` check for every module and test under test. No install, no change to a shared environment.

## Local observation (light, parent-topic only)

Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<wt>/src/core/src:<wt>/src/core/tests /tmp/rpi128-venv/bin/python -m unittest tests.test_paired_equity tests.test_journey_register tests.test_rai_release tests.test_rai_release_invalidation tests.test_ranking_publication tests.test_cohort_eval` from `src/core`. Exit 0, 74 tests OK in 0.062 s. Module-path assertions for all six modules and six tests passed (exit 0). Log: `/tmp/parent123-comparability-440/core74.log`. Python 3.12.3. Git status after: clean.

## Constraints and unresolved gaps (not closed)

* #128 acceptance not met: actual-model run, independent expected-pair manifest and threshold approval (PRD OQ-018, AC-073), keyboard and screen-reader testing, user research, lawful-field decision, named human acceptance. No actual AI, cohort, population fairness, threshold, lawful-field, assistive-technology or human acceptance evidence exists. Implemented helpers (`cohort_eval`, agent consumers, `paired_equity`) are not that evidence.
* Not run: `tools/rpi-checks.py`, SQL, Docker, browser, cloud, provider, model, private data, billing, broad or API/agents suites. Native FULL gate lock and receipt untouched.
* Disclosure survives: the prior #440 run removed `/tmp/s440` without retained finite selection, archive or restore proof. This task deletes nothing and is not a restoration.

## Planning Readiness

Ready. Append one dated section to the evidence pack, one index link and one log entry; no code, schema, coordinator or workflow change.
