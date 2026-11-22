# Research: issue 470 faster local gate (2026-11-22)

Date: 2026-11-22. Research disposition: executed. Planning Readiness: Ready.

* Issue 470 has one unticked criterion: measured full-run time before and after, recorded in the PR.
* #2186, #2187, #2188 and #2190 are issues, not PRs. Their delivery is merged PRs #2215, #2220, #2221 and docs PR #2216; the combined PR #2272 is still open.
* Tests run: `python3 -m unittest tools.test_rpi_checks -q`, 123 tests OK in 31.9 s.
* The earlier 2188 note records an image build cut from 80.7 s to 1.3 s (warm cache) and no comparable full-gate pair.
