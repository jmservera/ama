---
title: Demo sites correction phase details
description: Execution requirements and completion boundaries for the local correction round
ms.date: 2026-10-29
---

Task ID: eb7ee1f8-42fd-48a8-9c24-a1cbebb99513.
Plan: .copilot-tracking/plans/2026-10-29/demo-sites-correction-plan.md.
Initial direction: evidence-only local execution; no az or gh.

<!-- P01-T01 -->
## P01-T01: Record pending live sequence

Use #543 and historical deployment evidence, not fresh cloud claims.
The coordinator must first capture complete management configuration, auth,
all revisions and protected ACR/job state for both apps in private storage;
sanitized evidence contains names/counts/digests only, never resolved secrets.
Then update only the current resident view via the existing in-VNet init job,
preserving/restoring the exact job template and Manual trigger. Never run
the default initializer/reseed against live data. The VM cannot reach private
SQL. Do not add a private endpoint, enable public SQL, alter server settings,
broaden RBAC or emit row content. Require the exact 17 reader column names,
counts and existing principal narrow rights before any forward revision.

Build from an exact, freshly fetched main SHA using only the already approved
ACR route, preserve all protected digests and restore the complete frozen ACR
policy projection even on error. Use exact-template image-only updates, not
the previously observed CLI secretRef normalization. One forward resident
revision only; require its own Healthy/latestReady evidence and curl health.
The current source documents `/healthz`; do not assume `/health` is equivalent.
Probe the requested route too and record a non-200 honestly.
On actual startup failure, collect target console and system events while the
revision still exists BEFORE rollback to the captured previous digest.
Retain `ca-resident-demo--rollback-20261029-073718`.
Employee deploy follows successful resident verification, one revision only.
All eight jobs must remain Manual throughout; min replicas stays 0; exact
env/secretref/identity/registry/ingress preservation is mandatory.

Completion: document pending steps and unavailable fresh before/after state,
not check off live delivery.

Status: complete for the local record; all live steps explicitly not performed.

<!-- P01-T02 -->
## P01-T02: Park #521 authority apply

Read commit edd7f4dedd4b602a55bf2bc651c81b1b85521aed, not a branch-name
assumption. It is not in current main. Require coordinator integration/review
and an authority-enabled image/source choice compatible with the single
resident revision allowance; do not cherry-pick or create another revision.
Only after both sites are healthy, exact-version rotation needs an approved
secret writer and owner-held password-manager password, hidden verifier
generation and fresh session signing key. Existing Create-only helper cannot
Modify. Never pass values through command arguments or logs.

Use the existing private SQL path for the transactional checked constraint
migration and only named approved existing synthetic row renewals; preserve
provenance, revocations and narrow SID/rights. End is exclusive
2027-02-01T00:00:00Z (all January 31 UTC), not January 31 midnight.
No SQL password rotation for managed identity. Model tariff/inference cutoff
does not extend. Metadata readbacks, bounded rollback-version interval,
seven-day alerts and owner-performed sign-in/isolation/logout/session-expiry
verification remain required. Operator smoke stays unauthenticated.
Funding/headroom remains unknown; no cost query is needed for this blocked
local task. Owner/coordinator must supply the required current cost evidence
before a separately permitted paid renewal.

Status: parked with exact prerequisites in the changes artifact.

<!-- P02-T01 -->
## P02-T01: Local validation

Acquire `flock -n /tmp/ama-rpi-heavy.lock`; hold it across editable setup,
full suites and browser checks. If busy, do not modify shared editables:
use explicit current-worktree source/fixture paths for focused checks and
record the full suites/browser as blocked.
Core/API checks: `ruff check .`, `ruff format --check .`, `mypy`, and
`python -m unittest discover -s tests -q` from each project.
For each project set
`PYTHONPATH=<root>/src/<project>/src:<root>/src/core/src:<root>/src/agents/src:<root>/src/api/src:<root>/src/core/tests:<root>/src/agents/tests:<root>/src/api/tests`.
Clear inherited ZF_ settings and all Azure/OpenAI credential settings before
tests. Before application import set HOME to a new task-owned external
synthetic home, ZF_DATA to its nonexistent `data/zavaforward.json`, and
ZF_STATE to its own state path; never inspect the real default dataset.
Preserve only the explicit pre-existing Playwright executable cache path,
not the user's real home/data. Fixture-created apps control their own
constructed settings. Report actual discovery skip counts; this invocation
does not enumerate all skipped IDs and is not the complete gate's skip audit.
Install only the requested current-worktree distributions into `/tmp/mv`;
do not install unrelated tooling unless the chosen check actually reports
missing dependencies. No changes to dependency manifests or tests.

If lock admission fails, run only core
`python -m unittest test_resident_showcase test_resident_showcase_sql.RenderTests -q`
and API
`python -m unittest test_resident_demo_api test_resident_chat_api test_chat_panel test_workspace_scripts -q`
with that same isolated HOME/data/state and explicit worktree PYTHONPATH.
Do not install into shared `/tmp/mv` or start full/browser/SQL work on this
fallback path.

Run existing employee chat and resident assistant loopback browser harnesses
with their pinned axe dependency if available. The resident SQL-backed
browser/SQL compatibility checks additionally need an exactly owned disposable
SQL container; no configured/private DB is allowed. Report if that prerequisite
is unavailable; fixture-browser success is not SQL compatibility evidence.

Status: complete. Core/API lint, format, mypy and full discovery passed after
the recorded setup/path correction. Employee/resident assistant browser/axe,
34 actual resident SQL tests and SQL-backed resident browser passed.
General skips191/316 remain explicit; no exhaustive integration/full-gate
claim. Both exactly owned SQL containers were removed after their attempts.

<!-- P02-T02 -->
## P02-T02: Anonymous observations and reconciliation

Only anonymous GETs to the two documented app hosts; no auth cookies, tokens,
login, model calls or resident records. Record UTC time, path/status and body
hash without printing content. No cloud health/revision/configuration claim
from HTTP alone. Record each command and exit, skipped check and external
log hash. Verify tracking JSON, links and git diff; no pin change if no pinned
file changes. Full local publication gate remains not run because az is
forbidden.

Status: complete for local/anonymous evidence. Existing `/healthz` returned200
for both sites; `/health` returned404 resident/401 employee. Bodies discarded
(amendment: no body hash). No new-revision health or cloud-config equality
is inferred. Pre-Review source/evidence reconciliation is complete.

<!-- P03-T01 -->
## P03-T01: Original independent Review

Fresh reviewer reads the completed evidence boundary, original critique and
actual local outputs; writes only the designated Review artifact.
Require explicit execution/outcome and residual findings. No cloud commands,
secret access, repeated heavy suites, source edits or second Review.

<!-- P03-T02 -->
## P03-T02: Commit and handoff

Reuse repo-local `8036360+jmservera@users.noreply.github.com`, supported by the
prior task's authenticated account evidence; disclose that no fresh gh lookup
was performed. Use for both author and committer, retain configured name.
Commit only this task's explicit paths, Conventional Commit subject and
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>.
Verify exact commit contents and clean worktree; do not push, force-push,
open a PR or merge. Preserve original critique and Review outcomes.
