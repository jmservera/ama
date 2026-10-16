---
title: Issue 200 source cut-over changes and validation
ms.date: 2026-10-16
---

Task #200 / `repoint-ci-to-src-200`. Full plan scope; implementation complete,
reviewed and published in PR #321.
Plan/details/research share the same dated slug. Source edits begin after the
single final-candidate critique was dispositioned. No Azure or private-data action.

## P01 implementation

API module entry delegates to the existing typed server.main; version probes
explicitly import/print without starting a server. Workflow names, job IDs and
concurrency groups are unchanged; filters cover shared src build inputs. Existing
validation job also runs branding regressions when its tooling changes.

API image drops orchestrator; token maintenance and digest Bicep jobs select the
existing orchestratorImage parameter, preserving commands, identities and grants.
Branding tooling uses packaged web and policy targets and cannot recreate mvp/web.
Already-merged coverage imports, ignore rule and committed-data guard are reused.
The dataset builder now uses the shared data_file resolver directly, preserving
a custom ZF_DATA JSON filename rather than silently substituting zavaforward.json.

The shared data resolver is extracted to core.data_paths rather than making
runtime import synthetic tools (which image entry points must not import).
Synthetic.output_dir delegates to it, preserving existing generator paths; the
isolated installed-CLI fixture copies that new dependency too. This is a directly
relevant plan refinement, not a feature or dependency-boundary change.

## P02 commands and evidence

Preflight: `gh issue view 200 --comments` and JSON body read; clean specified topic
branch, no matching open PR; `gh api user` returned id 8036360/login jmservera.
`az bicep version`: 0.48.1, exit 0.
`docker info --format '{{.ServerVersion}}'`: permission denied (exit 1);
`sudo -n docker info --format '{{.ServerVersion}}'`: 29.9.0, exit 0.
`python3 -c 'import zava_forward.core'`: ModuleNotFoundError.
`ls /tmp/zf164/bin/{python,pip,mypy,ruff}`: python/pip present; mypy/ruff absent.
These missing-dependency probes authorize pip restoration, not dependency upgrades.

### Dependency restoration

| Command | Result |
| --- | --- |
| `/tmp/zf164/bin/pip install mypy ruff` | Exit 0; mypy 2.4.0, ruff 0.17.1 |
| `python3 -m venv /tmp/zf200` | Exit 0; task-isolated application environment |
| `/tmp/zf200/bin/pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator -e src/importer` | Exit 0; all five editable distributions |
| `/tmp/zf200/bin/python tools/rename-zava-tests.py` (first attempt) | Exit 1; seven errors for missing pptx/Pillow |
| `/tmp/zf200/bin/pip install -r tools/rename-zava-requirements.txt` | Exit 0; restored declared tooling dependencies |
| `/tmp/zf164/bin/pip install 'playwright==1.64.0'` | Exit 0 after API mypy reported missing Playwright imports |

### Unit and static checks

Executed from repository root with the task venv activated:

```bash
. /tmp/zf200/bin/activate
ROOT="$PWD"
for project in core api agents orchestrator importer; do
  (cd "src/$project" &&
    PYTHONPATH="$ROOT/src/$project/src:$ROOT/src/$project/tests:$ROOT/src/core/src:$ROOT/src/core/tests:$ROOT/src/agents/src:$ROOT/src/agents/tests" \
    python3 -m unittest discover -s tests -q) || exit
done
for project in core api agents orchestrator importer; do
  (cd "src/$project" && /tmp/zf164/bin/mypy &&
    /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check .) || exit
done
```

| Check | Final observed result |
| --- | --- |
| core full suite | 393 tests, 117.988 s, OK |
| API full suite | 517 tests, 289.723 s, OK, 101 skipped |
| agents full suite | 70 tests, OK |
| orchestrator full suite | 17 tests, OK |
| importer full suite | 39 tests, OK |
| mypy (core/api/agents/orchestrator/importer) | Exit 0 for all; 82/42/16/8/10 files |
| ruff check and format --check | Exit 0 in all five projects; existing migration exemptions retained |

Full suites ran 1,036 tests including 101 skips. API skips cover gated SQL Server
contracts (`ZF_TEST_MSSQL` unset), two missing azure-core integration paths and
the opt-in browser check. These are not live SQL/model/browser acceptance.
Existing sensor ResourceWarnings are recorded, not suppressed or changed.

The first core run exposed the isolated stock-fabric test's missing copied
data_paths dependency (8 subtest failures/1 error); fixed the fixture's copy list,
then the entire five-suite loop passed. Initial API mypy also caught the new
entry point's call to untyped main; annotated the existing main return as None,
then all project checks passed. No broad lint/type exemption was added.

Final generator filename refinement happened after that full run:

```bash
(cd src/core &&
  PYTHONPATH="$PWD/src:$PWD/tests" python3 -m unittest discover -s tests -p test_generated_dataset.py -q &&
  /tmp/zf164/bin/mypy && /tmp/zf164/bin/ruff check . &&
  /tmp/zf164/bin/ruff format --check .)
```

Exit 0; 14 tests (including the added exact-filename default test), 6.685 s.
Mocked fictional register only; deterministic 980-case fixture bytes agree.
No real stock register is opened by these tests.

### Infrastructure, branding and syntax

```bash
az bicep build --file infra/main.bicep --stdout > /dev/null
az bicep lint --file infra/main.bicep
REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -q
python3 tools/rename-zava-tests.py
node --check src/api/src/zava_forward/api/web/app.js
node --check src/api/src/zava_forward/api/web/assistants.js
node --check src/api/src/zava_forward/api/web/chat.js
test -z "$(git ls-files mvp/data ':(glob)src/**/data/**')"
git diff --check
```

All exit 0. Infra: 78 tests, 10.065 s; branding: 25 tests, 1.083 s.
The branding suite intentionally logs "Cannot migrate broken.pptx" for its
malformed-input negative test; the suite passes. Bicep creates no tracked ARM file.

Additional inline Python assertions passed: YAML workflow name, job ID and explicit
check name equality against HEAD for all three workflows; all five installed
namespace distributions (`zava_forward.__file__ is None`, five paths), explicit
API version stdout `zava-forward-api 0.1.0`; generator uses installed core resolver
and coverage imports installed core. Final import check confirms
`builder.data_file is data_file`; it does not execute the private generator.
Added relative Markdown link target check: ten targets exist. Git review confirms
only mvp/README.md remains tracked and is unchanged.

### Images and installed local application

```bash
sudo -n docker build -q -f src/api/Dockerfile -t zava-forward-api:issue-200 src
sudo -n docker build -q -f src/orchestrator/Dockerfile -t zava-forward-orchestrator:issue-200 src
sudo -n docker build -q -f src/agents/Dockerfile -t zava-forward-agents:issue-200 src
sudo -n docker build -q -f src/importer/Dockerfile -t zava-forward-importer:issue-200 src
python3 .copilot-tracking/changes/2026-10-16/repoint-ci-to-src-200-validate.py
```

All builds exit 0. API rebuilt after the final server annotation. Image IDs:
API d776e39d4909, orchestrator 117e2abdcdcb, agents 60ba62666eac,
importer 291a04a8e58c. The committed evidence harness records exact run commands
and assertions: UID 10001, no baked working dataset, read-only root, writable
state tmpfs, dropped capabilities, exact version stdout on every image; no SQL/
Blob client in agents; no orchestrator package in API; both job modules import
from orchestrator. API default entry point responds 200 on /healthz and returns
the exact packaged PNG. Installed API also responds 200 from outside checkout.
All data is a newly constructed empty cases/staff fixture.

First harness run exited on a Docker startup ConnectionResetError; broadened
only its bounded readiness retry to cover ConnectionError. Final harness passed
twice; task-created API container removed in finally and temporary data/process
cleaned. No Azure resources created. Local build tags retained as validation
outputs, not published.

## Amendments and divergences

PC-001's filesystem premise rejected in favor of caller-approved /tmp/zf164;
PC-002's explicit-print probe accepted. Existing generator, coverage imports,
ignore rule and installed infra-script imports are reused, not rewritten.
Added four focused methods (API delegation, core runtime/generator path agreement,
generator exact filename default, compiled Bicep job image/commands); no tests removed. Existing branding and
installed-CLI regressions updated for current canonical paths.

## Acceptance and remaining work

New-tag Azure deployment/healthy revisions, private copy/encrypted backup and
owner sign-off remain unmet; no mvp deletion, workflow/check rename or legal
approval is inferred.

| Issue criterion | Status and evidence boundary |
| --- | --- |
| Standard pyproject src packages; installed CI/scripts | Met locally; reuse merged packages and source installs |
| Workflow paths, context, requirements; deliberate naming | Met; src context/filters, existing hashed requirements; names unchanged by assertion |
| Non-root/no-data/read-only src images | Met locally on all four images |
| New tag deployed/healthy on existing Azure resources | Unmet, not attempted; running historical tags untouched |
| Bicep commands and build/lint | Met locally; correct existing module paths, isolated job image, compiled assertions |
| Private default output, ignore and committed-data check | Code/guards met; custom filename covered; actual private relocation/backup not performed |
| rename tests and infra/tests | 25 and 78 tests pass |
| Exact historical identifiers | Preserved; dated recipes, original case study and previous artifacts unchanged |

Implementation has no remaining source work or material decision blocker.
One post-implementation Review executed completely; outcome Residual work for
full issue acceptance, no local implementation defects. RV-001 deployment,
RV-002 private backup/retirement and RV-003 later naming are routed separately.
The local RPI task is complete; parent publication proceeds without another Review.

## Publication

Authenticated account rechecked with `gh api user`: id 8036360/login jmservera.
`git config --local user.email 8036360+jmservera@users.noreply.github.com`;
`git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both confirm it.
Publish only chore/repoint-ci-to-src-200 to main PR, never force-push.

* `git add -u` plus the exact eight new dated artifacts and core resolver:
  staged 36 intended files; prohibited-path guard and cached whitespace check
  passed. No .env/.vscode/github-issues/private data staged.
* `git commit -F -`: bed0c6a, `build(src): finish CI and image path cut-over`,
  `Refs #200` and required Copilot co-author trailer. Privacy-safe identity
  confirmed for author and committer.
* `git fetch origin main --quiet && git rev-list --left-right --count origin/main...HEAD`:
  exit 0, `0 1` (not behind).
* `bash .../skills/shared/pr-reference/scripts/generate.sh --base-branch origin/main --merge-base --output <session-files>/issue-200-pr-reference.xml`:
  exit 0, 1,757-line reference generated outside the repository; reviewed source
  evidence already covered by the single Review.
* `git push --set-upstream origin chore/repoint-ci-to-src-200`: exit 0, new topic
  branch published, no main push or history rewrite.
* `gh pr create --base main --head chore/repoint-ci-to-src-200 --title 'build(src): finish CI, image and tooling cut-over' --body-file <session-files>/issue-200-pr.md`:
  exit 0, https://github.com/jmservera/ama/pull/321.
* `gh pr view --json number,url,state,baseRefName,headRefName,commits,statusCheckRollup`:
  PR #321 OPEN, main base, expected topic/commit/co-author; checks not yet reported
  at creation. PR body includes commands/results, dated artifact links, remaining
  criteria and Refs #200, not a closing keyword.

Parent completion documentation records publication on the same PR in a further
commit; no source modification, repeat critique or repeat Review. Hosted checks
remain separate from measured local results. Merge remains the owner's decision.
