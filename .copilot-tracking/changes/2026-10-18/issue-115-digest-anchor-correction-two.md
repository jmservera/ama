---
title: Issue 115 digest anchor correction TWO
description: Final authorized enumeration and prefetch name qualification correction, not a Review
ms.date: 2026-10-18
---

## Adverse Finding and Authority

Same session afd14196-e65e-4c89-b2cb-12c95fe860b4, task115,
branch fix/digest-anchor-evidence-115, PR404.
Starting exact head123cb90230abab400a0668b0c194822f06d7224c, clean worktree.
Remote main/base still c803614e8ca7c604e509f1c088f8b8f90f3063ef.
Coordinator SAME-reviewer follow-up NOT ACCEPTED, one Medium:
list_digests filters .json before verify sees reserved prefixes. A valid head
plus digest-malformed.txt yields intactTrue/digests1/CLI0/OK. Supplied finding
is preserved, not recast as successful correction ONE acceptance.

User explicitly authorizes correction TWO, final permitted cycle (2of2),
enumeration/name-before-fetch gap only. No third cycle without owner authority;
no new/amended original Review or artificial Pass.
Correction ONE receipt/logs and both adverse coordinator findings stay intact.
Original critique SHA256
d1add2a5642689cb9a615f3aaa989871a3b405f7f5cab076689fdcc0110314e0
and original Review SHA256
dc72719806ba648af00d34c9ef6b0c0d049ed87372d60ee49e959b328694186e
checked unchanged at intake.

## Callsite Inspection and Bounded Design

Search src and infra/tests Python for list_digests and _valid_anchor:
only list implementation and verify consumer exist. publish never lists remote
names: it reads local ledger.read_digests/read_year_digests and create-only puts.
read_digest downloads only explicitly requested names. Preserve existing
list_digests inclusion of unrelated .json for compatibility, adding only reserved
case-sensitive digest-/year- candidates regardless extension. Do not broaden
to arbitrary unrelated non-JSON objects or introduce alternate prefixes.
Publisher uses lowercase exact prefixes/.json; matching is case-sensitive,
not a new case-folding policy.

Verifier must reject noncanonical reserved names before read_digest using the
same publisher count/year filename constraints as correction ONE. Keep payload
validation for canonical names and fixed invalid-anchor problem/no content.
Head format minimum10 ASCII digits, longer counts without leading zero;
year four ASCII digits excluding0000. Valid year/head and unrelated JSON/nonJSON
remain unaffected; malformed names never fetched. No container mutations.

## Plan and Initial Status

P04 only: failing-first suffix/prefetch matrix, minimal list/prefetch adjustment,
focused/full orchestrator/configured gates, normal commit/push/PR404 update,
same-reviewer exact-head follow-up. Use task-owned worktree TMPDIR, installed
venv, env -i, public fixtures/fake transport. No private inputs/.env/support,
Azure/IAM/Graph/SQL Server/Docker/deployment/spend/retention/services or board/
issue writes. All operational AC and legal/resident/human approvals unmet.
Status: active before regression/source changes; acceptance NOT ACCEPTED pending
independent follow-up.

## P04-T01 Failing-First Evidence

Added two existing-fake methods. Against unchanged source SHA256
9b684dd8828945903753ddcd8d6830dae46b91876a3fa2953a6a92adf44b8d0e,
two methods produced46 assertion failures, no setup/import errors (exit1).
45 matrix cases cover15 reserved bad names alone/validhead/validyear:33
non-JSON names miss invalid-anchor classification,12 malformed .json names
are wrongly fetched. One listing compatibility assertion exposes missing
reserved suffix candidates. Before log retained separately.
Positive head/year/unrelated controls ran before final listing assertion.

## P04-T02/T03 Actual Validation

Source changed only listing admission and a canonical filename check before
read_digest. Regex uses ASCII digits, exact publisher case, canonical minimum10
head count digits (longer without leading zeros), nonzero four-digit year.
Existing payload qualification unchanged. Two new test methods, prior21 digest
methods/fake untouched. 45 malformed matrix cases check report, CLI1/ALERT/noOK,
no name/content leak, no fetch, no PUT/DELETE. Good head/year controls pass with
unrelated JSON/nonJSON and alternative uppercase prefixes unfetched.

Installed task venv V =
/home/azureuser/.copilot/session-state/afd14196-e65e-4c89-b2cb-12c95fe860b4/files/digest-venv.
Every unittest/probe command prefix was exactly:

```bash
env -i PATH=/usr/bin:/bin TMPDIR=/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp PYTHONPATH=src/core/tests:src/orchestrator/tests <V>/bin/python
```

Actual commands from root (V substituted above), output in adjacent logs:

```bash
# before: unchanged source, exit1, 2 methods/46 assertion failures, no errors
<prefix> -m unittest test_digest_blob.BlobDigestTests.test_reserved_malformed_names_are_rejected_before_download test_digest_blob.BlobDigestTests.test_listing_and_unrelated_object_compatibility -q
# after: exit0, 27 tests, zero skips/errors
<prefix> -m unittest test_digest_blob test_recovery.YearLedgerTests -v
```

From src/orchestrator, full discovery exit0,46 tests, zero skips/errors:

```bash
env -i PATH=/usr/bin:/bin TMPDIR=/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp PYTHONPATH=../core/tests <V>/bin/python -m unittest discover -s tests -q
<V>/bin/ruff --version && <V>/bin/mypy --version && <V>/bin/ruff check . && <V>/bin/ruff format --check . && <V>/bin/mypy
```

Quality exit0: Ruff0.17.1 All checks passed; format9 files already formatted;
mypy2.4.0 Success12 source files. Existing per-file lint ignores, digest
format exclusions and mypy ignore_errors/follow_imports skip remain; configured
pass is not new strict coverage. No packages installed this cycle.

Probe used the same sanitized root prefix with `-` and inline Python:
load exact123cb902 digest_blob source via git show/compile into ModuleType,
construct existing BlobDigestTests fixture, actual make_digest for3 entries,
valid head plus digest-malformed.txt bytes PRIVATE_SENTINEL. Direct verify and
injected main assertions/log in correction-two-probes.log:
before intactTrue/digests1/CLI0/OK; after intactFalse/digests1/CLI1/ALERT.
Neither fetches malformed contents; corrected output has no remote name/content.
Probe also asserts tempfile.gettempdir equals task root; fixture teardown
completed and empty task TMPDIR removed with rmdir.

git diff --check exit0. No external SQL Server/Docker/Azure/browser validation:
N/A/not run, unchanged backend-only scope and offline authority. Coupled SQLite
unit is not external SQL/recovery acceptance. No services/private inputs/cloud
credentials/policy/irreversible operations. All operational issue ACs unmet.

## Frozen Parity and SHA256 Receipts

`git diff --name-only 123cb902 -- .copilot-tracking/reviews` and correction-one*
paths empty. Both frozen originals and all correction ONE receipts/logs unchanged.
No second critique or new/amended original Review.

| Path suffix | SHA256 |
| --- | --- |
| digest_blob.py | 9d2c726873b60a266249d023b75a48a551a2476094363c13282a2b8268a7247a |
| test_digest_blob.py | dbfdc96138b47486ff2e13d6df64efdb983268263f3fc5e487b6f26d369561ac |
| src/orchestrator/README.md | 53d2d095116044c9d4b5607314c43e8f23ec55a0153e8b38d22951e43b3742a4 |
| correction-two-before.log | a65d57232535b041db848fcbddd02c100ac05a6a5e5069b6a1b968cb9a852356 |
| correction-two-focused.log | 4eb3e2f262ee668290fa42a2a54ebfae438f618df7a51aacc3b9af7556820d90 |
| correction-two-orchestrator.log | 1d42fe0c34506ed9f01f925ae4c6aaaae3775b1f512dddaf5631997097bb0425 |
| correction-two-probes.log | 8aa4186a7e54f0d949d388251c1869a018c9e54bead91db340692c03ee3158b4 |
| correction-two-quality.log | ef29fcc39ea5cdd006365ec062fe5406748501ac545ea6f5dad8e7d0245d5e3c |

## Publication Status

gh api user re-resolved actual8036360/jmservera before commit. Configure only
local privacy-safe noreply author/committer, Conventional Commit and Copilot
trailer. Normal same-branch commit/push next, main must remain exact pinned base.
No rebase/force/merge/issue/board changes. Independent acceptance remains
NOT ACCEPTED pending SAME reviewer. This is correction TWO final, not a Review.
