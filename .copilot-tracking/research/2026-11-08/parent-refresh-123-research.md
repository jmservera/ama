<!-- markdownlint-disable-file -->
# Research: discovery parent refresh onto current main (#123, Refs #440 #128), 2026-11-08

Prospective: written before any merge. Continues native session b1e0f493 after the 2026-11-07 [reconciliation research](../2026-11-07/parent-reconciliation-123-research.md); that record and its author Review are unchanged.

## Preconditions observed (read-only)

* Worktree `/home/azureuser/source/ama-wt/integration-123`, branch `feat/discovery-assurance-integration-123`, HEAD `5beb7ba7d50dda8435b6ca9f34a6f7b3a0cfd749`, ignored-inclusive clean. `origin/feat/discovery-assurance-integration-123` equals HEAD. PR #1222 is OPEN, base main.
* Fresh `origin/main` is `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (#1267 ranking checkpoint). Earlier base was `b284d0d3`; the merge base with HEAD is still `b284d0d3`.
* Output directory `/home/azureuser/.local/share/ama/gates/c123-f14-1108` is absent.
* Prior partial receipt `g123-f13-1108` failed verification after main advanced the API server dependency. It is preserved as an adverse result and is not reused.

## Main-side delta (HEAD...origin/main)

* 324 files, +9256/-31. 311 are `.copilot-tracking` records of other tasks. Non-tracking: `.github/rubric/scores/latest.json`, evidence pack, `docs/reference/README.md`, `docs/reference/log.md`, `src/api/.../server.py`, `src/api/tests/test_ranking_publication_wiring.py`, `src/core/README.md`, `src/core/pyproject.toml`, `ranking_publication.py`, `ranking_publication_runner.py`, `store.py` and two ranking test files.
* This is main's already merged and reviewed ranking publication work (#1239, #1267). It is not part of this topic's own delta and is not touched by it. Main does not touch `paired_equity.py` or `test_paired_equity.py`.
* `git merge-tree --write-tree` forecasts a clean merge (tree `8493726d`) with no conflicts. The evidence pack, log and README append sections auto-merge. Rubric blob on main is `6741ddd6` (our side `4dd831ed`, unchanged by us since the base), so the merged blob must equal main's.

## Tier reassessment

* This topic's own delta remains the constructed-cohort paired-equity diagnostic, core tests, README, checkpoint documentation and RPI evidence. No SQL, security, auth, policy, infrastructure or deployment feature is introduced by it. The main-side ranking and API changes arrive through an ordinary merge of reviewed main and are not implemented here. FOCUSED stays, as admitted. A newly introduced full-tier category in a conflict resolution would stop work.
* The `--changed` selection will be recomputed read-only on the final candidate; the main-side API and core changes plausibly keep all projects, images and `logo-0600` selected. The admission authorises those derived groups only; browser, mssql, infra and migration are not authorised.

## Known facts that stay separate

* API SQLite versus SQL Server: gate tests skip SQL Server cases without an owned server; skips are not passes.
* Fixtures are not model, accessibility or human acceptance. `fairness_evidence=False` and `activation_allowed=False` stay unchanged. Whole #123, #128 and #440 and AC073 remain unaccepted. The joint support bundle is not split and not called a fixed finding.

## Planning readiness

Ready. Disposition: executed (read-only inspection of the exact local and main diffs, prior plan and state).
