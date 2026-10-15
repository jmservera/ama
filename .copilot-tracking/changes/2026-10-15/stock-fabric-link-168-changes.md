---
title: Stock fabric link 168 changes and validation
description: Implementation, command evidence, acceptance limits and delivery
ms.date: 2026-10-15
---

Refs #168. Inventory row: SN-01 (partial); dependency #167.

Draft delivery: one Review completed with **Defects found**. RV-001 remains open:
a wheel-installed CLI invoked outside a checkout can miss a repository at its
explicit output destination. Editable-source checks pass, but the general
containment guarantee is incomplete. Do not merge or treat this as full issue
acceptance until a later implementation addresses the finding. No second
implementation/review cycle ran inside this task.

Task 168 / stock-fabric-link-168. Scope: full ready plan, P01 and P02.
Implementation complete for P01/P02-T01/T02; one critique completed and
PC-001 through PC-007 incorporated. No significant divergence or owner decision.

## P01: Migration and Linking

Moved the existing fabric algorithm into installed core, removed the support
copy, and wired the retained builder/EPC imports. The v1 seed string and random
draw order are preserved, independently checked against pre-move A/B/C
mapped/fallback golden values captured before editing. Both synthetic label
fields are emitted. No SQL, dependency manifest, image or workload edge changed.

Core owns exact-reference resolution, per-case evidence and fabric attachment.
Duplicate/invalid cases fail; absent, malformed, unknown and ambiguous anchors
are unlinked with reasons. Shared valid anchors are explicit non-unit source
matches, not merged homes or households. Legacy numeric keys now define source
anchors honestly. The builder calls core before regenerating EPC assumptions.
The CLI drops previous derived stock EPC blocks when refreshing fabric; it
never overwrites original input or operational home/history/consent fields.

The CLI uses ZF_DATA defaults, validates before output creation, refuses
repository/symlink-to-repository and nonempty destinations, and writes CSV,
optional linked seed, summary assumptions, full core revision and payload hashes.
Retained support revision remains 16 hex but includes the moved source closure.
Top-level report is seed metadata; per-case evidence uses existing SQL JSON
storage. No existing live store is reseeded.

## Commands and Results

All commands run in the named worktree unless a project subdirectory is stated.
Read-only source searches and view calls examined the files cited in research.
No private data files or secrets were read.

| Command | Result |
| --- | --- |
| `git status --short && git branch --show-current` | Clean; feat/src-stock-fabric-link-168. |
| `gh issue view 168 --comments`; `gh issue view {168,167,166} --json title,body,comments` (individual calls) | Three #168 criteria unchecked; reopen requests verification; #166 owner review open. |
| `gh pr list --head feat/src-stock-fabric-link-168 --json number,state,baseRefName,url` | No existing PR. |
| `gh pr view N --json title,state,mergeCommit`, N=296..302 | All seven merged; moves reused. |
| `gh pr view 246 --json title,body,files` | Prior partial delivery and reconciliation limitation inspected. |
| `git log -4 --oneline` | Baseline a48d502; generator coverage #312 included. |
| `command -v python3; python3 --version; command -v ruff` | Python 3.12.3; ruff missing, chained later probes not executed. |
| `python3 -m pip show zava-forward-core zava-forward-api zava-forward-agents zava-forward-orchestrator zava-forward-import ruff mypy` | All missing; dependency restoration permitted. |
| `git ls-files .copilot-tracking`, `git ls-files '*instructions*'`, local `.venv` directory probe | Existing task artifacts; no extra matching instruction files or local venv. |
| `gh api user --jq '{id,login}'` | Authenticated jmservera, id 8036360; privacy-safe email matches explicit user value. |
| `python3 -m venv .venv && .venv/bin/python -m pip install --quiet -e 'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]' -e 'src/orchestrator[dev]' -e 'src/importer[dev]'` | Restored missing dependencies with pip; success. |
| `.venv/bin/python -` with old support `zf_stock_fabric.fabric` for GOLD-A/B/C, seed 7 | Captured pre-move golden values: A 1900/pre-1919/Flat/Solid brick/gas; B 1928/1919-1944/Terraced/Cavity/gas; C 1961/1945-1964/Detached/Cavity/heat pump. |
| `.venv/bin/ruff check src/core/src/zava_forward/core/synthetic/stock_fabric.py --fix && .venv/bin/ruff format ... && (cd src/core && ../../.venv/bin/mypy src/zava_forward/core/synthetic/stock_fabric.py)` | First lint failed: long lines and missing strict zip, so chained format/mypy did not run. Corrected without exemptions. |
| `.venv/bin/ruff format src/core/src/zava_forward/core/synthetic/stock_fabric.py src/core/tests/test_stock_fabric.py && .venv/bin/ruff check ...` | Formatting succeeded; one import-sort finding stopped chain. |
| `.venv/bin/ruff check src/core/tests/test_stock_fabric.py --fix && .venv/bin/ruff format src/core/tests/test_stock_fabric.py && (cd src/core && ../../.venv/bin/mypy src/zava_forward/core/synthetic/stock_fabric.py tests/test_stock_fabric.py)` | Import fixed; mypy found 5 missing/overly broad test annotations; corrected explicitly. |
| `cd src/core && ../../.venv/bin/python -m unittest discover -s tests -p test_stock_fabric.py -v` | 7 new tests pass, 5.475 s before annotation cleanup. |
| `git diff --stat; git status --short; git check-ignore .venv` | Discovered root .venv was not ignored; subsequent chained coverage probe did not execute. No environment/data files staged. |
| `mv .venv src/core/.venv` | Moved development environment into existing ignored project path; all subsequent commands use its interpreter via `python -m`. No ignore/config change. |
| `src/core/.venv/bin/python -m ruff format src/core/src/zava_forward/core/synthetic/stock_fabric.py src/core/tests/test_stock_fabric.py` | Success, two typed/non-exempt files. |
| `cd src/core && .venv/bin/python -m ruff check . && .venv/bin/python -m ruff format --check . && .venv/bin/python -m mypy` | Pass; 20 formatted files, 73 checked source files. Existing migration exemptions unchanged. |
| `cd src/core && .venv/bin/python -m unittest discover -s tests -q` | 332 tests pass, 119.563 s, no skips. Existing sensor-backfill unclosed-reader ResourceWarnings only. |
| `cd src/api && PYTHONPATH=../core/tests:../agents/tests ../core/.venv/bin/python -m unittest discover -s tests -q && ../core/.venv/bin/python -m ruff check . && ../core/.venv/bin/python -m ruff format --check . && ../core/.venv/bin/python -m mypy` | 477 tests, 196.510 s, pass with 97 skips; lint/format/mypy pass, 9 formatted/37 typechecked. Skips are unavailable SQL Server contracts and azure-core-dependent law tests. |
| `cd src/agents && ../core/.venv/bin/python -m unittest discover -s tests -q && ../core/.venv/bin/python -m ruff check . && ../core/.venv/bin/python -m ruff format --check . && ../core/.venv/bin/python -m mypy` | 70 tests pass, 7.539 s; static checks pass, 11 formatted/16 typechecked. |
| `cd src/orchestrator && PYTHONPATH=../core/tests ../core/.venv/bin/python -m unittest discover -s tests -q && ../core/.venv/bin/python -m ruff check . && ../core/.venv/bin/python -m ruff format --check . && ../core/.venv/bin/python -m mypy` | 17 tests pass, 0.111 s; static checks pass, 5 formatted/8 typechecked. |
| `cd src/importer && ../core/.venv/bin/python -m unittest discover -s tests -q && ../core/.venv/bin/python -m ruff check . && ../core/.venv/bin/python -m ruff format --check . && ../core/.venv/bin/python -m mypy` | 39 tests pass, 0.188 s; static checks pass, 11 formatted/10 typechecked. |
| `src/core/.venv/bin/python -m zava_forward.core.synthetic.coverage docs/reference/research/retrofit-synthetic-data/needs-inventory.json` | Exit 0; inventory 1.2.0, 2 covered/11 partial, routing shape valid, no missing/deferred gaps; owner/output/application acceptance explicitly not assessed. SN-01 stays partial. |
| `docker build -f src/api/Dockerfile -t zava-forward-api:issue-168 src` | Exit 1: permission denied on unix:///var/run/docker.sock. No local image evidence; rely on CI. |
| `gh issue view 168 --comments` (recheck) | No additional owner direction beyond reopen/verification request. |
| `git diff --check` and `git status --short` (repeated before review) | Clean whitespace; only intended source/docs/task artifacts, no working data/prohibited path edits. |
| `PYTHONPATH=src/core/tests:src/agents/tests src/core/.venv/bin/python -` (loopback smoke below) | Actual App/ThreadingHTTPServer with ZF_DATA synthetic seed and SQLite; health/login/case HTTP 200, 60000 stock/980 cases, 980 linked/0 unlinked; exact stock_link/fabric/EPC/home/decision retained. Server responsive and stopped/joined; temp files cleaned. |
| `cd src/core && .venv/bin/python -m unittest discover -s tests -p test_generated_dataset.py -q && .venv/bin/python -m unittest discover -s tests -p test_stock_fabric.py -v && .venv/bin/python -m ruff check . && .venv/bin/python -m ruff format --check . && .venv/bin/python -m mypy` | Final migration call-site metadata/path update: 12 existing generator tests pass (5.272 s), 7 new tests pass (4.128 s); all core static checks pass. |
| `python3 tools/rename-zava-tests.py` | 25 tests: 7 errors due to absent pptx/PIL, not changed behavior. Chained diff probes not run after failure. |
| `src/core/.venv/bin/python -m pip install --quiet -r tools/rename-zava-requirements.txt && src/core/.venv/bin/python tools/rename-zava-tests.py` | Restored documented missing tools; all 25 pass, 0.446 s. Expected invalid-zip diagnostic is a negative test. |
| `src/core/.venv/bin/python -` local Markdown path scan | Zero unresolved file links in core README, synthesis README, data dictionary and knowledge-base index. |

## P02: Validation and Documentation

Completed local engineering validation: 935 src tests total, including 97 skips,
plus 25 migration regressions and targeted final reruns. All five project ruff,
format and mypy checks passed; new code/test owner has no exemptions.
The connected test uses the same exact 60,000 fictional register rows for fabric
and retained 980-case builder, reconciles every categorical count to 60,000 and
every case to a resolution, and compares linkage, fabric/EPC, home/history/
resident-decision fields after a closed SQLite restart. Seed 20260901,
fabric seed 4820260930, as-of 2026-10-13. Source revision is computed from actual
generator sources, not a mutable Git HEAD or clock.

Updated core README, synthesis, dictionary, index and append-only log. Historical
private counts are explicitly historical. Data output and inventory ratification
are not conflated with coverage routing success.

No real AI call, SQL Server, Azure deployment or private corpus run is authorized
by a local engineering test. Existing real-AI configuration, release and human
approval/consent boundaries are unchanged.

## Acceptance and Remaining Work

* [ ] Actual retained private cases each resolve to a stock home ID or are
  explicitly unlinked: not revalidated against the private corpus.
* [ ] Actual retained private fabric is synthetic-labelled and seed reproducible:
  local fictional evidence pending; private regeneration unavailable.
* [x] Distributions are explicitly assumptions, not company facts: summary
  weights/labels, per-row synthetic labels and updated docs/tests.

Owner review of SN-01/inventory, private stock regeneration or explicit deferral,
unit-level linkage and home.built/type reconciliation remain open. No claim of
AI/SQL/Azure/human application acceptance.

## Loopback Smoke Reproduction

The executed Python stdin command imported `register` and `GENERATOR` from
the new typed test owner, patched only builder input to that fictional
60,000-row register, and invoked the retained builder with
`--seed 20260901 --as-of 2026-10-13 --out <TemporaryDirectory>/seed.json`.
It set ZF_DATA to that file and ZF_STORE=sqlite for `open_store`, created the
real API App, and served on loopback port 0. It verified health, authenticated
with the synthetic PM-01 fixture using a synthetic-only smoke password, fetched
the first case and compared all five stock_link/stock_fabric/stock_epc/home/
decision structures against the seed. A finally block shut down the server,
closed SQLite and joined the serving thread; TemporaryDirectory removed data.
No request invoked real AI or external services, and no credential/PII was logged.

## Review and Delivery

Review execution Complete, outcome Defects found, exactly one pass:
.copilot-tracking/reviews/logs/2026-10-15/stock-fabric-link-168-review.md.
RV-001 routes to later implementation (destination-ancestor repository check
and installed-wheel regression). RV-002 routes to owner-directed SN-01/private
data/unit reconciliation. RV-003 routes to authorized real-platform/human
validation. This task makes no source fixes after Review.

Topic commit/push and draft PR to main are authorized and pending; remote CI
has not run for this branch yet. Final delivery receipts will be appended
without amending or rewriting the implementation commit.

| Delivery command | Result |
| --- | --- |
| `gh api user --jq '{id,login}' && git config --local user.email 8036360+jmservera@users.noreply.github.com` | Authenticated identity reconfirmed; repository-local author/committer email configured. |
| `git branch --show-current && git diff --check && test -s .gitignore && git status --short` | Named branch, whitespace pass, existing ignore safety; only intended task changes. |
