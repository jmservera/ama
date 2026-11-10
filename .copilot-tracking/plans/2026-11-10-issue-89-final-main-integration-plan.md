# Plan: issue 89 final main integration (2026-11-10)

* [ ] 1. Record implement-start with source clean (already fast-forwarded to 4f5dc38), then `git merge --no-ff` main 65c2ab9.
* [ ] 2. Resolve only the mechanical scenario-manifest conflict: keep the parent `workbench` hash and main `recipe` hash, each checked against the actual file sha256 of the merged tree. Anything else: abort and HOLD.
* [ ] 3. Preservation proof: merged tree versus each parent, original RPI bytes, append-only log, app.js both intents.
* [ ] 4. Targeted tier in an owned venv; non-heavy first; heavy served/browser/SQL only under a non-queued holder lock.
* [ ] 5. One review, commit tracking, witness records, verify, handoff.

Critique: `.copilot-tracking/plans/critiques/2026-11-10-issue-89-final-main-integration-critique.md`. Details in the details file. No push, PR, rebase, reset, amend, force, hook bypass, source repair.
