# Plan: final integrated #1258 parent candidate (2026-11-09)

Refs #1258, #1259, #136. Research: `.copilot-tracking/research/2026-11-09-ranking-archive-blob-1258-final-parent-integration-research.md` (Ready). Details: `.copilot-tracking/details/2026-11-09-ranking-archive-blob-1258-final-parent-integration-details.md`. Local only. Source unchanged. No push, PR, issue or board write.

## Objective

One clean local head that contains C6 (`99814198`), the merged children via remote topic `ac41cce5b`, and current main `2be660e9`, whose source, infra, tooling, workflow and manifest inputs are byte-identical to the already qualified identities.

## Steps

1. Commit these prospective records (research, plan, details, critique, state) before any merge. Privacy-safe author and committer, Copilot trailer.
2. Pre-merge: re-resolve `origin/fix/ranking-archive-ancestor-durability` and `origin/main` and stop if they differ from `ac41cce5b1a7ded6a33fe5c57786affbca4783c0` and `2be660e9d290f95ff05fc5a56d6539768576732b`, or if the worktree is not clean. Then ordinary `git merge --no-ff ac41cce5b1a7ded6a33fe5c57786affbca4783c0` by commit id (ac41 stays an ancestor; no rebase, amend, reset, force or discard).
3. Ordinary `git merge --no-ff 2be660e9d290f95ff05fc5a56d6539768576732b` by commit id. Main is merged because its documentation (cutover pack, reference index and log) is part of the truthful final document set and the eventual PR is mergeable without conflicts; it carries no source.
4. Verify by hash and diff, not by test rerun:
   * `src` tree equals `f0df7dc4...`, `infra` tree equals `d94040329...`; `src/agents`, `tools`, `.github/workflows`, both `pyproject.toml` equal main/ac41.
   * Merge result tree equals `git merge-tree` prediction (`5f45a549...`) plus this task's own tracking files.
   * `git diff ac41 HEAD` contains only main's documentation paths, main's tracking records and this task's tracking records; no `src/`, `infra/`, `tools/`, `.github/` path.
   * `git diff main HEAD` outside tracking and `docs` equals the union of C6 and the two children; ancestry of `99814198`, `fbf0a0ab`, `ac41cce5`, `2be660e9`.
   * Both append histories (`docs/reference/log.md`, `docs/reference/README.md` additions) retained: HEAD file equals main's, because the topic did not touch them.
   * Original C6, 1259 and 136 tracking records unmodified: no modified or deleted tracking path against the originating commits.
   * Read the functional union at the actual files (flag-off/on selection, conditional create versus runner listing, status unknown/overdue, identity environment names, default-off retention in Bicep), not from summaries.
5. Per-check input binding (critique 1, 2): hosted child CI and C6 results are reported as historical child results over their own recorded identities (the #136 PR head `96f69163` carried a different `src` tree and the #1259 head a different `infra` tree than the final candidate; the hosted merge ref was not observed), not as CI of the final candidate. Doc-reading tests take docs inputs that are identical to main `2be660e9` (`docs` tree equal); source and infra inputs are identical to the qualified `ac41` bindings. The one test whose input genuinely changed on this candidate is the live Markdown link test `src/core/tests/test_live_doc_links.py` (scans live Markdown including main's new documentation); it is run once, from `src/core` in an owned core environment, as the smallest relevant existing check, and its result is reported as new evidence. A failure there is reported, not waived or fixed. Any source or dependency input difference: stop and report before running or repairing.
6. Author the changes record; after the final record commit repeat identity, ancestry, allowed-diff and clean-status checks so the handoff describes the frozen head (critique 4); and one original Review; write the state file; commit the final records; freeze.
7. Return the handoff with head, tree, fetched main, manifests, bindings, provenance, checks, skips and limits.

## Stop conditions

Any conflict, any unexpected `src/`, `infra/`, `tools/`, `.github/` difference, or any binding mismatch: stop, report exact finding and prospective scope before consuming C7. Do not repair by hand, rebase or reset.

## Validation evidence classes

* Reused, with identity: C6 and child test results and CI listed in the research.
* Newly observed: git identities, tree hashes, diffs, merge results, file reads.
* Not run: SQL, browser, Docker, `rpi-checks`, full gate, any new hosted CI. A new parent CI run does not exist and is not claimed.

## Budget

C6 spent; C7 to C10 remain, four. This integration makes no source correction, is not productive and resets nothing.
