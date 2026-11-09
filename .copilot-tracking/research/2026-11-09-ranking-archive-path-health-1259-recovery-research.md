---
title: Issue 1259 recovery preparation research
description: Prospective research for unchanged-source recovery preparation of the child path-health fix while the 1258 Blob contract is unfrozen
ms.date: 2026-11-09
---

## Disposition

Research executed 2026-11-09 (qualified rpi-agent, Sonnet 5.5). Planning Readiness: Ready for a bounded unchanged-source validation plan. Not Ready for parent integration or any source change, because the 1258 Blob contract is not frozen.

## Identities (read from the worktree and refs)

* Child worktree `/home/azureuser/source/ama-demo-wt/issue-1259-recovery`, branch `fix/ranking-archive-path-health`, seed `fab9159d9aaab76b5729c604ff0b8ea225987183`, tree `95f938b6c56e8a5d400c241f962a8b9c32d660bc`, clean at start.
* Declared target `fix/ranking-archive-ancestor-durability` (issue 1258), not main. Latest fetched `origin/main` `06e3f2f456ab008f8e41f013d9019c2d82ea05b9`; child merge-base with main `f548b65f4aa31eb92a2cc9cb801130e422daed7f`.
* Parent seed `61df2371508f4b549b7d3a85a86770f4f83cead9` (worktree `issue-1258-blob`, clean, no commits beyond the seed at read time). The remote ref `origin/fix/ranking-archive-ancestor-durability` was not fetchable by that name; the local parent branch is authoritative and unpublished.
* Child history preserved: `683ec2716` fix, `0868e0a1d` first parent merge (`26b4ea391`), `e174b2cfa` second parent merge (`6d793bc3a`), `fab9159d9` evidence correction.

## Child versus current parent

* The child contains parent `6d793bc3a`. The parent has since advanced six commits to `61df23715` (filesystem correction 2 mount table, correction 3 held folder and mount ids, plus records).
* Read-only dry run `git merge-tree --write-tree HEAD 61df23715` reports one content conflict in `src/core/src/zava_forward/core/ranking_publication.py` (the child `_names` / `_require_creatable` hunks against the parent's rewritten `publish` confirmation). Nothing was merged.
* Owner 2026-11-08T18:44:58Z on issue 1258: "Use a blob storage for JSON persistence". It selects Blob for ranking-archive JSON and supersedes further local directory and mount hardening. It does not approve migrating unrelated JSON, new Azure resources or permission changes. The Blob re-scope is underway in `issue-1258-blob` and is not frozen. Its research and plan records in that worktree are unreviewed by this task and are not treated as a contract.

## Old child evidence

* Original research, plan, details, single Revise critique (PC-001 to PC-007), changes and author review (Residual work) are under `.copilot-tracking/` with the `2026-11-08-ranking-archive-path-health-1259` prefix, plus the `-cont-` propagation records. All are preserved unchanged.
* Reported old results: failing-first six new tests with seven failures, then 90 ranking tests green; after propagation core 92 and API 54 green. Those were author-run outcomes; this task re-derives them below and does not rely on them.

## Productive correction count

Retained evidence shows one original implementation cycle and one parent propagation for 1259, no independent review, hence no review-correction cycle recorded against the five-cycle repository default (parent 1258 spent three plus one owner-authorized further cycle, separate budget). The historical count beyond retained evidence is unknown. This preparation makes no source edit, so it consumes and renews nothing and infers no extra grant.

## Scope relevance under the Blob contract

Under Blob persistence the production archive is no longer a local directory, so `_names` / `_require_creatable` (regular file, dangling link, stat failure) would apply only to a local test adapter, if one is retained. Whether the original AC survive in Blob terms (unusable store reports unknown, no healthy-empty, path-free diagnostics, absent store first-run) is a decision for the 1258 contract. Proposal only: carry the observable AC (archive-unreadable shape, unknown window, no healthy-empty, path-free, absent first-run) over to the Blob adapter's failure matrix; local filesystem path-health becomes fixture support. No AC is closed or deferred by this record.

## Validation environment finding

The installed `zava-forward-*` distributions in the default Python are editable installs pointing at the primary checkout, so they would test the wrong source. Validation used a fresh out-of-tree venv with non-editable installs from a `git archive HEAD` export.

## Gaps and unknowns

* The Blob contract (conditional create, committed-unconfirmed, status and runner semantics) is unknown until the parent freezes.
* Mocked stat failure, the stat-then-listdir race and Store overdue (PC-004) remain residual.
