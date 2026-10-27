---
title: ADR 0006 Source Layout and Cut-Over Policy
description: Accepted standard Python src layout with one isolated package per deployable workload plus a shared core, the zava_forward naming scheme, the move-not-copy migration rule, phases, cut-over gate, rubric counting and relocation of private working data
author: AMA programme
ms.date: 2026-10-27
ms.topic: reference
---

## Status

Accepted on 2026-10-15 by the owner, Juan Manuel Servera (issue #196, epic
#195). Nothing in this record moves code. Owner decisions of 2026-10-14 and
2026-10-15 are recorded below. The module-to-package mapping is the working
assumption for the parity matrix (#197), which sets the final per-file outcome. It extends
[ADR 0001](./0001-azure-architecture.md) (four workloads on Azure Container
Apps) and the delivery state in [ADR 0002](./0002-pilot-readiness-architecture.md).

## Context

The working application lives in `mvp/zavaforward_mvp/` (about 40 modules, about
10,300 lines, one image, one `server` entry point). `prototype/` is a retired
earlier prototype. New features keep landing in `mvp/` (for example the chat and
memory modules of ADR 0004 and the law store and rule cards of ADR 0005), which
raises the cost of every later move.

Verified facts that shape the decision (repository state at 2026-10-15):

* The rubric registry already counts `src/**/*` in `solution-code`
  (`.github/rubric/artifacts.json`); `mvp/data/**` and `mvp/web/vendor/**` are
  excluded, `src/` vendor and data folders are not yet.
* `mvp/Dockerfile` builds one image; the Container Apps jobs in
  `infra/modules/containerapps.bicep` run `python -m zavaforward_mvp.token_store`
  and `python -m zavaforward_mvp.digest_blob --publish` from that same image.
* ADR 0001 specifies four workloads with separate identities: `api`, `agents`,
  `orchestrator` and `import`. The `agents` identity has no database, blob or Key
  Vault access; today all of them are realised inside the single API
  ([ADR 0002](./0002-pilot-readiness-architecture.md)).
* `mvp/data/` (about 3.7 MB, git-ignored) holds real map addresses and must never
  be committed or baked into an image.

## Decisions Recorded From the Owner

| Date | Decision | Where it lands in this ADR |
| --- | --- | --- |
| 2026-10-14 | Standard Python `src` layout, tests outside the package, `pyproject.toml` packaging, not a custom layout | Layout |
| 2026-10-14 | `zavaforward_mvp` is not kept | Package naming |
| 2026-10-14 | `prototype/` may be retired before `mvp/` | Phases |
| 2026-10-14 | A temporary rubric score dip is accepted and recorded, not a blocker | Rubric counting |
| 2026-10-14 | Archive tag is `v<BRD version>`, created at cut-over (replaces `mvp-final`) | Phases |
| 2026-10-15 | Several isolated packages, one per deployable workload, each with its own `pyproject.toml` and tooling configuration, following ADR 0001 (API, agents, orchestrator, import) plus a shared core library | Package split |
| 2026-10-15 | Namespace `zava_forward` | Package naming |
| 2026-10-15 | All new code is built in `src/`; migrate what is needed first | New-feature rule |
| 2026-10-15 | Deploy on Azure only; non-Azure services only for local tests | Verification |

## Decision

### Layout

Each deployable workload is a self-contained project folder under `src/` that
follows the standard Python `src` layout: the importable code sits under that
project's own `src/`, tests sit beside it and outside the package, and
`pyproject.toml` is the only packaging definition.

```text
src/
  README.md                          index of the projects and the dependency rule
  core/                              shared library, distribution zava-forward-core
    pyproject.toml                   build, ruff, mypy, pytest/unittest config
    requirements.in / requirements.txt   hashed pins (library extras only)
    src/zava_forward/core/           importable code
      policies/  law/                runtime data shipped as package data
    evals/                           document control fixtures, outside the package
    tests/                           unit tests of the core, outside the package
  api/                               distribution zava-forward-api
    pyproject.toml  Dockerfile  requirements.in  requirements.txt
    src/zava_forward/api/
      web/                           HTML, JS, CSS and vendor assets (package data)
    tests/                           API, role matrix, UI and accessibility tests
    checks/                          browser checks that need a browser (not unit tests)
  agents/                            distribution zava-forward-agents
    pyproject.toml  Dockerfile  requirements.in  requirements.txt
    src/zava_forward/agents/
    evals/                           golden and registry fixtures, outside the package
    tests/
  orchestrator/                      distribution zava-forward-orchestrator
    pyproject.toml  Dockerfile  requirements.in  requirements.txt
    src/zava_forward/orchestrator/
    tests/
  importer/                          distribution zava-forward-import
    pyproject.toml  Dockerfile  requirements.in  requirements.txt
    src/zava_forward/importer/
    evals/                           document form fixtures
    tests/
```

Rules that follow from this:

* The folder `src/<project>/` is the project root. `src/<project>/src/zava_forward/<name>/`
  is the import root. The doubled `src` is deliberate: the outer folder is the
  repository's registered solution-code tree, the inner folder is the standard
  layout that prevents tests importing uninstalled code.
* Tests are never inside an importable package. Each project runs its tests from
  its own folder against an installed (editable) package, so no `PYTHONPATH`
  workaround is needed.
* Each project owns its `pyproject.toml` (build backend, dependencies, optional
  extras, linter, type checker and test settings). No repository-wide Python
  config binds the projects together, so a workload can change tooling or
  dependencies without touching another.
* Requirements: `requirements.in` lists direct dependencies, `requirements.txt`
  is regenerated with hashes and installed with `--require-hashes`; pins are
  never loosened to make a move pass. The shared core declares optional extras
  `sql` (`mssql-python`) and `blob` (`azure-storage-blob`), so an image installs
  only the drivers its identity may use. This is how the `agents` image stays
  free of SQL and blob client code, matching its ADR 0001 identity.
* Dockerfiles live in the project folder and use the `src/` folder as build
  context (clarified in #290: a workload image also needs the sibling `core`,
  which a project-folder context cannot reach), for example
  `docker build -f src/agents/Dockerfile src`. Each keeps the properties of
  today's `mvp/Dockerfile`: pinned base digest, non-root user 10001, no working
  data, read-only root file system. A workload image copies only its own
  package and the core, built as wheels in a build stage with hash-pinned build
  tools (`src/build-requirements.txt`).
* Web assets belong to the API project (only the API serves HTML). Policies and
  the law register are loaded by core rules (`ranking`, `lawstore`), so they are
  core package data and are located through `importlib.resources`, not
  `Path(__file__).parents[n]`. Evals are test inputs, not runtime data: they stay
  outside the package in the owning project's `evals/` folder and out of images.
* `src/**/web/vendor/**` and `src/**/data/**` are excluded from rubric scoring
  and from Docker context by the registry and `.dockerignore` (see Rubric
  counting).

### Package split and why

ADR 0001 gives each workload its own identity and scaling rule. A single package
would let any workload import code it must not be able to run (for example the
`agents` workload importing SQL access), which is a boundary the architecture
requires to be structural. Several isolated packages make that boundary an
install-time fact.

The real module dependencies in `mvp/zavaforward_mvp` constrain how thin the
workloads can be today:

* `store.py` imports almost every domain module (`finance`, `continuity`,
  `governance`, `grants`, `resident_decisions`, `signoffs`, `doc_controls`,
  `documents`, `procurement`, `quality`, `workflows`, `chatthreads`, `ai`,
  `ai_tasks`, `insights`, `ledger`, `projection`, `ranking`). `sqlstore.py` and
  `mssqlstore.py` implement the same `Store` interface. They form one cohesive
  domain and data-access block, so they belong in the shared core.
* `ai.py` (the bounded model client `Ai`) is imported by both `store.py` and
  `sqlstore.py`, so it cannot live in `agents` without a cycle. The model client
  contract stays in the core; the `agents` project owns the proposal-only
  assistants that use it.
* `assistants.py` imports `continuity`, `projection`, `quality`, `ranking`,
  `ai.FORBIDDEN` and `store.ConflictError`; `ai_registry.py` imports
  `assistants`; `ai_eval.py` imports `ai_tasks` and `Store`. All point one way:
  agents depend on the core, never the reverse.
* `server.py` imports `assistants`, `chat_isolation`, `chat_privacy`,
  `chatthreads`, `documents`, `lawstore`, `factory`, `timecapture`, `auth`,
  `profile`, `projection` and `quality`. The API therefore depends on the core
  and, while ADR 0002's single-API realisation lasts, on the `agents` library
  in process. That `api` to `agents` edge is temporary: it is removed when
  #144 deploys `agents` as a queue-driven workload that posts proposals to the
  API.
* `doc_controls.py` (content scanning, retention, legal hold) is imported by
  `store.py` and `sqlstore.py`, so it is core, not import-workload, code; the
  `importer` project starts as the owner of the document fixtures and the new
  import service that ADR 0001 describes and `mvp/` never built.
* `digest_blob.py` imports `ledger` and `documents`; `token_store.py` has no
  internal imports. Both are run as Container Apps jobs, which ADR 0001 gives to
  the orchestrator.

Dependency rule (enforced by an import test in each project): `api`, `agents`,
`orchestrator` and `importer` may import `core`; `api` may additionally import
`agents` until #144; no project imports `api`, and `core` imports no workload.

Trade-offs accepted: the core is large (most of the domain), so the first
benefit of the split is identity, image and dependency isolation, not smaller
code. Four extra `pyproject.toml` files and four Dockerfiles increase upkeep and
the number of CI jobs. A smaller core can follow later by extracting domains
into their own libraries; this ADR does not require that.

### Module mapping

Mapping from `mvp/zavaforward_mvp` (the final row-per-file outcome is the parity
matrix, #197).

| Target project | Takes these `mvp` modules | Reason |
| --- | --- | --- |
| `core` (`zava_forward.core`) | `store`, `sqlstore`, `mssqlstore`, `factory`, `controls`, `finance`, `grants`, `governance`, `signoffs`, `resident_decisions`, `procurement`, `quality`, `workflows`, `continuity`, `recovery`, `ledger`, `insights`, `projection`, `ranking`, `documents`, `doc_controls`, `chatthreads`, `chat_privacy`, `chat_isolation`, `ai` (model client), `ai_tasks`, `lawstore`, `rulecards`, `scale_fixture`, `sensor_backfill`, `loadcheck`; data `policies/ranking-v1.json`, `law/law-source-register.json`; eval `document_control_fixtures.json` and `test_document_controls` | One domain and store interface imported by every workload; the model client is imported by both stores |
| `api` (`zava_forward.api`) | `server`, `auth`, `profile`, `timecapture`; all of `web/` including `vendor/` | Only HTTP surface and sign-in; the sole write path (ADR 0001) |
| `agents` (`zava_forward.agents`) | `assistants`, `ai_registry`, `ai_eval`; evals `ai_priority_golden.json`, `registry.json` | Proposal-only assistants, task registry and offline evaluation |
| `orchestrator` (`zava_forward.orchestrator`) | `digest_blob`, `token_store` | Scheduled jobs, no interactive path |
| `importer` (`zava_forward.importer`) | No `mvp` module today; eval `document_form_fixtures.json` and `test_document_form_fixtures`. New quarantining import code (ADR 0001) is built here | `store.py` and `sqlstore.py` import `doc_controls`, so the scanner stays in the core; the import workload calls it and owns the new import service |

Notes: `chat_fixture.py` is test support (it imports `assistants` and `auth`), so
it moves to the test tree of the project that owns its subject rather than into
a package; `scale_fixture`, `sensor_backfill` and `loadcheck` are developer
tools kept in a `zava_forward.core.synthetic` sub-package that no image
entry point imports. Test modules follow their subject: for example
`test_assistants`, `test_ai_*` and `test_eval_registry` go to `agents/tests`;
`test_auth`, `test_role_matrix`, `test_role_endpoint_inventory`,
`test_ui_support`, `test_accessibility_baseline`, `test_design_system`,
`test_content_standard` and `test_mvp` go to `api/tests`; `test_digest_blob` and
`test_token_store` go to `orchestrator/tests`; `test_document_form_fixtures` goes to
`importer/tests`; the remainder go to
`core/tests`. The two browser scripts go to `api/checks`.

Pull request #287 (release admission for the five assistants) merged on
2026-10-15 into `mvp/`; its code is covered by the parity matrix (#197).

### Package naming

The owner selected the namespace `zava_forward` on 2026-10-15, and
`zavaforward_mvp` is not kept. Candidates considered, for the record:

| Candidate | Advantages | Disadvantages |
| --- | --- | --- |
| `zava_forward` (selected) | Matches the programme name used in docs, infra and the repository; stable beyond the MVP stage; works as a namespace shared by several distributions | Ties code to the product name |
| `zava_workbench` | Describes the staff workbench | Excludes the agents and import workloads that are not the workbench UI |
| `retrofit_workbench` | Neutral and company-independent | Departs from every existing identifier; weaker traceability to Zava Forward |
| `zava_flow` | Short | Collides with the retrofit-flow research naming |

Naming scheme:

* Import namespace `zava_forward` is a PEP 420 namespace; no `__init__.py` at the
  `zava_forward` level, so projects install side by side without file clashes.
* Sub-packages: `zava_forward.core`, `.api`, `.agents`, `.orchestrator`,
  `.importer` (`import` is a Python keyword, so the import workload is
  `importer`).
* Distribution names use hyphens: `zava-forward-core`, `-api`, `-agents`,
  `-orchestrator`, `-import`.
* Entry points: `python -m zava_forward.api` (replaces `zavaforward_mvp.server`),
  `python -m zava_forward.orchestrator.token_store` and
  `python -m zava_forward.orchestrator.digest_blob --publish`. The Bicep job
  commands change in #200.
* Historical identifiers inside dated records stay exact; only live instructions
  change (rename-zava policy).

### Move-not-copy rule

* A module and its tests move together, in one pull request, with `git mv` so
  history follows the file. The same pull request updates imports, the owning
  project's `pyproject.toml`, the CI workflow path filters and test commands
  that cover the moved files, and any Dockerfile or Bicep reference.
* No module exists in both `mvp/` and `src/` at merge. No shim, re-export or
  duplicated copy is left behind in `mvp/`; remaining `mvp/` modules
  import the moved modules from the installed `zava_forward` packages (imports
  updated in the same pull request) until `mvp/` is deleted.
* A pull request moves a coherent group in dependency order: core leaves
  (`controls`, `projection`, `ranking`, `ledger`, `insights`), the store layer,
  then `agents`, then `api` with `web/`, then `orchestrator` and `importer`. The
  application stays deployable after each step.
* Test count must be equal or greater than the baseline recorded in #197;
  skips are explained in the pull request.

### New-feature rule

From the date the owner approves this ADR, new features are built only in
`src/`. A feature that needs an unmigrated `mvp` module migrates that module
first, under the move-not-copy rule, in the same pull request chain. Fixes to
code that has not yet moved may still be made in `mvp/` while it lives, but they
must not add capability. No new module is added under `mvp/` or `prototype/`.

### Phases

| Phase | Content | Exit evidence |
| --- | --- | --- |
| 1 Create `src` | Skeleton projects, `pyproject.toml`, CI jobs per project, dependency-rule tests, registry exclusions for vendor and data | Empty projects install and test in CI; ADR accepted (2026-10-15) |
| 2 Dual window | Incremental move-not-copy pull requests (#199), each recording its rubric total against the baseline; repoint CI, Docker, Bicep, scripts and docs (#200) | Every pull request meets the move-not-copy rule |
| 3 Retire `prototype/` | Separate earlier pull request once its useful content is mapped in the parity matrix (#197): remove `prototype/`, `prototype-validation.yml` and the dead `prototype/deploy/**/*.bicep` glob; the rubric no longer reads `prototype/` | No tracked file under `prototype/`; owner agrees |
| 4 Cut-over | The cut-over gate below, then a registry pull request that drops the `mvp/` globs | Gate issue signed |
| 5 Delete `mvp/` | Create the archive tag `v<BRD version>` on the last commit that contains `mvp/` (version read from the BRD frontmatter at that time, currently 0.18.0, example only), then delete `mvp/` in its own pull request after the registry pull request | Tag and log entry exist; no tracked file under `mvp/` |
| 6 Verify | Rebuild images from `src/`, deploy to the existing Container Apps, verify health, check links and references (#203) | Images healthy; no stale path references |

Phase 3 may run any time after the parity matrix maps `prototype/`; it does not
wait for phase 2. Status 2026-10-15: delivered for #202 step 1 in a pull request
that removes `prototype/`, `prototype-validation.yml` and the dead registry glob.

### Cut-over gate

The gate is the checklist in the sign-off issue (#201). Deletion of `mvp/` is
blocked until every item is evidenced there and the owner signs off:

* This ADR accepted; `prototype/` already retired.
* Parity matrix complete (#197): every feature is migrated, mapped to a backlog
  issue or explicitly retired with the owner's agreement.
* Tests migrated and passing in CI with at least the baseline count; browser
  JavaScript syntax check and non-root, read-only, no-data image checks pass for
  every image.
* CI, Dockerfiles, Bicep image paths and scripts repointed; images built from
  `src/` deployed and healthy on Azure.
* Rubric tracks `src/`; before and after totals recorded with the cause of any
  dip and a recovery expectation. A dip is accepted and is not a blocker.
* Dependent epics (#113, #136, #165, #157, #149) have no open pull request on the
  old paths.
* Docs, ADRs, index, log and live instructions updated; links checked.
* Archive tag name confirmed; private data relocated and backed up (below).
* No soak period (owner, 2026-10-15): deletion follows owner sign-off and a healthy deployment of the images built from `src/`.
* Owner signs off in the issue.

### Rubric counting

* `src/` counts from the first migrated module with its tests. `src/**/*` is
  already registered in `solution-code`, and tests, `pyproject.toml` and
  Dockerfiles sit under `src/<project>/`, so the layout needs no extra include
  globs. The registry does need extra excludes (`src/**/web/vendor/**`,
  `src/**/data/**`, `**/*.egg-info/**`, `**/build/**`) so third-party and
  private files are not scored; that is its own registry pull request (#198),
  merged before the first module moves because registry changes reopen every
  criterion and take effect only after merge.
* While both trees exist the scorer sees one `solution-code` artifact, so lines
  are not double counted. Move-not-copy prevents ambiguous duplicate evidence.
* `mvp/` stops counting in the dedicated cut-over registry pull request that
  removes the `mvp/` globs (the dead `prototype/deploy/**/*.bicep` glob was removed with `prototype/` in phase 3). The deletion pull
  request that precedes it is scored by the old registry.
* A deleted or moved-out-of-glob file counts as a change and can lower scores
  but never raise them. The temporary dip is accepted by the owner (2026-10-14);
  each migration pull request and the sign-off record the total against the
  baseline (47 of 100 at the time of writing), the cause, and which criteria are
  re-evidenced from `src/` in which pull request. `rubric_version` is not bumped
  during the move.

### Private data relocation

* Location: working data moves out of the repository tree to a per-user
  directory selected by `ZF_DATA` (default `~/.zava-forward/data/` on the
  developer machine); it never lives under `src/`. The synthetic-data generator
  (`build_mvp_dataset.py`) writes there and is repointed in #200.
* Out of git: `.gitignore` keeps `/mvp/data/` while `mvp/` exists and adds
  `/src/**/data/`; the check that refuses committed working data is extended to
  `src/`.
* Out of images: every Dockerfile copies named packages only (never the project
  folder wholesale), each project has a `.dockerignore` for `data/`, and the CI
  image job keeps the "no working data" assertion (`/data` and `/app/data`
  absent). Runtime data is mounted at `/data` and state at `/state`.
* Move and backup: before the cut-over gate the owner copies `mvp/data/`
  (including `properwarm.json`) to the new location, confirms the copy opens with
  the application, and keeps an encrypted backup outside git. No agent reads,
  prints or commits its contents.

### Verification and deployment

Test locally first: each project's unit suite, then local checks (image build,
non-root and read-only runs, `node --check` of the web scripts). Use Azure
resource group `ama` only when a check needs it, and delete anything created.
Deployment is on Azure only; non-Azure services exist solely in local tests.

## Consequences

* Positive: workload boundaries from ADR 0001 become install-time facts; images
  shrink to what each identity may run; the rubric keeps one registered tree;
  history follows files via `git mv`; the standard layout removes
  `PYTHONPATH` workarounds.
* Negative: more packaging files and CI jobs; a large shared core at first; a
  temporary `api` to `agents` import until #144; a temporary rubric dip.
* Risks: a long dual window lets `mvp/` and `src/` drift (mitigated by the
  new-feature rule and move-not-copy); open pull requests on old paths (#287 and
  the dependent epics) may conflict; the Bicep job commands and `az acr build`
  context must change in step with the first image built from `src/`.

## Owner Answers of 2026-10-15

* ADR approved.
* The `agents` image does not carry `core[sql]` or blob code, and the temporary
  `api` to `agents` import is accepted until #144.
* No minimum soak period before deleting `mvp/`.
* Old workflow and check names stay until after the cut-over, then are renamed in
  one pull request (#200), so required checks keep matching.
* The archive tag `v<BRD version>` is accompanied by a GitHub release (#202).

### Soak reconciliation note (2026-10-21)

The 2026-10-15 answer above is unchanged and not superseded. The #201 body
still lists the minimum soak period as an open decision and the owner asked on
2026-10-20 for a soak proposal for review, so the conflict is pending owner
decision D1 in the
[cut-over evidence pack](../architecture/cutover-evidence-pack.md#pending-owner-decisions).
This note does not change the Status or the cut-over gate and records no soak,
sign-off or deletion.

## Cut-over execution note (2026-10-27)

The owner SIGNED OFF #201 on 2026-10-27 and authorized retirement of the
remaining pointer directory. Archive `v0.21.0` follows the current BRD version
and records the last pre-deletion main commit. `prototype/` was already absent;
all executable work is in `src/`. See the
[dated retirement evidence and owner tag command](../architecture/cutover-evidence-pack.md#owner-authorized-directory-retirement-2026-10-27).
Workflow/check names remain unchanged. The earlier soak reconciliation and
unchecked technical/human evidence remain historical; this note establishes
no new deployed health, rubric score, release or operational approval.

## Related

[ADR 0001](./0001-azure-architecture.md), [ADR 0002](./0002-pilot-readiness-architecture.md),
[ADR 0004](./0004-per-user-agent-chat-and-memory.md),
[ADR 0005](./0005-regulatory-compliance-assistant.md), issues #195 to #203,
#138 (CI/CD pipeline) and #144 (container hosting).
