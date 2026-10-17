<!-- markdownlint-disable-file -->
# Authorized issue88 integration onto setup391 main

## Actual Authorization and Rebase

Coordinator explicitly authorized own issue88 topic rebase onto current main
74617981b71bc3f10bd21d0b78691bc3cf36c473, expected old remote
cfeb18598ba8ae84cb8b80c0c7623e375ae886fe. Before writing, own worktree
status was clean, branch fix/resident-update-remedy-controls-88 and local/remote
heads matched that lease. Fetched main and inspected graph/diff: the sole main
delta from22670277 is setup-fix PR391, confined to infra/docs/evidence.

Executed git rebase74617981b71bc3f10bd21d0b78691bc3cf36c473.
Only conflict was docs/reference/log.md append insertion. Resolved by retaining
the complete upstream log followed by all issue88 entries, not choosing one
side. All later own commits applied cleanly. Rebased implementationedf63d12,
prior evidence chaine6c0604c. No source correction or new full Review/critique.
Original single Review/critique and every preceding issue88 RPI/integration
artifact remain byte-identical to the expected old remote.

## Exact Preservation Proof

Compared old22670277..cfeb1859 with new74617981..e6c0604c using
git diff --unified=0 additions/removals: exact own patch-line parity across
all fourteen src production/test/guide paths. Stronger whole-tree comparison:
git diff cfeb1859 HEAD -- src is empty, so the entire application source/test/
configuration/web tree is byte-identical to the last tested progress integration.
No runtime or persistence conflict, no change to report source/export/role
checks, full-precision UTC handoff events/authoritative sequence, current quality
selector, current actor/stale approval or pre-/post-COMMIT exactly-once guards.

Direct git show byte comparisons also preserve setup391 exactly:

| Upstream file | SHA256 |
| --- | --- |
| infra/scripts/setup-entra.py | f1579774ae790e56130a80c5377945294021471ff682a9c481583f755076f25d |
| infra/tests/test_setup_entra.py | d1e7a9af987816b8429a4845d0d3bb8f8718effbc11319d04000b2c6dc461849 |
| infra/README.md | 155f2ec6dadec4b77303da60f7c251a20710d914a38ce65b9ee2001ace9f9803 |

This retains the current setup classifier and its negative guard tests; it
does not claim those infra tests were rerun here. New upstream KB log is an
exact byte prefix, SHA256
3527c0d0bf59b51f3075633d403583940c279259d706d80b7491ad742ab61235.
All own appended log entries retained in order. All table route keys from both
old topic and new main survive; setup391's revised route wording retained.

## Actual Focused Validation

```bash
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest \
  test_resident_decisions.JsonResidentDecisions \
  test_resident_decisions.SqlResidentDecisions test_resident_api -q
git diff --check
```

65run,63pass,two existing skips,24.648seconds. Skips: JSON file rollback
inapplicable in SQLite subclass, opt-in browser. Real authenticated local HTTP/
SQLite and JSON tests exercise full commitments/identity/version refusals,
independent remedy/response close/reopen, mixed closure/restart, legacy Unknown
provenance, concurrent writers, rollback/recovery and truthful post-COMMIT
outcomes. Unloaded law-store fixture emits explicit Unknown rule-check logs,
not legal clearance. No new dependencies; existing pip-installed worktree src.

No full SQL/Docker/browser or repeated static suite: source/test/config bytes
are unchanged and this docs-only base integration explicitly permits focused
checks plus source fingerprints/diff hygiene. Previous progress integration's
140 relevant checks/static and quality integration's actual SQL/browser/image
receipts remain historical, not relabelled newly run.

All three exact issue88 criteria retain their earlier direct source/test mapping
and these focused regressions. Broader governance remains separately routed to
planning parent/repository owner at next #81 triage with Legal/Housing/Complaints
approval. Full event capture stays with issue102events; no expansion here.

## Publication Boundary

Fresh gh api user supplies repository-local privacy-safe noreply author/committer
and required Copilot trailer on own metadata/evidence commit. Verify old remote
still equals the authorized expected head before topic-only push:

```bash
git push --force-with-lease=refs/heads/fix/resident-update-remedy-controls-88:cfeb18598ba8ae84cb8b80c0c7623e375ae886fe \
  origin HEAD:refs/heads/fix/resident-update-remedy-controls-88
```

Do not widen changed lease. Update same PR392 with base/head and actual limits;
verify clean local/remote/PR head equality then stop. CI absence is pending,
not green; no idle watch. No other worktree/main/cloud/private write, new
authority, independent Pass, new full Review, merge or issue closure.
Resume3a36c179-e1e3-4332-9c33-fa947262fd79.
