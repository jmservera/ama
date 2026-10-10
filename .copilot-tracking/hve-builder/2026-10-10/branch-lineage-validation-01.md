---
title: Branch Lineage Mechanical Validation
description: Low-profile final local validation for the branch-lineage instruction update
ms.date: 2026-10-10
ms.topic: reference
---

* Mode: validate.
* Target: `.github/copilot-instructions.md`.
* Approved write boundary: this log only.
* Profile: Low.
* Behavior report consumed: `.copilot-tracking/hve-builder/2026-10-10/branch-lineage-behavior-report-01.md`; final simulation was Complete/Pass. Human-review box remains unchecked; no regrade performed.
* Pre-validation workspace: branch `chore/branch-lineage-guidance`; source was modified and the tracking directory was already untracked.
* Pre/post source SHA-256: `86b083ef217752368c7c093dadd26945acfa2ad4e536290bf034c93e59742acf`; unchanged.

## Checks

| Check | Owner | Status | Evidence |
| --- | --- | --- | --- |
| `git diff --check` | local | Passed | Exit 0; no output. |
| Pinned Markdown lint | local | Passed | `markdownlint-cli2 v0.18.1`; 7 files; 0 errors. MD013 remained excluded by the supplied configuration. |
| Frontmatter and protected bytes | local | Passed | Frontmatter, every byte before `## Branch and Pull Request Workflow`, and every byte from `## Knowledge Base Conventions` onward match `origin/main`. |
| Markdown rendering and decision table | local | Passed | `python3` with installed `yaml` and `markdown`; tables extension rendered the decision table; all required situations were present. |
| Table width inspection | local | Passed | Rendered table widths were consistent: `[[2, 2, 2, 2, 2]]`. |
| Safety, privacy and owner-merge clauses | local | Passed | Required clauses were present in both baseline and target. |
| Source hash consistency | local | Passed | Matches behavior-report candidate SHA-256 above. |
| CI lane | CI | Not requested | No CI lane was requested or required for this local artifact-validation outcome; hosted merge checks remain separate `Pending CI` when a PR exists. |
| Distribution wiring | local | Not applicable | Existing repository instruction; no new distributable artifact. |

## Tool and workspace notes

* The `python` command was unavailable; no installation was attempted. The required read-only checks ran successfully with `python3` and the installed `yaml` and `markdown` modules.
* Post-validation source hash remained unchanged. No Git mutation, network access, agent, source edit or new source artifact was performed.
* The approved log is the only write made by this validation stage.

## Result

* Mechanical validation: Pass.
* Overall stage result: Pass.
* Next action: stop this validation report; hosted merge checks, if a pull request exists, remain separately governed.
