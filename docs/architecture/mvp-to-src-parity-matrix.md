---
title: MVP and Prototype to src Parity Matrix
description: Per-file outcome for every tracked mvp/ and prototype/ file, review of PRs 235 to 287 against their issues, issues to reopen, and the proposed migration order for issue 199
ms.date: 2026-10-15
ms.topic: reference
---

## Purpose and Status

This is the evidence for the cut-over gate in issue
[#201](https://github.com/jmservera/ama/issues/201), under the epic
[#195](https://github.com/jmservera/ama/issues/195). It records one outcome for
every file that git tracks under `mvp/` and `prototype/`, reviews what merged
pull requests 235 to 287 delivered against their issues, and proposes the
migration order for issue
[#199](https://github.com/jmservera/ama/issues/199).

Status: proposal for owner review. The target column follows the module
mapping of [ADR 0006](../adrs/0006-src-layout-and-cutover.md), accepted on
2026-10-15 (issue #196). Where the code shows that the mapping cannot be applied
as written, the row keeps the ADR target and the point is listed under
[Proposed ADR amendments](#proposed-adr-amendments).

Evidence base: `git ls-files mvp prototype` on the branch merged with `main` at
commit `736b387` (578 tracked files: 128 real files plus 450 sandbox files, see
[Sandbox Debris](#sandbox-debris)), the import graph of `mvp/zavaforward_mvp/`
(top-level and function-level imports read from source), the issue bodies and
comments of #195 to #203, the pull request bodies, file lists and linked issues
of #235 to #287, and a run of the MVP unit suite on 2026-10-15.

Limits: no Azure resource was used or created. Acceptance criteria are read from
the issue text; a criterion is "unmet" only where the pull request body, the
code or the repository record shows it is not delivered.

## Working Layout

The layout is the one accepted in ADR 0006: five projects under `src/`, each
with its own `pyproject.toml`, importable code under `src/<project>/src/zava_forward/<name>/`,
tests and evals outside the package. There is no `devtools` package.

| Project | Holds |
| --- | --- |
| `core` | Shared domain, stores, model client, policies, law register, `synthetic` tools, `evals/` (document controls), `tests/` |
| `api` | `server`, `auth`, `profile`, `timecapture`, `web/`, `Dockerfile`, `tests/`, `checks/` |
| `agents` | `assistants`, `ai_registry`, `ai_eval`, `evals/` (golden, registry), `tests/` |
| `orchestrator` | `digest_blob`, `token_store`, `tests/` |
| `importer` | `evals/` (document forms), `tests/`; new import service later |

`zava_forward` is a PEP 420 namespace: no `__init__.py` at that level. Target
paths in the tables use short prefixes:

| Prefix | Expands to |
| --- | --- |
| `core/`, `api/`, `agents/`, `orchestrator/`, `importer/` | `src/<project>/src/zava_forward/<project>/` |
| `core-evals/`, `agents-evals/`, `importer-evals/` | `src/<project>/evals/` |
| `core-tests/`, `api-tests/`, `agents-tests/`, `orchestrator-tests/`, `importer-tests/` | `src/<project>/tests/` |
| `api-checks/` | `src/api/checks/` |

Placement notes taken from ADR 0006:

* `scale_fixture`, `sensor_backfill` and `loadcheck` go to
  `zava_forward.core.synthetic`, a sub-package that no image entry point
  imports. `chat_fixture` is test support and goes to the test tree of the
  project that owns its subject (`agents-tests/`, because it drives `assistants`).
* `digest_blob` and `token_store` go to `orchestrator`; their Bicep job
  commands become `python -m zava_forward.orchestrator.<module>` (#200).
* `importer` has no existing `mvp/` module. Its first content is the document
  form fixtures and their test; the import service is new code.
* Each image installs its package and `core` from `pyproject.toml`; no
  `PYTHONPATH` use. During the dual window the remaining `mvp/` code installs
  `core` from `src/core` in CI. The `agents` image installs `core` without the
  `sql` extra (owner, 2026-10-15).

## Proposed ADR Amendments

Rows keep the ADR 0006 target. These points are where the code does not fit
the mapping or the mapping is silent. They are proposals for the owner, not
decisions.

| # | Finding | Evidence | Proposed amendment |
| --- | --- | --- | --- |
| A1 | Core imports workload code, which the dependency rule forbids | `ai_tasks`, `continuity` and `sqlstore` import `ai_registry` (agents); `chat_privacy`, `chatthreads` import `assistants` (agents) lazily inside functions | Move the registry data (`ai_registry`, the `REGISTRY` and `VERSION` constants) to `core` and keep dispatch in `agents`; or invert the call by injection. Until decided, M2 moves both sides in one pull request |
| A2 | `assistant_release.py` (PR 287) is not in the mapping | Imported by `assistants` (agents) and, lazily, by `sqlstore` (core) | Place it in `core/assistant_release.py`; tests with it |
| A3 | Agents tests import the API server | `test_assistants`, `test_ai_tasks` use `server`; ADR sends both to `agents/tests`, and `agents` may not import `api` | Allow `agents/tests` to depend on `api` for the temporary in-process edge until #144, or split the HTTP cases to `api/tests` |
| A4 | `test_digest_blob` and `test_token_store` use SQL and Blob fakes | They go to `orchestrator/tests` per ADR, but the jobs need SQL and Blob roles that ADR 0001 withholds from the orchestrator identity | Confirm the job identity for the two jobs, or the roles ADR 0001 grants the orchestrator |
| A5 | Four core-subject tests drive the API server | `test_lawstore`, `test_ledger`, `test_ranking_scale`, `test_workflows` import `server`; ADR sends the remainder to `core/tests` | Keep them in `api/tests`, or split the pure-store cases into `core/tests` |

## Outcome Definitions

| Outcome | Meaning |
| --- | --- |
| migrate | Move (git rename, not copy) to the target, imports rewritten, behaviour unchanged, tests move with it |
| rebuild | The delivered code cannot move as is. Build it in `src/`; the linked issue is reopened if closed, or stays open |
| archive | Not carried forward; kept in git history and the archive tag `v<BRD version>` |
| retire | Deleted at the cut-over with a stated reason; owner agreement is requested in this pull request |

Migration group column: M1 to M6 are defined in
[Proposed migration order](#proposed-migration-order-for-199).

## Coverage Baseline

Recorded on 2026-10-15 on the branch merged with `main` (`736b387`), from `mvp/`:

```text
PYTHONPATH=. python3 -m unittest discover -s tests -q
Ran 719 tests in 201.736s
OK (skipped=92)
```

The skips are SQL Server contract tests guarded by `ZF_TEST_MSSQL=1`
(test_mssqlstore, test_assistants, test_lawstore) that run in the `mvp-ci`
job with a SQL Server service, plus a test skipped when `azure-core` is not
installed. Pull request 287 is merged; its 16 tests in test_assistant_release
account for the rise from 703. The migration gate is equal or greater count
with the same skips explained. `node --check` on the web scripts and the image checks
(non-root, read-only, no data) are the other recorded gates. The prototype
suite is not part of this baseline: it has 15 tests in two files that
`prototype-validation` runs separately.

## Architecture Fit Findings

These drive the rebuild outcomes below.

* ADR 0001 gives the `agents` Container App no database, blob or Key Vault
  access and scales it from the `agent-tasks` queue. In `mvp/`,
  `assistants.py` keeps its task queue, leases and fences in SQL tables
  (`assistant_tasks`) inside the API process, and `ai.py` calls the model from
  the API process. The proposal logic can move. The dispatch path (lease,
  provider call, completion) cannot be moved as is to the target; it is a
  rebuild under issue #107 (open). PR 287, merged on 2026-10-15, extends exactly
  this path with release admission (`assistant_release.py`).
* `store.py` imports 18 sibling modules at top level and `sqlstore.py` imports
  10. Together with `assistants`, `continuity`, `ai_registry`, `ai_tasks` and
  `ledger` they form one import cluster that cannot be split without leaving
  `mvp/` importing half a package. This is why group M2 is one large mechanical
  move.
* `store.py` (JSON file store) and `sqlstore.py` (SQLite) serve local and test
  use. The owner rule (Azure only for deployment) means they migrate as local
  and test engines; the deployed engine is Azure SQL through `mssqlstore.py`.
* Core modules lazily import `assistants` and `ai_registry`, which ADR 0006 maps
  to `agents`; see amendment A1.

## Sandbox Debris

Pull request 287 committed 225 `mvp/.assistant-test-*` directories, 450 files
(`cases.sqlite`, `seed.json`), which are test debris. Outcome for all 450:
retire, group S1. A separate pull request, `fix/remove-assistant-test-sandboxes`,
removes them and adds a `.gitignore` pattern, so they are not carried into
`src/`.

| Pattern | Files | Outcome | Target | Group | Evidence and note |
| --- | --- | --- | --- | --- | --- |
| `mvp/.assistant-test-*/cases.sqlite` | 225 | retire | none | S1 | Generated by test runs; reproducible |
| `mvp/.assistant-test-*/seed.json` | 225 | retire | none | S1 | Generated seed for the same runs |

## Module Matrix: mvp/zavaforward_mvp

Delivery evidence is the pull request or test that proves current behaviour.
"Pre-235" means delivered before the reviewed range; its proof is the named test.

| File | Outcome | Target | Group | Evidence and note |
| --- | --- | --- | --- | --- |
| `mvp/zavaforward_mvp/__init__.py` | retire | none | M6 | Empty file (0 lines). The new namespace has no `__init__.py` |
| `mvp/zavaforward_mvp/ai.py` | migrate | `core/ai.py` | M1 | Model client and `FORBIDDEN` guard; test_ai_identity. `store` and `sqlstore` import it, so it cannot sit in `agents`. In-process call sites are a rebuild, see assistants.py |
| `mvp/zavaforward_mvp/ai_eval.py` | migrate | `agents/ai_eval.py` | M4 | PR 258 (#108, open); test_ai_eval. Reads `evals/ai_priority_golden.json` |
| `mvp/zavaforward_mvp/ai_registry.py` | migrate | `agents/ai_registry.py` | M2 | PR 260 (#105); test_ai_tasks. Imports `assistants` at top level and is imported lazily by core (A1), so it moves with the cluster |
| `mvp/zavaforward_mvp/ai_tasks.py` | migrate | `core/ai_tasks.py` | M2 | PRs 260, 263 (#105, #106); test_ai_tasks. Citations resolve or are marked Unverified |
| `mvp/zavaforward_mvp/assistants.py` | rebuild | `agents/assistants.py` (proposal logic moves as is; dispatch worker rebuilt in `agents/`) | M2 then #107 | Proposal logic moves as is. SQL leases and in-process dispatch conflict with ADR 0001 agents isolation. Issue #107 stays open. test_assistants (50 tests) is the behaviour to preserve |
| `mvp/zavaforward_mvp/assistant_release.py` | migrate | `core/assistant_release.py` (A2) | M2 | PR 287 (#107, merged 2026-10-15); 124 lines, release admission for the five assistants; test_assistant_release. Imported by `assistants` and lazily by `sqlstore`. Not in the ADR mapping |
| `mvp/zavaforward_mvp/auth.py` | migrate | `api/auth.py` | M5 | PR 275 (#116, open); test_auth |
| `mvp/zavaforward_mvp/chat_fixture.py` | migrate | `agents-tests/chat_fixture.py` (test support) | M3 | PR 283 (#172, open); test_chat_fixture |
| `mvp/zavaforward_mvp/chat_isolation.py` | migrate | `core/chat_isolation.py` | M4 | PR 286 (#162, open); test_chat_isolation |
| `mvp/zavaforward_mvp/chat_privacy.py` | migrate | `core/chat_privacy.py` | M4 | PRs 281, 285 (#163, #161, open); test_chat_privacy, test_chat_memory |
| `mvp/zavaforward_mvp/chatthreads.py` | migrate | `core/chatthreads.py` | M2 | PRs 282, 285 (#160, #161, open); test_chatthreads. `sqlstore` imports it at top level |
| `mvp/zavaforward_mvp/continuity.py` | migrate | `core/continuity.py` | M2 | PR 269 (#122, open); test_continuity |
| `mvp/zavaforward_mvp/controls.py` | migrate | `core/controls.py` | M2 | Pre-235; test_finance_signoffs |
| `mvp/zavaforward_mvp/digest_blob.py` | migrate | `orchestrator/digest_blob.py` | M5 | PR 268 (#115, open); test_digest_blob. Job command in `containerapps.bicep` changes (#200) |
| `mvp/zavaforward_mvp/doc_controls.py` | migrate | `core/doc_controls.py` | M2 | PR 270 (#117, open); test_document_controls |
| `mvp/zavaforward_mvp/documents.py` | migrate | `core/documents.py` | M2 | Pre-235, extended by PR 262; test_documents |
| `mvp/zavaforward_mvp/factory.py` | migrate | `core/factory.py` | M2 | Store selection (JSON, SQLite, Azure SQL); test_ledger |
| `mvp/zavaforward_mvp/finance.py` | migrate | `core/finance.py` | M2 | Pre-235; test_finance_signoffs |
| `mvp/zavaforward_mvp/governance.py` | migrate | `core/governance.py` | M2 | PR 261 (#126, open); test_governance |
| `mvp/zavaforward_mvp/grants.py` | migrate | `core/grants.py` | M2 | Pre-235; test_finance_signoffs |
| `mvp/zavaforward_mvp/insights.py` | migrate | `core/insights.py` | M2 | Pre-235; test_ranking_scale, test_sqlreads, test_generated_dataset |
| `mvp/zavaforward_mvp/lawstore.py` | migrate | `core/lawstore.py` (CLI later to `importer`) | M5 | PRs 248, 253 (#210). Azure SQL ledger and Blob backends verified against fakes only. test_lawstore. The seed CLI becomes an importer job when #213 lands |
| `mvp/zavaforward_mvp/ledger.py` | migrate | `core/ledger.py` | M2 | PRs 262, 268 (#114, #115, open); test_ledger, test_recovery |
| `mvp/zavaforward_mvp/loadcheck.py` | migrate | `core/synthetic/loadcheck.py` | M3 | PR 262 (#114, open); test_recovery. Load run on dev Azure SQL not done |
| `mvp/zavaforward_mvp/mssqlstore.py` | migrate | `core/mssqlstore.py` | M2 | Azure SQL engine (deployed path). test_mssqlstore skips without SQL Server; runs in `mvp-ci` |
| `mvp/zavaforward_mvp/procurement.py` | migrate | `core/procurement.py` | M2 | Pre-235; test_quality_procurement |
| `mvp/zavaforward_mvp/profile.py` | migrate | `core/profile.py` | M1 | Pre-235; test_profile |
| `mvp/zavaforward_mvp/projection.py` | migrate | `core/projection.py` | M2 | Role field projection; test_role_matrix, test_role_endpoint_inventory (PR 275) |
| `mvp/zavaforward_mvp/quality.py` | migrate | `core/quality.py` | M2 | Pre-235; test_quality_procurement |
| `mvp/zavaforward_mvp/ranking.py` | migrate | `core/ranking.py` | M2 | Pre-235; test_ranking_policy, test_ranking_scale. Reads `policies/ranking-v1.json` |
| `mvp/zavaforward_mvp/recovery.py` | migrate | `core/recovery.py` | M4 | PR 262 (#114, open); test_recovery |
| `mvp/zavaforward_mvp/resident_decisions.py` | migrate | `core/resident_decisions.py` | M2 | Pre-235; test_workflows |
| `mvp/zavaforward_mvp/rulecards.py` | migrate | `core/rulecards.py` | M1 | PRs 250, 259 (#211 open, #127); test_rulecards. No import of siblings |
| `mvp/zavaforward_mvp/scale_fixture.py` | migrate | `core/synthetic/scale_fixture.py` | M3 | PRs 236, 249 (#174, #169); test_eval_registry, test_chat_fixture |
| `mvp/zavaforward_mvp/sensor_backfill.py` | migrate | `core/synthetic/sensor_backfill.py` | M3 | PR 272 (#183, open); test_sensor_backfill. `validate_reading` mirrors a contract #110 has not defined |
| `mvp/zavaforward_mvp/server.py` | migrate | `api/server.py`, routers split in later work | M5 | 626-line single HTTP server. In-process model calls via `assistants` are the rebuild noted above. test_mvp (21), test_role_matrix, test_ui_support |
| `mvp/zavaforward_mvp/signoffs.py` | migrate | `core/signoffs.py` | M2 | Pre-235, edited by PR 242; test_finance_signoffs |
| `mvp/zavaforward_mvp/sqlstore.py` | migrate | `core/sqlstore.py` | M2 | Local and test SQLite engine and shared DDL; test_sqlstore, test_sqlreads |
| `mvp/zavaforward_mvp/store.py` | migrate | `core/store.py` | M2 | Hub (817 lines, 18 imports); JSON local engine. test_mvp and most suites |
| `mvp/zavaforward_mvp/timecapture.py` | migrate | `api/timecapture.py` | M5 | PR 267 (#120, open); test_timecapture. Gated on DPIA, notice approval and audited enabling |
| `mvp/zavaforward_mvp/token_store.py` | migrate | `orchestrator/token_store.py` | M5 | EasyAuth SAS renewal job; test_token_store. Bicep job command `python -m zavaforward_mvp.token_store` becomes `python -m zava_forward.orchestrator.token_store` (#200). Identity: A4 |
| `mvp/zavaforward_mvp/workflows.py` | migrate | `core/workflows.py` | M2 | Pre-235, edited by PR 261; test_workflows |

## Web Assets, Policies, Evals and Law Data

| File | Outcome | Target | Group | Evidence and note |
| --- | --- | --- | --- | --- |
| `mvp/web/app.js` | migrate | `api/web/app.js` | M5 | PRs 242, 244, 267 edit it; `node --check`; test_design_system, test_content_standard |
| `mvp/web/assistants.js` | migrate | `api/web/assistants.js` | M5 | PR 242; browser check assistants_browser_check |
| `mvp/web/index.html` | migrate | `api/web/index.html` | M5 | test_accessibility_baseline |
| `mvp/web/law.html` | migrate | `api/web/law.html` | M5 | PR 248 (#210) read-only provision viewer |
| `mvp/web/law.js` | migrate | `api/web/law.js` | M5 | PR 248 |
| `mvp/web/ops.js` | migrate | `api/web/ops.js` | M5 | Pre-235 |
| `mvp/web/panels.js` | migrate | `api/web/panels.js` | M5 | PR 242 |
| `mvp/web/style.css` | migrate | `api/web/style.css` | M5 | PRs 241, 244; test_design_system, test_accessibility_baseline |
| `mvp/web/timecapture.js` | migrate | `api/web/timecapture.js` | M5 | PR 267; screens not browser-tested |
| `mvp/web/welcome.html` | migrate | `api/web/welcome.html` | M5 | Pre-235 |
| `mvp/web/zava-logo.png` | migrate | `api/web/zava-logo.png` | M5 | Brand asset |
| `mvp/web/vendor/LICENSE` | migrate | `api/web/vendor/LICENSE` | M5 | Leaflet licence; keep beside the library |
| `mvp/web/vendor/leaflet.css` | migrate | `api/web/vendor/leaflet.css` | M5 | Vendored; excluded from the rubric |
| `mvp/web/vendor/leaflet.js` | migrate | `api/web/vendor/leaflet.js` | M5 | Vendored |
| `mvp/web/vendor/images/layers.png` | migrate | `api/web/vendor/images/layers.png` | M5 | Vendored |
| `mvp/web/vendor/images/marker-icon.png` | migrate | `api/web/vendor/images/marker-icon.png` | M5 | Vendored |
| `mvp/policies/ranking-v1.json` | migrate | `core/policies/ranking-v1.json` (package data) | M2 | Loaded by `ranking.py`; test_ranking_policy. Policy file must be declared as package data and checked in the image |
| `mvp/law/law-source-register.json` | migrate | `core/law/law-source-register.json` (package data) | M5 | PR 248 seed; Dockerfile copies `law/` today. Snapshots stay out of the image; ingest is a later importer job |
| `mvp/evals/ai_priority_golden.json` | migrate | `agents-evals/ai_priority_golden.json` | M4 | PR 258 (#108); test_ai_eval |
| `mvp/evals/document_control_fixtures.json` | migrate | `core-evals/document_control_fixtures.json` | M3 | PR 270 (#117); test_document_controls |
| `mvp/evals/document_form_fixtures.json` | migrate | `importer-evals/document_form_fixtures.json` | M3 | PR 235 (#171); test_document_form_fixtures. Set split is 30 tuning, 30 calibration, 60 held-out |
| `mvp/evals/registry.json` | migrate | `agents-evals/registry.json` | M3 | PRs 236, 249, 270, 283; test_eval_registry |

## Tests

Rule used: ADR 0006 sends each test to the project of its subject (`test_ai_*`
and `test_eval_registry` to `agents-tests`, job tests to `orchestrator-tests`,
document form fixtures to `importer-tests`, the remainder to `core-tests`). The
migration group is the highest group among the modules a test imports. Four
tests that drive `server` (`test_lawstore`, `test_ledger`, `test_ranking_scale`,
`test_workflows`) stay in `api-tests` because `core` may not import `api`
(amendment A5).

| File | Outcome | Target | Group | Evidence and note |
| --- | --- | --- | --- | --- |
| `mvp/tests/assistants_browser_check.py` | migrate | `api-checks/assistants_browser_check.py` | M5 | Browser check for the assistants panel; not in unittest discovery |
| `mvp/tests/browser_check.py` | migrate | `api-checks/browser_check.py` | M5 | Browser check; not in unittest discovery |
| `mvp/tests/test_accessibility_baseline.py` | migrate | `api-tests/test_accessibility_baseline.py` | M5 | PR 244 (#151). Static checks only; no rendered scanner |
| `mvp/tests/test_ai_eval.py` | migrate | `agents-tests/test_ai_eval.py` | M4 | 6 tests |
| `mvp/tests/test_ai_identity.py` | migrate | `agents-tests/test_ai_identity.py` | M1 | 2 tests |
| `mvp/tests/test_ai_tasks.py` | migrate | `agents-tests/test_ai_tasks.py` | M5 | 22 tests, uses `server` (A3) |
| `mvp/tests/test_assistant_release.py` | migrate | `agents-tests/test_assistant_release.py` | M5 | PR 287 (#107); 16 tests, 245 lines; imports `test_assistants` Base and `release_support`, so it moves with them (A2, A3) |
| `mvp/tests/release_support.py` | migrate | `agents-tests/release_support.py` | M5 | PR 287; 44 lines of test helpers for test_assistant_release; not a test module |
| `mvp/tests/test_assistants.py` | migrate | `agents-tests/test_assistants.py` | M5 | 50 tests, uses `server` (A3). Preserved as the behaviour contract for the #107 rebuild |
| `mvp/tests/test_auth.py` | migrate | `api-tests/test_auth.py` | M5 | 23 tests |
| `mvp/tests/test_chat_fixture.py` | migrate | `agents-tests/test_chat_fixture.py` | M3 | 9 tests |
| `mvp/tests/test_chat_isolation.py` | migrate | `core-tests/test_chat_isolation.py` | M4 | 12 tests |
| `mvp/tests/test_chat_memory.py` | migrate | `core-tests/test_chat_memory.py` | M4 | 11 tests |
| `mvp/tests/test_chat_privacy.py` | migrate | `core-tests/test_chat_privacy.py` | M4 | 13 tests |
| `mvp/tests/test_chatthreads.py` | migrate | `core-tests/test_chatthreads.py` | M2 | 12 tests |
| `mvp/tests/test_content_standard.py` | migrate | `api-tests/test_content_standard.py` | M2 | PR 242 (#153); 4 tests over store copy |
| `mvp/tests/test_continuity.py` | migrate | `core-tests/test_continuity.py` | M2 | 15 tests |
| `mvp/tests/test_design_system.py` | migrate | `api-tests/test_design_system.py` | M5 | PR 241 (#150); reads `web/style.css` |
| `mvp/tests/test_digest_blob.py` | migrate | `orchestrator-tests/test_digest_blob.py` | M5 | 9 tests |
| `mvp/tests/test_document_controls.py` | migrate | `core-tests/test_document_controls.py` | M2 | 12 tests |
| `mvp/tests/test_document_form_fixtures.py` | migrate | `importer-tests/test_document_form_fixtures.py` | M3 | Imports the `support/` generator; path repointed by #200 |
| `mvp/tests/test_documents.py` | migrate | `core-tests/test_documents.py` | M2 | 10 tests |
| `mvp/tests/test_eval_registry.py` | migrate | `agents-tests/test_eval_registry.py` | M3 | 7 tests |
| `mvp/tests/test_finance_signoffs.py` | migrate | `core-tests/test_finance_signoffs.py` | M2 | 15 tests |
| `mvp/tests/test_generated_dataset.py` | migrate | `core-tests/test_generated_dataset.py` | M2 | 12 tests; imports `support/` generator and writes private data |
| `mvp/tests/test_governance.py` | migrate | `core-tests/test_governance.py` | M2 | 12 tests |
| `mvp/tests/test_lawstore.py` | migrate | `api-tests/test_lawstore.py` | M5 | 16 tests, uses `server` |
| `mvp/tests/test_ledger.py` | migrate | `api-tests/test_ledger.py` | M5 | 6 tests, uses `server` |
| `mvp/tests/test_mssqlstore.py` | migrate | `core-tests/test_mssqlstore.py` | M2 | Skips without SQL Server; keep the CI service |
| `mvp/tests/test_mvp.py` | migrate | `api-tests/test_mvp.py` | M5 | 21 tests, end-to-end API |
| `mvp/tests/test_needs_inventory.py` | migrate | `core-tests/test_needs_inventory.py` | M3 | PRs 240, 243; reads `docs/reference/research/retrofit-synthetic-data` |
| `mvp/tests/test_profile.py` | migrate | `core-tests/test_profile.py` | M1 | 4 tests |
| `mvp/tests/test_quality_procurement.py` | migrate | `core-tests/test_quality_procurement.py` | M2 | 11 tests |
| `mvp/tests/test_ranking_policy.py` | migrate | `core-tests/test_ranking_policy.py` | M2 | 10 tests |
| `mvp/tests/test_ranking_scale.py` | migrate | `api-tests/test_ranking_scale.py` | M5 | 18 tests, uses `server` |
| `mvp/tests/test_recovery.py` | migrate | `core-tests/test_recovery.py` | M4 | 12 tests |
| `mvp/tests/test_role_endpoint_inventory.py` | migrate | `api-tests/test_role_endpoint_inventory.py` | M5 | PRs 275, 286 (#116) |
| `mvp/tests/test_role_matrix.py` | migrate | `api-tests/test_role_matrix.py` | M5 | Role matrix gate in #199 |
| `mvp/tests/test_rulecards.py` | migrate | `core-tests/test_rulecards.py` | M1 | 11 tests |
| `mvp/tests/test_sensor_backfill.py` | migrate | `core-tests/test_sensor_backfill.py` | M3 | 5 tests |
| `mvp/tests/test_sensor_plausibility.py` | migrate | `core-tests/test_sensor_plausibility.py` | M3 | PR 280 (#191); 8 tests |
| `mvp/tests/test_sqlreads.py` | migrate | `core-tests/test_sqlreads.py` | M2 | 14 tests |
| `mvp/tests/test_sqlstore.py` | migrate | `core-tests/test_sqlstore.py` | M2 | 9 tests |
| `mvp/tests/test_synthetic_provenance.py` | migrate | `core-tests/test_synthetic_provenance.py` | M3 | PR 238 (#175); reads the register under `docs/` |
| `mvp/tests/test_timecapture.py` | migrate | `api-tests/test_timecapture.py` | M5 | 16 tests |
| `mvp/tests/test_token_store.py` | migrate | `orchestrator-tests/test_token_store.py` | M5 | 4 tests |
| `mvp/tests/test_ui_support.py` | migrate | `api-tests/test_ui_support.py` | M5 | 9 tests |
| `mvp/tests/test_workflows.py` | migrate | `api-tests/test_workflows.py` | M5 | 10 tests, uses `server` |

## Build, Container and Documentation Files

| File | Outcome | Target | Group | Evidence and note |
| --- | --- | --- | --- | --- |
| `mvp/.dockerignore` | migrate | `src/api/.dockerignore` | M5 | Keep `data/` and tests out of the image |
| `mvp/Dockerfile` | migrate | `src/api/Dockerfile` | M5 | Pinned digest, non-root uid 10001, `libltdl7`, `libkrb5-3`. Installs the package instead of copying folders. Same non-root, read-only, no-data checks. Image tag history kept (#200) |
| `mvp/README.md` | migrate | `src/api/README.md`, split per package | M6 | Holds the dated evidence sections for PRs 236 to 286. Preserve them; they are the validation record. The rubric scores it as solution-code |
| `mvp/requirements.in` | migrate | `[project.dependencies]` in `src/api/pyproject.toml` and `src/core/pyproject.toml` | M5 | `mssql-python==1.15.0`, `azure-storage-blob==12.31.0`; regenerate hashes without loosening pins |
| `mvp/requirements.txt` | migrate | `src/api/requirements.txt` (hashed lock, one per image) | M5 | Regenerated with `--generate-hashes`; hashes must verify at image build |

## Prototype Matrix

`prototype/` is a retired 199-line slice (125-line domain, 73-line server) that
is not scored by the rubric and not deployed. Its useful ideas are already in
`mvp/`, with the exception noted. Owner decided on 2026-10-14 that it may retire
before `mvp/`, once this mapping exists.

| File | Outcome | Target or reason | Group | Evidence |
| --- | --- | --- | --- | --- |
| `prototype/README.md` | archive | Concepts in ADR 0001 and the PRD; history keeps the text | P1 | Dated 2026-08-26 |
| `prototype/Dockerfile` | retire | `mvp/Dockerfile` is the deployed image | P1 | Prototype is not deployed |
| `prototype/requirements.txt` | retire | No third-party dependencies of value | P1 | Superseded by `mvp/requirements.txt` |
| `prototype/zavaforward/__init__.py` | retire | Empty package marker | P1 | 1 line |
| `prototype/zavaforward/domain.py` | retire | Stage order, gated approver, version and idempotency, hash-chained audit and proposal rules are implemented in `mvp/` `workflows.py`, `store.py`, `ledger.py` and `ai_tasks.py` | P1 | Behaviours proven in test_workflows, test_ledger, test_ai_tasks. Coverage gap check below |
| `prototype/zavaforward/server.py` | retire | Read of `X-MS-CLIENT-PRINCIPAL` is in `mvp/` `auth.py` and `server.py` | P1 | test_auth |
| `prototype/web/app.js` | retire | 6-line health client; `mvp/web/` replaces it | P1 | None needed |
| `prototype/tests/test_domain.py` | retire | 11 tests; equivalents in test_workflows, test_ledger, test_ai_tasks | P1 | See gap check |
| `prototype/tests/test_server.py` | retire | 4 tests; equivalents in test_mvp, test_auth, test_role_matrix | P1 | See gap check |
| `prototype/scripts/evaluate_agent.py` | retire | Offline reject-unsafe-proposal contract cases are covered by `ai_eval.py` and test_ai_eval; no model-quality value | P1 | PR 258 |

Gap check before deleting `prototype/`: the prototype asserts that agent,
orchestrator and importer service roles can never transition a case
(`test_agent_and_service_roles_cannot_transition`, `test_only_agent_submits`).
The `mvp/` role matrix tests cover staff roles; no `mvp/` test names the three
service identities. When `agents`, `orchestrator` and `importer` are created,
a service-role denial test must be added in `src/api/tests/`. Until then the
check is recorded as an open item, not as a reason to keep `prototype/`.

## Items Used Outside mvp/ and prototype/

| Item | Reference to repoint | New path or change | Issue |
| --- | --- | --- | --- |
| `.github/workflows/mvp-ci.yml`, `mvp-validation.yml` | `mvp/` filters, `docker build mvp`, requirements path, image tag names | `src/**`, per-package install, `src/api` build context; keep the old check names until after the cut-over, then rename in one pull request (owner, 2026-10-15) | #200, #138 |
| `.github/workflows/prototype-validation.yml` | `prototype/` detection | Delete with `prototype/` in P1 | #202 |
| `infra/modules/containerapps.bicep` | Job command `python -m zavaforward_mvp.token_store`, digest job command from PR 268 | `python -m zava_forward.orchestrator.token_store` and `python -m zava_forward.orchestrator.digest_blob --publish`; `bicep build` and lint | #200, #144 |
| `infra/README.md` | `az acr build ... mvp`, `PYTHONPATH=mvp` | `src/api` build context, installed package | #200 |
| `infra/scripts/initialize-workbench-staff.py`, `create-sql-users.py`, `infra/tests/test_initialize_workbench_staff.py`, `infra/tests/test_identity_rbac.py` | `PYTHONPATH=mvp`, `zavaforward_mvp` imports | Import from `zava_forward.core` after M2 | #200 |
| `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py`, `zf_mvp_coverage.py`, `zf_documents.py`, `zf_document_controls.py` | Import from `mvp`; writes `mvp/data/zavaforward.json` | Import `zava_forward.core` (including `zava_forward.core.synthetic`); write to the `ZF_DATA` directory outside git and the package | #200, #165 |
| `tools/rename-zava.py`, `rename-zava.md`, `rename-zava-tests.py` | `mvp/` paths | Update live paths only; dated historical identifiers stay exact | #200 |
| `.github/rubric/artifacts.json`, `README.md`, `scripts/test_prepare.py`, `scripts/test_safe_output_runtime.py`, `scores/latest.json` | `mvp/` globs, dead `prototype/deploy/**/*.bicep` | `src/**/*` already registered; add `tests/` and `pyproject.toml` globs in a registry-only pull request; drop `mvp/` globs at cut-over | #198 |
| `.github/copilot-instructions.md`, `README.md`, `.gitignore` (`/mvp/data/`) | `mvp/` paths | `src/` paths; private data ignore path | #200, #203 |
| `mvp/data/` (git-ignored, about 3.7 MB, real map addresses) | Local only | Relocate outside git and the image before cut-over | #201 |
| `mvp/properwarm_mvp/` | Untracked `__pycache__` only | Not in git; remove locally | #202 |

## Review of Pull Requests 235 to 287

Disposition: "move as is" means the code can be renamed into `src/` with imports
rewritten. "Rebuild" means it cannot. Pull requests that change no code under
`mvp/` or `prototype/` are classified by what they touch. Issue state is as read
on 2026-10-15.

| PR | Issue and state | Delivered | Move or rebuild | Remaining against the issue |
| --- | --- | --- | --- | --- |
| 235 | #171 closed | Document, form and field fixtures; 30 tuning, 30 calibration, 60 held-out | Move as is (M3); generator stays in `support/` | Gold labels generator-owned, human adjudication needed before held-out testing. Not an unmet criterion |
| 236 | #174 closed | Eval dataset registry, seeded scale fixture | Move as is (M3) | None unmet. Dataset owners are a placeholder |
| 237, 257 | #176 open | Determinism, manifests, refresh policy; stock fabric and EPC determinism | Generators stay in `support/`; test moves (M2) | Stock register generator and sensor generator byte-identity unproven; refresh values await approval |
| 238 | #175 closed | Provenance register, PII-free check | Move as is (M3) | Unmet, see reopen list |
| 239, 247, 254, 255, 264, 284 | no issue | Coordinator agent definition changes | None; `.github/agents/` | Not code |
| 240, 243 | #166 open, #167 open | Needs inventory, coverage baseline | Move as is (M3) | Inventory approval, volumes and #103 link open |
| 241 | #150 open | Design system CSS and test | Move as is (M5) | Owner confirmation of extend decision; marker shapes and contrast unverified |
| 242 | #153 open | Content standard, copy audit | Move as is (M2, M5) | No named reviewer; user testing not recorded |
| 244 | #151 closed | WCAG 2.2 static baseline | Move as is (M5) | Unmet, see reopen list |
| 245 | none | Docs: synthetic regulatory fixtures permitted | None | Not code |
| 246, 251, 252 | #168 open, #170 closed, #173 closed | Stock link, fabric, EPC, lifecycle fixtures | Generators stay; tests move (M2) | #168: 980-case and stock fabric reconciliation undecided. #170 and #173 met; deferrals recorded |
| 248, 253 | #210 closed | Law store, SQLite plus Azure SQL ledger and Blob backends | Move as is (M5) | Criteria met in code against fakes. Azure SQL ledger and WORM Blob deployment not exercised; verify at #144 deploy, no reopen |
| 249 | #169 closed | Residents, households, tenancy fixture | Move as is (M3) | None unmet; rules are demonstrator inventions |
| 250, 259 | #211 open, #127 closed | Rule cards, approval, change review | Move as is (M1) | #211: named owners, rule engine, UI, #116 role binding. #127 met |
| 256 | none | Dependency bump in `tools/program-workbench-assets` | None | Not under `mvp/` |
| 258 | #108 open | AI eval harness evidence gate | Move as is (M4) | Live model runs and model selection open |
| 260, 263 | #105 closed, #106 closed | Task registry, proposal envelope, provenance, hold, review evidence | Move as is (M2) | Met in code. Accountable individuals and priority path envelope are owner and later items |
| 261 | #126 open | Frozen protocol, benefits register, phase gates | Move as is (M2) | Gates not wired into every workflow; HTTP route tests missing |
| 262 | #114 open | Per-year ledger digests, load check, restore re-application | Move as is (M2, M3, M4) | Azure SQL load run, restore drill and DPO decision open |
| 265, 273, 274, 276, 277, 278 | #142, #140, #147, #139, #141, #143 open | Bicep and scripts under `infra/` | None; stay in `infra/`; PR 276 edits `mvp-validation.yml` and PR 278 edits `containerapps.bicep` (repoint in #200) | Live Azure evidence not produced for any |
| 266 | none | Portable meta upsert on SQL Server | Move as is (M2) | Fix to `sqlstore.py`; keep |
| 267 | #120 open | Time capture gated on DPIA | Move as is (M5) | Real DPIA references, final notice text, browser test |
| 268 | #115 open | Immutable Blob digests, scheduled verification | Move as is (M5); Bicep job command changes | Legal retention, policy lock, Azure run |
| 269 | #122 open | Continuity, versioning, export | Move as is (M2) | Witnessed drill, Azure SQL drill, supplier terms |
| 270 | #117 open | Malware scan, retention, legal hold | Move as is (M2, M3) | Scanner is a labelled synthetic test; Defender not enabled |
| 271 | none | Removed `.github/mcp.json` | None | Not code |
| 272, 280 | #183 open, #191 open | Sensor backfill generator, plausibility tests | Move as is (M3) | #183: real open data not retrieved; #110 contract undefined |
| 275 | #116 open | Role endpoint inventory, note holding | Move as is (M5, M2) | Role confirmation by DPO and Legal, guest contractor model, per-role browser acceptance |
| 279 | #158 closed | ADR 0004 accepted | None | Met; OD-45 to OD-49 carried forward as the issue allows |
| 281 | #163 open | Chat privacy controls, DPIA record | Move as is (M4) | Not wired to UI; provider terms not recorded |
| 282, 283, 285 | #160, #172, #161 open | Chat threads, fixtures, memory lifecycle | Move as is (M2, M3, M4) | Retention, memory administrator role, wiring |
| 286 | #162 open | Chat and memory isolation | Move as is (M4) | Break-glass policy (OD-46) undecided; no live injection evaluation |
| 287 | #107 open | Release admission for five assistants; merged 2026-10-15 into `mvp/` | Move `assistant_release.py` and its tests as is (M2, A2); rebuild the dispatch part in `src/agents` (R1) | #107 stays open: dispatch rebuild and the queue-driven worker (#144) |

Pull request 287 note. It merged on 2026-10-15, so there is no hold action. It
extends the in-process lease and dispatch path that the architecture review
marks for rebuild, and adds `assistant_release.py` (124 lines),
`release_support.py` (44) and test_assistant_release (245 lines, 16 tests).
These are mapped in the tables above. Its 450 sandbox files are retired by the
separate `fix/remove-assistant-test-sandboxes` pull request, which also adds a
`.gitignore` pattern (see [Sandbox Debris](#sandbox-debris)). The SQL DDL it
added to `sqlstore.py` moves with M2.

## Issues to Reopen

Closed issues whose acceptance criteria are not all evidenced by delivered work.

| Issue | Delivered by | Unmet criteria | Reason | Code disposition |
| --- | --- | --- | --- | --- |
| [#151](https://github.com/jmservera/ama/issues/151) WCAG 2.2 conformance baseline | PR 244 | "Automated checks run in CI against key screens"; "Manual screen-reader and keyboard checks are recorded for each role workflow"; "Map, charts and tables have accessible equivalents (#119)"; the first criterion (target level decided) is only proposed, open item O-1 | PR 244 states a rendered-page scanner was not added, manual results are not recorded and O-1 to O-5 are open. Only static HTML, CSS and JS checks exist | Move as is (M5). New scanner check is built in `src/api/tests/` |
| [#175](https://github.com/jmservera/ama/issues/175) Data dictionary, provenance, PII-free | PR 238 | "Dictionary covers every dataset including sensor and chat data"; "Each external source records licence, retrieval date and attribution" | `DS-SENSOR` is still `not-generated` although PR 272 (#183) now generates sensor data. `SRC-CENSUS-TS054`, `SRC-IMD-2025` and `SRC-ONS-BOUNDARIES` have a null retrieval date, which the test tolerates when flagged | Data and documentation fix; test moves as is (M3) |

No `mvp/` module needs a rebuild in a closed issue. The only rebuild
(`assistants.py` dispatch) sits in open issue #107.

Closed and not reopened, with the caveat that holds:

| Issue | Reason not reopened |
| --- | --- |
| #171, #174 | Criteria met; gold-label adjudication and dataset owners are owner actions |
| #169, #170, #173 | Criteria met; deferrals are recorded as the criteria allow |
| #105, #106 | Criteria met in code; named accountable individuals are an owner decision |
| #127 | Criteria met; rule cards trace to requirements and tests |
| #158 | Met by acceptance of ADR 0004 |
| #210 | Code criteria met. Deployment of Azure SQL ledger and WORM Blob is unverified. Recheck after the first deployment from `src/`; reopen only if it fails |

## Proposed Migration Order for #199

Each pull request moves a module group and its tests, repoints CI, and keeps the
image deployable. Order follows the import graph: leaves first, the cyclic hub
as one step, then dependants, then the API surface last. Each pull request
records its rubric total against the baseline of 47; a temporary dip is accepted
and needs its cause and a recovery expectation in the description.

| Step | Pull request scope | Modules | Tests moved | Why here |
| --- | --- | --- | --- | --- |
| M0 | ADR 0006 accepted; scaffold `src/core` and `src/api` `pyproject.toml`, tooling config, additive `src-ci` workflow | none | none | Blocks everything (#196) |
| M1 | Isolated leaves | `profile`, `rulecards`, `ai` | test_profile, test_rulecards, test_ai_identity | No sibling imports; proves packaging, namespace and CI. About 450 lines |
| M2 | Core hub, mechanical move, one pull request | `store`, `sqlstore`, `mssqlstore`, `factory`, `ledger`, `continuity`, `chatthreads`, `doc_controls`, `documents`, `controls`, `finance`, `grants`, `governance`, `signoffs`, `resident_decisions`, `workflows`, `quality`, `procurement`, `insights`, `projection`, `ranking`, `ai_tasks`, `assistant_release` to `core`; `ai_registry`, `assistants` to `agents`; `policies/ranking-v1.json` | the rows marked M2 | `store` imports 18 siblings and the cluster is cyclic through `assistants`, `ai_registry` and `ledger` (A1), so no smaller step leaves a working tree. Use `git mv` and keep it free of behaviour change so rename detection shows a small diff. `mvp/` CI installs `core` from `src/core` |
| M3 | Synthetic tools and data governance | `scale_fixture`, `sensor_backfill`, `loadcheck` to `core/synthetic`; `chat_fixture` to `agents-tests`; `document_control_fixtures.json`, `document_form_fixtures.json`, `registry.json` | the rows marked M3 | Depends only on M2 `insights`. Coordinate with #165 (generator imports) |
| M4 | Core features | `chat_privacy`, `chat_isolation`, `recovery` to `core`; `ai_eval` to `agents`; `evals/ai_priority_golden.json` | the rows marked M4 | Depend on M2 and M3. Open work on #160 to #163 and #108 must be merged or rebased first |
| M5 | API and orchestrator workloads and image | `server`, `auth`, `timecapture`, `lawstore` (core), `digest_blob`, `token_store` (orchestrator); all of `mvp/web/`; `law/` register; Dockerfile, hashed requirements, Bicep job commands, mvp-ci replacement | the rows marked M5, browser checks, `node --check` | Needs every module. Image gates (non-root, read-only, no data) re-run. The `agents` image installs `core` without the `sql` extra. Coordinate with #149 (UX edits to `mvp/web`), #144, #138 |
| M6 | Remaining files and docs | `README.md` split, `__init__.py` removal; repoint docs | none | Leaves `mvp/` empty for #201 and #202 |
| S1 | Remove assistant test sandboxes | 450 `mvp/.assistant-test-*` files; `.gitignore` pattern | none | Separate pull request `fix/remove-assistant-test-sandboxes`; independent of the move |
| P1 | Retire `prototype/` | all prototype files, `prototype-validation.yml`, dead registry glob | none | Independent; may run any time after this matrix is approved |
| R1 | Rebuild assistants dispatch | `assistants.py` dispatch half, `agents` package, #107 dispatch worker | `test_assistants` and `test_assistant_release` contracts | After M2; new code only in `src/` |

Sequencing rules:

* No module exists in both places at merge. Where a lazy import crosses the
  boundary during the dual window, `mvp/` imports the installed `zava_forward`
  package; no shim copies remain after M5.
* New features start in `src/` from M0. Open feature branches that edit moved
  files (any pull request touching `store.py`, `sqlstore.py`, `assistants.py` or
  `server.py`) need a rebase onto the moved path; schedule M2 and M5 when those
  branches are quiet.
* Hashed requirements are regenerated in M5 without loosening pins.
* The M2 test list is every row above in the Tests table with group M2.
  Test totals are checked after each step against 719 tests (92 skipped).

## Owner Answers of 2026-10-15

Recorded from the owner; they close the open questions of the earlier draft.

| Question | Answer | Effect |
| --- | --- | --- |
| Rename of the old CI check names (#200) | Keep the old check names until after the cut-over, then rename them in one pull request | Workflows keep `mvp-ci` and `mvp-validation` job names while paths change; one rename pull request follows cut-over |
| GitHub release (#202) | The GitHub release accompanies the archive tag `v<BRD version>` | The cut-over checklist creates both together |
| `agents` image and the SQL driver | The `agents` image installs `core` without the `sql` extra | Matches the ADR 0001 identity; reflected in M5 |
| Soak period | None | Deletion follows owner sign-off and a healthy deployment, as in the ADR 0006 cut-over gate |

## Open Decisions for the Owner

* Decide the ADR 0006 amendments A1 to A5 above, or accept the matrix targets
  as stated and record the exceptions.
* Reopen #151 and #175, and agree the rebuild of the assistant dispatch under
  #107.
* Agree each `retire` row for `prototype/`, and the service-role denial test
  to add once `agents`, `orchestrator` and `importer` exist.
* Whether `mvp/README.md` evidence sections are preserved verbatim in the split
  READMEs (recommended).

## Related Documents

* [ADR 0001 Azure architecture](../adrs/0001-azure-architecture.md)
* [ADR 0006 Source layout and cut-over policy](../adrs/0006-src-layout-and-cutover.md)
* [ADR 0002 Pilot readiness architecture](../adrs/0002-pilot-readiness-architecture.md)
* [Zava Forward MVP README](../../mvp/README.md)
* [Rubric registry notes](../../.github/rubric/README.md)
* [Knowledge Base Log](../reference/log.md)
