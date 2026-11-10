---
title: Issue 109 sensor-review stack integration plan
ms.date: 2026-11-10
task_id: 109-integration-preparation-1110
---

## Objective

Prospectively plan the later ordinary integration, into the local topic `feat/demo-sensor-review-109-1110` (currently equal to `origin/main` `6cc59776666620309fb6b67ad2fdafb343d40998`), of the actually merged child-parent remote head plus current main. This invocation covers research and planning only and pauses before `implement-start`.

Research: [research](../research/2026-11-10-sensor-review-109-integration-prep-1110-research.md). Details: [details](../details/2026-11-10-sensor-review-109-integration-prep-1110-details.md). Critique: [critique](critiques/2026-11-10-sensor-review-109-integration-prep-1110-plan-critique.md). Prospective changes: [changes](../changes/2026-11-10-sensor-review-109-integration-prep-1110-changes.md).

## Classification and tier

* DEMO focused tier. The planned change is an ordinary merge that authors no source, workflow, dependency, Dockerfile, permission, schema or infrastructure line. Persistence (SQL store) and main composition are touched by inherited content, so actual disposable SQL selectors apply.
* Not applicable and not run: blanket full gate, `--changed`, full discovery, unrelated browsers or images, Azure, live Hub, credentials, private data, shared installs, paid runs. This tier does not replace independent exact-head review, human approval or hosted CI.
* Doubt rule: if the merge brings any workflow, dependency-manifest, Dockerfile, permission or gate-semantics change beyond the identified `src/core/pyproject.toml` `iothub` and `dev` extras and the child's mypy override, stop and ask Root for the stricter tier.

## Steps

* [x] Phase 1 research (witness `research-open` recorded).
* [x] Phase 2 plan, details, one critique, prospective changes (this record); witness `plan-done`. The invocation ends here with phase status awaiting-input.
* [ ] Phase 3 (future, only after Root admission): re-verify identities, ordinary merge, targeted checks, complete changes record. Witness `implement-start` precedes the merge; `implement-done` follows checks.
* [ ] Phase 4 (future): one Review, witness `review-done`; commit the merge and records, witness `commit-complete`.
* [ ] Follow-up (Root, not this loop): the new #440 sensor-integration checkpoint.

## Resume point and admission gate

Resume before `implement-start`. Preconditions that Root must supply or confirm:

1. PR #1395 actually merged into remote `feat/demo-sensor-review-109-1110`; the merged remote parent head SHA is stated and fetched. Root admits the reviewed child.
2. Hosted checks for the merged child head are observed as complete by Root (`mssql`, `src-core`, `src-api` were in progress at preparation). Absent or unobserved hosted workflows are not successes.
3. Current `origin/main` is re-read. If it moved beyond `6cc59776`, the plan applies to the new main only after a recorded identity comparison; the new main commits are listed and any file overlap with the child net source set (`sensor_review_draft.py`, `projection.py`, `server.py`, `ops.js`, `quality_sensors_browser_check.py`, the two test files, `src/core/pyproject.toml`) is flagged to Root before merging.
4. The worktree is clean at the committed preparation head, with no Root-instructed push, rebase, reset, amend or force.

## Planned integration (ordinary merge only)

* `git fetch origin`; record `origin/main`, the remote parent head `P` and `git merge-base --is-ancestor` relations. Do not assume `2b050647bff51eef4c1b34d6434bba7eae3d5f9a` is an ancestor of `P`: a squash or rebase merge removes that ancestry, in which case compare trees and record the difference instead of transplanting source.
* Predict with `git merge-tree --write-tree --name-only HEAD P`; a conflict list or nonzero exit stops for Root.
* Run `git merge --no-ff --no-commit P` on the local topic (main already included). No rebase, reset, amend, force-push, cherry-pick, patch application or hand-authored source. Only mechanical, content-preserving overlap resolution of `src/core/pyproject.toml` is tolerated, and only if disjoint-hunk auto-merge fails for a stated mechanical reason; any actual semantic conflict stops for Root and no correction pool is opened.
* After staging, parse `src/core/pyproject.toml` with `tomllib`; confirm both main's `iothub`/`dev` lines (`azure-iot-hub==2.7.0`, `six==1.17.0`) and the child's scoped mypy override are intact. Confirm `sensor_review_draft.py` and `test_sensor_review_draft.py` equal the child blobs and that Registry files equal main.
* Commit only after review, with the GitHub-resolved repository-local noreply identity and the Copilot trailer. No push, PR or GitHub write unless Root separately instructs.

## Planned checks (targeted, DEMO tier, nothing run in this invocation)

Environment: external venv and caches, `PYTHONDONTWRITEBYTECODE=1`. The child venv `/tmp/zf-111-1110/venv` predates main's `azure-iot-hub` and `six` dev extras; if configured mypy or tests fail on a missing import, report it as a prerequisite blocker and do not install into shared environments without Root's permission.

1. Import origin: `zava_forward.core.sensor_review_draft`, `zava_forward.core.synthetic.device_registry_azure` and the API server resolve to this worktree.
2. Core draft: `PYTHONPATH=src:tests python -m unittest tests.test_sensor_review_draft` from `src/core` (expect 65 discovered, 22 opt-in skipped locally; skips are not SQL evidence).
3. Core analysis: `python -m unittest discover -s tests -p 'test_sensor_analysis*.py'` (expect 30, 10 opt-in skips).
4. API callers from `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest tests.test_sensor_review_draft_api` (expect 6, no skips). The sensor GET and POST routes, `projection.redact_staff_detail` and `ops.js` are the affected caller boundary.
5. Main-owned surfaces are not rerun by default (Registry module and tests, `script_retry.py`, workspace oracle tests): they do not overlap child files and were merged under their own PR checks. Run them only if the merge unexpectedly changes them relative to main, or if Root asks; a failure there is reported as an adverse main-owned result, never repaired here.
6. Configured static checks from `src/core`: `ruff check .`, `ruff format --check .`, `python -m mypy --no-incremental --cache-dir <external>`. Pass is stated as a configured pass with the disclosed scoped `disallow_untyped_calls = false` exemption, not unchanged strict typing. TOML parse as above.
7. Actual disposable SQL: `tests.test_sensor_review_draft.MssqlDraftCases` with `ZF_SENSOR_DRAFT_MSSQL=1` and the task-owned disposable local container pattern used by the child (`ROOT/checks-111-parent-adoption-1855/run-mssql.sh`). Admission is exactly one non-queued `flock -n /tmp/ama-rpi-heavy.lock` attempt that identifies the actual holder. If the lock is busy, record BUSY with the holder and stop that check: no spin, queue, retry loop, kill or interruption of a holder. Pass requires all cases run, 0 skips and exit 0 (22 expected); any container is removed afterward. Synthetic local SQL is not Azure IoT Hub, Azure SQL or live acceptance. No password is logged.
8. Sensor browser check (`quality_sensors_browser_check.py`) only if Root separately admits it through the same heavy-lock rule; otherwise stated as not run. It is not an exact-final-tree accessibility or assistive-technology acceptance.

Explicit coverage gaps carried forward, never described as passes: unforced `ConflictError` and `CommittedReloadError` branches; the scoped mypy exemption; skipped opt-in tests; no Azure Hub, Azure SQL, live UI or model approval; no sensor browser run.

## Stop rules

Any actual semantic conflict, new defect, refused witness marker, missing prerequisite or unexpected main movement overlapping the child: stop, preserve evidence and state, report to Root. No self-heal, retrospective record, correction pool, new agent or heavy check outside lock admission.

## Epic and dependent follow-up (due, not performed here)

A sensor-integration checkpoint under #440 is due before epic #109 closure or dependent expansion (for example #110 live Hub acceptance, #184 live streaming, #111 approved task wiring). Child merges, this integration and the local tests above are not integrated or live acceptance. The existing NomUX and Bicep observation record in #440 is distinct and is not reused as sensor coverage. Root routes the checkpoint through #440 RPI; this loop neither implements it under #109 nor approves any owner pivot or deferral. Requirement changes, architectural pivots and deliberate deferrals require owner approval.

## Criteria status

All #109 criteria stay open (checkpoint, all children closed or deferred, no signal diagnoses a hazard or changes ranking) unless independently and literally proved after main integration. No new ticks, closing keywords or acceptance are claimed. A later PR for this integration should use `Refs #109 #111` only, with unmet criteria listed.
