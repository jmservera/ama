---
title: Issue 200 phase details
ms.date: 2026-10-16
---

Task #200 / `repoint-ci-to-src-200`. Parent plan:
`.copilot-tracking/plans/2026-10-16/repoint-ci-to-src-200-plan.md`.

<!-- P01 -->
## P01: Runtime and automation

<!-- P01-T01 -->
### P01-T01: API and CI

Delegate API __main__ to existing server.main under a normal main guard.
Test delegation without opening sockets. Both the API image probe and namespace
API invocation explicitly run `python -c 'from zava_forward.api.version import __version__; print(f"zava-forward-api {__version__}")'`,
not silent version-module execution or a server startup that hangs namespace CI. Preserve workflow names,
concurrency groups and job IDs. Trigger existing checks on src/** so shared build
pins and dockerignore changes are covered too.

<!-- P01-T02 -->
### P01-T02: Isolated images

Remove orchestrator wheel/source from API Dockerfile. Keep pinned stages and
requirements. Bicep token maintenance and digest jobs use orchestratorImage;
retain token-maintenance and API ledger identities. Do not change SQL/blob grants.
Test compiled containerapps template commands and images, not textual proxies.
Keep explicit versioned image parameters; never rewrite historical deployed tags.

<!-- P01-T03 -->
### P01-T03: Data and tooling

Extract the existing synthetic path resolution into core.data_paths and delegate
synthetic.output_dir to it so runtime never imports synthetic tools; explicit filename
must not be replaced. Update the isolated installed-CLI fixture's dependency list.
Patch factory in its existing migrated style. Test default,
configured folder and custom filename via mocked Store (no private filesystem read).
Repoint branding HTML/CSS, policy hash and public logo destination. Retain historical
branding assertions and add a no-mvp-output assertion. Existing generator and
coverage package imports were already correct; generator now shares data_file
directly so a custom ZF_DATA filename stays exact. Verify with mocked register
tests and installed imports, never a private run.

<!-- P02 -->
## P02: Evidence and delivery

<!-- P02-T01 -->
### P02-T01: Local validation

Create/restore /tmp/zf164 tools with pip only after confirmed missing tools.
Install source packages in a task-local virtualenv after missing-package failure.
Absolute PYTHONPATH covers sources and shared fixtures without touching installed
packages in another worktree. Docker works via sudo -n; uniquely name task containers
and clean only task-created resources. Bicep 0.48.1 available locally.
Record commands, counts, exit codes and limitations in changes artifact.

<!-- P02-T02 -->
### P02-T02: Documentation

Update src index, API/orchestrator commands, infra live source-image recipe,
branding guide, root README and reference routing; append log only.
Preserve dated recipes, historical identifiers, snapshots and original case study.
Explain packaging and installed tooling in copilot instructions.

<!-- P02-T03 -->
### P02-T03: Review and publication

Review implementation once against plan and actual test evidence. Route remaining
cloud/owner gates, do not invent completion. Resolve gh identity before local git
email; commit only intended paths including new artifacts, excluding github-issues.
PR uses Refs #200, local results and unmet criteria; push only specified topic.

## Current implementation handoff

P01, P02-T01 and P02-T02 complete. Four focused test methods added, none removed.
All five full suites and static checks passed; the final generator refinement
passed all 14 generator tests and repeated core static checks. Bicep/infra,
branding, namespace, link/syntax/data guards and four local image checks passed.
P02-T03 awaits the single Review and publication only. No source blocker remains.
Azure rollout/private backup/owner sign-off remain external acceptance gates.
