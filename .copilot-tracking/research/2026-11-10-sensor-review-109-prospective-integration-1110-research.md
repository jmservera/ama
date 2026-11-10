---
title: Issue 109 prospective local integration research
ms.date: 2026-11-10
task_id: 109-prospective-integration-1110
---

## Objective

Build and test, locally only, the PROSPECTIVE composition of fresh `origin/main` and the exact reviewed child head into this topic while the child's new-head hosted CI runs. Integration only: no new product, test, config or source behavior. This is a prospective, implemented-unverified local integration. It is not the delivered remote parent, not main, and not the actual PR #1395 merge. Root changed local sequencing for this; actual child merge and admission still gate publication, and nothing is pushed while #1395 is open (a push of the parent would alter the child PR diff).

## Attribution correction (additive; original records untouched)

The original preparation chain (commit `a3d5e615f0b2617b40cd5bdd23d00db0be11284e`, six `.copilot-tracking` files, witness `phase109-integration-preparation-evidence-1110` with three events launch, research-open, plan-done) stays as written. The earlier report there that `verify` exited 0 was incorrect: the shell `$?` was taken after a pipe to `tail`. Re-run directly in this session, `verify` on that chain exits 1 with four missing future phases (implement-start, implement-done, review-done, commit-complete). That chain is not retrospectively completed; this task uses a NEW canonical chain `phase109-prospective-integration-evidence-1110`.

## Exact identities (after `git fetch`, 2026-11-10 ~15:40Z)

| Ref | Identity | Note |
| --- | --- | --- |
| local topic HEAD | `a3d5e615f0b2617b40cd5bdd23d00db0be11284e`, tree `288c39d9cb527bf605c48241568eced8a4776e62`, clean | `6cc59776` plus the six-file preparation commit |
| `origin/main` | `c66370042eb08f07839d054433f4483078703cf2` | After `6cc59776`: `eff05737e` (#1396 docs, NomUX and Bicep checkpoint records, `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `log.md`, one `.copilot-tracking` state) then `c66370042` (rubric score metadata only, `.github/rubric/scores/latest.json`). No BRD, PRD, ADR, `src`, `infra` or `tools` change. |
| remote `feat/demo-sensor-review-109-1110` | `06374dfcac47cf6bcce9e7b91f573e8565ab45e8` | unmoved, an ancestor of main; not pushed |
| child `origin/feat/demo-sensor-drafts-111-1110` = PR #1395 head | `6b0ba7b14f9985cddd0d8cbc8ad27430c9acb9d2`, tree `8906ef415145fb6819fa638df6cb094a18976c03` | parent `2b050647bff51eef4c1b34d6434bba7eae3d5f9a`. PR open, mergeable, base is the declared parent. |

PR #1395 live hosted checks at observation: mssql, src-core, src-agents, src-importer, src-namespace, src-orchestrator, image-paths, src-changes, src-no-working-data pass; src-api pending. Not final; hosted success is not claimed.

## Dry-run evidence

`git merge-tree --write-tree --name-only` of local HEAD with the child head exits 0, no conflicted paths (tree `1ef571e30feccaf03c6d9cb3df8b1b3ee70cd9b1`); of `origin/main` with the child head exits 0 (tree `7c652a3665811867aa8de693c5b3a084ce5d31c4`). A clean ordinary merge is predicted. The child contains the remote parent `06374dfcac` as an ancestor, so both ancestries are kept.

## Child delta since the earlier preparation (`2b050647b` to `6b0ba7b14`)

Eight paths: seven dated `.copilot-tracking` C2 records and `src/api/tests/test_sensor_review_draft_api.py` (3 insertions, 1 deletion): `app = App(self.store, PASSWORD)  # type: ignore[no-untyped-call]` with a justification, an exact-call suppression of the legacy untyped `App`. No config, production, UI or dependency edit. It is not strict typing of `App` and not a global policy change.

## Child boundaries and main overlap (unchanged from the preparation research, re-confirmed)

* Child net source: `sensor_review_draft.py`, `projection.py` (+1), API `server.py` GET `/api/cases/<id>/sensor-drafts` and POST `/api/cases/<id>/sensor-draft`, `ops.js`, `quality_sensors_browser_check.py`, two test files, scoped Core mypy override in `src/core/pyproject.toml`.
* Main-ahead Core source: Registry (#1393) `device_registry_azure.py` and its tests, `src/core/README.md`, `src/core/pyproject.toml` `iothub` extra and `dev` list (`azure-iot-hub==2.7.0`, `six==1.17.0`), workspace oracle repair (#1392) in `script_retry.py`, two workspace browser checks and `test_workspace_scripts.py`. Only `src/core/pyproject.toml` is touched by both sides, in disjoint hunks. The Core SDK pins and the child mypy stanza must both survive.
* Old Core mypy exemptions (the sensor-consumer and `test_historical_backfill` group, and the draft module group) remain disclosed and are not to be broadened. API mypy: configured `strict = true`, `files = ["src","tests","checks"]`, API `server` is in an `ignore_errors` override; the child's earlier red (one untyped `App` error) is fixed by the exact-call suppression.

## Child evidence read

`handoff-111-api-type-c2-1110.md`, `handoff-111-short-cwd-browser-1110.md`, `pr111-c2-qualified-1919.txt`, plus the earlier parent-adoption handoff and `independent-111-parent-adoption-1869` report. Independent reviewer 1b06482a: bounded approve, zero findings, for the child tree `8906ef41` (source, API typing, browser) against the old parent, not against this composition. Child-reported results: configured API mypy red (one error, 220 files) then green; six API draft tests, zero skips; Ruff and format on the touched file; Node syntax check of `ops.js`; actual sensor browser check 33 passed from a short owned cwd after the first launch failed (Chrome `Socket path too long`, preserved, not a pass); actual MSSQL 22 cases, 0 skips, carried forward on source-qualified identity (the earlier run was on the staged `2b050647b` composition, not a literal later commit); Core ordinary runs had 22 and 10 opt-in skips, which are not SQL passes. Unforced `ConflictError` and `CommittedReloadError` branches remain coverage gaps.

## Requirement and decision status (document-qualified; unchanged since the preparation research)

BRD (`docs/brds/agentic-retrofit-programme-brd.md` v0.21.0, draft): FR-048, AC-090, OD-43. PRD (`docs/prds/zava-forward-retrofit-programme-demonstrator.md` v0.21.0, in-review): FR-050, AC-066 to AC-068, all "Not run". ADR 0003 decision 6: owner-accepted with amendment 2026-10-15, no deployment, cost, credential, DPO or live approval. BRD AC-066 to AC-068 and BRD FR-050 are different requirements. BRD draft and PRD in-review are candidates, not owner-approved. Final source flags, default-off, `PROPOSED_UNAPPROVED`, served-write refusal, consent withholding and role denial must remain unchanged by this integration. #109 "Not implemented" is historical; all #109, #111, #110, #184 and #185 live criteria stay open.

## Environment facts

* The child venv `/tmp/zf-111-1110/venv` has editable installs of core, agents and api pointing at the OTHER worktree `issue-111-sensor-draft-1110` and lacks `azure-iot-hub` and `six`. Using it directly could silently import the wrong source and would fail Core mypy on the Registry module. A task-owned venv under `/tmp` with this worktree's sources on import path is needed; installs only into that owned env, after an observed missing-dependency failure, never shared.
* The browser check hard-codes its fixture root at the current directory, so it must run from a short owned cwd (for example `/tmp/z109b.XXXX`), as the child's supplement did, with `PYTHONPATH` pointing at this worktree and actual import origins verified. No patched check or proxy.
* Heavy lock `/tmp/ama-rpi-heavy.lock` was free at a zero-cost probe. Heavy checks take one non-queued `flock -n` attempt each; BUSY stops with holder identification, no waiting.
* Node v24.21.0 is available for `node --check`.

## Planning readiness

Ready. Research disposition: executed (read-only git and gh reads; no tests run yet). Candidate versus approved distinctions preserved.
