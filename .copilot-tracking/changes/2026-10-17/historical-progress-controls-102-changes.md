---
title: Historical progress controls 102 changes
description: Implementation, validation and correction evidence
ms.date: 2026-10-17
---

## Scope and State

Full approved plan; P01/P02 implemented and ready for one Review. Research executed;
one critique executed and all compatible findings applied. No domain authority,
audit writer, private dataset, AI provider or web changes authorized.

## P01: Read-only report baseline

P01-T01/T02 complete: typed progress.py normalizes exact existing structured
returns/reopens and handoff events; no narrative/prose/current-stage clocks.
Sequential versions, aware UTC times, valid stage directions, exact pause
labels, stage/handoff consistency and handoff participant identity are checked.
Unknowns remain null/explicit exceptions. Raw actors/references/notes withheld.
Store adapter reuses `_filtered` under sync lock and staff-only direct access.
Existing stats/CSV support report=progress; legacy default paths unchanged.
Forecast requires declared ready count; EXA-009 independent-pool simulation
reproduces all four exact sensitivity arrays. No model/provider is called.
One canonical progress/v1 report serializes to stable typed JSON cells in CSV.
Malformed/unavailable ledger verification is logged and reports Unknown with
untrusted clocks, not an empty success or mutated ledger.

## P02: Validation and Documentation

P02-T01/T02 complete. Pip editable core[dev,sql], agents, api[dev] installed
in worktree .venv before tests. Owned files only: test_progress_reports.py and
test_progress_report_api.py; no existing fixtures/tests removed or modified.

| Actual execution | Result |
| --- | --- |
| New pure/JSON/SQLite HTTP tests after strengthened edge cases | 24 passed |
| Actual uniquely named loopback MSSQL HTTP/Store suite | 6 passed |
| Prior targeted combined existing/new suite | 90 passed, one import error: test_handoff_api requires documented src/api cwd; not a source failure |
| Corrected test_handoff_api from src/api | 6 passed |
| Configured core ruff check / format check / mypy | Passed; 115 source files typed |
| Configured API ruff check / format check / mypy | Passed; 55 source files typed |
| Source API Docker build | Passed; initial image sha256:d5d4e1b791521eb27060a25698b3dada346ab2285eff2d5f2024d69bf4a3688c |
| Actual hardened non-root image report smoke | Passed health, UID/GID 10001, read-only root, zero capabilities, NoNewPrivs, writable state, authenticated JSON/CSV parity and exact synthetic clock/scenario |
| Git diff whitespace and KB append-prefix check | Passed |

MSSQL server: task-owned zf-issue102-mssql-8807b1c699, published only on
127.0.0.1:32799. Each test creates its own zf_progress102_UUID database; none
is shared or deleted. Task-owned image container zf-issue102-api-78adc056cc
was stopped, not removed. No unrelated container inspected or changed.
Image smoke predates final audit-unknown/participant guards; final image
rebuild/smoke is required after Review/corrections before publication.
Existing generic check-container.py was not run because it deletes containers,
contrary to caller's no resource deletion constraint; named retained-container
equivalent above executed actual positive hardening and app behavior.

P02-T03 complete: core/API guides, existing programme journey synthesis and
KB index/log updated; upstream log remains exact byte prefix. No web assets
changed, so no browser/design/WCAG claim or browser check is applicable.
No Azure, paid AI, operational authority or human outcome validation.

## Amendments and Divergences

Local judgment: retain UUID SQL databases and stop owned containers without
deletion; use named manual image checks instead of destructive generic harness.
New test module mypy override permits calls to migrated untyped Store/server
boundary and resolves core-owned fixture module, not blanket source exemptions.
Completed reopen origin is source-defined;
ordinary current-stage/closure flags are not accepted-handover history.

## Review and Corrections

Original full Review executed once: Complete / Defects found.
Original Review SHA256:
0b33722d868a9e3165210b0720e5c467cbe8baa2066e637276dc66f45e75050e.
RV-001 blank query inputs drop explicit report/scenario intent;
RV-002 UTC range overflow escapes malformed timestamp handling.
User-authorized correction ONE starts with failing-first cases in the existing
two owned test files. Scope: those exact concrete defects only.
No source/domain choice or second full Review is authorized or implied.

### P03-T02: Correction ONE completion evidence

Failing-first execution reproduced 18 blank-query subcase failures and three
UTC overflow errors across three selected tests. RV-001 correction parses
report-specific query fields with blanks retained, explicitly rejects empty
or repeated values, and leaves default legacy parsing untouched. RV-002 guards
UTC conversion as well as parsing and reports unrepresentable times as the
existing ValueError/unknown-event contract.

Final configured core/API ruff check, ruff format --check and mypy passed
(115/55 source files). Final focused new plus handoff/workflow/ledger/role
regressions ran 88 tests, all passed. Actual task-owned loopback MSSQL ran
eight report/HTTP/persistence tests, all passed; no skips in either selection.
These include original defect regressions, source refresh/reopen, immutable
audit, direct/HTTP denial and full visible/export semantic equality.

Final corrected source API image:
sha256:e035732d04afafa38063af41df54916443ab8809873a09f0fad72011404859dc.
The actual final image smoke verified installed progress/Store/server source
SHA256 equality to this worktree, health, UID/GID 10001, read-only root,
all zero capability sets, NoNewPrivs, writable state, authenticated JSON/CSV
parity, exact stage/handoff clocks/scenario and RV-001/RV-002 HTTP 400 cases.
Own image container zf-issue102-api-final-e969f8bc and own SQL container were
stopped, retained and not removed. No unrelated resource touched.

Nine added documentation links/anchors, upstream log exact byte prefix,
Git diff whitespace and unchanged original Review SHA256 passed.
Correction TWO not used. This is parent targeted correction evidence, not a
second full Review or independent coordinator Pass. Original Review remains
Complete / Defects found byte-for-byte.

### P03-T03: Publication

Published https://github.com/jmservera/ama/pull/390 targeting main from the
supplied feat/historical-progress-controls-102 topic and exact supplied base.
Implementation commit bfdcd2289d1f430653e94ae6dde1394b50895880 contains only
the 18 owned source/test/docs/dated-artifact paths. Fresh `gh api user`
returned id 8036360 / login jmservera; repository-local privacy-safe
8036360+jmservera@users.noreply.github.com was configured for author/committer.
Conventional Commit includes Refs #102 and required Copilot co-author trailer.
Normal push, no merge, issue close, rebase or force push.

Initial remote PR checks started; they were in progress, not claimed passed.
Final publication metadata is a separate owned-artifact-only commit, with the
final exact head read from PR #390 after normal push rather than attempting a
self-referential commit hash in this record.
Session resume ID: 047eef1a-9e80-4725-946a-20da710900a6.
The user explicitly requested stopping at clean pushed PR delivery; no child
task or additional full Review starts. Coordinator owns final-head acceptance.
Commit-helper limitations: its auxiliary commit-message instruction file and
get_changed_files tool are unavailable in this host. Repository Conventional
Commit/privacy/trailer rules and explicit owned-path staging are used instead
of its blanket-stage suggestion, preserving the user's own-changes-only rule.
The PR helper's auxiliary instruction file is likewise absent, and no
content-policy-citation.instructions.md exists in this worktree. The user-
specified evidence-rich PR contract is followed directly; its parallel
re-review suggestion is not used because exactly one full Review was requested.

## Remaining Work and Limitations

No complete forward-event capture or operational resource validation can be
inferred from existing sources. Human/coordinator acceptance is not a local test.
