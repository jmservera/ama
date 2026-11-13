# Details: 113-platform-auth-verify-1222

Phase 1 (verification): modules as listed in the research artifact. Commands run from the component directories; bare unittest module names (mssqlstore rerun as `tests.test_mssqlstore` from src/api). Phase 2 (evidence): write changes.md with per-module counts (parsed from verbose logs), skip reasons, log sha256, exit codes. Phase 3: cleanup of /tmp/venv-113-1222 and logs, review, commit.

Constraints: no Docker/MSSQL/browser/network; no reads of .env or ~/.zava-forward; no src/ or docs/ edits.
