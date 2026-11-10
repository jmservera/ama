# Research: integrate frozen #1258 C5 parent into the #136 Blob Bicep child (Refs #136, #1258)

Date 2026-11-09. Disposition: executed (read-only git and tool inspection). Planning Readiness: Ready. Prospective: no integration, merge or check run had happened when this was written.

## Findings

* Child HEAD `a23f5d3c64e760a3aeadef833728eb33752afe0e` is clean; its original RPI records (`2026-11-09-ranking-blob-bicep-136-*`, review Approve with Minor F1 applied) are preserved and not edited.
* Pinned parent `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8`, tree `20901b61eddb68d3740f6976187d17ff5fc0cea2`, is a commit object present locally and is exactly one commit above the child seed and merge base `f724f4bca`. It is NOT on main (fetched `origin/main` `daf45a46ca85b93cfac510ef6f8b2d685dec5136`, not merged); #1292 is still pending and is not imported.
* Parent delta (13 files): C5 `_parse_listing` in `ranking_archive_blob.py`, Core and API tests, `src/core/README.md`, six `ranking-archive-blob-1258-c5-*` records and state. The env contract constants `ZF_RANKING_ARCHIVE` and `ZF_RANKING_BLOB_CONTAINER` and the `azure-blob` selector are unchanged, so the environment interface used by the Bicep wiring does not change.
* Child delta touches `infra/`, `infra/README.md` and its own records. `git merge-tree` of the two heads reports a clean merge (tree `2e47aa63575590cc49ae2ec85160d5e6b3639a9f`); the two README intents sit in different files (`src/core/README.md` and `infra/README.md`).
* Prior productive review corrections for this child: exactly one (review F1, restore of a removed `# noqa: S307`, applied in `a23f5d3c6`). The repository default is five total per issue; this integration is not a review-correction cycle and no reset or extra grant is requested. The original review was authored, not an independent coordinator review.
* Formatting baseline (retained adverse evidence): plain `ruff format --check` and the CI command `ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py` both FAIL at child HEAD. The same CI command PASSES on the seed `f724f4bca` copy, and the diff touches only lines added by this child (four hunks), so existing lines need no reformatting. Plain `ruff format` without the CI flags would reformat the whole file and is not the project command (`.github/workflows/src-ci.yml` lines 243-244, `infra/README.md` line 1193). `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` is the matching CI lint.

## Gaps and absences (not claimed)

No runtime, emulator or real-account behaviour, no WORM or immutability lock, no approved retention duration, no folder-record migration, no deployment, and the existing account-scope Blob Data Contributor still permits delete. No role, key, SAS, public access, capacity or paid resource is added by this integration.
