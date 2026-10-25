# Research: grant-application-admin.py --apply failure (issue 360)

Date: 2026-10-25 (directory dated 2026-10-24 to sit with the issue 360 artifacts)
Task: grant-cli-360. Base: origin/main 5d79aaee. Research disposition: executed (read-only, local).

## Honest ordering note
The one-line fix and its first tests were written before these artifacts. Research reading
below was done first, but the written research, plan and details were committed after the
first edit. No pre-implementation critique ran. The phase order deviation is recorded here and
in the review; nothing below is a retrospective claim of an earlier phase.

## Findings
* infra/scripts/grant-application-admin.py main() built `setup.Azure(args.tenant_profile)` with no
  `body_directory`.
* `setup-entra.py` `Azure.call` (lines ~140-185) writes any request body to a
  `NamedTemporaryFile(dir=self.body_directory, delete=False)` and removes it in a `finally`. With
  `body_directory is None` it raises "Mutation body storage is unavailable in read-only mode."
  So dry run worked, `--apply` failed at the POST.
* setup-entra `contexts()` supplies the body directory only for non-readonly runs, after
  `private_path(profile, directory=True, create=...)` which refuses symlinks, in-repo paths and
  non-0700 directories.
* Existing tests (infra/tests/test_grant_application_admin.py) exercised only grant() with a fake
  graph, so the entrypoint defect was invisible.
* The earlier live grant used the grant() function directly with a body directory.

## Options
* A (chosen): in main(), pass `setup.private_path(profile, directory=True)` as `body_directory` only
  when `--apply`; reuse the existing temp-file lifecycle. Dry run stays read-only.
* B: always pass a body directory. Rejected: gives dry runs write capability and a new failure mode.
* C: new temp-file helper. Rejected: duplicates the existing mechanism.

## Out of scope
sensor_consumer ALTER COLUMN, live Graph calls, permissions, deployment.
