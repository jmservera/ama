---
title: "HVE Builder Static Review 1: AMA Repository Instructions and Backlog Delivery Coordinator"
description: "Fresh-context independent static review (improve mode) for .github/copilot-instructions.md and .github/agents/ama-backlog-delivery-coordinator.agent.md."
ms.date: 2026-11-15
---

## Review Scope and Metadata

* Mode: `improve`
* Reviewer context: fresh-context independent static review
* Worktree: `/home/azureuser/source/ama-demo-wt/docs-hve-builder-coordinator`
* Target 1 (`instructions`): `.github/copilot-instructions.md`
* Target 2 (`agent`): `.github/agents/ama-backlog-delivery-coordinator.agent.md`
* Reference standards applied:
  * `skills/hve-core/hve-builder/references/requirements-catalog.md`
  * `skills/hve-core/hve-builder/references/review-rubric.md`
  * Repository Markdown and workflow conventions in `.github/copilot-instructions.md`

## Requirement Verification Summary

1. Default `tmux` RPI worker model updated to `--model gemini-4-carbon` (`--claim-model gemini-4-carbon`): verified in `.github/agents/ama-backlog-delivery-coordinator.agent.md` across `rpi_phase_witness.py record launch` (line 615), the `copilot` CLI command in the launcher heredoc (line 639), and the launch model requirement prose (lines 655 to 657).
2. `tmux` launcher creates `/mnt/tmp`, exports `TMPDIR=/mnt/tmp`, and redirects `< /dev/null`: verified in `.github/agents/ama-backlog-delivery-coordinator.agent.md` (lines 636 to 641).
3. Concurrency target (`8` live native `rpi-*` `tmux` sessions, no numerical active-issue cap when using coherent parent stacks) and stacked-PR CI economy (`src-ci.yml` on any PR branch vs `rubric-score.lock.yml` on `main` only): verified in `.github/agents/ama-backlog-delivery-coordinator.agent.md` (lines 102 to 105 and 375 to 380) and `.github/copilot-instructions.md` (lines 206 to 210).
4. Review-correction cycle limit updated to 5 total cycles per issue (preserving spent cycles, finite extensions, and at least 3 scoped diagnostic RPI cycles with validation): verified in `.github/agents/ama-backlog-delivery-coordinator.agent.md` under `Human blockers` (lines 51 to 59) and step 6 (lines 822 to 829).
5. Adaptive 10 to 30 minute delivery schedule cadence plus hourly cleanup maintaining `/mnt/tmp`: verified in `.github/agents/ama-backlog-delivery-coordinator.agent.md` under `Recurring schedules` (lines 198 to 204).
6. Local pre-push `src-ci.yml` parity commands (`mypy` inside `src/<project>`, `ruff format --isolated --line-length 100 --check` on `infra/` Python files, `src/api/tests` on `PYTHONPATH`, `scenario-manifest.json` recipe SHA sync, and `test_accessibility_baseline.py` / `test_content_standard.py` guards): verified in `.github/copilot-instructions.md` (lines 67 to 83) and `.github/agents/ama-backlog-delivery-coordinator.agent.md` (lines 387 to 395).

## Rubric Dimension Assessment

### 1. Purpose and activation (Architecture fit, Subagent design, Frontmatter currency)

* Status: Pass
* Evidence:
  * `.github/copilot-instructions.md` preserves its capability-bearing frontmatter (`description` and `applyTo: "**"`) unchanged.
  * `.github/agents/ama-backlog-delivery-coordinator.agent.md` preserves its `name` and routing `description` frontmatter unchanged and keeps `model:` omitted in frontmatter so the coordinator session stays on Automatic while explicitly passing `--model gemini-4-carbon` to delegated `tmux` CLI worker sessions.
  * Agent `tools:` configuration is outside static review scope per the rubric and tool-configuration boundary.

### 2. Authority and load timing (Load-timing placement, Reference discipline, Extension precedence)

* Status: Pass
* Evidence:
  * Always-loaded repository-wide pre-push CI parity rules and PR check trigger distinctions (`Source projects CI` vs rubric scoring on `main`) are placed concisely in `.github/copilot-instructions.md` because every contributor and worker needs them before pushing or stacking PRs.
  * Coordinator-specific orchestration rules (adaptive 10 to 30 minute delivery schedule, `/mnt/tmp` launcher environment setup, `gemini-4-carbon` worker claim/launch flags, 5-cycle review-correction cap, and 8-session stack concurrency) remain scoped to `.github/agents/ama-backlog-delivery-coordinator.agent.md`.
  * Both files cross-reference canonical workflows and references (`.github/workflows/src-ci.yml`, `scenario-manifest.json`, `src/README.md`) without duplicating full external schemas or weakening existing gates.

### 3. Instruction quality (Workflow contract, Outcome and structure, Emphasis calibration, Model fit, Evaluation hooks, Context handling)

* Status: Pass
* Evidence:
  * Connected stage gates agree across both files and across internal sections of the coordinator agent: `Human blockers` (lines 51 to 59) and step 6 (lines 822 to 829) state the identical 5-cycle review-correction rule, preserved history, finite extension handling, and minimum of 3 scoped diagnostic RPI cycles with validation.
  * Pre-push `src-ci.yml` parity checks are concrete, runnable commands (`python3 -m mypy`, `python3 -m ruff format --isolated --line-length 100 --check`, `PYTHONPATH` entries, manifest SHA sync, and targeted test modules) grounded in observed CI failure modes (`Living documentation` and `Mechanically checkable where possible`).
  * The explicit `--model gemini-4-carbon` and `--claim-model gemini-4-carbon` updates are internally consistent and include an explicit no-silent-fallback blocker rule if the model is unavailable.

### 4. Safety and containment (Safety and enforcement, Reviewer bounding, Evidence fidelity)

* Status: Pass
* Evidence:
  * Adding `< /dev/null` to the `copilot` CLI invocation in the launcher script prevents non-interactive worker hangs on unexpected standard input reads while keeping `--deny-tool 'shell(git push --force)'` intact.
  * Creating `/mnt/tmp` (`mkdir -p /mnt/tmp 2>/dev/null || true`) and exporting `TMPDIR=/mnt/tmp` in the worker launcher and maintaining `/mnt/tmp` in the hourly cleanup contract prevent root-disk exhaustion without loosening the finite per-run manifest rules in the `Cleanup contract`.
  * All human blockers, safety/privacy/accessibility review gates, and exact-head verification requirements remain intact.

### 5. Style and repository conventions (Convention conformance, Portability and maintenance, Stale-pattern absence)

* Status: Pass
* Evidence:
  * Exact `git diff` inspection confirms `*` is used for all unordered list items, plain ASCII punctuation is used throughout, no em dashes (`—`) or en dashes (`–`) are introduced, and no bolded-prefix list items are introduced in new or modified bullets.
  * Heading hierarchy and fenced `bash` code blocks follow repository conventions.

## Findings

No Critical, High, Medium, or Low findings identified.

## Verdict

* Verdict: `Pass`
* Evidence path: `/home/azureuser/source/ama-demo-wt/docs-hve-builder-coordinator/.copilot-tracking/hve-builder/2026-11-15/coordinator-instructions-static-review-1.md`
