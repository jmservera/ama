# Changes: 218 RAI controls unit verification (74a93a137a)

* Scope: offline unit verification of Epic #218 modules (Refs #218, #220, #221, #222, #223; #219 release record covered by rai_release, rai_release_invalidation and assistant_release). Tracking-only; `src/` and `docs/` unchanged (`git status` showed no non-tracking changes after the run).
* Environment: venv with system site packages, editable `--no-deps --no-build-isolation` installs; `zava_forward.{core,agents,api}.__path__[0]` verified inside `child-218-rai-1222/src/<pkg>/src/`. `env -u ZF_DATA -u ZF_TEST_MSSQL`, `PYTHONDONTWRITEBYTECODE=1`, no Docker, MSSQL, Chromium or network. Venv removed.
* Command per module: `python -m unittest discover -s tests -p test_<module>.py -v` from `src/<pkg>`; exit code saved directly from the producer.
* Totals: 11 modules, 239 tests, all exit 0, 8 explicit skips.

| Package | Module | Exit | Ran | Skips | Log sha256 |
| --- | --- | --- | --- | --- | --- |
| agents | test_cohort_ai_eval | 0 | Ran 5 tests in 0.752s | 0 | 394547f9d243d4e9edc36146ff833aedae31ef2f2540fe196ac4713fe2644999 |
| agents | test_cohort_ranking_eval | 0 | Ran 20 tests in 0.836s | 0 | 9945a7ba416d10b75eb36d849e736149e5efdc2323e1ee1196e7bdb0159f3706 |
| agents | test_review_effectiveness | 0 | Ran 34 tests in 21.738s | 0 | d9e99bfad0540d70fa2c49deb45eaf9b167c534ef0a49b26bb0d08b48e6b5357 |
| api | test_assistant_release | 0 | Ran 60 tests in 169.547s | 7 | e91e94f2f73ab021e51c715004fc723c0b87fd155d0cb2fe1793aef779ee042d |
| api | test_operator_suspension | 0 | Ran 17 tests in 162.499s | 0 | 5a7f49e06f4ec3b1fa7c1af0eb834bf8ced40d6703046b7caf44c88bf0f4e382 |
| core | test_challenges | 0 | Ran 19 tests in 0.078s | 0 | 505bb92455d98dd5ca04c96f2d3bd66c759120b10cdfe20a4b2dd4b474674e71 |
| core | test_cohort_eval | 0 | Ran 25 tests in 0.337s | 0 | fc4c0f07a5dd0b5d4286d91a9d1a3d962c9fd07599bbdd7e5ad29c6a2f821b64 |
| core | test_hazard_referral | 0 | Ran 41 tests in 93.914s | 1 | 346b4bbcd727663cffb85b4dc13b4315f9ca3597d1bc9bcecfb914cb60955a91 |
| core | test_rai_release | 0 | Ran 6 tests in 0.032s | 0 | 65e615c4de7e9e5b0d21cbb301a7ee98a09a91d3fba8067f07f8e6d39b758582 |
| core | test_rai_release_invalidation | 0 | Ran 6 tests in 0.040s | 0 | 692afd868d4f1a6abfbf2d3d8e63f2f63f1bb4960ccbd59e74e9b373313cb63d |
| core | test_resident_assistant | 0 | Ran 6 tests in 0.037s | 0 | ad949c729468deb635fa4ba6649149523dbb1bf3cacac4d6654c0e67c59923ad |

## Explicit skips

* api test_assistant_release: 7 `MssqlUnleasedRevocation` tests skipped, "needs disposable SQL Server (ZF_TEST_MSSQL=1)". SQL durability of unleased revocation is not evidenced here.
* core test_hazard_referral: 1 skip, `test_json_postsave_audit_failure_reports_persisted_uncertainty` ("JSON-only separate-file audit ordering").
* #105/#106 task-registry/suggestions fallback: no dedicated module found; only test_resident_assistant (core) and test_assistant_release (api) run as nearest coverage.

## Acceptance-criteria boundaries

* Results are synthetic or scripted unit proof only.
* Human OQ-017, OQ-018 and OD-35 exercises (and any real operator, affected-person or reviewer practice) are not performed or evidenced.
* No browser (Chromium), SQL Server, cloud or live model checks ran. Validation tier Focused; not a complete-gate receipt.
