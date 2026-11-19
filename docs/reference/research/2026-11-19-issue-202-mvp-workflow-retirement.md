---
title: Issue 202 mvp workflow retirement evidence (2026-11-19)
ms.date: 2026-11-19
---
Scope: the single unticked criterion, "Old workflows (`mvp-ci`, `mvp-validation`) removed or replaced, and branch protection required checks updated". Demo, desktop only; no Azure resource involved.

Research disposition: executed. Planning Readiness: Ready (outcome is a stop-and-report).

## Evidence

* `mvp/` and `prototype/` are absent from the worktree (`ls` fails for both).
* `.github/workflows/mvp-ci.yml` and `mvp-validation.yml` still exist but are already replaced in content: both are `workflow_dispatch` only, named `Source CI` and `Source validation`, and run `src/*` packages. `src-ci.yml` is the active pull request workflow.
* Rulesets (`gh api repos/jmservera/ama/rulesets`): `main` is disabled, `mainprotect` is active; neither lists a `required_status_checks` rule. Classic branch protection returns 404 (not protected). No required check names `mvp-ci` or `mvp-validation`, so no check needs repointing.
* Remaining references to the file names: `tools/rpi-checks.py` (workflow list lines 72-81 with pinned SHA-256 values, job map lines 2517-2520), `tools/check-legacy-references.py:54`, `tools/test_src_cutover_repoint.py:126`, `infra/tests/test_pipeline.py` (lines 129-365), `infra/README.md`, `.github/workflows/src-ci.yml` (paths filter line 5, actionlint line 281) and `.github/rubric/README.md:641`.

## Classification

Deleting the two workflows edits workflow files, a gate tool with pinned hashes (`rpi-checks.py`), its tests and the `src-ci` path filter and actionlint step. Per repository instructions that changes gate semantics and needs the FULL tier with an external full receipt. The brief forbids `rpi-checks.py --all` and any protection change, and the owner has reserved the branch-protection update for a deliberate post-cut-over step. The criterion therefore cannot be completed here.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Parity matrix, owner agrees | Ticked in issue | Not re-proven |
| `prototype/` removed, no tracked file | Ticked; re-observed absent | `ls prototype` fails |
| Archive tag recorded | Ticked in issue | Not re-proven |
| Rubric registry PR merged first | Ticked in issue | Not re-proven |
| Old workflows removed or replaced, protection updated | Unproven (blocked) | FULL tier needed; protection change out of scope; no required check references them |
| No tracked file under `mvp/` | Ticked; re-observed absent | `ls mvp` fails |

## Addendum, 2026-11-19 re-observation

The active `mainprotect` ruleset carries a `required_status_checks` rule whose list is empty (`gh api repos/jmservera/ama/rulesets/<id>`), and `main` has no classic protection (HTTP 404). No required check names `mvp-ci` or `mvp-validation`, so nothing needs repointing. Removing the two workflow files still edits pinned-hash gate tooling and needs the FULL tier with an external receipt, so the criterion stays unticked. Working files: `.copilot-tracking/research/2026-11-19-issue-202-live-research-r2.md`.
