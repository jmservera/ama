---
title: Resident chat logout and validation follow-up changes
ms.date: 2026-10-28
---

Task 520-logout-followup; parent 520-review-correction. P01/P02 complete;
original child Review Complete / Not accepted; local commit handoff,
publication blocked.
Current plan/details/research/critique/state share this slug and date.
Full plan declared; P01 starts first. Prior original evidence is unchanged.

## Plan Decisions and Amendments

Exactly one original critique Complete / Revise; PC-001 and PC-002 adopted in
plan/details before source implementation. Isolated urllib transport and an
inert test-only response cookie establish the actual browser application
boundary. Current-base full receipt and independent exact-head assessment must
precede push. No new method/dependency/cookie scheme or significant divergence.

## Execution and Validation

P01-T01/T02 implemented in existing app._logout, SessionTests logout method and
shared_session_checks; no new methods/dependencies. Logout sends no Set-Cookie
and still revokes the exact bound token. HTTP regression proves retained bytes
cannot authenticate and /session is signed out. README explains lifecycle.
Three focused logout/binding HTTP tests passed. Changed-file Ruff100 passed;
format check initially requested one expression reformat, applied with Ruff.

First actual browser admission: two busy retries then acquired at 19:21:01Z,
using /tmp/ama-rpi-heavy.lock, nonblocking flock/60-second retry. Both delayed
logout replacement identities and earlier scenarios passed their assertions.
The complete harness then failed at loading-manual-launcher-focus because
target_sizes selects descendants, not the selector roots: #main had no visible
controls and #chat-launcher itself was excluded. Correct the existing scan
selector to body, which includes the visible launcher without weakening target
assertions or changing shared scanner logic. Original failure retained:
/tmp/ama-520-logout-browser-20261028-1/command.log. No complete browser pass yet.
This is a directly coupled harness correction within the existing run method,
not a new scenario, changed runtime behavior or scope divergence.

Corrected complete browser execution passed in
/tmp/ama-520-logout-browser-20261028-2: actual Chromium 156.0.8078.4,
hash-pinned axe 4.10.3, 31 scanned states, zero reported violations, no uncaught
page errors or external browser requests. All five original scenarios plus
delayed logout across different/same-resident login executed. Six states retain
axe incomplete results (not accessibility acceptance). A subsequent mypy run
found one TypedDict dynamic-key indexing error in the harness; replaced it
with typed dictionary-comprehension equality excluding only refreshed CSRF
expiry. Full API Ruff/check-format100 and mypy (94 source files), JS syntax
then passed. Final byte-current browser rerun also passed under the held lock
at /tmp/ama-520-logout-browser-20261028-3/report.json.

An additional isolated Ruff probe from the repository root reported two
import-group differences because it omitted the API project's first-party
configuration; repository-configured Ruff100 passes. No unrelated import
reordering was applied. Original failures are retained, not converted to passes.

P02-T02 in progress: five project suites/static/types use external logs under
/tmp/ama-520-logout-validation-20261028. Core passed 1454 tests with 190 general
discovery opt-in skips, Ruff/format and mypy (156 files). The initial agents
command incorrectly included its own tests behind core in PYTHONPATH, causing
test_dependency_rule import collision; corrected documented core-only fixture
path passed 116 tests, no skips, Ruff/format and mypy (24 files).

Permitted non-az matrix uses unchanged Runner methods with explicit exclusions,
a new external detached checkout plus the exact source patch, and one held
heavy lock. It is raw partial command evidence, not a canonical run/receipt.
It does not weaken or execute mandatory az preflight/infra operations.
Output: /tmp/ama-520-logout-nonaz-20261028-1 and matching .log.

All five project suites now passed: core 1454 (190 skips), agents 116 (zero
skips, corrected invocation), API 1167 (314 skips), orchestrator 46 (zero),
importer 39 (zero). Total 2822 tests, including 504 general-discovery skips;
these skips are not SQL/browser execution evidence. Each project's existing
Ruff100, format100 and mypy passed: 156/24/94/12/10 source files respectively.
The existing logout regression was also tested against the original 618777a2
handler in process: it fails on the original destructive Set-Cookie response
and passes on the corrected handler. Negative/positive evidence:
/tmp/ama-520-logout-validation-20261028/logout-red-green.log.
Browser/source integrity and exact incomplete rule IDs:
/tmp/ama-520-logout-validation-20261028/browser-evidence-summary.json.
Final report SHA-256:
de24204cef6e56d1da5e76029d51b548b0ef66570ae4896e95eac7a9f0a4aaf8.
All six browser incompletes are color-contrast, not zero unresolved findings.
Separate local non-az container and governance contracts also passed 7/8 tests.

The admitted non-az matrix completed successfully: namespace, static (30 runner
tests), migration, actual common browser/regulatory checks, disposable loopback
SQL, four image contracts/scans and logo-0600. The 77 command rows include two
expected absent-import probes and five expected SQL startup/readiness failures
before successful readiness and SQL execution; no unexpected failure.
SQL: 263 tests, OK with one enumerated JSON-only separate-file ordering skip,
not a skipped SQL integration selector. Its task-owned SQL container was
removed by the unchanged runner ownership guard.

Each consumer image passed the existing fixable HIGH/CRITICAL scan policy.
Full reports still contain 59 HIGH and two CRITICAL unfixed vulnerabilities
per image; no claim that images are vulnerability-free or deployment-approved.
Full reports and SPDX are retained under the non-az external output.
The output explicitly says partial raw command evidence, NOT a full or partial
canonical receipt. No runner source, preflight, protections or scan policy was
modified. Complementary non-az infrastructure checks also completed under the
same bounded nonblocking admission contract: 26 standalone Bicep builds and
26 lints, workflow coverage inventory, every runner infra Ruff100/format/type
set, and 379 non-az infrastructure tests, zero errors/failures/skips.
Four modules requiring az compilation were excluded explicitly:
test_bicep_policy, test_iothub_module, test_resident_assistant,
test_resident_demo_deploy. The no-az audit guard observed zero attempted az
launches; no cloud/deployment activity occurred.
Evidence: /tmp/ama-520-logout-nonaz-infra-20261028-1 and matching .log.

External summary SHA-256 values:
nonaz-results.json = 79cfef8ab5546c30764a77d5d2ac4cd280d0634cd14301e08a7525e1bd7d5ccc;
nonaz-infra-results.json = dd36230bd922a118d9f6e5eaa0e0ce8e40ef723c9ec56a3a5708953865ffb143.
All source fingerprints remain identical to the final browser integrity summary.

## Remaining Work and Boundaries

P01/P02 complete; P03-T01 original child Review complete. Full-tier publication requires a full receipt; canonical
preflight invokes prohibited az, so partial non-az evidence cannot satisfy that
gate. No push or thread resolution until publication prerequisites are met.
Human/resident/content, AT/native zoom and real-model acceptance stay pending.

## Review Handoff

Review the distinct child's complete current diff against 618777a2, necessary
unchanged session/JS context and all five original scenarios. Preserve parent's
Not accepted Review. No new runtime methods, test methods or dependencies;
no method removal. One original critique Complete / Revise, PC-001/002 adopted.
Known full-receipt publication blocker is not a new source defect or permission
to repeat Review. Local commit is authorized; push and thread resolutions are
not eligible without the required current-base full receipt/exact-head assessment.

## Original Review and Local Commit Handoff

Exactly one original independent child Review completed, outcome Not accepted.
Reviewer verified the source patch, all four current source fingerprints, both
external summary hashes, all 77/67 command-log hashes and actual suite/browser/
scan results. No additional confirmed implementation defect. RV-001 High:
mandatory committed exact-head full receipt and publication unavailable; route
to later authorized rpi-research. RV-002 Medium: existing unfixed image risk,
nonblocking for the narrow logout fix, routed to distinct image maintenance.
No source correction or repeated Review follows this assessment. The original
parent Not accepted Review and original child Revise critique remain untouched.

Before local commit, fetched origin again: remote topic is still
685547ed548464ebe58222e21ea3557fb53be963, already an ancestor of local
618777a26bf62566a0d920c7127d3a8313b85e65. No newer bot commit exists on the
remote topic, so no rebase is necessary. Current main remains
413ccaf253fce4566e855bae9d0a924b2a82b506.
Authenticated account resolved again with gh api user: id 8036360, login
jmservera. Derive and configure the repository-local noreply email for both
author and committer; use a Conventional Commit and exact Copilot trailer.
This commit is a blocked local handoff, not a purported passing full candidate.

Task-created five editable-build metadata directories were moved, not deleted,
to the session's external files/generated-metadata. No ignored candidate inputs
remain. External evidence checkout, reports, images and environments are
deliberately retained for provenance; no foreign artifacts/resources were
removed. No az, .env, private dataset, merge, deployment, force push, PR-body
change or remote thread mutation occurred. Push and all five replies/resolutions
remain blocked; the local fixing commit must not be described as pushed.
