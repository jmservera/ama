# Details: issue 360 live re-run

## Phase 2

* Add section "Re-run at 11:30 UTC" with: config snapshot facts, anonymous curl, browser-mode 302, staff sign-in, role probes, and the resident-account finding.
* Resident account finding: `~/.ama-resident-test-user` is the credential of the separate resident showcase login on `ca-resident-demo`, not an Entra identity, so it cannot serve as a second staff role. Second-role denial stays unproven.
* Per-criterion table: a to f with proven/unproven and basis.
* No secrets; evidence in `.copilot-tracking/evidence/2026-11-18/issue-360-live-rerun/`.

## Phase 3

* One log entry at the end of `docs/reference/log.md`.

## Validation

* Link check of changed docs, secret literal scan of evidence, `git diff --check`. No src change, so no mypy, ruff or rpi-checks.
