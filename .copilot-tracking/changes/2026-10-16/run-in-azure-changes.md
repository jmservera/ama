---
title: In-VNet staff initialization changes
description: Implementation and validation evidence for Refs #360
ms.date: 2026-10-16
---

## Scope

Full plan 360-run-in-azure. P01 complete; P02 validation/delivery active. One critique executed,
PC-001 through PC-008 accepted. No Azure execution or image build authorized.

## Amendments

Worker-owned restart replaces the initial operator-only proposal to honor the
literal requirement. A standalone Bicep template grants only API reads/restart
to the existing SQL-admin identity; it is not deployed in this task.
The logs interface has a documented running-pod dependency; hold encrypted
results briefly while polling, then require successful execution status.

## P01 Implementation

* Added explicit/automatic Azure candidate/check/apply transport, with no
  fallback after uncertain local apply or validation refusal.
* Canonical SQL preparation now accepts a lazy person resolver, preserving
  existing pre-Graph validation order. Worker receives locally resolved people,
  uses MSI SQL, rereads after commit and invokes canonical replica convergence
  through a fixed-target MI ARM adapter.
* Proof image adds two modules, the existing initializer/roster helper and
  manifest. Original proof entrypoint and installed package/driver base remain.
* Standalone Bicep adds API-only custom restart role and ama guard, separately
  inventoried/tested in role-assignments.json. No identity or broad role added.

## P02 Evidence and adjustments

* Fake az covers explicit/fallback setup, generated admin/seed preservation,
  codes-free Azure output, secret transfer, encryption, source guards, timeout,
  job/start/create/log/stop/delete failure, interruption and collision.
* Local input is bounded to 12 KiB for secret transport. Job tags retain
  existing source governance tags. Each command honors execution deadline;
  cleanup has its own 90-second budget and ownership/absence proof.
* A pre-provisioning 404 after an uncertain create is not called cleanup proof.
  Cleanup refusal prints owned resource name and exact runbook recovery.
* ARM registry responses may include null username/password reference fields.
  Guards accept those empty fields but reject populated credentials; the job
  receives only the reconstructed server/MI pair. The final 304-test run
  includes this realistic response fixture.
* Updated runbook, cut-over acceptance table, reference index and append-only
  log. CI now gates the new Python modules/test with Ruff and scoped mypy.
* Existing role-matrix parser handled only built-in roles; extended it with a
  separate inventoried custom-role assertion rather than weakening the matrix.
* No package manifests changed. Missing local source distributions and
  Ruff/mypy were installed using pip in a session-only venv after validation
  failed for missing packages/tools. No system-environment override.

## Validation

Targeted staff tests: 34 passed; setup tests: 95 passed. Final full infra
run: 304 passed without skips (including all targeted cases).
Standalone Bicep build/lint passed without Azure access. All ten CI-gated infra
Python files passed Ruff/format; new worker/transport mypy passed.
Responsive loopback app auth suite: 32 passed; synthetic missing-law-store
diagnostic is expected, not a raw private-data failure. No live model call.
Live image build, role deployment, job/log/private SQL, real Entra/browser,
cross-host enforced mutex and human acceptance remain Not run/unmet.

## Review Handoff

Implementation and docs are ready for one Review. No source blockers or plan
divergences remain. The live prerequisites are explicit acceptance gaps, not
reported passes. Review owns later-work routing; no current-task correction loop.
Publication (privacy-safe commit/push/PR) follows the recorded review outcome.

## Publication

Implementation commit: 37af66e, pushed to origin/feat/run-in-azure-360.
PR: https://github.com/jmservera/ama/pull/370, targeting main, Refs #360.
Authenticated owner account was resolved before committing; author and
committer use the repository-local privacy-safe noreply address. No merge,
force-push, issue checkbox mutation or Azure execution was performed.

Review execution is Complete; outcome Residual work. Implementation is
delivered; authorized image/role activation, live acceptance and serialized
operator recovery remain distinct follow-ups, not active implementation.

The installed commit/PR commands referenced supplemental instruction files
not present at their advertised paths; no repository citation-policy file
was found. Repository/user conventions were used. Existing tracked
.copilot-tracking/pr/pr.md was not overwritten; PR body and generated XML
reference were kept in the session workspace.
