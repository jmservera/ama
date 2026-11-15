<!-- markdownlint-disable-file -->
# Changes: Issue #201 C1 rebase onto origin/main b64ec641

* Rebased `docs/demo-201-cutover-evidence-pack-2333` onto `b64ec641f89158b5d324cb7f8c522201278e2277`.
* One conflict in `docs/architecture/cutover-evidence-pack.md` (both sides appended at end of file). Resolved by keeping the merged PR 1586 "Post-wave stabilization checkpoint" section first and this PR's "Current-main cut-over local verification" section after it, with a blank line between. 0 entries dropped.
* `docs/reference/log.md` is not changed by this PR (by recorded instruction); it was not touched by the rebase.
* Original 2026-11-13 RPI artifacts are preserved unchanged.
