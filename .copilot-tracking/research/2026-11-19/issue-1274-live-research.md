# Issue 1274 live research (2026-11-19)

Opening note. Scope: prove each unticked acceptance criterion with evidence for the synthetic demo. Prior art: merged #1275 delivered tools/install-actionlint.py and tests.

Rerun 2026-11-19T14:43Z. Re-checked: `python3 -m unittest discover -s tools -p test_install_actionlint.py` gives 12 tests OK. `gh run list --workflow "Source projects CI" --limit 200` returns no run for heads fb7231c78, 0639b6e3d or c1628cb50, so criterion 1 for #1271/#1273 cannot be re-observed (the #1243 job 128696067639 504 was captured in docs/reference/research/issue-1274-live-release-download-criteria-2026-11-19.md). Remaining unticked criteria 1 and 4 need retained logs that no longer exist or a push, independent review, hosted CI and merge; none is code-addressable. Planning readiness: Ready for an evidence-only decision.
