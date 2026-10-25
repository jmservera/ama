# Phase details: grant-cli-360

* Phase 1: `main()` computes `body_directory` inside the existing try so a `SetupError` from
  `private_path` (symlink, in-repo, mode not 0700, missing) prints `refused:` and returns 1 before
  any az call. Dry run keeps `body_directory=None`.
* Phase 2: tests patch `setup.subprocess.run` (not `grant()` or `Azure`), so token inspection,
  Graph reads, the POST with `--body @file` and the finally-unlink all run for real. The profile is a
  0700 directory under the system temp directory (outside the repository).
* Authorization contract (tenant/app/OID checks, role and member checks, write-permission refusal,
  idempotency, readback wait) is unchanged.
