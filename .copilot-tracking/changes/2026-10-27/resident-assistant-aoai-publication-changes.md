---
title: Resident assistant publication changes
ms.date: 2026-10-27
---

## Scope and Current State

Task 469-publication-2026-10-27, full publication plan P01-P03.
No application, infra, Azure or ingress changes. Original implementation
Review remains Not accepted for whole-task/live acceptance.
Research Complete / Ready; Plan Complete / Ready after one independent
critique and parent dispositions. P01/P02 implemented and validated; ready
for one independent publication Review. P03 publication remains pending.

## P01: Preparation

Fetched main 49c942b33b89100c084d48a91215989e22de5887 already belongs to
candidate ancestry. Initial head 8f51686a3fbc4b1ca9a6e258a921b96f4fdeb8a6.
No rebase/merge needed; no existing head PR. Acquired shared lock with
`flock -w 0` in attached foreground process, not nohup/disown.
Authenticated GitHub id/login resolved; repository-local privacy-safe email
used for author and committer. Preparation committed as
7f1a9f3c3e381c184217cad6f96fe8eb78ba1110 with required Copilot trailer.

## Amendments and Divergences

Critique reported two concerns. Parent rejected the claimed temporary-path
prohibition as absent here (explicit owner tmp lock instruction and actual
successful acquisition), and the claimed automatic full-scope mismatch as
contradicted by runner `main()` selecting partial/full automatically.
Standalone partial verification was clarified in details. Original critique
is unchanged; no repeated critique, user decision or source modification.

## P02: Validation

Full tracking snapshot archived and restored/hash-checked externally at
`/tmp/ama-469-publication-cleanup-0ti878or`; 3400 directory/file members.
At the actual preservation checkpoint, ignored/untracked candidate file
selection was empty. Both authorized `git clean -fdxq` invocations completed;
protected tracked bytes remained identical. No historical tracking deletion.
External receipt and cleanup journal retain exact inventory and hashes.

The initial lock reservation was released only for the unchanged runner's
own timeout-zero acquisition; runner acquired immediately. No bypass or
other owner's process/resource operation. Command, exit zero:

```bash
git clean -fdxq
PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --changed --jobs 3 \
  --base 49c942b33b89100c084d48a91215989e22de5887 \
  --out /tmp/ama-469-aoai-publication-scoped-7f1a9f3c-20261027 \
  --lock-timeout 0
```

External receipt:
`/tmp/ama-469-aoai-publication-scoped-7f1a9f3c-20261027/receipt.json`.
Status passed, scope full, mode changed, all 17 required groups executed.
Automatic default full-scope verification succeeded on exact head
7f1a9f3c3e381c184217cad6f96fe8eb78ba1110, tree
f25fcf29142c739e532c8004af0608198056b166, base above. Conservative workflow
selection supplies the complete matrix; a redundant separate all-mode run
is unnecessary. Resource-bound worker limit selected two jobs from request
three. Isolated pip setup installed all five namespace distributions.

| Suite | Result | External log |
| --- | --- | --- |
| src/core unit discovery | 1388 tests, OK, 186 enumerated opt-in skips | 0043-project-core.log |
| src/api unit discovery | 1108 tests, OK, 314 enumerated opt-in skips | 0048-project-api.log |
| infra unit discovery | 450 tests, OK, zero skips | 0128-infra.log |
| Real SQL selector | 263 tests, OK, one inherited JSON-only non-applicability | 0145-mssql.log |

All six `test_resident_aoai_sql.AccountingSqlTests` actually ran and passed:
exact cap/concurrent last cent, five-per-resident concurrency/independence,
lost-response/failed-completion no-refund, missing-budget reapply no-reset,
restricted principal EXECUTE-only and restart/reapply/completion persistence.
This supplies new isolated local SQL evidence for parent RV-001, without
rewriting its original missing-evidence Review.

Other groups passed: all five project unit/lint/type suites, namespace,
static/workflow/Bicep checks, migration, Chromium design-system/regulatory
and pinned axe, real SQL, four hardened Docker/negative-probe/startup
contracts, fixable HIGH/CRITICAL Trivy gates, full retained scan reports and
SPDX, and logo-0600 startup contract. Not a vulnerability-free image or
human accessibility claim. Existing focused resident-assistant Chromium
result remains historical; the full matrix does not run that extra harness.

External receipts/logs are authoritative. This evidence/Review commit will
invalidate the first receipt for publication; fresh exact-head gate and
verification remain mandatory.

## P03: Review and Publication

One independent child Review executed Complete, outcome Residual work; no
established source defect or publication-blocking decision gap. RV-001 Medium
retains excluded live integration; RV-002 Low retains hosted/human acceptance.
The reviewer independently checked 191 command-log hashes and 208 retained
file hashes, archive identity and actual accounting-test results, not a fresh
gate or parent source re-review. Original parent verdict remains unchanged.

Final exact-head gate/verification/assessment and remote publication remain
pending. No branch push or PR yet. Private SQL migration
and authenticated managed-identity resident smoke remain explicitly unmet.
Do not deploy or alter deliberately open demo ingress.

Fresh fetch immediately after Review found new main
d455d67dc661b795d0d2f0e0bf5992722187fbcd (PR #429). Its changes are
documentation, original tracking evidence and rubric score only, with no
executable overlap. Integrate with an ordinary merge after committing this
child's original Review/evidence, preserve both index/log additions, and
rerun full-covering changed gate on the merged clean committed head. This
is requested publication maintenance, not another critique/Review.

The committed state records completion of the RPI assessment and the still
pending publication action. Final receipt, independent exact-head assessment
and actual remote PR metadata will be external; no post-gate metadata commit.
