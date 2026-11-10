<!-- markdownlint-disable-file -->
# Research: Bicep public-simulation current-main observation (#440, 2026-11-10)

Status: complete (findings added after the witness `research-open` record). Disposition: executed (new investigation of a new trigger; the earlier NomUX records are unrelated and untouched). Planning Readiness: Ready.

## Scope and trigger

* Brief: `ROOT/brief-440-bicep-observation-1334.txt` (exact launch brief). New completed-feature-wave trigger, not a retry of the NomUX execution (committed `e2f55915b`, Root-verified seven records), not the old C6, no new source budget. Docs-only: no command, test, gate, image, SQL, browser, cloud, model, live or private-data run.
* Trigger: PR 1380 (`Refs #136`, published head `1752260338f519a79cb427448bd7c45c34ae80ff`, 19 reported checks) merged 13:29:38Z as `0a6dc0b3f0b3ecf098536369a8308b02226b98b8`, tree `55e6b6a36b9e53378f2c0cc8d7172d307fd2b8e4`, parent `83503b74e` (rubric bot commit).

## Verified identities (read-only git and gh, this session)

* `origin/main` equals `0a6dc0b3...` at launch; this topic branch stays at `e2f55915b` on base `65c2ab9d9` by explicit choice (no merge or rebase).
* Subtrees at the pin: `src` `70d956b06f31cabfd8321b4ee9c203ae8b21d89c` (unchanged by this infra merge), `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `docs` `c8dba5f98ac3`, `.github` `d1fbaeba4b94`.
* Diff `83503b74e..0a6dc0b3f`: 54 files, 1882 insertions, 8 deletions; no `docs/` change, so the BRD, PRD and ADR blobs equal those recorded in the NomUX section.
* Bicep blobs at the pin: `infra/main.bicep` `7074af59dbc8`, `infra/modules/guard.bicep` `f08d8b235078`, `infra/modules/containerapps.bicep` `da71bef970a9`, `infra/README.md` `b4a2a2c49a3d`, `test_bicep_policy.py` `751afd16a69c`, `test_public_simulation_startup.py` `c68c04cfcc8f`, `test_resident_demo_deploy.py` `77237ef15d76`. Pack `5f223b53b7ed`, index `28b3ec408855`, log `058338f4903c` at the pin (before the NomUX commit on this branch).
* Documents unchanged: BRD `docs/brds/agentic-retrofit-programme-brd.md` 0.21.0 draft `34d88395de86`; PRD Zava Forward `c788b917bafa` 0.21.0 in-review; PRD Proper Warm `f7f9b7675e60` 0.13.0 in-review; ADR-0006 `956da1a3b804`; ADR-0007 Proposed `abb21088a9bb`. Statuses are not approval.
* Issues read live, all OPEN: #136, #89, #133, #132, #1288, #440, #1384, #1388, #130, #149. Number 1400 does not resolve (not an issue or PR); nothing is opened or closed.
* Local aftercare candidate: branch `feat/demo-quality-workflows-89-1109` at `c6c0e4d2590eab632238e45cfec0c009d15691e1`, `src` subtree `3ad519b53426`; not an ancestor of `origin/main`. It awaits Root consumption of the NomUX gate.

## Source facts (static read of the pin)

* `main.bicep`: `enablePublicSimulationLane` default false; five guards (`publicSimulationRequiresDirectDemo` needing `demoDirectIngress` and the development profile, `...BrowserAuthentication` needing `entraClientId` and not `entraBearerOnly`, `...Applications` needing `deployApplications`, `...RealApiImage` rejecting the quickstart placeholder, `...SingleReplica` requiring `apiMinReplicas <= 1`); forwarded to `containerapps.bicep`.
* `containerapps.bicep`: `command` is null when off and a fixed `python -c` recipe when on; `ZF_SIM_STORE=/state/public-simulation/store.sqlite` and `ZF_SIM_KEY_FILE=/state/public-simulation/hmac.key` only when on; `maxReplicas` is 4 when off and 1 when on. The recipe provisions only when both files are absent, opens (validates) the lane, prints an error code to stderr on any exception (import failure included) leaving files untouched, then runs the ordinary API module.
* README: replica-local volatile state (lost on replacement or scale to zero), accounting unchanged on Azure SQL (`ZF_STORE=mssql`), a restart that retains a valid key and store does not itself revoke seals, loss or replacement of the pair invalidates prior seals, the `apiImage` guard rejects only the placeholder, no deployment, Azure, MSSQL, auth, live IoT Hub or model evidence.

## Consumed Root evidence (read, not re-run)

* `handoff-136-current-main-verification-1314.md` and `checks-136-current-main-verification-1314/`: aux `b9bae9f2b51c67e2edc0fbe0d4ccdc7aaa856e63` tree `fd357610b99e9c14461e6de9a50150fc9a9d9770` (published head merged with then-main `65c2ab9d9`; prediction equal). Raw exits re-read: policy 60, container contract 7, resident demo 17, secrets 16, IoT Hub 23, API simulation 30, live control 34, Core resident 41, ruff check and format 0, resident mypy 0, six offline Bicep build and lint 0. Supplemental mypy over policy and startup tests exit 1 with three baseline errors in `tests/test_bicep_policy.py` (lines 2023, 2024, 2047), unwaived. Two image attempts with the heavy lock busy exited 1 and are retained as adverse history; the old `d6d6` image is not current proof.
* `handoff-136-image-later-admission-1324.md` and `checks-136-image-later-admission-1324/`: one non-queued build exit 0, image id `sha256:38361713e1856ab6ae0b749b542ee0f99717e60fd55985b8445e7aa8eccd1d98` (manifest identity, not config digest), four startup tests `Ran 4 ... OK` exit 0 (fresh start and reuse, partial or corrupt left untouched, slot crossing, unimportable lane module). Local JSON-store harness: not MSSQL, auth or Azure evidence.
* `136-current-main-prediction-1332.json`: main `83503b74e` plus head predicted tree `55e6b6a3...` differs from tested aux only at `.github/rubric/scores/latest.json`; `src`, `infra`, `tools` subtree ids equal. The actual merged main tree equals the prediction (read here with `git rev-parse`).
* `independent-136-current-main-composition-1326/{functional,readiness}`: 54-file, 2423-line packet, approve, 0 findings each; original published-175 reviews and C1-C5 adverse and chronology qualifications unchanged.
* PR comment 6768612559 holds the dated actual qualifications; the 19 PR-head checks SUCCESS and MERGEABLE before merge are PR-head metadata, not a result for the merge commit.

## Limits and decisions

* No command is claimed on `0a6dc0b3f`; aux observations are source-qualified local runs; current-tree equivalence is metadata (tree ids).
* Azure observed: NONE. No live SQL, auth, resident or model acceptance. Whole #136, #1288 and #440 remain unmet. No human approval invented.
* No new defect confirmed, so no new issue; the three baseline policy mypy errors are known and tracked, not newly fixed. #1384 and #1388 are separate checker work with no source waiver.
* Keep the NomUX record (`65c2ab9d9`, historical) unchanged; the new section is distinct; the old CSV-learning record and frozen review 912 are untouched.
