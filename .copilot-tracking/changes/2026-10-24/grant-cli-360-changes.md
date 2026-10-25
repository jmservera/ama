# Changes: grant-cli-360

* infra/scripts/grant-application-admin.py: `--apply` builds `setup.Azure` with
  `body_directory=setup.private_path(profile, directory=True)` inside the try block.
* infra/tests/test_grant_application_admin.py: `OfflineAz` double and `GrantCliTests` (6 tests).

## Validation
* `python3 -m unittest infra/tests/test_grant_application_admin.py`: 10 OK.
* With the script change stashed: 3 new tests fail (body storage unavailable).
* No Azure, m365 or Graph call; no live state touched. Tooling fix only: it does not prove owner
  login or a fresh directory assignment.
