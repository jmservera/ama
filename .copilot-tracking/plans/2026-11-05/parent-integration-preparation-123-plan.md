<!-- markdownlint-disable-file -->
# Plan: parent topic integration preparation (#123, Refs #440 #128), 2026-11-05

Research: [research](../../research/2026-11-05/parent-integration-preparation-123-research.md). Details: [details](../../details/2026-11-05/parent-integration-preparation-123-details.md). Critique: [critique](parent-integration-preparation-123-critique.md).

Validation tier (prospective, coordinator confirms): FOCUSED, only while the final fresh-main-relative scope stays bounded metric tooling, tests and documentation. Not documentation only: it includes the constructed `paired_equity.py` diagnostic and its tests. Any mixed infrastructure, security, SQL, finance, deployment or big-feature expansion stops for reclassification to FULL and new coordinator admission.

## Phases

* [ ] Phase 1: Resolve privacy-safe identity (`gh api user`, repository-local email) and verify no unexpected changes.
* [ ] Phase 2: Preflight that `origin/feat/discovery-assurance-integration-123` still equals `63dd5798`; merge that pinned SHA into the local topic (ordinary merge commit, no reset, rebase or force). Expected fast-forward-eligible; keep a merge commit only if Git requires one. Record the resulting identities.
* [ ] Phase 3: Merge the recorded fresh main `bb3a3b03` (ordinary merge commit). Preflight: prove `origin/main` still equals `bb3a3b03` and merge the pinned SHA. `git merge-tree` (critique) shows `docs/reference/log.md` auto-merges without conflict; resolve nothing manually, then verify both sides' log entries survive in order. Stop only on an actual conflict or ambiguous intent.
* [ ] Phase 4: Recompute the complete final fresh-main-relative scope (files, additions, deletions, source versus documentation) and re-confirm or reclassify the tier.
* [ ] Phase 5: Append one dated integrated source-qualified checkpoint to `docs/architecture/cutover-evidence-pack.md`, one link in `docs/reference/README.md` and one append-only entry in `docs/reference/log.md`.
* [ ] Phase 6: Light local observation only: paired-equity unit tests (and coupled core test modules if cheap), explicit source-path assertion, Markdown link and anchor check of changed docs, JSON parse, `git diff --check`, append-only check. record actual commands, exits and skips. Record the tested tree; after the commit prove `HEAD^{tree}` matches and rerun `git diff --check` and the link check against committed `HEAD`.
* [ ] Phase 7 (baseline: only this task's `.copilot-tracking` research, plans, details, changes, reviews and rpi-sessions records are untracked and intended for the final commit): Single review of the final candidate; commit RPI records and checkpoint with Conventional Commit message, privacy-safe identity and Co-authored-by trailer; freeze, verify clean tracked, untracked and ignored state.

## Planned parent validation (PENDING after coordinator admission; not performed in this task)

Final selected-tier validation on the actual final candidate, run by the coordinator's admitted gate and not by this preparation:

* Directly relevant tests: paired-equity, journey-register, release and invalidation, ranking-publication and cohort-evaluation modules (historical 74 tests is context, not a required count or pass).
* Core Ruff check, Ruff format check and configured mypy including tests, from the core project.
* Applicable offline requirement and design traces; known trace blockers stay blocked, never fake passes.
* Changed Markdown links and anchors, append-only checks, JSON parse and `git diff --check`.
* Actual final candidate source, import and base identities recorded with the run.
* Independent exact-head review, hosted checks and the guarded merge remain coordinator-owned. Child receipts are historical and are not parent results. Shell commands are not imported from receipts.

## Boundaries

* No new runtime behaviour; `fairness_evidence=False` and `activation_allowed=False` unchanged; no production mapping, approved threshold, actual-model evaluation or human approval is inferred.
* No push, pull request, issue, board or acceptance mutation; Refs only, never closing keywords.
* No cleanup, deletion, archive, stash, reset or worktree removal.
