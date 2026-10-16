---
title: Regulatory evaluation changes
description: Issue 216 implementation evidence
ms.date: 2026-10-16
---

## Starting scope

Full plan P01-P03, synthetic-only src code and tests, component README updates,
reference index/log and requested RPI artifacts. Clean existing topic branch;
merged prerequisites confirmed. No private data/cloud access.

## Planning reconciliation

One final-candidate critique, five planner-owned corrections accepted in details.
No user decision changed. Implementation begins with P01-T01; validation is
targeted unit/HTTP tests, per-project ruff/mypy and deterministic report rerun.
External owner agreement, staff trial and continuing-stock acceptance remain unmet.

## P01: Independent per-check evaluation

Added pure agents grader, 24 frozen development questions, independently authored
source/fact/template oracles and external offline runner. Removed legacy aggregate
pass without removing historical cases or their 3/3 and 10/10 evidence.
Registered both new datasets and versioned the historical report.
Recorded 7/7 supported citations, 24/24 answer/refusal contracts (17 refusals);
targets 1.0 provisional pending Juan Manuel Servera, no agreement invented.
Added automated-source coverage as an immediately relevant fixture refinement,
within both approved rule purposes and test budget.

Generated 60,000 fictional seed-174 homes, 120,000 exact state agreements and
78,000 required-flag matches; zero critical misses among 42,000 required hazard
flags. Recall denominator excludes clear/not-applicable outcomes and threshold
remains unset. Ten SQLite hazard profiles independently match, five alert
publications retained. This is not continuing-stock pipeline/Azure evidence.
Comparison records same-role/source-version card links and structural fragments
but no staff benefit: cards-only ship recommendation, development access unchanged.

## P02: Cadence visibility

Added shared read-only source/card freshness with existing monitoring cadence,
last successful observation and exact due boundary. Missing storage/config/
observations and future attempted clock are unknown; failed attempts never
refresh success. Any overdue source wins the card reduction.
Decorated collection/history HTTP reads and actual chat cards; UI shows textual
label and historical as-of. No eligibility, activation or alert mutation.

## Validation state and local corrections

Initial targeted run: 91 tests, three errors from the minimal existing fixture's
missing blob on simulated failed observation. Corrected only the new cadence-test
fixture by writing its wholly synthetic blob; no runtime workaround.
Initial mypy/lint failures corrected with proper narrowing, explicit fixture/
class types, test import paths and formatting; no source type errors suppressed.
Final agents full discovery: 89 tests passed, including exact 60,000-home report
rerun and registry. Earlier targeted rule/source/chat/core/API batch: 92 passed.
Core/API project lint, format and mypy passed; agents lint/format/mypy passed.
Final core regression batch: 85 tests passed. API/rule-alert/law-store batch:
44 tests, 14 live-platform tests skipped, 30 local tests passed. Synthetic
loopback server health, cited turn, card collection/history and unchanged alerts
observed. API lint/format/mypy rerun passed; no cloud acceptance implied.
Documentation relative links and git whitespace review passed.

Component READMEs, reference index and append-only log carry the full six-row
acceptance audit and explicit unproven boundaries. Issue checkboxes unchanged.

## Review readiness

P01/P02 and P03-T01 complete with matching plan/details/evidence. P03-T02
contains the one review and subsequent delivery; commit/push/PR are pending,
not represented as complete. No unresolved local implementation blockers.
Follow-ups remain owner threshold agreement/independent grading, staff paired
trial and continuing-stock integration; no follow-up is claimed as acceptance.

## P03-T02: One review and implementation disposition

One independent Review executed Complete, outcome Not accepted at its assessed
snapshot. It reproduced three in-scope grader/report defects, not live safety
incidents. Historical review record is retained unchanged; no second review
or claim of independent closure is made.

* RV-001: Added independently authored full card/cadence/date oracles; exact
  visible labels, card collections and answer/cadence as-of must match.
* RV-002: Seeded expected item identity is preserved in rule units and matched
  along with state. Wrong/duplicate/omitted items are critical hazard misses;
  SQL selects the correct home/card and checks expected item too.
* RV-003: Invalid-output counts/IDs are separate; contract-invalid responses
  can no longer count as correct refusals or supported answers.

These are implementation corrections preserving approved intent, not a new
plan decision. Added four methods (23 total additions of 45 allowed), no removals.
Full agents rerun passed 93 tests, lint/format/mypy passed; local API rerun
passed five tests. Canonical report regenerated with unchanged positive counts
and zero invalid outputs. SQL home filter is an additional identity refinement. Final report regenerated
and reproduced exactly by the full 93-test agents suite; lint, format and mypy
passed after that refinement. No local source changes remain pending.
Source/artifact commit 7056d8d was pushed on feat/regulatory-eval-gates-216.
PR #355 opened against main, using Refs #216 only and the six-criterion audit.
No merge or issue-checkbox update. Final delivery-artifact status update follows
in a separate ordinary commit; no history rewrite.

## P04 starting scope and integration

User supplied independent CHANGES verdict at 7c87293 and explicitly requested
implementation of the retained-history regression and full-suite investigation.
P04 is the active full correction scope; first boundary P04-T01 merged
origin/main as c311752, preserving both sides of the append-only reference log.
Source changes confined to src/; documentation and existing RPI evidence may
change. No new critique/review cycle, issue-checkbox update or Azure work.

Initial API/agents discovery could not import uninstalled editable packages.
Installed core/agents/API plus declared validation tools in an isolated session
venv using pip after that missing-dependency failure. Core's requested absolute
source/test paths ran 529 tests, 528 passed, one skipped. Next boundary is
full API reproduction with packages installed, then surgical corrections.

## P04-T02: Whole-suite reproduction and surgical correction

Complete API reproduction: 558 tests, one failure, 110 skips. CI logs likewise
show only the raw-storage-versus-decorated-history assertion failure.
Unavailable-law-store tracebacks are expected logged diagnostics from
post-commit safety handling, not uncaught suite errors. Runtime already returns
unknown with the human safety route, preserving committed reports; no runtime
exception suppression or invented fixture approval is appropriate.

Strengthened the retained-version test: compare the entire decorated history
before/after reopen, remove only the additive cadence field for exact equality
with retained storage, assert unknown cadence and verify storage unchanged.
Extended outage coverage to both alert/check HTTP 503/unknown, safe route and
saved hazard. Added a loaded-but-empty LawStore HTTP regression covering draft
collection/history, unknown cadence, role-visible unknown checks and no alerts.
Initial new-test assertions corrected to the actual sources envelope and
role-scoped hazard-only check projection; no production behavior was changed.

Full agents reproduction also exposed main's new required decision reasons:
the fixture's recorded human review lacked them. Added synthetic reasons,
without relaxing the engine or changing expected states. Regenerated the report:
only fixture_sha256 changed; 120,000 exact matches, 78,000 required flags and
zero misses among 42,000 hazard flags remain. Agents lint/format/mypy and core
lint/format/mypy passed. All three whole-suite final runs are now in progress.

## P04-T03: Final integrated local evidence

All whole suites ran from project roots with the exact requested absolute
PYTHONPATH values in phase details, using installed editable packages:

| Project | Run | Passed | Skipped | Outcome |
| --- | ---: | ---: | ---: | --- |
| core | 529 | 528 | 1 | OK |
| agents | 93 | 93 | 0 | OK |
| api | 559 | 449 | 110 | OK |

Total: 1,181 discovered/run, 1,070 executed passes, 111 skips, zero failures or
errors. Skips remain existing opt-in platform/browser or environment gates.
API full run still logs expected unavailable-store diagnostics; assertions
verify honest unknown states. No test removed or runtime error hidden.

Ruff check, Ruff format check and mypy passed in each project (core 99,
agents 22, API 45 checked source files). API's first mypy run lacked the declared
Playwright dependency; installed playwright==1.64.0 via pip after that explicit
missing-dependency result, then reran all API quality gates successfully.
The browser test remains explicitly opt-in, not an executed browser claim.

Final local HTTP run: 20 tests passed across RuleHttpTests, rule alerts and
regulatory chat. Responsive ephemeral loopback servers exercised health/app,
fixture authentication, complete retained lifecycle, cadence collection/history,
cited turns, empty/unavailable stores, saved safety work and unchanged alerts.
No outbound provider call or Azure/private data use. git diff --check passed.
Component README, index/log and supplied-review routing updated; every unmet
issue criterion remains unmet. P04-T04 commit/push/PR publication is pending.
