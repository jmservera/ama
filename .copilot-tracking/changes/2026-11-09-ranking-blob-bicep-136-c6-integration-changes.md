# Changes: C6 parent integration (Refs #136, #1258)

Plan: `.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-c6-integration-plan.md`. Date 2026-11-09. Tier: owner-selected DEMO-targeted. No source edit was made by this lane.

## Changes

* Prospective research/plan/details/critique committed first as `735069b4e17101c6908b1ed5b4065a91bd755fb6` (child of `fba4273a4`, four tracking files only).
* Local `--no-ff` merge `437f68ca9f4ec840b886724b41770a36a2a19707` of exact parent `99814198079c7c8fcd641497826986c706627b0f` (tree `0658fe7f...`); parents `735069b4e` and `99814198`; tree `3bf3cc7e041366baccde5a2a7ca5f21ff72b7142`, equal to the recomputed `git merge-tree` prediction; no conflict. `git diff fba4273a4 HEAD -- infra` is empty: the child's Blob Bicep, parameter and test files are byte-identical. The merge brings main `5c3b8b4be` through the parent only; `origin/main` `1a84b3b0` and sibling #1259 code are not merged. No rebase, reset, force or parent mutation.
* Critique PC-1 (Blocking, merge identity after records commit) and PC-2 (Minor, hash inventory) applied before the merge.

## Commands and exits (integrated head; tools: Python 3.12.3, ruff 0.17.3 local vs CI pin 0.17.1, az bicep)

| Command | Result |
| --- | --- |
| `infra`: `az bicep build --file main.bicep --stdout` | exit 0 |
| `infra`: `az bicep lint --file main.bicep` | exit 0 |
| `infra`: `az bicep build-params --stdout` for `iot-hub-live`, `main`, `main.pilot.example`, `main.test` | exit 0 each |
| `infra`: `python3 -m unittest tests.test_bicep_policy tests.test_identity_rbac tests.test_secret_lifecycle tests.test_api_ingress_transport tests.test_governance` | exit 0, Ran 100 OK |
| `src/core` (fresh `/tmp` venv, editable installs of this worktree): discover `test_ranking_archive_blob.py` | exit 0, 25 OK |
| same, `test_ranking_publication_runner.py` | exit 0, 45 OK |
| same, `test_ranking_publication.py` | exit 0, 57 OK |
| `src/api`: discover `test_ranking_publication_wiring.py` (`PYTHONPATH=../core/tests:../agents/tests`) | exit 0, 35 OK |
| import check of `ranking_archive_blob.SELECTOR` and `CONTAINER_VAR` | `ZF_RANKING_ARCHIVE`, `ZF_RANKING_BLOB_CONTAINER` (unchanged; the policy test also parses them) |
| `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py` | exit 0 |
| `ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py` | exit 0 |

## sha256 of qualified inputs on the integrated head

```text
c8b52c6c4f67b5003c192d851197115612f5ba52cb6fa91210d564b40afb8c02  infra/main.bicep
612c218c2321490c296a67a37a37340fd3108e2495b57db72261e3f5eb1391e1  infra/modules/storage.bicep
d741041f351d12f1a9b751ff5197b03e7fe7e7ebc534ab3b5937c835ac83d6bf  infra/modules/containerapps.bicep
e8a0acb68fff46d170c4022234c929b0bcc2133bc246325463ed96f0f11cd8da  infra/modules/guard.bicep
f4aa7e296551ef5aff4b36dc6ed19f5a0ae47bd56bf7db121d953bec5c54e16a  infra/iot-hub-live.bicepparam
51b3507d6989ca4ef65b7a445d4d0a09eaaa6fd305f22814d5536ca0e6dda7ba  infra/main.bicepparam
b5aa7f00bb584aa92f54b8c7e6bc1f24b0d0d17ce6683e5b149962041b74f7d0  infra/main.pilot.example.bicepparam
82fa0c3456ee142d7cac12cf36e3fd4171179883d175b23bda13c1152f1db5a7  infra/main.test.bicepparam
672b18699c69626f1291203446816d1a4514057c1efb3474bc7f9e4d0cd2e253  infra/tests/test_bicep_policy.py
4ac0b5811827ff660492baeabb859d44761b19aa90262391a8b7328b9ab90589  src/core/src/zava_forward/core/ranking_archive_blob.py
275035b3b91ab8fd878425c80abbd69dbb0c8e75eed3381ebf255f4f2614d364  src/core/tests/test_ranking_archive_blob.py
fe971299f7a42f64fe09e53252e913d679bea505e2cbc3f5f0031abe60c6ca67  src/core/tests/ranking_blob_fixture.py
c25f022ca7646b691a624e0135e90d6617cb6ccb0e445c2540b5f13901f272ca  src/api/tests/test_ranking_publication_wiring.py
```

## Skipped, absent, not claimed

Full Core84/API9+10 parent profiles (parent-owned, not rerun to refresh metadata), full rpi-checks, SQL, browser, Docker, scanners, cloud what-if, deployment, identity grants, account/storage calls, model calls, emulator, runtime. No WORM lock, approved retention duration, migration or container-scoped role (account-scope Blob Data Contributor still permits delete). Parent independent Functional review `362c0bec-b992-4f6f-bb93-4a6c5506c8a6` was still running: publication blocked; if the parent changes, preserve this qualified source and record a refresh. Adverse records of earlier child runs are untouched.
