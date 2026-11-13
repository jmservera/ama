# Plan: Wave-1045 parent integration (Refs #440)

1. Merge the 8 child commits into the parent branch with one octopus merge (fallback sequential `--no-ff`), Co-authored-by trailer.
2. Verify the 86 child blobs byte-identical (`git ls-tree`/`git diff <child> HEAD -- .copilot-tracking` per child path) and zero diffs in `src/ infra/ tools/ .github/` vs base.
3. Append one section to `docs/architecture/cutover-evidence-pack.md`, one index row to `docs/reference/README.md`, one entry to `docs/reference/log.md`.
4. Check links/anchors, ASCII, `git diff --check`; no tests or venvs are run (all evidence is reused child evidence, classified `local observed` or `deferred`).
5. Independent code-review; review file; single commit; witness records.

Validation tier: Focused. No push, no PR.

## Critique amendments (applied)

* Final-scope check: base-to-final changed paths must equal the 86 child paths, the 3 target docs, and parent tracking records of this slug (and the critique/changes/review files); child blobs re-verified after the last commit.
* Merge recovery: confirm HEAD is base and tree clean before merging; if octopus fails run `git merge --abort` before the sequential fallback.
* ASCII and `Refs`-only wording checked in added text and commit message.
