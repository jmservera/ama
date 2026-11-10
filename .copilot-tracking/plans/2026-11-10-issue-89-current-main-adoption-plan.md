# Plan: issue 89 current main adoption (2026-11-10)

* [ ] 1. Validate unique-key JSON in its own call, then record implement-start (source clean, changes registered).
* [ ] 2. Ordinary `git merge --no-ff` of `origin/main` 6cc59776. Mechanical overlap only; parse TOML and derive any manifest hash from resulting bytes. Substantive conflict or defect: abort and HOLD.
* [ ] 3. Preservation proofs: tree against both parents, original RPI and witness bytes, append-only log lines of both sides, dependency and source identities.
* [ ] 4. Targeted tier in the own environment. Non-heavy first. Heavy SQL and browser only under a non-queued `flock -n /tmp/ama-rpi-heavy.lock`.
* [ ] 5. Real changes, validate, implement-done; one review, validate, review-done; commit, literal HEAD, commit-complete; verify; handoff.

Critique: `.copilot-tracking/plans/critiques/2026-11-10-issue-89-current-main-adoption-critique.md`. Details in the matching details file. No push, PR, rebase, reset, amend, force, hook bypass, source repair or new agents.
