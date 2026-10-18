---
title: Issue 120 DPIA reference implementation evidence
description: Bounded changes, failing-first regressions, validation and handoff
ms.date: 2026-10-18
---
<!-- markdownlint-disable-file -->

# RPI Changes: issue-120-dpia-reference

## Metadata

Task ID: issue-120. Implementation date: 2026-10-18.
Plan: .copilot-tracking/plans/2026-10-18/issue-120-dpia-reference-plan.md.
Details: .copilot-tracking/details/2026-10-18/issue-120-dpia-reference-phase-details.md.
Base: a86282c4badebc58eabbf9e441410d930a201ac2.

## Execution Status

Complete, full plan scope. P01-P03 and P01-T01/P02-T01/P03-T01 complete.
Allowed writes: timecapture.py, existing test_timecapture.py, narrow API README
and task artifacts. No implementation blocker; sole original Review is next.

## Execution Summary

Research executed before Plan. Sole independent critique completed with original
Revise. PC-001 local-scratch improvement applied; unsupported no-/tmp provenance
is explicitly not adopted. `.venv/task-tmp` created and Python confirms
`/home/azureuser/source/ama-wt/issue-120-dpia/.venv/task-tmp`.
Delivered the bounded predicate, seven regressions, narrow API guidance, full
focused and installed-image evidence. No material divergence from approved intent.

## Original Evidence Hashes

| Original | Git blob | SHA-256 |
| --- | --- | --- |
| timecapture.py | 29635e36b03097fab523a1f0d09227edb32a2847 | c920dcf4c1c3728080049c936180ce14ee2e530626ba8ac4e39c88a90152a044 |
| test_timecapture.py | 019076b8ba1b94ae039ea7effde1b057858153d2 | d5a3ecc4926ce601f04e8f0269dba991de1dcd6ff70c284cb38678aebfaae88b |
| API README | 4030ab26e4e281046a94b77bfd15f4805985dcda | c19ccaf46861883dd1b69521c5e4725dbfa9330cf5e0e39261c00aceb971ff72 |
| Failing-first direct/HTTP probe log | Not committed yet | 1b5862bd16557a5bd61b660c3711627c31ba7e92a05b3862b870ecf2dbc67a51 |
| Original independent plan critique | Not committed yet | 5a529f8a51d2c00b12746e854a1a997ca01dd75fa810442495d35dccaf7aef14 |

## Completed Work

### P01-T01: Failing-first regressions

Added seven test methods and two module helpers in the existing test file,
with no removals. Covers missing/blank/token matrix; four writer denials with
no fresh local path; local/shared literal historical controls, retained rows
and restart; valid trimmed references; immediate invalidation/new reference
renewal; and authenticated existing-handler HTTP denials with no success audit.

Before any production edit, ran three selected new tests against unchanged
timecapture.py: exit 1, three tests, thirteen assertion/subtest failures.
All failures point to the intended defect: token presence reported true,
HTTP request admitted, historical token controls treated as enabled.
Original output: issue-120-dpia-reference-failing-first-tests.log.

### P02-T01: Shared status predicate and documentation

timecapture.py now derives dpia_recorded from existing trimmed value and
casefold token exclusion. The same boolean drives refusal reason and status,
therefore both existing admission gates reject all four writers. Module prose
and the narrow API README explain token rejection and presence-only limits.
No SQL, server, shared fixtures, schema, imports or web edits.

First post-change suite ran 23 tests with one new test-harness defect:
the audit snapshot compared generator identities rather than materialized rows.
Retained issue-120-dpia-reference-tests.log unchanged. Corrected only the new
HTTP test to compare lists, then full suite passed all 23 tests, no skips,
10.713 seconds. This is ordinary pre-Review test development, not a repeated
Review or post-Review correction cycle.

### P03-T01: Current verification

Original probe now passes both tests: four HTTP 403s, zero audit events,
no new store, direct all-writer denial. Exact-base AST proof passes:
all production AST outside status/module prose unchanged, all existing test
methods unchanged, exactly seven added methods and exactly three src paths.
Current configured API Ruff passes, 24 files already formatted, mypy succeeds
on 56 files. Legacy timecapture/test_timecapture format and type exclusions
are unchanged; this is not full static checking of those legacy files.
Source-hardened Docker image built successfully, ID
`sha256:16c372c236db1dab393b85ca6a8d80d4d87bd761e206d08adaa35461d013e51e`.
Runtime also passed all 23 tests (6.143 seconds) and both probe tests
(0.685 seconds), with no skips. Actual local HTTP responds on the existing
handler, including all four invalid-DPIA 403 denials. Installed source path
`/usr/local/lib/python3.12/site-packages/zava_forward/api/timecapture.py`
has SHA-256 `5655acfcdcd5c9326cac823d14c272bb82de58fd6afa762a88521e26037c9289`,
identical to this worktree source. Image uses UID/GID 10001, read-only root,
network none (loopback only), all capabilities dropped, NoNewPrivs=1 and
repository-backed task scratch `/scratch`. Scratch was empty after tests and
its host permissions restored to 0700. Container auto-removed.

No MSSQL engine run: exact-base AST comparison proves every SQL statement,
DDL, import, connection and dialect/storage hook unchanged. The cited
2026-10-15 review claims prior SQL Server tests passed, but lacks precise
counts/logs; it is historical evidence only and not counted as this task's pass.
No broader auth/role suite needed: existing full time suite already exercises
current manager/nonmanager denials, independent roles and success audits using
actual HTTP. No UI changed; no browser or fresh WCAG claim.

### Actual commands and outcomes

All host commands from repository root unless shown inside `cd src/api`.
Each logged pipeline used `set -o pipefail`; all expected/nonexpected failures
are retained separately, never overwritten.

```bash
# Initial actual failure: python3 import -> ModuleNotFoundError, before install.
python3 -c "import zava_forward.api.timecapture as t; print(t.__file__)"
python3 -m venv .venv
.venv/bin/python -m pip install --quiet -e 'src/core[sql,blob]' -e src/agents -e 'src/api[dev]'
# Imported path then matched this worktree.
(cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_timecapture -q)
# Exact base: 16 passed, 7.132 seconds.
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-probe.py
# Exact base: exit 1, two failed probes; HTTP four 200, new store and successful audits.
mkdir -p .venv/task-tmp
export TMPDIR="$PWD/.venv/task-tmp"
.venv/bin/python -c 'import tempfile; print(tempfile.gettempdir())'
(cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_timecapture.TimeTests.test_invalid_dpia_flags_refuse_all_writes_without_creating_store test_timecapture.TimeTests.test_api_invalid_dpia_refuses_all_writes_without_audit test_timecapture.SharedStoreTests.test_invalid_historical_dpia_controls_cannot_enable_after_restart -v)
# Before production edit: exit 1, three tests, thirteen expected assertion/subtest failures.
(cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_timecapture -v)
# First implementation run: 23 tests, one generator-comparison test-harness failure.
# Same command after list materialization: 23 passed, 10.713 seconds; no skips.
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-probe.py
# After: two passed, 0.688 seconds; four HTTP 403, no audit writes/new store.
.venv/bin/python .copilot-tracking/changes/2026-10-18/issue-120-dpia-reference-boundary-check.py
# Passed exact-base AST/test/source-boundary and emitted original/final hashes.
(cd src/api && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy)
# Passed both runs; 24 files formatted, mypy 56 files; legacy exclusions retained.
docker build -t zf-dpia-reference-120:20261018 -f src/api/Dockerfile src
# Exit 0. Existing Dockerfile and dependency manifests unchanged.
chmod 0777 .venv/task-tmp
docker run --rm --name zf-dpia-reference-120-20261018 --network none --read-only --cap-drop ALL --security-opt no-new-privileges --user 10001:10001 \
  --mount "type=bind,src=$PWD/.venv/task-tmp,dst=/scratch" \
  --mount "type=bind,src=$PWD/src/api/tests,dst=/tests/api,readonly" \
  --mount "type=bind,src=$PWD/src/core/tests,dst=/tests/core,readonly" \
  --mount "type=bind,src=$PWD/src/agents/tests,dst=/tests/agents,readonly" \
  --mount "type=bind,src=$PWD/.copilot-tracking/research/2026-10-18/issue-120-dpia-reference-probe.py,dst=/probe.py,readonly" \
  -e TMPDIR=/scratch -e PYTHONPATH=/tests/api:/tests/core:/tests/agents \
  zf-dpia-reference-120:20261018 sh -c 'id && python -c "import hashlib,os,tempfile; from pathlib import Path; import zava_forward.api.timecapture as t; h=hashlib.sha256(Path(t.__file__).read_bytes()).hexdigest(); print(t.__file__, h); assert h == \"5655acfcdcd5c9326cac823d14c272bb82de58fd6afa762a88521e26037c9289\"; assert os.getuid() == 10001; print(\"TMPDIR\", tempfile.gettempdir()); print(*[x for x in Path(\"/proc/self/status\").read_text().splitlines() if x.startswith((\"CapEff:\", \"NoNewPrivs:\"))], sep=\"\\n\")" && python -m unittest test_timecapture -v && python /probe.py'
# Exit 0, installed-image 23+2 passed; CapEff=0, NoNewPrivs=1.
find .venv/task-tmp -mindepth 1 -maxdepth 1 -print
chmod 0700 .venv/task-tmp
git diff --check
git ls-remote origin refs/heads/main
# Main remains exact requested base before original Review.
```

## Implementation-Time Plan and Detail Updates

PC-001 affects validation setup only. Plan/details now prescribe task-local
TMPDIR and equivalent repository-backed container scratch. No user intent or
architecture change, no repeated critique. Original failure evidence retained.

## Validation Record

| Check | Status | Evidence |
| --- | --- | --- |
| Installed import before setup | Failed, actual missing dependency | ModuleNotFoundError: zava_forward; then pip-installed src distributions/dev extra |
| Exact-base full time suite | Passed, 16 tests | Research C12, 7.132 seconds |
| Exact-base direct and HTTP probe | Failed as expected, 2 tests | Original research baseline-probe.log; all four HTTP actions returned 200 |
| Contrarian valid refs/restart | Passed | Research contrarian.log |
| Failing-first new tests | Failed as expected, exit 1 | failing-first-tests.log, 3 tests / 13 failures |
| First implementation run | Failed, new test-harness issue | tests.log, generator identity comparison; original retained |
| Final focused suite | Passed, 23 / zero skips | tests-final.log |
| Final direct/HTTP probe | Passed, 2 / zero skips | probe-after.log |
| Configured Ruff/format/mypy | Passed | api-checks-final.log, exclusions disclosed |
| Exact-base boundary and hashes | Passed | boundary-check.log / reproducible .py |
| Source image build | Passed | image-build.log |
| Hardened installed image tests/probe | Passed, 23+2 / zero skips | image-runtime.log |
| Actual MSSQL | Not rerun | SQL/schema/runtime unchanged proof; historical engine claim only |
| Browser/WCAG/live governance | Not performed or established | Out of scope; no web edits |

## Pre-Review Reconciliation

Ready for sole original Review. All plan/task markers checked and details
synchronized with actual evidence. Completed work, source hashes, preserved
failures, validation exclusions, no implementation blockers and human/coordinator
follow-ups reconciled. No active implementation remains.

## Blockers

No implementation blocker. Human governance and coordinator acceptance are not
code gates satisfied by synthetic fixtures.

## Remaining Work

One original Review and authorized PR delivery. No remaining Pxx tasks.

## Follow-Up Items

Canonical plan Follow-Up Items: issue-owner human DPIA/consultation/notice/admin
ratification; independent coordinator acceptance/integration.

## Return-to-Caller State

Full-plan implementation complete and review-ready; automatic parent owns
continuation to the sole original Review and authorized delivery. Human
governance/issue acceptance and independent coordinator integration stay unmet.

## Sole Original Review Outcome

Review execution: Complete, exactly once. Outcome: Conformant with justified
divergence. No implementation defects; RV-001 Medium is human governance,
RV-002 Low is independent coordinator acceptance/integration. Both are distinct
existing follow-ups, not active patch defects. Historical-test setup uses the
unchanged `_conn`/DDL then literal INSERTs instead of independently handwritten
DDL; reviewer accepts this instrumentation divergence because admission is
bypassed and DDL is independently proven unchanged. No correction cycle used.
Review also notes stale early Research question labels; later evidence mapping
and Ready disposition answer every question. The original is retained unchanged.
Its Task ID label uses the slug; canonical wrapper task identity remains
`issue-120` with slug `issue-120-dpia-reference`.

| Preserved original | SHA-256 |
| --- | --- |
| Research baseline-probe.log | 1b5862bd16557a5bd61b660c3711627c31ba7e92a05b3862b870ecf2dbc67a51 |
| Failing-first new-tests.log | 8f428de094070baa7864f4638d0f20864038a0a2d92167642242836a0b4560cf |
| Original plan critique | 5a529f8a51d2c00b12746e854a1a997ca01dd75fa810442495d35dccaf7aef14 |
| Original Review | 356d8500cfc949c4bddba9e2fb6b79760df0b289efa41db19247c7fdc83f9cc7 |

Original Review: .copilot-tracking/reviews/logs/2026-10-18/issue-120-dpia-reference-review.md.
No subsequent source changes or repeated Review. Delivery remains authorized
by caller, never inferred from reviewer permission. Latest read-only main check
still returns the exact supplied base. Authenticated account resolved via
`gh api user`: id 8036360, login jmservera; use repository-local noreply identity
`8036360+jmservera@users.noreply.github.com` for author and committer.

Delivery staging exposed raw-output whitespace in two lines of the adverse
failing-first unittest log and two Docker progress lines. These originals are
intentionally not stripped or normalized. Unfiltered staged `git diff --check`
therefore exits 2 on those four log lines; the non-log source/artifact check
is the delivery whitespace gate. Earlier pre-staging `git diff --check` passed
for then-tracked source edits and did not include untracked logs.
The optional commit skill's referenced instruction file and changed-file tool
are unavailable in this host; repository-required explicit bounded staging,
local identity and ordinary Git commands remain the authoritative delivery path.
