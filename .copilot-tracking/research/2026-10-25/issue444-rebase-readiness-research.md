# Issue 444 rebase and review-readiness research

Date: 2026-10-25. Task slug: issue444-rebase-readiness. Parent: issue444-main-lineage-integration (artifacts preserved, including its Conformant review and the PR 455 verified receipt for head 6878d6ec).

## Scope

Same owner-authorised #444 read-only synthetic loopback preview only. #441 backlog acceptance is paused: nothing from #441 is implemented. No new resident capability, no runtime authority inferred, no live resources.

## Evidence

* Local HEAD 6878d6ec; PR 455 head e1bb33ef (one extra bot commit: `chore(rubric): record score 64/100`, changes only .github/rubric/scores/latest.json). PR is draft, CONFLICTING/DIRTY; only check rubric/score SUCCESS.
* origin/main 0245944a04d44444de9c9f1af765121e961a075c adds #457 non-destructive seed merge (core factory.py, seed_merge.py, sqlstore.py, tests), #456 and #448 docs, rubric score files. Previous base 36996d70.
* `git merge-tree` of the PR head with main: conflicts only in docs/reference/log.md (both append) and .github/rubric/scores/latest.json (bot metadata). README files auto-merge.
* Prior outcomes retained: 2026-10-24 Review "Conformant with follow-ups" (Medium finding fixed); lineage Review "Conformant"; both critiques "Proceed with changes". Previous receipt /tmp/rpi-444-gate-main36996d70 (SHA 9ecb9317...) is historical and invalid for the new base. Browser checks: 36 PASS on the prior head (35 earlier before the fix).
* Services 8350, 8444, 8445 return 200 and are not touched. The #441 acceptance is paused.
* Resident modules do not call factory.py, seed_merge.py or sqlstore.py changes; resident boundary opens a private JSON copy only. Semantic drift expected nil; the full suites and gate confirm.

## Intent per conflict

* log.md: preserve both sides' append-only entries; #444 entries stay after main's.
* latest.json: bot-generated score metadata of an obsolete head; take main's version. The bot commit e1bb33ef is not carried (its score describes superseded head); history remains visible on the remote until the lease push, and the rubric bot will rescore the new head.

## Planning readiness

Ready. Disposition: executed. Authority: coordinator authorises run-owned rebase and `--force-with-lease` push; no plain force.
