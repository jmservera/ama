<!-- markdownlint-disable-file -->
# RPI Changes: Resident authority extension

## Metadata

* Task ID: 521
* Slug: resident-authority-extension-521
* Date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/resident-authority-extension-521-plan.md
* Details: .copilot-tracking/details/2026-10-30/resident-authority-extension-521-phase-details.md

## Execution Status

Partial, full-plan invocation. P01/P01-T01/P01-T02 and P02-T01 executed.
P02/P02-T02 incomplete: complete current-base gate and exact-head assessment blocked.
Rebased existing local implementation to 92b66933 on a02984e8; preserved both
knowledge-base conflict sides. No new source correction yet.

## Execution Summary

Research executed / Ready. One critique Complete / Revise, with all six findings
disposed directly in the plan. Parent has no temporary-directory prohibition;
current user explicitly requires the /tmp shared flock and a 600-second wait.
Sanitized direct checks and separate owned-SQL coverage address material concerns.

## Implementation-Time Plan and Detail Updates

PC-002 adds separate core SQL fixture validation because the default full runner
does not select that class. PC-003 adds env -i isolation. PC-005 concretizes
changed-infra checks. PC-006 adds a distinct external exact-head assessment only
after a passing receipt. No new source/tool scope or repeated critique.

## Validation Record

Before setup, python3 namespace import failed (ModuleNotFoundError); Ruff/mypy
absent on PATH. This justifies pip restoration of existing manifests.
Created only owned external venv/home/cache/tmp/Azure-config directories under
/tmp/ama-521-validation-20261030. No ambient credentials/config copied.
At current admission lslocks reports foreign PID 2308530 on the heavy lock.
Caller expressly permits flock -w 600; no foreign process/output is accessed.

The initial locked setup attempt timed out after 600 seconds without running pip.
Restored missing dependencies with pip as lightweight setup, outside a heavy
gate. The next locked validation invocation acquired the lock and executed.
Core resident/rendering: 78 tests, 27 explicitly opt-in SQL skips, exit 0.
Infra resident helpers: 32 tests, no skips, exit 0.
API/core Ruff check, format check and mypy each passed.
First full API run: 1380 tests, 76 errors, 320 skips, exit 1. Errors report Node
missing because the allowlist omitted its installed nvm directory. Correct the
validation PATH and rerun; this is harness configuration, not a source defect.
Targeted infra static checks exposed pre-existing renderer typing/formatting and
helper lint debt; baseline comparison pending. Owned real-SQL execution ongoing.

### P01-T01 final local results

All commands used the owned external venv and allowlisted environment; heavy
gates held /tmp/ama-rpi-heavy.lock using flock -w 600. Full command arrays and
exits are in /tmp/ama-521-validation-20261030/results.json.

| Check | Result | External log in /tmp/ama-521-validation-20261030/ |
| --- | --- | --- |
| Core resident/rendering | 78 tests, 27 explicit SQL opt-in skips, exit 0 | core-resident.log |
| Infra secret/deploy fake CLI | 32 tests, no skips, exit 0 | infra-resident.log |
| Final requested API discovery from src/api with exact PYTHONPATH | 1380 tests, 320 opt-in integration skips, exit 0 | api-tests-final.log |
| API Ruff check/format/mypy | All exit 0 | api-lint.log, api-format.log, api-types.log |
| Core Ruff check/format/mypy | All exit 0 | core-lint.log, core-format.log, core-types.log |
| Separate actual local SQL | 27 tests, no skips, exit 0 | resident-real-sql.log |
| Owned SQL cleanup | Exact labelled container removed, exit 0 | sql-cleanup.log |
| Changed infra Ruff/format/mypy | Each exit 1, same findings reproduced on base | infra-*.log, infra-baseline-*-final.log |

Preserved harness failures: initial API errors were absent Node in isolated PATH.
The first Node-restored retry mistakenly ran from repository root and failed
discovery before tests; api-tests-node-restored.log retains it. Final correct
src/api invocation with installed Node passed. No application change was needed.

SQL endpoint/container ownership is in sql-identity.json, without authentication
material. Ephemeral synthetic DB authentication existed only in process memory/
environment; no actual credential file or secret was read, printed or stored.
The 27 actual SQL tests include old-constraint migration, trusted reapply,
row/revocation/rights preservation, exact cap insertion and failed replacement
rollback with zero remaining transactions.

Targeted infra findings: RUF100 in pre-existing test import noqa, FURB162 in
pre-existing datetime conversion; renderer's pre-existing formatting; invariant
attrs_before dict type at renderer connect call. All reproduce using files from
a02984e8. Baseline extraction initially lacked executable mode/import search
paths; corrected mode/MYPYPATH removes those probe-only findings and leaves the
same two lint/one type/format findings. No unrelated suppression or cleanup.

Evidence hashes:

* api-tests-final.log: 0c703e30f5ddf8b105fc061e3bf8a4a01a622275cc59b86965125801c59d2ae2
* resident-real-sql.log: df83f5482433ca090c7659f047e1ffbea6c5a54574c1d0335ac71e1a4e3509b7
* results.json: 772cee27ce0e9c8cd2b5dcc731332b0a07b9a95c564164b44637fee2a53f381c

### P01-T02 documentation reconciliation

Added fresh evidence and explicit limits to infra/README.md, the knowledge index
and append-only log. No further runtime/test/SQL correction was justified.
Removed only owned generated build/egg-info directories and root Ruff cache.

### P02-T01 original independent Review

Executed once, Complete / Residual work; no new source defect. Technical
credential/SQL renewal assessment completed positively within conditional source
scope; exact operational review/owner approval is not inferred. AC1 locally
proven, AC2 estimate/no-resource-change portion proven but live headroom unknown,
AC3 technical plan documented/reviewed with operational approval pending,
AC4 unproven. RV-001 High publication/current-base, RV-002 Medium owner/live/
funding and RV-003 Low pre-existing infra static debt route to distinct follow-ups.
No source fix or second Review follows.

### P02-T02 commit and gate handoff

Commit source documentation and all current original dated artifacts locally.
After this commit, invoke the unchanged full runner against reviewed a02984e8
with --out /tmp/ama-521-final-20261030 and native 600-second shared lock.
Capture actual exit/refusal externally at
/tmp/ama-521-validation-20261030/final-gate.log; it is not pre-recorded as an
observed result here. Current origin/main fetched at finalization remains
4b37c2c9. Runner admission logic makes the reviewed-base mismatch a known blocker;
no receipt/full success/independent exact-head assessment is claimed.
Any passing gate would require fresh current-base verification, but no silent
rebase, fabricated receipt, cloud fallback, push or PR is permitted.

## Pre-Review Reconciliation

Review-ready as source-only candidate with residuals, not fully accepted.
Plan/details/changes agree on completed P01 and pending P02. Historical original
adverse evidence remains intact. Live/owner acceptance remains outside this run.

## Blockers

Origin/main advanced to 4b37c2c9ae5553e55604a10e97e7ab21a2a265fb during execution.
The candidate was reviewed/tested on a02984e8; unchanged runner refuses that stale
base. Do not silently rebase/reuse validation. Targeted pre-existing infra static
debt remains failed. Live apply/headroom/operational review remain owner gates.

## Remaining Work

P02 original independent Review, evidence commit and full-gate refusal recording.
A passing full receipt/current-base exact-head assessment requires later
coordinator reconciliation. No push.

At closeout the Review is executed; only evidence commit/admission recording
remain administrative parent actions. P02-T02 acceptance stays incomplete.

## Follow-Up Items

Owner exact live approval, funding/headroom, operational review/apply/verification;
coordinator gated publication.
