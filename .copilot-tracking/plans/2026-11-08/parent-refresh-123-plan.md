<!-- markdownlint-disable-file -->
# Plan: discovery parent refresh onto current main (#123, Refs #440 #128), 2026-11-08

Research: [research](../../research/2026-11-08/parent-refresh-123-research.md). Details: [details](../../details/2026-11-08/parent-refresh-123-details.md). Critique: [critique](parent-refresh-123-critique.md).

Tier: FOCUSED (admitted), bounded paired-equity tooling, coupled tests, documentation and support-bundle records. Not documentation-only. Any new SQL, security, auth, policy, infrastructure or deployment scope stops work for a Full-tier coordinator handoff.

## Phases

* [ ] Phase 1: commit this prospective Research, Plan, details, critique and state (planning commit) before any merge, with the fresh `gh api user` privacy-safe local email, Conventional Commit message and Copilot trailer.
* [ ] Phase 2: re-fetch; if `origin/main` is not `f548b65f` stop and replan before merging. Ordinary merge of `origin/main` into the topic (no rebase, reset, amend or force). Resolve only understood conflicts; none are forecast.
* [ ] Phase 3: verify the merge: both tips are ancestors; `.github/rubric/scores/latest.json` blob and mode equal main's and parse; evidence pack, log and README keep every historical line from both sides (checkpoint sections of the parent and of main present, no removals); `paired_equity.py` and its tests are byte-identical to the pre-merge topic; recompute the complete main-relative scope and re-confirm FOCUSED.
* [ ] Phase 4: light checks with bytecode off, external caches, installed source distributions or explicit current-source imports and declared tool versions: paired-equity, journey-register, release and invalidation, ranking-publication, cohort-evaluation tests (select actual files, count is not predetermined); core Ruff check, format check and configured mypy including tests; JSON parse of changed JSON; changed Markdown links and anchors; append-only checks; `git diff --check`. API-side tests only through the gate.
* [ ] Phase 5: write Changes, one author Review and final state as genuine records of what ran; any needed pack, index or log append is surgical (a refreshed parent-topic note) and append-only. Commit implementation and records before the gate, with Pending gate facts recorded as Pending at commit time.
* [ ] Phase 6: if `origin/main` advanced (for example a rubric-only commit), plan and normal-merge it before the final gate and re-run Phase 3 and 4 as needed.
* [ ] Phase 7: freeze: clean tracked, untracked and ignored; compute the actual `--changed` selection read-only; check physical and logical heavy lock ownership. Run `python3 tools/rpi-checks.py --changed --jobs 1 --lock-timeout 0 --base <fresh origin/main> --out /home/azureuser/.local/share/ama/gates/c123-f14-1108 < /dev/null`, no queueing, no skip token. Verify with `--verify-receipt <receipt> --required-scope partial --base <fresh origin/main>` from the same clean source. Gate results are emitted externally; no source commit follows.

## Critique dispositions (see critique)

* PR-001: `git fetch` immediately before the freeze and before the gate; if `origin/main` differs from the pin, stop and replan.
* PR-002: after any permitted late main merge, repeat Phases 3 and 4 and recommit refreshed records before gating.
* PR-003: run `git diff --check origin/main...HEAD` on the committed delta and validate JSON, links and records before the last commit.
* PR-004: verify each pre-merge tip's historical lines in the pack, log and README as an ordered, multiplicity-preserving subsequence of the merged file, and again after Phase 5.

## Stop conditions

* Main differs from the planned pin before a merge; an understood-intent failure in a conflict; new full-tier scope; selected groups outside the derived set (browser, mssql, infra, migration); lock held; failed group (return the scoped failure, no reruns or fixes).

## Boundaries

* No source, threshold, approval or requirement edits; `fairness_evidence=False`, `activation_allowed=False` unchanged. No push, PR edit, merge to main, issue tick, model or cloud call, private dataset or cleanup. Original and adverse records, the failed `g123-f13-1108` receipt and the #1231 R35 images and receipt stay untouched. Refs only; no closing keyword.
