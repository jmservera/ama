---
title: Building shared systems implementation evidence
ms.date: 2026-10-15
---

Task: 75 / shared-systems-75. Scope: full P01/P02 plan.

## Implementation State

Ready plan and details consumed; independent critique PC-001 to PC-004 applied.
P01 and local P02 implementation complete; ready for the one post-implementation
Review. Publication follows Review as administrative delivery, not more source
implementation. No material divergence, approval authority or deployment.

## P01 Model, Storage and Views

Added typed `core/buildings.py`, strict source-backed schema and exact
case/package applicability. Reused `SqlStore.DOCS`, inherited by MSSQL, without
new SQL. Added scoped checks to home readiness and new/reissued/corrective
instructions; unknown linked context blocks, not unknown legacy unlinked homes.
Home gates are not replaced. Hazard intake/referral remains independently usable.

Staff-only GET and read-only home/building/home UI preserve Finance-role cost
projection. Shared costs are never combined with home allocation. No building
approval, release, editor or AI prompt enrichment was added. Existing AI registry
and proposal/human-gate paths remain available; actual release enablement and
real inference are not established by this change.

## P02 Validation Corrections and Current State

The first core check found formatting/loop-lambda lint problems. Replaced
temporary test lambdas with bound-method/argument tables and formatted additions.
Strict typing required a local test fixture search path in core and a narrow
API mypy missing-import declaration for that same fixture (strictly checked
in core); no production or new-test error exemption was added.

The first full API suite rejected internal wording "Holds". Changed visible
copy to "Work stopped pending review" and allowed only the exact code-key
expression in the existing copy audit, not the user-visible term.

The first remaining-project suite command incorrectly supplied core fixtures
to agents, resolving a duplicate test module. Corrected commands to each
component's documented path; all three projects then passed.

An actual browser click into the sibling exposed incomplete synthetic quality
metadata, not a production model failure. Completed the fixture and reran the
same home/building/sibling navigation successfully. Added separate quality,
closure, hazard referral and SQL document sync/conflict regressions.

## Commands and Results

Commands run from repository root unless a project directory is specified.
File reads/searches and apply_patch are tools, not shell commands.

| Command | Result |
| --- | --- |
| `git status --short && git branch --show-current` | Clean, feat/src-shared-systems-75 |
| `gh issue view 75 --comments` and `gh issue view 75 --json title,body,comments` | Read all three criteria and owner src pivot |
| `gh pr list --head feat/src-shared-systems-75 --state all --json number,state,baseRefName,url` | No prior PR |
| `gh pr view N --json title,state,mergedAt` for N=296..302 | All seven moves merged on 2026-10-15 |
| `git log -3 --oneline && git status --porcelain=v1 && git ls-files 'src/*/pyproject.toml' 'src/core/zava_forward/core/*' 'src/api/zava_forward/api/*' '.copilot-tracking/*/*75*'` | Clean branch at f593555, project manifests found; import roots use inner src |
| `python3 --version && command -v ruff && command -v mypy && python3 -m pip --version` | Python 3.12.3; command stopped at missing ruff |
| `python3 -m pip --version; python3 -m ruff --version; python3 -m mypy --version; git ls-files '*requirements*' \| head -20` | pip 26.2.1; ruff/mypy missing; requirements available |
| `python3 -m venv /home/azureuser/.copilot/session-state/0de863c2-0148-4822-ac4b-49f7cf41eb19/files/venv` then `python -m pip install --quiet -e 'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]' -e 'src/orchestrator[dev]' -e 'src/importer[dev]'` | Installed existing manifests and missing dev tools; pip only |
| core: `python -m unittest discover -s tests -p test_buildings.py -v` then `ruff check src/zava_forward/core/buildings.py tests/building_fixture.py tests/test_buildings.py` | Initial 7 tests passed; 9 lint findings, fixed |
| core: focused tests `-q`, focused `ruff check`, `ruff format --check`, `mypy` | 7 tests/lint passed; formatting identified one file, fixed |
| api: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_buildings.py -v` then focused lint/format/mypy and JS syntax | 3 HTTP tests passed; import order/line length findings fixed before remaining checks |
| `ruff format src/core/src/zava_forward/core/buildings.py src/core/tests/building_fixture.py src/core/tests/test_buildings.py src/api/tests/test_buildings.py` | 1 reformatted, 3 unchanged |
| core: `ruff check . && ruff format --check . && mypy`, then planned API checks | Lint/format passed; 4 core typing findings, fixed; API portion did not execute |
| core: `python -m unittest discover -s tests -q && ruff check . && ruff format --check . && mypy` | First full run: 268 passed, static checks passed; pre-existing sensor ResourceWarnings |
| api: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q && ruff check . && ruff format --check . && mypy && node --check src/zava_forward/api/web/app.js` | First full run: 462 tests, 1 copy-audit failure, 92 skipped; fixed wording |
| `for project in agents orchestrator importer; do (cd src/$project && PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q && ruff check . && ruff format --check . && mypy) \|\| exit; done` | Wrong fixture path caused agents duplicate test import; no source defect, corrected below |
| `git diff --stat && git status --short && docker info --format '{{.ServerVersion}}'` | Diff inspected; Docker socket permission denied; no image built locally |
| `tail -28 docs/reference/log.md && sed -n '1,115p' .github/workflows/src-ci.yml` | Confirmed append-only style and authoritative per-project CI paths |
| `for project in agents orchestrator importer; do (cd src/$project && if [ "$project" = orchestrator ]; then export PYTHONPATH=../core/tests; else unset PYTHONPATH; fi && python -m unittest discover -s tests -q && ruff check . && ruff format --check . && mypy) \|\| exit; done` | agents 70, orchestrator 17, importer 39: all passed; all project lint/format/mypy passed |
| api: `ruff check . && ruff format --check . && mypy && node --check src/zava_forward/api/web/app.js` then targeted copy audit | Lint/format passed; broad fixture path exposed legacy mypy errors, removed it and used narrow shared-fixture import config |
| core focused tests and all static checks, then api all static/JS checks and `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_content_standard.py -q` | Core 7 tests and all static checks passed; API typing 34 files and copy audit 4 tests passed |
| `python3 tools/rename-zava-tests.py && git diff --check` | 25 tests: 7 missing-dependency errors (pptx/Pillow); no migration performed |
| `python -m pip install --quiet -r tools/rename-zava-requirements.txt && python tools/rename-zava-tests.py && git diff --check` | Existing pinned tooling restored via pip; 25 passed, expected broken-PPTX diagnostic; diff clean |
| api: full 462-test command above repeated after fixes | 462 tests OK, 92 skipped; all lint/format/mypy/JS syntax passed |
| core: `python -m unittest discover -s tests -p test_buildings.py -v && ruff check . && ruff format --check . && mypy` | Expanded 9 regressions passed; 65-file typing and lint/format passed |
| core: full suite/static command above repeated on final fixture, then api focused 3 tests/static/JS command | Final core 270 passed; API 3 HTTP tests passed; core/API lint/format/mypy and JS syntax all passed |
| `git status --short && git diff --check && git diff --numstat && gh api user --jq '{id,login}'` | Only task files changed; whitespace clean; authenticated 8036360 / jmservera |
| `git --no-pager diff -- src/core/src src/api/src src/core/pyproject.toml src/api/pyproject.toml src/api/tests/test_content_standard.py src/api/tests/test_role_endpoint_inventory.py && git diff --check && git status --porcelain=v1 -- mvp .env .vscode .copilot-tracking/github-issues` | Final integrated diff reviewed once; whitespace clean; forbidden paths unchanged |

All venv commands use
`export PATH=/home/azureuser/.copilot/session-state/0de863c2-0148-4822-ac4b-49f7cf41eb19/files/venv/bin:$PATH`.
Repeated commands are recorded above with each distinct result rather than
presented as only the final success.

## Local App and Browser Commands

Executed twice with `PYTHONPATH=src/core/tests ZF_AUTH=password ZF_ENV=local`
using the venv Python. Server startup:

```python
import signal
import tempfile
from http.server import ThreadingHTTPServer
from building_fixture import fixture, open_store
from zava_forward.api.server import App, make_handler

def stop(*args):
    raise SystemExit(0)

signal.signal(signal.SIGTERM, stop)
with tempfile.TemporaryDirectory(prefix="ama-building-75-") as folder:
    store = open_store(folder, True, fixture())
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, "synthetic-only")))
    print(f"SYNTHETIC_APP_URL=http://127.0.0.1:{server.server_address[1]}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()
        store.db.close()
```

First server: port 44731. Browser navigate `/app`, fetch `/healthz` and POST
`/api/login` for `pam@example.test`: both 200. Followed home ZF-2 to building;
all categories visible with GBP 12000.00 shared cost. Sibling navigation exposed
incomplete fixture `quality.items` (TypeError); completed source fixture and
stopped that server.

Final server: port 42231. Repeated health/login (200), home ZF-2 -> building
SYN-B1 -> sibling ZF-3. Browser DOM assertions verified all six headings,
both home links, focus on MAIN, shared GBP 12000.00 without GBP 6000.00 home
allocation, and successful sibling rendering with its own allocation.
Reauthenticated as `sam@example.test`: restricted-cost notice present,
building API omitted costs and home API omitted allocation. Final browser
console: zero errors/warnings. Initial unauthenticated 401 responses are
expected before login. Closed browser and stopped both servers; temporary
SQLite data removed by the server context manager. This is engineering browser
evidence, not direct human UX or screen-reader acceptance.

## Acceptance Mapping

* [x] Building record displays shared systems, dependencies, holds (plain-language
  stopped-work section), shared works and costs: core/API tests and browser.
* [x] Home evidence and cost allocation remain home: exact serialization and
  Finance/non-Finance checks, separate browser views and no shared aggregation.
* [x] Shared ID does not inherit home approvals: separate resident/funding/
  technical negative tests, independent quality/closure/evidence tests and
  affected/unaffected home/package checks.
* [ ] Real SQL Server/Azure durability and actual model run for this revision.
* [ ] Real register, named operational owners, governed updates/release and
  direct human UX/accessibility acceptance.

The issue's three bounded model criteria have local synthetic evidence; this
does not tick the wider PRD AC-001/002/003/043 or platform acceptance wholesale.
Publish with `Refs #75`, not an automatic closing keyword.

## Evidence Boundaries and Remaining Work

No real building register, live SQL Server, real inference, Azure deployment,
Docker image or human UX acceptance claimed. Existing gated AI remains in
place. A synthetic local check cannot satisfy full PRD platform acceptance.
Record test and publication commands below as execution proceeds.

## Review and Publication Handoff

One Review executed Complete, outcome Residual work:
`.copilot-tracking/reviews/logs/2026-10-15/shared-systems-75-review.md`.
No implementation defects established within the local assessed slice.
RV-001 actual-platform evidence, RV-002 authoritative register/governed update
rights and RV-003 direct human acceptance remain separate follow-ups.
Do not start them without owner selection/authority. No second Review planned.

Authenticated GitHub account was verified as 8036360 / jmservera; the requested
privacy-safe email matches. `.gitignore` exists and excludes runtime/test data.
Next administrative actions: configure local author/committer identity, stage
the reviewed files, commit with Conventional Commit and coauthor trailer, push
only feat/src-shared-systems-75 and create the main PR using Refs #75.
Actual publication results will be appended after creation, without amending
or rewriting any commit.

## Publication Results and Concurrent Main Synchronization

* Source and all RPI artifacts committed as `acf40ba`
  (`feat(core): model scoped building systems and costs`), correct privacy-safe
  author/committer and coauthor trailer. Topic push succeeded.
* PR https://github.com/jmservera/ama/pull/310 opened against main with Refs #75,
  complete acceptance limitations, validation results and command ledger.
* Main advanced concurrently to `a63351f` (merged #308). Initial PR state was
  CONFLICTING with no checks scheduled; the conflict was the simultaneous
  append to `docs/reference/log.md`, not executable code.
* Administrative topic synchronization uses a regular merge, never rebase,
  amend, force push or merge into main. Kept both log entries verbatim, removed
  only conflict markers; index/core README changes auto-merged. Main's accepted
  inventory documents/tests are inherited, not reimplemented. This is not a
  Review-finding correction or a second Review.

| Administrative command | Result |
| --- | --- |
| `rm --` the eight exact task-generated `.playwright-mcp` snapshot/log files, then `rmdir .playwright-mcp` | Browser scratch files removed; no broad/recursive deletion |
| `git config --local user.email 8036360+jmservera@users.noreply.github.com && git config --local user.name jmservera && git add -A` then `printf ... \| GIT_AUTHOR_EMAIL=8036360+jmservera@users.noreply.github.com GIT_COMMITTER_EMAIL=8036360+jmservera@users.noreply.github.com git commit -F -` | acf40ba created, 25 files, full RPI artifacts included |
| `git push --set-upstream origin feat/src-shared-systems-75` | Topic pushed, upstream set; main untouched |
| `bash .../skills/shared/pr-reference/scripts/generate.sh --base-branch origin/main --merge-base --output .../files/shared-systems-75-pr-reference.xml` | Generated 2061-line reference in session artifacts |
| `git fetch origin main && git rev-list --left-right --count origin/main...HEAD && git ls-files .github docs \| grep -i pull_request_template \|\| true` | Main advanced one commit; branch one commit ahead; no PR template |
| Python generated session PR body from summary plus existing command ledger; `gh pr create --base main --head feat/src-shared-systems-75 --title 'feat(core): model building shared systems and scoped costs' --body-file .../files/shared-systems-75-pr-body.md` | PR #310 created |
| `gh pr view 310 --json number,url,state,baseRefName,headRefName,mergeable,statusCheckRollup && gh pr checks 310` | Correct head/base; CONFLICTING, no checks reported |
| `git log --oneline HEAD..origin/main && git diff --name-only HEAD...origin/main && git merge-tree "$(git merge-base HEAD origin/main)" HEAD origin/main \| grep ...` | Read-only conflict inspection; log append overlap from #308 |
| `git status --short && git branch --show-current && git merge --no-commit origin/main` | Clean expected topic; log conflict only, index and core README auto-merged |
| Post-sync core full suite/static command, then API focused building suite/static/JS command; `git add` resolved log and delivery evidence, `git diff --cached --check && git diff --check` | Core now **275 passed** (five inherited #308 tests); API 3 passed; all affected static checks passed; staged resolution clean |

### Final Publication Evidence

* Regular merge commit `440620c` synchronized the topic with main; push
  succeeded. PR #310 is MERGEABLE. No merge into main or history rewrite.
* At code revision `440620c`, all **11 scheduled CI checks passed**, including
  all five source projects, namespace/no-working-data gates, image, MSSQL,
  legacy test and validation jobs. Source CI builds the four workload images
  and verifies their runtime and dependency boundaries.
* CI SQL Server coverage exercises existing store/five-assistant contracts.
  It is not evidence of Azure deployment, real model inference, or a new
  building-specific SQL Server acceptance scenario.
* The Capstone Rubric Scorer is **disabled_manually** on GitHub. It did not
  run; no rubric pass is claimed and no workflow setting was changed.
  Owner disposition is needed before treating the rubric gate as satisfied.
* Local Docker remains permission denied; successful CI image evidence does
  not change that local result. Register authority, real Azure/model evidence
  and human UX/accessibility acceptance remain unticked.
* No feature executable changes or second Review followed the single Review.
  The final additional commit only records publication evidence and state.

| Command | Result |
| --- | --- |
| From `src/core`: `python -m unittest discover -s tests -q && ruff check . && ruff format --check . && mypy`; from `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_buildings.py -q && ruff check . && ruff format --check . && mypy && node --check src/zava_forward/api/web/app.js` | Post-sync core 275 passed, API 3 passed, all affected static checks passed |
| `git add` resolved log and delivery artifacts; `printf ... \| GIT_AUTHOR_EMAIL=8036360+jmservera@users.noreply.github.com GIT_COMMITTER_EMAIL=8036360+jmservera@users.noreply.github.com git commit -F - && git push origin feat/src-shared-systems-75` | Merge commit 440620c created with required trailer and pushed |
| `gh pr view 310 --json mergeable,statusCheckRollup`; `gh run list --branch feat/src-shared-systems-75 --limit 5 --json databaseId,name,status,conclusion,headSha` | Initial eventual-consistency response CONFLICTING, refreshed MERGEABLE; checks subsequently scheduled |
| `gh pr checks 310`; `gh api repos/jmservera/ama/actions/permissions --jq '{enabled,allowed_actions}'`; commit check-runs API | Actions enabled; 11 checks scheduled |
| `gh pr checks 310 --watch --interval 20` | All 11 checks passed; runs 38807461342, 38807461367 and 38807461702 successful |
| `gh api repos/jmservera/ama/actions/workflows/rubric-score.lock.yml --jq '{name,state,path}'` | Capstone Rubric Scorer disabled_manually; requires owner disposition |
| `gh run list --branch feat/src-shared-systems-75 --limit 10 --json databaseId,name,status,conclusion,headSha && gh pr view 310 --json mergeable,reviewDecision` | Three successful workflows at 440620c, MERGEABLE, no human review decision |

Closeout commands use `git diff --check`, an ordinary evidence-only Conventional
Commit with the same privacy-safe author/committer and coauthor trailer, normal
topic push, regenerated session PR body, `gh pr edit 310 --body-file ...`,
`gh pr checks 310 --watch --interval 20` and final read-only branch/status checks.
Their live publication/check status is reported in PR #310; none merge the PR,
enable the disabled rubric workflow or start follow-up implementation.
