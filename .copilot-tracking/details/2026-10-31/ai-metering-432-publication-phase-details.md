<!-- markdownlint-disable-file -->
# RPI Phase Details: AI metering publication remainder

## Metadata

* Task ID 432-publication; slug ai-metering-432-publication; date 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-publication-plan.md
* Research: .copilot-tracking/research/2026-10-31/ai-metering-432-publication-research.md
* Initial direction: continuous inherited-lock exclusion, not unlock/reacquire.
* Boundaries: source-only; no metering rewrite, paid call or parent review rewrite.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Compose lock / candidate | P01-T01 complete; candidate commit pending | P01-T01, P01-T02 |
| P02 | Queued integration validation | Pending P01 | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Compose lock safely and prepare candidate

<!-- rpi:task id=P01-T01 -->
### P01-T01: Validated inherited lock

Context C2/C5: current independent os.open conflicts with the outer flock's
open file description. An explicitly passed util-linux fd 3 is proven inherited
by an isolated probe. Reuse fcntl and stat already imported by runner.

Implement heavy_lock(timeout, inherited_fd=None) and CLI --heavy-lock-fd.
Validate regular fstat and lstat path identity before locking the duplicate.
Nonblocking exclusive flock must reject contention; close the owned duplicate
on all exits, never unlock/close caller FD. os.dup defaults non-inheritable.
Standalone open/no-follow/wait is unchanged. Preserve lock throughout Runner.run
and verify. No canonical generated files are targets.

Tests: maximum five new methods in tools/test_rpi_checks.py, removals none;
parameterized failure cases can share methods. Use owned tempfile locks and
existing path redirection/mocking, never contend on the real shared gate lock
in tests. Add an actual util-linux subprocess test with bounded timeout and
explicit child exit, plus competing independent-open refusal and preservation
through exceptions. Full existing runner tests are regression coverage.

PC-003 allocation: (1) real util-linux composition and descendant FD exclusion,
(2) wrong/negative/closed/nonregular/symlink descriptors, (3) contended
independent-open denial and pre-yield duplicate closure, (4) normal/exception
duplicate closure plus caller survival, (5) main forwards fd and run/verify both
observe lock exclusion, with acquisition after caller release. Patch heavy
Runner work, not the flock semantics. Duplicates are non-inheritable; existing
Popen close_fds excludes the caller's intentionally inheritable handle.

Validation: python3 -m unittest discover -s tools -p test_rpi_checks.py -q;
python3 -m ruff check/format --check tools/rpi-checks.py tools/test_rpi_checks.py;
python3 -m mypy tools/rpi-checks.py tools/test_rpi_checks.py.
Completion requires all pass with no uncontrolled lock or new skips.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Reconcile and commit

Fetch main; non-rewriting merge with main side for rubric JSON if conflict.
Current main is already ancestor at intake, so an up-to-date merge is valid.
Preserve originals with task-owned external hashes. Git identity obtained from
gh api user; repository-local noreply author/committer, required trailer.
Record P01 completion and P02 candidate/gate-pending boundary before commit.
No broad cleanup or existing work movement.

<!-- rpi:phase id=P02 -->
## P02: Complete queued integration validation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Complete gate

Use literal caller outer flock -w 1800 /tmp/ama-rpi-heavy.lock around full runner
command with --heavy-lock-fd 3, --all --jobs 3, fresh current base and external
output. Keep external stdout/log and all original failed evidence. No duplicate
gates, holder interruption, foreign artifacts, uv or secrets.

Known B023/test_chat_panel failures: record exact commands/logs; refetch main.
If fix/gate-baseline-b023 landed, merge and commit updated candidate before a
fresh full run. Otherwise explicitly retain failure and proceed under caller
exception, without calling receipt passed/verified. Other failed prerequisites
are not within that exception.

PC-002: produce a per-group/per-command matrix naming candidate/base/tool
identities, logs/exits/test IDs or B023 locations, actual completed/failed/
not-executed coverage and causal prerequisite links. Classify all root failures:
direct B023/chat baseline exceptions and their disclosed blocked descendants
are permitted; unrelated failures, unexpected skips, cleanup, ownership and
identity errors still block. Check actual fix/main ancestry and source at
failure and final fetch, not merely an absent branch name.

PC-001: reconcile and freeze all in-tree markers/details/changes/state and the
Review preparation pointer before final gate and the sole child exact-head
Review. Final Review/state/results live under an external dated
.copilot-tracking mirror in the task-owned session files directory and are
included in the durable PR body. No new commit follows that Review.
An in-tree Review preparation artifact points to the external result and is
not a claimed execution/outcome. Preserve every original adverse result.
Source/base/tool change after the sole Review invalidates its publication
boundary and routes later work, never silently upgrades its assessed identity.

Completion evidence: actual full receipt and counts/status, current-base
verification if passing, or precise allowed baseline exception. Publication
after child Review must normal-push HEAD and open main PR with sources/evidence,
validation and Refs #432; hosted/human approval remains open.
