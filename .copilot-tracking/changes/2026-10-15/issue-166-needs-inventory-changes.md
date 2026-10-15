---
title: Issue 166 needs inventory implementation evidence
description: Changes, command outcomes and explicit acceptance limits
ms.date: 2026-10-15
---

## Context and scope

Task issue-166 / issue-166-needs-inventory. Automatic full-loop direction
from caller; implementation follows the Ready plan and single critique.
Plan: .copilot-tracking/plans/2026-10-15/issue-166-needs-inventory-plan.md.
Details: .copilot-tracking/details/2026-10-15/issue-166-needs-inventory-phase-details.md.
Research: .copilot-tracking/research/2026-10-15/issue-166-needs-inventory-research.md.
Critique: .copilot-tracking/reviews/plans/2026-10-15/issue-166-needs-inventory-plan-critique.md.

## P01: Metadata and test tooling

P01-T01 and P01-T02 complete: inventory v1.2.0, scenario v0.1.0, provenance
v1.1.0, documented review/citation rule and eleven inventory tests (five new).
All eleven canonical tests passed, including independently mutated copies.
No application runtime changes, SQL, workload imports, billable
AI calls, private data reads or deployment authorized by this tooling slice.
All row owners remain proposed; full #103 and owner review are not claimed.

## Command ledger: intake and planning

Commands are run from the repository root unless a directory is stated.
Read-only view/glob/rg calls inspected the issue-named documentation and public
source/tests; they made no writes. Patch tools created only RPI evidence so
far. One independent critique ran and returned Revise; all three planning
corrections were applied directly.

| Command | Result |
| --- | --- |
| `git status --short && git branch --show-current && gh issue view 166 --comments && gh pr list --head feat/src-needs-inventory-166 --state all --json number,state,baseRefName,url && gh api user --jq '{id,login}'` | Exit 0; clean assigned topic branch, no prior PR, authenticated 8036360/jmservera |
| `gh issue view 166 --json title,body,comments && gh issue view 103 --json title,body,comments && gh pr view 240 --json title,body,files && for n in 296 297 298 299 300 301 302; do gh pr view "$n" --json number,title,state,mergedAt,mergeCommit; done` | Exit 0; acceptance and open owner evidence verified; all seven moves merged |
| `git log -3 --oneline && python3 -m pip --version && command -v ruff && command -v mypy && git status --short && tail -45 docs/reference/log.md` | Exit 1 at missing ruff; later chained commands not executed. Base f593555; pip 26.2.1 |
| `python3 -m ruff --version; python3 -m mypy --version; python3 -c 'import zava_forward.core; print(list(zava_forward.core.__path__))'; git status --short; tail -30 docs/reference/log.md; ls -d /home/azureuser/source/ama-wt/issue-166/.venv* 2>/dev/null || true` | Missing ruff, mypy and zava_forward, each interpreter exit 1; final shell exit 0. Only owned RPI files untracked, no pre-existing local venv |
| `mkdir -p .validation-166/tmp && export TMPDIR="$PWD/.validation-166/tmp" TMP="$PWD/.validation-166/tmp" TEMP="$PWD/.validation-166/tmp" && python3 -c 'import tempfile; print(tempfile.gettempdir())' && python3 -m venv .validation-166/venv && .validation-166/venv/bin/python -m pip install --quiet -e 'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]' -e 'src/orchestrator[dev]' -e 'src/importer[dev]'` | Exit 0; scratch resolves inside the worktree; restored missing packages with pip only |
| `.validation-166/venv/bin/python -m unittest discover -s src/core/tests -p test_needs_inventory.py -v && .validation-166/venv/bin/ruff check --isolated --select E,F,I,B,UP --line-length 100 src/core/tests/test_needs_inventory.py && .validation-166/venv/bin/ruff format --isolated --check --line-length 100 src/core/tests/test_needs_inventory.py && .validation-166/venv/bin/mypy --strict --follow-imports=skip src/core/tests/test_needs_inventory.py` (same scratch exports) | Eleven tests passed; lint exit 1 on two 102-character lines; later chained checks not run. Lines corrected before rerun |

## Validation and deviations

P02-T01 complete. Core: 264 tests passed with two private-file readers excluded
before execution. Agents: 70 passed. API: 459 tests, OK with 92 skipped.
Orchestrator: 17 passed. Importer: 39 passed. All five projects' ruff,
format-check and mypy passed. Explicit isolated lint/format and strict mypy
passed for the changed test, bypassing its migration exemptions.

Local HTTP/SQLite smoke passed: responsive loopback app, login, four scoped
fictional cases, and an unchanged controlled-stage block with two missing
consent/funding reasons. This is a non-delivery development check, not an
AI-enabled prototype/MVP delivery. No AI was disabled or release authority
enabled; no real model was configured/called. Actual real AI, SQL Server and
Azure acceptance remain Not run. No application runtime behavior changed.

Docker `info` failed with permission denied on `/var/run/docker.sock`; image
and disposable SQL Server execution rely on CI, not a claimed local pass.
API's 92 skips remain explicit. The two further core exclusions are:

* `test_synthetic_provenance.ProvenanceRegisterTests.test_private_register_is_labelled_and_has_no_person_fields`
* `test_synthetic_provenance.ProvenanceRegisterTests.test_private_and_public_outputs_are_separated`

The first multi-project runner incorrectly supplied core fixture PYTHONPATH
to agents, causing a duplicate `test_dependency_rule` discovery ImportError.
No source change was needed: rerunning agents without PYTHONPATH and API/
orchestrator with their documented fixture paths passed. This was an
invocation correction, not a test or dependency fallback.

PC-001/002 safeguards were executed. PC-003 identity check passed: fresh
`gh api user` returned 8036360/jmservera; configured repository-local
`8036360+jmservera@users.noreply.github.com`. Author/committer verification
passed after commit 029f15f: both author and committer are
`jmservera <8036360+jmservera@users.noreply.github.com>`, with the requested
Copilot coauthor trailer.

## Command ledger: implementation and local verification

All validation scratch used
`TMPDIR=TMP=TEMP=/home/azureuser/source/ama-wt/issue-166/.validation-166/tmp`.
`PY` below is `.validation-166/venv/bin/python`; commands run from project
folders use `../../.validation-166/venv/bin/{python,ruff,mypy}`.
Here-document bodies are preserved below so the executed selection is
reproducible; stdout logs remained in owned scratch and contain no private
dataset values.

| Command | Result |
| --- | --- |
| `ruff format --isolated --line-length 100 src/core/tests/test_needs_inventory.py` | Exit 0, one file formatted |
| `ruff check --isolated --select E,F,I,B,UP --line-length 100 src/core/tests/test_needs_inventory.py` | Exit 0, clean |
| `ruff format --isolated --check --line-length 100 src/core/tests/test_needs_inventory.py` | Exit 0 |
| `mypy --strict --follow-imports=skip src/core/tests/test_needs_inventory.py` | Exit 0, one source file clean |
| For `core agents api orchestrator importer`: `(cd src/$project && ruff check . && ruff format --check . && mypy)` | Exit 0 throughout; mypy source counts 62/16/33/8/10; format counts 9/11/6/5/11 |
| `PY - <<'PY'` with multi-project runner below | Core 264 passed; agents discovery failed, exit 1, inappropriate shared PYTHONPATH; API/orchestrator/importer not reached |
| For `agents api orchestrator importer`: `(cd src/$project && python -m unittest discover -s tests -q)` with documented PYTHONPATH below | All exit 0; agents 70, API 459 (92 skipped), orchestrator 17, importer 39 |
| `git diff --check && git diff --stat && docker info --format '{{.ServerVersion}}'` | Diff checks exit 0; Docker exit 1, socket permission denied; no build attempted |
| `grep -E 'Ran [0-9]+ tests\|^OK\|^NOT RUN' .validation-166/core-tests.log .validation-166/api-tests.log && git status --short && git diff -- src/core/tests/test_needs_inventory.py` | Exit 0; counts/exclusions and intended diff inspected |
| `PY - <<'PY'` with local HTTP smoke below, PYTHONPATH=`$PWD/src/core/tests` | Exit 0, all smoke assertions passed; thread shut down and owned temporary directory removed |
| `PY -m unittest discover -s src/core/tests -p test_needs_inventory.py -q` | Exit 0; eleven tests passed again after formatting |
| `PY - <<'PY'` with JSON/link/boundary check below, then `git diff --check` | Exit 0; three JSON files parse, three relative links resolve, prohibited paths unchanged, no whitespace errors |

### Executed multi-project runner

The heredoc below ran under the scratch exports above. Its deliberate
private-reader exclusion occurred before running any core test:

```python
import os
from pathlib import Path
import subprocess
import sys
root = Path.cwd()
python = root / '.validation-166/venv/bin/python'
core_runner = '''import unittest, sys
excluded = {
 'test_synthetic_provenance.ProvenanceRegisterTests.test_private_register_is_labelled_and_has_no_person_fields',
 'test_synthetic_provenance.ProvenanceRegisterTests.test_private_and_public_outputs_are_separated',
}
def cases(suite):
 for test in suite:
  if isinstance(test, unittest.TestSuite):
   yield from cases(test)
  else:
   yield test
all_tests = list(cases(unittest.defaultTestLoader.discover('tests')))
assert excluded <= {test.id() for test in all_tests}
for name in sorted(excluded): print('NOT RUN (private-file reader):', name, flush=True)
result = unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(t for t in all_tests if t.id() not in excluded))
sys.exit(not result.wasSuccessful())
'''
for project in ('core', 'agents', 'api', 'orchestrator', 'importer'):
 env = dict(os.environ, PYTHONPATH=str(root/'src/core/tests')+os.pathsep+str(root/'src/agents/tests'))
 command = [str(python), '-c', core_runner] if project == 'core' else [str(python), '-m', 'unittest', 'discover', '-s', 'tests', '-q']
 log = root / f'.validation-166/{project}-tests.log'
 with log.open('w') as stream:
  result = subprocess.run(command, cwd=root/'src'/project, env=env, stdout=stream, stderr=subprocess.STDOUT)
 print(f'=== {project}: exit {result.returncode} ===', flush=True)
 print('\n'.join(log.read_text().splitlines()[-18:]), flush=True)
 if result.returncode:
  sys.exit(result.returncode)
```

Corrected remaining-suite invocation:

```bash
export TMPDIR="$PWD/.validation-166/tmp" TMP="$PWD/.validation-166/tmp" TEMP="$PWD/.validation-166/tmp"
for project in agents api orchestrator importer; do
  echo "=== $project tests ==="
  (cd "src/$project" &&
    if [ "$project" = api ]; then export PYTHONPATH=../core/tests:../agents/tests
    elif [ "$project" = orchestrator ]; then export PYTHONPATH=../core/tests
    else unset PYTHONPATH; fi &&
    ../../.validation-166/venv/bin/python -m unittest discover -s tests -q
  ) > ".validation-166/$project-tests.log" 2>&1
  result=$?
  tail -14 ".validation-166/$project-tests.log"
  echo "exit=$result"
  if [ "$result" != 0 ]; then exit "$result"; fi
done
```

### Executed local HTTP smoke

Invocation: scratch exports plus `PYTHONPATH="$PWD/src/core/tests" PY - <<'PY'`.

```python
import copy
import json
import tempfile
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from dataset import DATA
from zava_forward.api.server import App, make_handler
from zava_forward.core.sqlstore import SqlStore

with tempfile.TemporaryDirectory(prefix='smoke-166-') as scratch:
    seed = Path(scratch) / 'seed.json'
    seed.write_text(json.dumps(copy.deepcopy(DATA)))
    store = SqlStore(str(seed), str(Path(scratch) / 'smoke.sqlite'))
    assert not store.ai.endpoint, 'Smoke must not use a real model endpoint'
    app = App(store, 'synthetic-smoke-only')
    with ThreadingHTTPServer(('127.0.0.1', 0), make_handler(app)) as httpd:
        thread = threading.Thread(target=httpd.serve_forever)
        thread.start()
        base = f'http://127.0.0.1:{httpd.server_port}'
        def call(path, body=None, cookie=None):
            request = urllib.request.Request(base + path,
                data=None if body is None else json.dumps(body).encode(),
                headers={'Content-Type': 'application/json', **({'Cookie': cookie} if cookie else {})})
            try:
                with urllib.request.urlopen(request, timeout=5) as response:
                    return response.status, response.read(), response.headers
            except urllib.error.HTTPError as error:
                return error.code, error.read(), error.headers
        try:
            assert call('/')[0] == 200
            assert call('/api/cases')[0] == 401
            status, _, headers = call('/api/login', {'email': 'sam@example.test', 'password': 'synthetic-smoke-only'})
            assert status == 200
            cookie = headers['Set-Cookie'].split(';')[0]
            status, body, _ = call('/api/cases', cookie=cookie)
            assert status == 200 and len(json.loads(body)['items']) == 4
            status, body, _ = call('/api/cases/ZF-2/advance', {}, cookie)
            assert status == 409 and len(json.loads(body)['reasons']) == 2
            assert store.detail('ZF-2')['stage'] == 'Final checks before ordering'
            print('PASS: local HTTP responsive; login, four scoped synthetic cases, SQLite and consent/funding safe block; no real inference or Azure acceptance')
        finally:
            httpd.shutdown()
            thread.join(timeout=5)
            assert not thread.is_alive()
    store.db.close()
```

### Executed JSON/link/boundary check

```python
import json
import re
import subprocess
from pathlib import Path
root = Path.cwd()
pack = root / 'docs/reference/research/retrofit-synthetic-data'
for name in ('needs-inventory.json', 'scenario-manifest.json', 'provenance-register.json'):
    json.loads((pack / name).read_text())
checked = 0
for name in ('README.md',):
    path = pack / name
    text = path.read_text()
    start = text.index('## Synthetic data needs inventory and phase gate')
    end = text.index('### Generator gap closure', start)
    for link in re.findall(r'\]\(([^)]+)\)', text[start:end]):
        if not link.startswith(('https:', 'http:', '#')):
            assert (path.parent / link.split('#')[0]).resolve().exists(), link
            checked += 1
assert subprocess.check_output(['git','diff','--name-only','--','mvp','.env','.vscode','.copilot-tracking/github-issues'], text=True) == ''
print(f'PASS: three JSON files parse, {checked} changed-section relative links resolve, prohibited paths unchanged')
```

## Plan reconciliation and review readiness

P01 complete; P02-T01 complete. No significant divergence: invocation and
formatting corrections were ordinary local judgment. Five new test methods,
one manifest, no new runtime module/dependency/SQL, no removed test coverage.
P02-T02 review/publication are complete. Required owner evidence remains unchecked.
One post-implementation Review is Complete, outcome Residual work. No bounded
engineering defect identified; RV-001 owner ratification/historical matrix,
RV-002 full #103 evidence and RV-003 CI verification are routed. No second
Review or implementation of residuals is performed. PR #308 is open on main
with Refs #166; first commit 029f15f is pushed. All eleven initial CI jobs
were IN_PROGRESS when checked; no remote success or merge is claimed.

## Command ledger: Review and publication preflight

| Command | Result |
| --- | --- |
| `git diff -- docs/reference/README.md docs/reference/log.md docs/reference/research/retrofit-synthetic-data/README.md docs/reference/research/retrofit-synthetic-data/needs-inventory.json docs/reference/research/retrofit-synthetic-data/provenance-register.json src/core/README.md src/core/tests/test_needs_inventory.py && git diff --check` | Exit 0; combined display exceeded tool limit, so canonical portions were read separately |
| `git diff -- docs/reference/research/retrofit-synthetic-data/needs-inventory.json docs/reference/research/retrofit-synthetic-data/provenance-register.json` | Exit 0; complete corrections reviewed |
| `git diff -- docs/reference/research/retrofit-synthetic-data/README.md docs/reference/log.md src/core/README.md && git diff --numstat -- docs/reference/README.md` | Exit 0; docs/gate/log reviewed, index is one-row replacement |
| `gh api user --jq '{id,login}' && git branch --show-current && git config --local user.email 8036360+jmservera@users.noreply.github.com && git config --local user.name && git diff --check && git status --short` | Exit 0; correct account and branch, local privacy email configured; only intended files and owned scratch |
| `git fetch origin main --quiet && git rev-list --left-right --count origin/main...HEAD && test -s .gitignore && git diff --name-only && git ls-files --others --exclude-standard .copilot-tracking docs/reference/research/retrofit-synthetic-data && gh pr list --head feat/src-needs-inventory-166 --state open --json number,url` | Exit 0; 0 behind/0 ahead before first commit, nonempty gitignore, fifteen scoped paths, no duplicate open PR |

No repository PR template was found. PR body uses the one RPI Review and
this command ledger rather than creating another source review or parallel
review artifacts. Publication remains under the caller's explicit request;
the PR uses Refs #166 and leaves unavailable acceptance unchecked.

## Publication outcome and command record

PR: https://github.com/jmservera/ama/pull/308. Base main, head
feat/src-needs-inventory-166. The public body includes this command/result
ledger, the exact fixture selection and local smoke code. No tracked private,
configuration or mvp path changed. All fifteen staged paths were explicitly
named rather than staging the owned validation environment.

| Command | Result |
| --- | --- |
| `git add --` the fifteen scoped files listed by the preflight, then `git diff --cached --check && git diff --cached --stat` | Exit 0; fifteen intended files, no scratch/private data |
| `git -c user.email=8036360+jmservera@users.noreply.github.com commit -F -` with subject `feat(core): link synthetic needs inventory to iteration review`, Refs #166 and requested coauthor trailer | Exit 0; commit 029f15f, fifteen files |
| `git --no-pager show -s --format='%h%nAuthor: %an <%ae>%nCommitter: %cn <%ce>%n%B' HEAD` | Exit 0; both identities and trailer verified |
| `bash /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/shared/pr-reference/scripts/generate.sh --base-branch origin/main --merge-base --output .validation-166/pr-reference.xml` | Exit 0; generated 1702-line temporary reference, not staged; existing one-pass RPI Review reused |
| `git push --set-upstream origin feat/src-needs-inventory-166` | Exit 0; only assigned topic branch pushed |
| `gh pr create --base main --head feat/src-needs-inventory-166 --title 'feat(core): version synthetic needs inventory and iteration gate' --body "$(cat .validation-166/pr-body.md .copilot-tracking/changes/2026-10-15/issue-166-needs-inventory-changes.md)"` | Exit 0; PR #308 created |
| `gh pr view 308 --json number,url,state,baseRefName,headRefName,body --jq '{number,url,state,baseRefName,headRefName,refs166:(.body\|contains("Refs #166")),closes166:(.body\|contains("Closes #166"))}' && gh pr checks 308 --json name,state,link && git status --short` | Exit 0; correct open PR/base/head, Refs true/Closes false; eleven CI jobs IN_PROGRESS; only owned scratch untracked |

Closeout updates only these RPI evidence files, refreshes the PR body with
the final ledger, removes the explicitly owned `.validation-166/` directory,
and commits/pushes that evidence without amending history. Final CLI checks
verify the remote head and clean worktree. It does not run another Review,
start routed work, merge, change issue acceptance or claim pending CI passed.

## Open acceptance and follow-up

* Owner inventory/row-owner ratification and volume/scope decisions.
* Historical 2026-10-14 matrix unavailable; reconciliation Not run.
* Full #103 profile/default/workflow/endpoint execution evidence deferred.
* Actual AI/SQL/Azure acceptance is Not run by this documentation/test slice.
