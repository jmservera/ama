---
title: Coordinator Sonnet 5.5 Author Evidence
description: Bounded HVE Builder improve author stage for launched RPI session model selection
ms.date: 2026-10-20
---

## Scope and requirements

* Mode: improve; author stage only.
* Source write boundary: .github/agents/ama-backlog-delivery-coordinator.agent.md.
* Evidence write boundary: .copilot-tracking/hve-builder/2026-10-20/coordinator-sonnet-55-author-01.md.
* Worktree: /home/azureuser/source/ama-wt/coordinator-sonnet-55.
* Branch: docs/coordinator-rpi-sonnet-55; upstream origin/main.
* Owner requirement: "Write this in your coordinator instructions, use Sonnet 5.5 model for all the RPI loops to make them faster."
* Owner clarification: "I was referring to the launched sessions, this one can stay on Automatic".
* Caller-provided CLI evidence: local help supports --model <model>, and claude-sonnet-5.5 appears in the host model list. No independent runtime or performance claim is made.

## Baseline

* Initial git status --short: clean in the assigned worktree.
* Baseline HEAD: 993a7b88c03f5240f1e7a4c7c7afa7c064281622.
* Baseline target Git blob: 0d6fd620c2df39f1644eb6a448a3cfb7db3a2936.
* Existing step 5 launches native copilot --agent hve-core-all:rpi-agent inside a named tmux session without an explicit model argument.
* The existing contract requires isolated issue worktrees, RPI artifacts, original RPI Review, independent assessment, local validation receipts and publication/merge gates. Retries and correction cycles already exist.
* Author finding A1: the launch command does not pin the requested model, and its text does not extend that selection explicitly to retries, corrections and validation continuations.
* Coordinator Automatic mode is preserved as requested. No frontmatter or default configuration change is authorized or made. Tools configuration is opaque and was excluded from inspection and decisions.
* No exploration, research, delegation, issue implementation, commit, push or PR operation is part of this stage. Unrelated primary-checkout changes remain untouched.

## Authoring and rationale

* Added --model claude-sonnet-5.5 to the existing native launch command; preserved its route, agent, permissions, denial, prompt, logging and session structure.
* Added one adjacent rule applying that argument to every coordinator-launched RPI issue session, explicitly including retries, corrections and validation continuations.
* Preserved coordinator Automatic mode and independent reviewer selection explicitly.
* Required a specific model/tool blocker for the affected loop only when unavailable, with no silent model fallback.
* Classification: Medium. This selects a caller-requested launch model parameter within the existing execution route, rather than adding a new action, output, authority, gate or non-tool frontmatter capability. No independent reviewer, permission, parallelism or gate changes are introduced.
* Canonical criteria applied: requirements-catalog.md, Outcome and structure: stop rules and missing-evidence behavior; Evaluation and validation: revise surgically and evidence, not assertions; Safety and enforcement: preserve non-tool capability fields; Tool-configuration boundary. workflow-contract.md supplies baseline, change classification and stage-status vocabulary.

## Stage result and limits

* Authoring status: Complete.
* Author self-check: the diff is limited to the requested launch argument, adjacent model rule and this evidence file. Existing source outside that insertion is unchanged.
* Self-check results: git diff --check passed; exact body-delta assertion passed; zero-context diff has one hunk at baseline line 167 and no frontmatter changes. Final status lists only the target modification and the new owned evidence directory.
* Static review: not run by this author; reserved for the parent lifecycle.
* Medium behavior gate disposition for parent handoff: Satisfied-and-skipped; execution status Not run; verdict Not applicable; fidelity Not applicable. Reason: launch-parameter adjustment within the existing issue-session workflow, with no materially new action, output, authority or gate.
* Mechanical validation stage: not run by this author. Bounded git diff --check and exact-delta checks are author self-checks, not an independent validation verdict.
* No RPI session was launched; no tests or tooling were added. Faster execution is the owner's objective, not a measured result.
* Next action: parent performs the remaining applicable lifecycle stages. This record claims author-stage completion only, not overall HVE Builder Pass.
