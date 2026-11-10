<!-- markdownlint-disable-file -->
# Details: Blob plus Quality merged-main qualification (2026-11-09)

Recorded 2026-11-09T22:53Z before observation.

* Merge: `git merge --no-ff origin/main` (resolved SHA 1b7a1719b). Expected: src identical to main, local docs retained. Additive-only doc conflicts may keep both sides; otherwise stop.
* M1: from a fresh issue-qualified mktemp dir, `flock -n /tmp/ama-rpi-heavy.lock env -i HOME PATH PLAYWRIGHT_BROWSERS_PATH python -m checks.quality_sensors_browser_check --axe <owned copy of axe-4.10.3.min.js> --out results.json`, in the owned venv (preserved from the parent run; editable installs re-pointed or verified against the merged worktree).
* Fixture: the check's constructed synthetic seed, mock provider, SQLite in the owned dir, loopback server. No ZF_DATA, no network beyond localhost.
* Expected: exit 0, guarded-off refusal label and separately labelled seeded rendering; axe may report serious contrast incompletes, reported in detail. A failure is preserved and routed to #1288 without a fix.
* Evidence: stdout, stderr, exit, start and end times, versions and SHA256SUMS copied to the session files; scratch kept; only my own helper PIDs stopped.
