---
title: Issue 176 src determinism implementation evidence
description: Changes, exact local commands, results and open acceptance boundaries
ms.date: 2026-10-15
---

## Scope and status

Task #176; automatic full RPI requested. P01/P02/P03 complete; implementation
commit 774137a pushed, PR #309 open to main. Evidence-only handoff commit
records delivery. Review Complete / Residual work; issue remains open.
Plan and details share slug issue-176-src-determinism. No private data or live
service reset. Source changes limited to migrated core/synthetic and core tests.

## Research and planning commands

All commands ran in the prescribed worktree; read-only source inspection used
view/glob/rg tools in addition to these shell commands.

| Command | Result |
| --- | --- |
| `git status --short && git branch --show-current` | Clean at intake; feat/src-synthetic-determinism-176 |
| `gh issue view 176 --comments` | Owner reopen and src pivot read; AC unchanged |
| `gh issue view 176 --json title,body,state,url` | Three ACs open; exact scope captured in research |
| `gh pr list --head feat/src-synthetic-determinism-176 --json number,state,baseRefName,url` | No existing PR |
| `gh api user --jq '{id,login}'` | 8036360, jmservera; prescribed privacy-safe address verified |
| `for n in 296 297 298 299 300 301 302; do gh pr view "$n" --json number,title,state,mergedAt; done` | All seven merged, source migration reused |
| `git log -5 --oneline` | Baseline f593555 includes migrated source and later chat/import work |
| `gh issue view 183 --json state,title; gh issue view 177 --json state,title; gh issue view 200 --json state,title` | All remain open; code existence is not full acceptance |
| `python3 --version; python3 -m pip --version` | Python 3.12.3, pip 26.2.1 |
| `command -v ruff; command -v mypy; python3 -m ruff --version; python3 -m mypy --version` | Missing tools; module probes exit 1 |
| `python3 -c 'import zava_forward.core; print("core:", zava_forward.core.__file__)'` | ModuleNotFoundError, local install required |
| `git ls-files '*copilot-tracking.instructions.md' '*stock*generator*'; ls -d .venv /tmp/ama* 2>/dev/null \| head` | No applicable tracking instructions or stock-generator source found |
| `ls -la /home/azureuser/source/ama-wt/issue-176 \| head -18; git ls-files .github/workflows/src-ci.yml; wc -l docs/reference/log.md` | Worktree and CI locations confirmed; log 3126 lines before append |
| `python3 -m venv /home/azureuser/source/ama-wt/issue-176/.venv && .venv/bin/python -m pip install -q -e 'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]' -e 'src/orchestrator[dev]' -e 'src/importer[dev]'` | Exit 0; isolated worktree environment, pip only |

## P01 compatibility capture

Before any generator edits, ran `.venv/bin/python -` with the following script
(exit 0). Expected digests will be asserted by new regression tests.

```python
import tempfile, hashlib
from pathlib import Path
from zava_forward.core.synthetic import scale_fixture as sf, sensor_backfill as sb
for name, run in [('scale', lambda d: sf.write(d, n=12, per_home=3)),
                  ('sensor', lambda d: sb.write(d, homes=12, days=3))]:
    with tempfile.TemporaryDirectory(dir='.venv') as d:
        run(d)
        print(name, {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted(Path(d).iterdir())
                     if p.suffix in ('.csv', '.jsonl')})
```

| Payload | SHA-256 |
| --- | --- |
| scale/events.jsonl | 32157fc81abf5c9d6a12dfe564283ec1f067736ea6cf1f1f5864e5cf64e70e60 |
| scale/homes.jsonl | 7a40714ae50da64be9733c4fa0a39e1c8db71acdac31996b449f42feb907763f |
| scale/households.jsonl | 12ccc7a2ad73f235748ee7f005547e9a7fc684f604a1b1b319776ad47e02cfea |
| sensor/readings-0000.csv | 657ff373107807b34bd4bb6720dec534fcef13134292c5d753ef24bdbd723549 |
| sensor/sensors.csv | 1bb5907d55570685a40f0603abd9086def4bd3540726d5f13316d6816b99c400 |

## Amendments and divergences

PC-001 through PC-005 applied directly to plan/details. PC-006 readiness gate
accepted, but post-Review fix-loop advice rejected per RPI one-pass routing.
Omitted sensor as-of preserves historical START for custom days as well as
defaults; explicit date is exclusive end. This resolves compatibility without
changing generator physics. No significant user decision is required.

## Validation

### P01 implementation

Added typed provenance helper: strict ISO dates, stable length-delimited named
source hashes, streaming payload hashes and new/empty destination guard.
Extended existing scale/sensor writers; no new workload imports, dependency
extras, SQL or loader changes. Scale v1.2.0 registry metadata synchronized.
Sensor v2 records exclusive UTC end and propagates start into estimator and
all shards. Existing default payloads remain byte-identical to captured hashes.
Implementation-time boundary check replaced strftime with ISO formatting for
four-digit years below 1000; ordinary historical bytes are unchanged. The
valid minimum-calendar-window test now parses its first timestamp explicitly.

### Commands and results

All commands below run from repository root unless a subshell `cd` is shown.
No uv, sudo, Docker privilege change or Azure deployment was used.

| Command | Result |
| --- | --- |
| `../../.venv/bin/python -m unittest discover -s tests -p 'test_synthetic_determinism.py' -v && ../../.venv/bin/python -m unittest discover -s tests -p 'test_sensor_backfill.py' -q` (incorrectly from root) | Exit 127, relative interpreter not found; corrected cwd below |
| `.venv/bin/ruff check src/core/src/zava_forward/core/synthetic/provenance.py src/core/tests/test_synthetic_determinism.py && .venv/bin/ruff format src/core/src/zava_forward/core/synthetic/provenance.py src/core/tests/test_synthetic_determinism.py && (cd src/core && ../../.venv/bin/mypy)` | Initial exit 1: one long literal and two loop-closure warnings. Fixed literal layout and bound captured variable; rerun exit 0, one file formatted, mypy 64 files clean |
| `cd src/core && ../../.venv/bin/python -m unittest discover -s tests -p 'test_synthetic_determinism.py' -v && ../../.venv/bin/python -m unittest discover -s tests -p 'test_sensor_backfill.py' -q` | Exit 0: 7 new and 5 existing tests pass; existing sensor tests emit unclosed-file ResourceWarnings |
| `mkdir -p .venv/issue-176-evidence && (cd src/core && ../../.venv/bin/python -m unittest discover -s tests -q) > .venv/issue-176-evidence/core-tests.log 2>&1; result=$?; tail -8 .venv/issue-176-evidence/core-tests.log; exit "$result"` | Exit 0: 268 tests, 86.475 seconds |
| Initial remaining-suite loop with `PYTHONPATH=../core/tests:../agents/tests` for every project | Exit 1 on agents: test_dependency_rule module collision. Corrected to exact per-project CI paths below; no source change |
| Per-project suite loop below | Exit 0: agents 70, api 459 (92 skipped), orchestrator 17, importer 39 |
| `for project in core agents api orchestrator importer; do echo "== $project =="; (cd "src/$project" && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy) \|\| exit; done; git diff --check; docker info --format '{{.ServerVersion}}'` | All five lint/format/mypy gates pass: mypy 64/16/33/8/10 files; diff clean. Docker exit 1: permission denied connecting to unix:///var/run/docker.sock. Images, SQL Server and image identity checks rely on CI, not claimed locally |
| Namespace Python probe below | Exit 0: all five distributions 0.1.0 import; PEP 420 namespace has five paths and no init |
| `python3 tools/rename-zava-tests.py` | Exit 1: 25 tests, seven missing python-pptx/Pillow dependency errors |
| `.venv/bin/python -m pip install -q python-pptx Pillow && .venv/bin/python tools/rename-zava-tests.py > .venv/issue-176-evidence/rename-tests.log 2>&1; result=$?; tail -7 .venv/issue-176-evidence/rename-tests.log; exit "$result"` | Exit 1: remaining PyYAML missing (one failure/one error); dependency restoration only after failures |
| `.venv/bin/python -m pip install -q PyYAML && .venv/bin/python tools/rename-zava-tests.py > .venv/issue-176-evidence/rename-tests.log 2>&1; result=$?; tail -7 .venv/issue-176-evidence/rename-tests.log; exit "$result"` | Exit 0: 25 tests pass; intentional broken.pptx fixture reports expected error |
| `git --no-pager diff --stat && git --no-pager diff -- src/core/src/zava_forward/core/synthetic/scale_fixture.py src/core/src/zava_forward/core/synthetic/sensor_backfill.py && git status --short` | Scoped diff inspected; generated .venv untracked and excluded from explicit staging; removed at cleanup |
| `git diff --check && git diff --name-only -- mvp .env .vscode .copilot-tracking/github-issues && git ls-files ':(glob)src/**/data/**'` | Exit 0, no protected-path diff and no tracked src working data |
| `git grep -n 'synthetic/scale_fixture.py\|237, 257\|determinism' -- docs/architecture/mvp-to-src-parity-matrix.md; git grep -n 'def write\|def test_mvp_output\|def test_same_seed' -- src/core/src/zava_forward/core/synthetic/sensor_backfill.py src/core/src/zava_forward/core/synthetic/scale_fixture.py src/core/tests/test_generated_dataset.py` | Architecture/source evidence locations verified |
| `(cd src/core && ../../.venv/bin/python -m unittest discover -s tests -q && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy) > .venv/issue-176-evidence/core-final.log 2>&1; result=$?; grep -E 'Ran [0-9]+ tests\|^OK\|^FAILED\|checks passed\|already formatted\|Success:' .venv/issue-176-evidence/core-final.log; if [ "$result" -ne 0 ]; then tail -40 .venv/issue-176-evidence/core-final.log; fi; exit "$result"` | Exit 0: final core 268 tests in 72.179 seconds; lint, format and mypy clean |
| `git diff --check && gh api user --jq '{id,login}' && git config --local user.email 8036360+jmservera@users.noreply.github.com && git config --local user.name && git status --short` | Exit 0; confirmed privacy-safe local identity jmservera; no global configuration change |

Exact per-project suite loop (logs are temporary, results above are durable):

```bash
for project in agents api orchestrator importer; do
  case "$project" in
    api) testpath=../core/tests:../agents/tests;;
    orchestrator) testpath=../core/tests;;
    *) testpath=;;
  esac
  (cd "src/$project" && PYTHONPATH="$testpath" ../../.venv/bin/python -m unittest discover -s tests -q) > ".venv/issue-176-evidence/$project-tests.log" 2>&1
  result=$?
  printf '\n%s exit=%s\n' "$project" "$result"
  grep -E 'Ran [0-9]+ tests|^OK|^FAILED|^ERROR|^FAIL' ".venv/issue-176-evidence/$project-tests.log"
  if [ "$result" -ne 0 ]; then tail -40 ".venv/issue-176-evidence/$project-tests.log"; exit "$result"; fi
done
grep -E 'Ran [0-9]+ tests|^OK|^FAILED' .venv/issue-176-evidence/core-tests.log
```

Namespace probe, executed with `.venv/bin/python -`:

```python
import importlib.metadata
import zava_forward
for name in ('core', 'agents', 'api', 'orchestrator', 'importer'):
    __import__('zava_forward.' + name)
    dist = 'zava-forward-' + ('import' if name == 'importer' else name)
    print(dist, importlib.metadata.version(dist))
assert zava_forward.__file__ is None
assert len(list(zava_forward.__path__)) == 5
print('Namespace distribution isolation: PASS')
```

### P02 local application smoke

Command: `PYTHONPATH=src/core/tests .venv/bin/python -` with the exact script
below. Exit 0. Generated 980 fictional cases (443 open), 10 fictional staff,
seed 20260901, as-of 2026-10-15. Real server process started on loopback with
explicit ZF_DATA/SQLite/state, responsive health/app/login/cases endpoints
all 200. ZF_AI=on, summary route returned `source=template`, label
`Template draft, not approved`; stage and resident decision unchanged.
Actual Azure model NOT RUN: isolated local environment has no configured
Azure endpoint/identity. This is not AI inference acceptance.

```python
import http.cookiejar, json, os, socket, subprocess, sys, time
import urllib.error, urllib.request
from pathlib import Path
from unittest.mock import patch
from test_generated_dataset import builder, register
root = Path('.venv/issue-176-evidence/app').resolve()
root.mkdir(parents=True, exist_ok=True)
data = root / 'zavaforward.json'
with patch.object(builder, 'load_register', return_value=register()), patch.object(sys, 'argv', ['builder', '--seed', '20260901', '--as-of', '2026-10-15', '--out', str(data)]):
    builder.main()
fixture = json.loads(data.read_text())
user = next(p for p in fixture['staff'] if p['code'] == 'PM-01')
case = next(c for c in fixture['cases'] if c['decision']['status'] in ('Waiting', 'Not yet asked'))
with socket.socket() as listener:
    listener.bind(('127.0.0.1', 0))
    port = listener.getsockname()[1]
env = {'PATH': os.environ['PATH'], 'HOME': str(root), 'ZF_DATA': str(data), 'ZF_STATE': str(root / 'state'), 'ZF_STORE': 'sqlite', 'ZF_AI': 'on', 'ZF_PASSWORD': 'synthetic-local-only', 'ZF_AUTH': 'password', 'ZF_BIND': '127.0.0.1', 'PORT': str(port)}
base = f'http://127.0.0.1:{port}'
client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def request(path, body=None):
    raw = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(base + path, data=raw, headers={'Content-Type': 'application/json'})
    with client.open(req, timeout=5) as response:
        return response.status, response.read()
with (root / 'server.log').open('w') as log:
    proc = subprocess.Popen([sys.executable, '-m', 'zava_forward.api.server'], env=env, stdout=log, stderr=log)
    try:
        for _ in range(100):
            assert proc.poll() is None, 'Server exited before becoming responsive'
            try:
                status, health = request('/healthz')
                break
            except urllib.error.URLError:
                time.sleep(0.1)
        else:
            raise AssertionError('Server did not become responsive')
        assert status == 200 and health == b'ok'
        assert request('/app')[0] == 200
        assert request('/api/login', {'email': user['email'], 'password': 'synthetic-local-only'})[0] == 200
        status, listing = request('/api/cases?view=all&limit=5')
        assert status == 200
        status, before = request('/api/cases/' + case['id'])
        assert status == 200
        status, result = request('/api/cases/' + case['id'] + '/ai', {'task': 'summary'})
        result = json.loads(result)
        assert status == 200 and 'not approved' in result['label']
        assert result['source'] != 'ai', 'No Azure model configured in this isolated smoke environment'
        _, after = request('/api/cases/' + case['id'])
        before, after = json.loads(before), json.loads(after)
        assert before['stage'] == after['stage'] and before['decision'] == after['decision']
        print(json.dumps({'health': '200 ok', 'app': 200, 'login': 200, 'cases': 200, 'synthetic_cases': len(fixture['cases']), 'as_of': fixture['as_of'], 'ZF_AI': 'on', 'actual_model': 'NOT RUN: no configured Azure endpoint/identity in isolated local environment', 'draft_source': result['source'], 'draft_label': result['label'], 'stage_and_resident_decision': 'unchanged'}))
    finally:
        proc.terminate()
        proc.wait(timeout=10)
```

The process was terminated and reaped in `finally`; no local server remains.
Temporary generated data and environment are excluded from staging and removed
during final delivery cleanup.

## Review readiness

P01/P02 complete and plan/details reconciled. Single post-implementation Review
executed Complete, outcome Residual work. No in-scope engineering blocker found.
Review record: .copilot-tracking/reviews/logs/2026-10-15/issue-176-src-determinism-review.md.
P03 delivered in PR #309. RV-001 private-source recovery routes to research,
RV-002 approval to owner/planning, RV-003 platform evidence to distinct CI/
authorized validation follow-up. All issue-wide ACs remain open.

## P03 delivery preparation

`git --no-pager diff -- docs/reference/research/retrofit-synthetic-data/README.md
src/core/README.md src/agents/evals/registry.json && git diff --check &&
git diff --numstat`: exit 0, one-pass review evidence checked.

`git branch --show-current && git status --short &&
git check-ignore src/core/.mypy_cache src/core/.ruff_cache &&
gh pr list --head feat/src-synthetic-determinism-176 --state all --json number,state,url`:
exit 0, correct branch, no existing PR, tool caches ignored. Explicit staging
will exclude the untracked worktree-local virtual environment and generated
synthetic files. Conventional commit trailer and privacy-safe author/committer
identity are required. No amend, rebase, force-push or merge.

## P03 delivered result and CI

Implementation commit: `774137a`, subject
`feat(core): record synthetic provenance and protect fixture refreshes`.
Author and committer both `8036360+jmservera@users.noreply.github.com`.
Required Copilot co-author trailer verified.
PR: https://github.com/jmservera/ama/pull/309, OPEN,
head feat/src-synthetic-determinism-176, base main, uses Refs #176.
All seven RPI phase/state artifacts are in the implementation commit.

| Command | Result |
| --- | --- |
| `git add` with explicit 16 implementation/documentation/RPI artifact paths, followed by `git diff --cached --check && git diff --cached --stat` | Exit 0; only intended paths, no .venv/generated data |
| `printf '%s\n\n%s\n' 'feat(core): record synthetic provenance and protect fixture refreshes' 'Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>' \| GIT_AUTHOR_EMAIL=8036360+jmservera@users.noreply.github.com GIT_COMMITTER_EMAIL=8036360+jmservera@users.noreply.github.com git commit -F -` | Exit 0, 774137a, 16 files |
| `git push --set-upstream origin feat/src-synthetic-determinism-176` | Exit 0, new remote topic branch; no main push |
| PR creation pipeline below | Exit 0, PR #309 created |
| `gh pr view 309 --json url,state,baseRefName,headRefName,mergeStateStatus,statusCheckRollup --jq '{url,state,baseRefName,headRefName,mergeStateStatus,checks:[.statusCheckRollup[]\|{name,status,conclusion}]}' && git log -1 --format='%h %s%nAuthor: %ae%nCommitter: %ce%n%b' && git diff --check && git status --short` | Exit 0, PR OPEN/correct branches, CI started, exact author/committer/trailer verified; only .venv remained untracked |
| `bash /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/shared/pr-reference/scripts/generate.sh --base-branch origin/main --merge-base --no-md-diff --exclude-path .copilot-tracking --output /home/azureuser/source/ama-wt/issue-176/.venv/issue-176-evidence/pr-reference.xml && bash /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/shared/pr-reference/scripts/read-diff.sh --input /home/azureuser/source/ama-wt/issue-176/.venv/issue-176-evidence/pr-reference.xml --summary` | Exit 0, source-only PR reference generated; source paths checked. Summary helper printed malformed per-file counts, not used as validation |
| `mkdir -p .copilot-tracking/pr/2026-10-15 && cp .venv/issue-176-evidence/pr-reference.xml .copilot-tracking/pr/2026-10-15/issue-176-src-determinism-reference.xml && git diff --check && gh pr view 309 --json body --jq '.body' \| grep -E '^Refs #176\|^##\|^<summary>\|^\| Core\|^\| Docker'` | Exit 0; generated XML preserved, published PR includes exact command-ledger appendix |
| `timeout 480 gh pr checks 309 --watch --interval 20` | Exit 0, all eleven checks passed on 774137a |

PR creation, including the complete committed changes/command ledger:

```bash
{
  cat .venv/issue-176-evidence/pr-body.md
  printf '\n\n<details>\n<summary>Exact local command and result ledger (committed changes artifact)</summary>\n\n'
  cat .copilot-tracking/changes/2026-10-15/issue-176-src-determinism-changes.md
  printf '\n</details>\n'
} | gh pr create --base main --head feat/src-synthetic-determinism-176 \
  --title 'feat(core): deterministic synthetic snapshots and protected refresh (Refs #176)' \
  --body-file -
```

CI observed on implementation commit:

| Check | Conclusion | Duration |
| --- | --- | --- |
| src-core | SUCCESS | 39s |
| src-api | SUCCESS | 2m0s |
| src-agents | SUCCESS | 57s |
| src-orchestrator | SUCCESS | 1m3s |
| src-importer | SUCCESS | 1m4s |
| src-namespace | SUCCESS | 17s |
| src-no-working-data | SUCCESS | 7s |
| test | SUCCESS | 1m27s |
| image | SUCCESS | 1m20s |
| mssql | SUCCESS | 2m54s |
| validate | SUCCESS | 2m17s |

Source CI run: https://github.com/jmservera/ama/actions/runs/38806176933.
MVP compatibility/image/SQL run:
https://github.com/jmservera/ama/actions/runs/38806176779.
Validation run: https://github.com/jmservera/ama/actions/runs/38806176943.
CI does not supply real Azure model, private stock-generator, owner approval
or full-scale sensor evidence. Those remain RV-001/RV-002/RV-003 follow-ups.

Final administration uses one further conventional documentation-only commit,
the same author/committer/trailer and a normal push to the same topic.
PR body is refreshed from this ledger using `gh pr edit 309 --body-file -`.
The specifically created `/home/azureuser/source/ama-wt/issue-176/.venv`
environment is removed after publishing; no pre-existing directory is removed.
Final remote-head and clean-worktree verification is recorded in the PR
delivery comment rather than requiring a self-referential commit.

### Generated reference serialization

The first evidence-only delivery chain stopped before commit at
`git diff --cached --check` (exit 2): raw unified-diff context blank lines in
the generated XML contain trailing spaces. No second commit or push occurred
in that attempt. An initial `python3 -` formatter attempting
`ET.fromstring(path.read_text())` failed before writing (exit 1, invalid XML
at line 11): the installed generator emits escaped CDATA markers and an
unescaped full_diff. This is a tool artifact issue, not a source change or
an implementation Review finding.

Repaired the generated reference only with `python3 -` (exit 0), without
altering the installed tool. The complete successful formatter follows;
round-trip assertions preserve decoded diff and metadata:

```python
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
path = Path('.copilot-tracking/pr/2026-10-15/issue-176-src-determinism-reference.xml')
raw = path.read_text()
prefix, rest = raw.split('<full_diff>', 1)
diff, suffix = rest.rsplit('</full_diff>', 1)
parseable = prefix.replace('<\\![CDATA[', '<![CDATA[') + '<full_diff>' + escape(diff) + '</full_diff>' + suffix
root = ET.fromstring(parseable)
assert root.findtext('full_diff') == diff
serialized = ET.tostring(root, encoding='unicode')
encoded = re.sub(r'[ \t]+(?=\n)', lambda m: ''.join(f'&#{ord(c)};' for c in m[0]), serialized)
assert ET.tostring(ET.fromstring(encoded)) == ET.tostring(root)
path.write_text(encoded + '\n')
print('Generated XML repaired/serialized; decoded unified diff and metadata preserved')
```

Final administrative command sequence: explicit staging of changes/details/
plan/state and generated reference, `git diff --cached --check`, conventional
commit `docs: record synthetic determinism delivery and CI evidence` with the
same required co-author trailer, normal topic push, PR-body pipeline above
using `gh pr edit 309 --body-file -`, exact-path
`rm -r -- /home/azureuser/source/ama-wt/issue-176/.venv`,
`git status --short`, `git log -2 --format='%h %s%nAuthor: %ae%nCommitter: %ce'`,
and `gh pr view 309 --json url,state,baseRefName,headRefName,headRefOid`.

## Open issue acceptance

* [ ] AC1: byte identity for every generator including unavailable private register.
* [ ] AC2: manifests for every generator including unavailable private register.
* [ ] AC3: approved cadence, approver and live-record protection policy.

Bounded src results do not close private source reproduction, owner refresh
approval, real climate/device inputs or full-scale/Azure model evidence.
