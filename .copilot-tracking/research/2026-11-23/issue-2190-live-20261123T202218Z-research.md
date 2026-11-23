# Research: issue 2190, glued header angle (Refs #2190)

Earlier workers covered: glued "ok" after a log fragment, the late_success settle wait and its Chromium test, and the 218 timeout budget test. No criterion is open except robustness of flake 1.

New angle: the mirror of the glued "ok" case. A thread log fragment without a newline can end right before the next verbose header ("status=503test_b (Mod.Cls.test_b) ... ok"). `_test_header_indexes` uses re.match, so the header is missed. Probe on current HEAD: `_required_tests_passed` returns False (a false gate failure, i.e. a flake); `_classes_executed` silently stops counting that test (weaker evidence, not a failure).

Disposition: executed. Planning Readiness: Ready. Owner-only items skipped (billing, DPO, assistive-technology tests). No Azure resource used; the issue concerns local gate tooling.
