<!-- markdownlint-disable-file -->
# Integration note: inherited #80 C3 state conflict (2026-11-11)

* Conflict path: `.copilot-tracking/rpi-sessions/2026-11-10/issue-80-capacity-c3-diagnosis-1110-state.json` (add/add when merging main into the #1420 topic). Inherited #80 evidence, not authored by #1420.
* Earlier Plan-phase blob (topic side, at `e913aa805e6662da7cae71345190252791173ce1`, ancestry `c50cfa2a` / parent `12d3ac842`): sha256 `ad70bad2f5fe40d6b60521ef7d1c985f2d131e335fab8f251d88dc72bbf486c2`. Preserved byte-exact, without normalising its missing trailing newline, at `.copilot-tracking/rpi-sessions/2026-11-11/issue-1420-inherited80-c3-plan-original.json`.
* Later Review-phase blob (main, from #1423 `3dbb79e90`): sha256 `c9521feacee756a845cbedc281d496d3bf55fe4641f37e3f4c442c93f21b91e5`. It adds genuine executed changes and review links, the original High and Medium adverse findings and the earlier failed browser result.
* Root decision (2026-11-11): resolve only this path to the exact main bytes and assert the hash, so the later adverse history is not hidden. Old findings and blockers are not edited to mark them resolved; they remain historical C3 outcomes. Any other tracking conflict or unexpected source change stops for Root.
* Fetched main `a853cce16fafdfe32c7a5fe90f3b0c8b544eef0b` (includes #1433); `src`, `infra`, `tools` and `.github` are unchanged from the earlier fetch `e0dec207`.
* The stopped handoff `handoff-1420-admitted-implementation-1111.md` remains unchanged as adverse history. This is integration and provenance handling, not a #1420 source correction and not #80 C6.
