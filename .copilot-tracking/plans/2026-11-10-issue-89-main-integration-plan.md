# Plan: issue 89 parent main adoption (2026-11-10)

* [ ] 1. Record `implement-start`, then fast-forward the local branch only to published `a05b7e6b2` (`git merge --ff-only`).
* [ ] 2. Ordinary merge of `origin/main` a600 (`git merge --no-ff`, Conventional message, `Refs #89`, Copilot trailer). Compare the result with the predicted tree `08fb66ce7...`. No conflict resolution beyond mechanical; any conflict or defect needing design repair is STOP/HOLD with raw reproduction.
* [ ] 3. Preservation proof: both parents' non-tracking blobs equal their side except the two auto-merged files; `docs/reference/log.md` keeps every line from both parents; Stage A six source files equal a05; main source equals a600 except the README merge.
* [ ] 4. Owner demo targeted tier in the owned venv `/tmp/i89-1110` (Core aftercare_intake, resident/adopted, API aftercare screen, static, auth, role tests, simulator and live control, configured ruff/format/mypy). Browser: consume the recorded e951 results by tree identity; aftercare browser is an unavailable baseline.
* [ ] 5. Review once, commit tracking artifacts and handoff, record witness events, return a clean local frozen candidate.

Critique (single, final candidate): see the critique artifact. Details: `.copilot-tracking/details/2026-11-10-issue-89-main-integration-details.md`. No push, PR, rebase, reset, amend, force or hook bypass.
