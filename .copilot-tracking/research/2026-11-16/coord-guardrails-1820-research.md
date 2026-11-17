---
title: Research for issue 1820 coordinator worker-brief guardrails and model fit
ms.date: 2026-11-16
---

## Scope

Issue #1820: add worker brief guardrails (phase-witness ordering, execution hygiene) and model-fit guidance to the Backlog Delivery Coordinator instructions. Base `origin/main` 5e0c7f74432ffce73cfeaa672e4e40a605ca6274; branch `docs/coordinator-guardrails-models-1820`.

## Research disposition

`executed` (direct inspection). Planning Readiness: `Ready`.

## Placement rationale

* `.github/agents/ama-backlog-delivery-coordinator.agent.md` Step 5 ("Run one RPI loop per issue", line 578) already owns brief generation, the phase-witness call list (lines 600-604) and the launch model rule (line 630: Sonnet 5.5 for all launched RPI sessions). Launch and orchestration rules are coordinator-specific, so the new guardrails belong there.
* `.github/copilot-instructions.md` applies to every agent and contains no model names (grep for "model" finds none relevant). It stays model-agnostic and is not changed.

## Evidence

* `tools/rpi_phase_witness.py record` accepts `research-open`, `plan-done`, `implement-start`, `implement-done`, `review-done`, `commit-complete` with `--claim-commit`; it observes canonical artifacts named by `--state`, so the artifact must exist before the call.
* `tools/rpi-checks.py:93` defines `HEAVY_LOCK_PATH=/tmp/ama-rpi-heavy.lock`; line 3269 defines `--lock-timeout` default 600.
* Existing line 630 mandates Sonnet 5.5 for all issue sessions; the new guidance must refine it (validation-only/docs-only loops may use gemini-4-carbon or Automatic) rather than contradict it.

## Behavior-bearing assessment

The change alters coordinator behavior (brief contents, model choice). HVE canonical static/behavior evidence is limited to what is runnable locally: a static review of the diff for internal consistency, and a justified non-applicability for a full simulated behavior run (no executable code path; no hve-builder-tester fixture exists for this agent file). Independent exact-head review is required.
