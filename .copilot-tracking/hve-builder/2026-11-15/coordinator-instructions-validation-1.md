---
title: "HVE Builder Mechanical Host Validation: Coordinator and Instructions"
description: "Mechanical host validation log for .github/copilot-instructions.md and .github/agents/ama-backlog-delivery-coordinator.agent.md."
ms.date: 2026-11-15
---

## Stage Inputs

* Stage: `validate` (mechanical host validation)
* Target artifacts:
  * `.github/copilot-instructions.md` (`instructions`)
  * `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`agent`)
* Evidence path: `.copilot-tracking/hve-builder/2026-11-15/coordinator-instructions-validation-1.md`
* Source write boundary: read-only on target source files; write only this validation log.

## Evidence Inspected

* `.github/copilot-instructions.md` frontmatter and 12 relative Markdown links
* `.github/agents/ama-backlog-delivery-coordinator.agent.md` frontmatter, 6 relative Markdown links, and `bash` fenced code block at line 632
* `git --no-pager diff` output across `.github/copilot-instructions.md` and `.github/agents/ama-backlog-delivery-coordinator.agent.md` (65 added/modified lines)

## Mechanical Validation Checks

| Check ID | Validation Check | Owner | Status | Evidence Summary |
| --- | --- | --- | --- | --- |
| VAL-01 | YAML frontmatter parses cleanly (`description` and `applyTo` on `.github/copilot-instructions.md`; `name` and `description` on `.github/agents/ama-backlog-delivery-coordinator.agent.md`) | `local` | `Passed` | `yaml.safe_load` parsed both frontmatter blocks cleanly with exact expected keys (`['description', 'applyTo']` and `['name', 'description']`). |
| VAL-02 | Relative Markdown links resolve to existing files in workspace | `local` | `Passed` | All 12 relative links in `.github/copilot-instructions.md` and all 6 relative links in `.github/agents/ama-backlog-delivery-coordinator.agent.md` resolved to existing paths (`src/README.md`, `docs/reference/method/tracking-retention-policy.md`, `docs/architecture/cutover-evidence-pack.md`, `.agents/skills/*`, `docs/reference/research/ux/*`, and `.github/skills/web-design-guidelines/SKILL.md`). |
| VAL-03 | Repository Markdown style conventions on changed lines (`git --no-pager diff`) | `local` | `Passed` | Inspected all 65 added/modified diff lines and surrounding blocks: unordered lists use `*`, all characters are plain ASCII (`ord(c) <= 127`), zero em/en dashes, zero bolded-prefix list items, and the fenced code block at `.github/agents/ama-backlog-delivery-coordinator.agent.md:632` specifies `bash`. |
| VAL-04 | No unexpected mutations to target source artifacts during validation | `local` | `Passed` | Target files were inspected read-only; `git diff` on tracked files remained unchanged. |

## Stage Result

* Validation result: `Pass`

## Limitations

* Only local mechanical validation checks were executed in this stage; hosted CI workflows (`src-ci.yml` and `rubric-score.lock.yml`) run on pull request publication.

## Next Action

* Return `Pass` to the parent HVE Builder workflow for final outcome resolution.
