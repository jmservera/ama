# Issue 444 current-main integration (round 3) details

Date: 2026-10-25. Plan: ../../plans/2026-10-25/issue444-main-ea5577b2-integration-plan.md.

## Phase 2

* Local backup branch `backup/444-pre-round3-ab07351a` at ab07351a (not pushed). Fetch origin; `git rebase origin/main`.
* Verify after: resident source and tests diff against ab07351a is empty; log.md adds only the #444 entry versus main; README diffs versus main only add #444 content; `.github/rubric` equals main.
* Identity: repo-local noreply email from `gh api user` (verify), Copilot trailer on commits.

## Phase 4

Venv /tmp/ama444/venv, pip only. Core and api full suites, ruff, mypy. Browser check src/api/checks/resident_preview_browser_check.py picks free loopback ports and temp data itself (distinct from 8350/8444/8445); expect 36 PASS.

## Phase 5 review boundary

Whole `git diff origin/main...HEAD`: source, fixtures, tests, web assets, READMEs, tracking. Against #444 criteria: scope denial, grant revocation, representative authority, offers vs confirmed, unavailable actions, allowlist projection, XSS/CSP/host, plain language and accessibility semantics, using the fetched guidelines. Reviewer must state what it did not verify.

## Phase 6

Fetch; if remote branch is still 9c896630 push `--force-with-lease=feat/resident-feedback-preview-444:9c896630107156f8bb82b49c7730931ec97d8d3b`. Edit PR body: Refs #444 only; exact head, base, evidence or pending gate; limits. Confirm closingIssuesReferences empty. Queue `python3 -B tools/rpi-checks.py --all --base <origin/main> --out <new dir> --lock-timeout 14400` in the background after cleaning ignored caches; report PID and log; verify the receipt when complete. If the bot advances the head, inspect the delta and refresh.

## Critique amendments (applied directly)

* C1 (blocking): commit every tracking artifact (research, plan, details, critique, state, changes, review) before the gate; require `git status --porcelain --untracked-files=all` and `git ls-files --others --ignored --exclude-standard` both empty.
* C2 (blocking): after the gate passes, fetch and compare the remote branch with the gated SHA. If the bot advanced it, inspect the delta, and rerun the complete gate for the final pushed SHA.
* C3: push with `git push origin HEAD:feat/resident-feedback-preview-444 --force-with-lease=feat/resident-feedback-preview-444:9c896630107156f8bb82b49c7730931ec97d8d3b` after a fresh fetch.
* C4: rebasing local ab07351a already omits bot commit 9c896630, so main's latest.json is kept with no manual edit; the rubric conflict occurs only if replaying the bot commit.
* Gate ordering decision: gate the final committed local head, then push; because the bot may re-score after the push (C2), any bot commit triggers inspection and a refresh.
