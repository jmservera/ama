---
title: Demo sites correction research
description: Local research for the owner-authorized live correction, with execution restrictions preserved
ms.date: 2026-10-29
---

## Research Brief

Prepare the coordinator's correction of both demo sites to latest main,
including the resident SQL projection prerequisite and the separate authority
extension. Audience: owner and deployment coordinator. Output: convergence
for a locally committed, reviewable handoff, not a claimed live deployment.
Trusted evidence root: `.copilot-tracking/`.

## Research Parameters

Focused posture, selected from the named commits, existing runbooks and explicit
deployment constraints. Research is read-only except dated evidence and state.
No `.env`, private data, credentials, Azure execution, GitHub CLI, push,
network/RBAC changes, image deletion or authenticated smoke tests.

## Direction Controls and Participation

The user explicitly requests all four RPI phases in order and local commits.
The later "do NOT use az" instruction controls execution despite earlier
live-change approvals. No alternate SDK or REST route will bypass it.
Non-interactive execution prevents clarification. Preserve blocked live work.
`git pull --rebase` was the first shell command and returned exit 0,
"Already up to date." Initial worktree is clean on
`ops/sites-redeploy-20261029b`, tracking `origin/main`.

## Extension Registry and Provenance

* Repository instructions: selected for branch, evidence, data and local gates.
* RPI research/plan/implement/review: selected by explicit full-loop request.
* Independent critique and Review: selected by RPI phase contracts.
* Web design/accessibility skills: not selected; no web edits or design audit.
* Deployment execution: excluded by the current no-az instruction.

## Questions and Candidate Areas

1. What SQL projection must precede the resident image?
2. What exactly does the unmerged #521 commit change and require?
3. What historical revision/digest evidence exists, and what remains unknown?
4. Which safe local checks and evidence can this round complete?

Start with #543's API README and SQL tests, #521's commit and runbook,
the prior redeploy artifacts, component READMEs and local gate tooling.

## Research Cycle Log

Cycle 1 completed inline in order; low-volume coupled evidence did not justify
research agents.

### Wider

Read merged #543's docs and original diagnosis, original two-app redeploy
evidence, #521's exact commit, component guides and validation manifests.
Reflection: the requested live sequence is documented but this round cannot
execute it. Historical healthy metadata cannot substitute for fresh backups.

### Deeper

Read the current view definition and reader/startup contract, and #521's
SQL renderer/migration and rotation plan. The main view includes the new
document projection; its schema apply is distinct from image deployment.
The #521 migration replaces the allowlist check transactionally but does
not extend existing rows. Current `/tmp/mv` editables point at another worktree;
validation must install this worktree's distributions under the heavy lock.
Reflection: neither rebuilding main nor changing app expiry alone enables
the January authority.

### Contrarian

Tested the assumption that #521 is already in main using
`git merge-base --is-ancestor edd7f4de HEAD`: exit 1. It is not.
Latest main's packaged cap remains December, so January configuration would
fail closed. The request to deploy latest main, then apply #521 after both
sites are healthy, with only one resident revision, cannot be assumed
compatible: an authority-enabled image and expiry refresh may require another
revision. Do not silently cherry-pick the branch, amend main, add a second
revision or increase the revision allowance. Existing secret helper refuses
Modify, so it cannot safely rotate existing secret names.
Reflection: park authority apply with exact owner/coordinator prerequisites,
not a fabricated successful renewal. No further local research can remove
the explicit execution prohibition.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | `src/api/README.md:3737-3777` | #543 documents the 17-column prerequisite and old-ready-revision health trap; local reproduction is not live causality. |
| C2 | `infra/sql/resident-showcase.sql:53-194` | Current view includes documents_json with restricted document metadata; no row-window renewal is part of that view. |
| C3 | `src/core/src/zava_forward/core/resident-demo.json:2` | Main cap remains 2026-12-31T23:59:59Z. |
| C4 | `infra/README.md:3493-3600` at commit `edd7f4dedd4b602a55bf2bc651c81b1b85521aed` | #521 sets exclusive 2027-02-01T00:00:00Z end; exact-version credential writes and individually approved SQL rows remain separate live work. Lines refer to the unmerged commit, not this worktree. |
| C5 | `.copilot-tracking/changes/2026-10-29/both-demo-sites-redeploy-changes.md:87-175` | Historical employee main revision and recovered resident old-image revision; exact-template handling avoids CLI-added empty value fields beside secretRef. |
| C6 | `src/README.md:70-150` | Complete publication gate includes az/Bicep preflight and cannot run under the current restriction. Focused checks do not replace it. |
| C7 | `src/api/README.md:268-283` | Existing synthetic employee chat browser check covers the merged #541 local path without a live model. |
| C8 | `src/api/checks/resident_demo_browser_check.py:1-11` | SQL-backed resident browser check requires an owned disposable loopback SQL database, not private SQL. |

Observed repository baseline: `77c87e0d76b827544fde9b2f2ce7dfbd9d879232`
for HEAD and `origin/main` after the requested pull. Authority ancestry test
returned 1. Prior session search returned no additional relevant deployment
evidence; repository artifacts are the source of truth. Memory is context only.

## Findings, Alternatives and Parent Synthesis

All four research questions are locally answered by C1-C8, except current
cloud metadata, actual SQL shape, exact approved rows, secret version metadata
and health, which remain unavailable without authorized execution.

Accepted: evidence-only correction handoff and requested local validation.
Rejected: Azure REST/SDK workaround, blindly copying the unmerged authority
source, repeating a resident revision, fallback empty documents, or changing
credentials via the Create-only helper. Deferred: all live writes and cloud
readbacks, exact-version credential rotation, row renewal and live acceptance.

Owner approval at 2026-10-29 09:36Z is recorded from the current user request,
not independently fetched. It does not override the same request's later
tool restriction, nor identify the individually approved row IDs or secret
version operation.

## Decisions, Risks and Readiness

Research disposition: executed. Planning Readiness: Ready for local evidence
and validation only; live implementation Blocked. Select this bounded approach
because it honors both the ordered full-loop request and the explicit tool
restriction. No second cycle is useful: remaining facts need live authority,
private execution and owner-held credentials, not broader local search.

Self-check: three waves, source provenance, alternatives, constraints and
smallest missing evidence recorded. No source, private data or cloud changes.
