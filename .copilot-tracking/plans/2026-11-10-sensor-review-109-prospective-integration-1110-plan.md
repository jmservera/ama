---
title: Issue 109 prospective local integration plan
ms.date: 2026-11-10
task_id: 109-prospective-integration-1110
---

Research: [research](../research/2026-11-10-sensor-review-109-prospective-integration-1110-research.md). Details: [details](../details/2026-11-10-sensor-review-109-prospective-integration-1110-details.md). Critique: [critique](critiques/2026-11-10-sensor-review-109-prospective-integration-1110-plan-critique.md). Changes: [changes](../changes/2026-11-10-sensor-review-109-prospective-integration-1110-changes.md).

## Objective and classification

One ordinary `--no-ff --no-commit` merge of fresh `origin/main` (`c66370042eb08f07839d054433f4483078703cf2`) and the exact reviewed child `6b0ba7b14f9985cddd0d8cbc8ad27430c9acb9d2` into local `feat/demo-sensor-review-109-1110` (HEAD `a3d5e615f0b2617b40cd5bdd23d00db0be11284e`), committed once after review. Integration only. The result is PROSPECTIVE, implemented-unverified local composition: not the delivered remote parent, not main, not the actual PR #1395 merge. Root compares the actual remote squash source and fresh main after CI and merge before any publication. No push, PR, retarget, GitHub write, agent, provider, cloud or private data.

Tier: DEMO focused. The merge authors no workflow, dependency, Dockerfile, permission, schema or gate line, but inherited `src/core/pyproject.toml` content carries dependency pins and a mypy override, so the doubt rule applies to any NEW such line beyond the known disjoint hunks: stop for Root. Not run by design: blanket full gate, `--changed`, full source unit discovery, unrelated browsers or images, Azure.

## Steps

* [x] Research (witness `research-open`).
* [ ] Plan, details, one critique, prospective changes, witness `plan-done` (this step).
* [ ] Implement: re-verify identities, witness `implement-start`, merge, assert invariants, run checks, complete changes record, witness `implement-done`.
* [ ] Review: one Review, witness `review-done`; commit, literal 40-hex HEAD, witness `commit-complete`, verify.

## Merge protocol

Recheck `git fetch`; if main or the child moved from the pinned identities, stop for Root. `git merge-tree --write-tree --name-only` first. Then `git merge --no-ff --no-commit origin/main 6b0ba7b14f9985cddd0d8cbc8ad27430c9acb9d2` (one merge with two extra parents; if git refuses, stop and report to Root, no unplanned intermediate commit). No rebase, reset, amend, force, cherry-pick, patch, copy or hand-authored source. Any unmerged path, semantic conflict or defect stops with precise evidence; no fix under an invented grant, alias, scope or counter reset.

Invariants after staging (hash or `git diff` proofs): every non-tracking child path equals the child blob; every main-only path equals main; `src/core/pyproject.toml` parses with `tomllib`, holds main's `iothub` extra and `dev` pins (`azure-iot-hub==2.7.0`, `six==1.17.0`) and the child's scoped `disallow_untyped_calls = false` stanza for the draft module group, and the older sensor-consumer exemption group is unchanged (not broadened); API test line `# type: ignore[no-untyped-call]` present exactly once; no change to flags, `PROPOSED_UNAPPROVED`, served write refusal. Excluded: unmerged aftercare #1400 and unmerged sibling branches.

## Environment (owned only)

Create `/tmp/z109-pi-1110/venv`. Install only after an observed missing-dependency failure, from pinned manifests (`mypy==2.4.0`, `ruff==0.17.1`, `mssql-python==1.15.0`, `playwright==1.64.0`, `azure-iot-hub==2.7.0`, `six==1.17.0`, and what Core and API runtime need), never into shared or the child's venv. Import sources via `PYTHONPATH` from this worktree and verify actual import origin of `sensor_review_draft`, `device_registry_azure`, API server, check module and test helpers resolve inside this worktree (a first-try venv that resolves to the other worktree is wrong and is rebuilt). `PYTHONDONTWRITEBYTECODE=1`, external `HOME` and mypy caches, synthetic fixtures only.

## Checks (raw outputs, commands, true exit codes under `ROOT/checks-109-prospective-integration-1110/`)

1. Import origin and TOML parse.
2. Core, from `src/core`: `tests.test_sensor_review_draft` (expect 65, 22 opt-in skips), `test_sensor_analysis*` (expect 30, 10 skips), `tests.test_scenario_manifest`, `tests.test_device_registry_azure` (offline, no provider).
3. API, from `src/api`, CI-style `PYTHONPATH`: `tests.test_sensor_review_draft_api` (expect 6, 0 skips).
4. Configured Core `ruff check .`, `ruff format --check .`, `mypy --no-incremental` (expect pass; scoped exemptions disclosed, not strict).
5. Configured API `ruff check .`, `ruff format --check .` and `mypy --no-incremental` with the CI `PYTHONPATH` (child reported red 1 then green 220 files; here a red is a stop, not a fix); `node --check src/api/src/zava_forward/api/web/ops.js`.
6. Actual sensor browser check `checks.quality_sensors_browser_check`: one `flock -n /tmp/ama-rpi-heavy.lock` attempt with holder identification, cwd a short owned `/tmp/z109b.XXXX` (real dir), verify `Path.cwd()` fixture length is safe, `PYTHONPATH` to this worktree, synthetic fixture and local mock only, unchanged check, no patch or proxy. Expect 33 passed. BUSY stops that check; no queue, wait or spin. Remove the owned directory afterwards.
7. Fresh scoped MSSQL `tests.test_sensor_review_draft.MssqlDraftCases` (22 expected, 0 skips) under one `flock -n` attempt with an own disposable container (pattern of `ROOT/checks-111-parent-adoption-1855/run-mssql.sh`, adapted to this worktree and owned venv, no password logged, container removed). Decision rule: the earlier 22-case run on child `2b050647b` carries only if Core SQL and dependency inputs are unchanged. Here main adds a Core dependency (`azure-iot-hub`, `six`) and Registry source, so the composition is new for Core; run it fresh rather than carry, and record the inputs. BUSY or missing prerequisite is reported and blocks that check (no cloud fallback).

Skips are not passes. Carried gaps, never described as passes: unforced `ConflictError` and `CommittedReloadError`; scoped Core mypy exemptions; API `App` suppression (exact-call); opt-in skips; no WCAG or assistive-technology claim; no Azure Hub, Azure SQL, live UI or model acceptance; local synthetic SQL only.

## Stop rules

Fetched identity drift, merge conflict, a failing configured check, missing prerequisite beyond the owned-env install, BUSY lock, refused marker, or any new defect: stop, preserve evidence and state, report. No self-heal, retrospective record, correction pool or counter reset.

## Follow-up and criteria

A #440 sensor-integration checkpoint remains due before epic closure or dependent expansion; Root routes it. All #109, #111, #110, #184 and #185 criteria stay open. A later PR would use `Refs #109 #111` only.
