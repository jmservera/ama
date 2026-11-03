# Research: issue #228 simulator and vulnerability-canary pin

Disposition: reused. Planning Readiness: Ready.

Evidence: merged PRs #655, #782, #820, #867, #930 (and closed #492); prior reviews under reviews/2026-11-0*-issue-228-*.md. Criteria 1 and 2 are met. Criteria 3 to 6 remain unmet or partial. Capture of submission and correction needs OD-47 and supplier-scoped access (security tier), so it is out of scope.

Gap found: no test pins "no role simulator in user views" (criterion 6, half) or proves contractor view never emits vulnerability data when the case and order carry it (criterion 4). #960 did the simulator pin for asset and board screens only.

Smallest slice: two tests in src/api/tests/test_procurement_screens.py. No product code change.
