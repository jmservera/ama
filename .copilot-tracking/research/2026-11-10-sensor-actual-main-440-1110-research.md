# Research: Sensor-review wave (PR 1404) actual-main observation (2026-11-10, Refs #440 #109 #111)

Disposition: executed. Planning Readiness: Ready. Docs-only; no runtime, test, install, image, SQL, browser, cloud, model, live or private-data work, and no source, test, oracle, tool, workflow or gate change.

## Scope and dependency

* New recurring observation of the merged sensor-review wave. Not another implementation, not a retry, no source-correction pool, no counter grant.
* Worktree `issue-440-sensor-actual-main-1110`, branch `docs/demo-sensor-main-checkpoint-440-1110`, created from actual `origin/main` `4c1b4099869d132e06291a29ee476e98286c2245`. Independent main-target candidate; no parent topic.
* Concurrent aftercare checkpoint PR 1405 (head `5450b07a89a6`) is OPEN, not main, and owns its own pack, index and log section. Nothing from it is copied or described as merged.

## Pin (fetched 2026-11-10 ~16:41Z, `origin/main` unmoved)

* `origin/main` `4c1b4099869d132e06291a29ee476e98286c2245`, tree `7515820333a23e76d1d200ea558ad01127024aab`, equal to the Root prospective tree; one squash parent `d240cc589f483c03e9c728bd3615a966775c90dc` (rubric baseline), author `jmservera` noreply, committer GitHub, 2026-11-10T17:38:21+01:00 (16:38:21Z).
* Lineage: child PR 1395 (head `6b0ba7b14f99`, base `feat/demo-sensor-review-109-1110`) merged 15:51:03Z into the declared parent as `bd2a6494464b451572fc3dc7c8d53c549e0f9dad`, not main. Parent PR 1404 (base `main`, closing references none) merged 16:38:22Z as `4c1b4099`. Reviewed head `6fe2218c7960a60a9d18c9680230b37fad7e972c` (tree `00c7abf4209d`); Root gate lists 19 contexts, all SUCCESS, MERGEABLE.
* Preceding main commits: `64c3f9191a2f` (PR 1400 aftercare) then `d240cc589` (rubric score record).

## Source equivalence (git read-only)

* `src` `49c7b0b06f97`, `infra` `f7f31c0934cf`, `tools` `432a4e8f7d74` are identical on actual main, reviewed head `6fe2218c` and the tested staged tree `d45426bd`. `.github` is `e2ecbb8ea5b2` on `6fe2218c` and `d45426bd` but `ce96a8f4c2c5` on main.
* The only non-tracking path that differs between `6fe2218c` and main is `.github/rubric/scores/latest.json` (blob `b0bc2db354d0` on `6fe`, `b9c8b5d9e978` on `d240cc589` and main): main's rubric baseline advanced by commit `d240cc589`. No `.copilot-tracking` path differs either. This is the exact `.github` exception; no workflow, action or gate file differs.
* The raw runs executed on the staged tree `d45426bd28850d893622b48df1a2649a13135992` while the branch metadata still named `20addb9ae` with 83 dirty entries. They are not literal post-commit or current-main executions.

## Selected contracts and code (blobs at actual main)

* `sensor_review_draft.py` `15055cd59a0a` (388 lines): flag `ZF_SENSOR_REVIEW_DRAFTS`, case key `sensor_review_drafts`, schema `sensor-review-draft-v1`, state `PROPOSED_UNAPPROVED`, roles Quality Inspector and Retrofit Programme Manager, at most 20 drafts, manual route `manual-sensor-review`; the module docstring states no task, owner, queue, model call, ranking, hold, hazard clock or consent change, and a served write refuses because no approved policy source exists.
* `sensor_analysis.py` `dd6a363db74b` (255 lines); `projection.py` `14892308364e` (204 lines, generic detail removal of drafts); `server.py` `ab381d0718ba` (draft read at `/api/cases/{id}/sensor-drafts` and a request route dispatched before generic case access, 503 pointing to the manual route); `ops.js` `2178e06f299c`; `pyproject.toml` (Core) `caeac749acca`.
* Tests: `test_sensor_review_draft.py` `1fe0a7469455` (619 lines), `test_sensor_review_draft_api.py` `7aef271edf4e` (168), browser check `quality_sensors_browser_check.py` `80a1bf730adf` (509).
* The squash `4c1b4099` changes 56 paths (3216 insertions, 2 deletions) against its parent `d240cc589`: 8 source and test paths and 48 tracking records.

## Requirement documents at actual main (not changed by the wave)

* BRD Agentic Retrofit Programme 0.21.0 `draft` blob `34d88395de86` (FR-048, RULE-014).
* PRD Zava Forward 0.21.0 `in-review` blob `c788b917bafa` (FR-050; AC-066, AC-067, AC-068 all "Not run" in the acceptance table).
* ADR 0003 blob `d60645397b20`. Draft and in-review are not approval.

## Consumed Root evidence (read raw, not re-run)

Under ROOT: `root-1404-final-merge-gate-2013.json`, `pr109-actual-parent-qualified-1993.txt`, `handoff-109-actual-parent-main-1110.md`, `independent-109-actual-parent-1987/functional/` (approve, zero findings, plus the metadata supplement), `root-109-actual-parent-1986.json`, `checks-109-actual-parent-main-1110/`, `phase109-actual-parent-main-evidence-1110/`.

* Raw results read: Core draft 65 run, 22 skips OK; analysis 11; analysis store 9; manifest 8; Registry 39; intake 39; aftercare store 36 run, 13 skips; API draft 6; aftercare served 8; screen 13; accessibility baseline 12; workbench 5; Ruff and format pass (Core 243, API 142); mypy Core 296 and API 224 pass; browser 33 passed exit 0; MSSQL 22 run, zero skips, exit 0 on SQL Server 2022 CU27-GDR 16.0.4305.5.
* Preserved adverse result: the first `test_role_endpoint_inventory` attempt exited with `ModuleNotFoundError: test_role_matrix` (command omitted the tests directory from `PYTHONPATH`); one corrected-path rerun passed 24 tests. The first failure is not a pass.
* Witness: seven records, `verify` records 7, log sha256 `4fe3212a1ff10ba42af278e94325d9662e02d55f6b5bebf90bf3603b6ed6a3d8`, with six "artifact changed after observation" notes; local writable record, not attestation.
* The `node --check` results appear only in the handoff and transcript, not as separate raw files (Functional supplement says the same).

## Open issue comparison (live, 2026-11-10)

* #109, #111, #110, #184, #185, #1288, #81, #440 OPEN. #132 and #144 OPEN and excluded. Inherited aftercare #1401 and #1402 OPEN and unrepaired here. #1297 (bind sensor MSSQL skips to required SQL execution) and #1298 OPEN: existing owners for the skip-is-not-pass gap. PR 1405 OPEN, not main.
* #111 criteria seen: thresholds labelled exercise values ticked; reproducible outputs and R1 to R3 research unticked.

## Findings

* No new defect and no refactoring claim: nothing read contradicts the Functional approve; the retained gaps are already owned.
* Gaps: unforced `ConflictError` and `CommittedReloadError` coverage; opt-in skips are not SQL passes; scoped mypy exemptions; fixture checks do not show a real provider consumed readings; no live Hub, Quality model, resident, human, WCAG or axe acceptance.

## Planning Readiness

Ready: docs-only section, index entry and log entry with these identities.
