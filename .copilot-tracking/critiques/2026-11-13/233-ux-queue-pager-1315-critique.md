# Independent plan critique (rubber-duck), verdict: Revise, amendments applied

* PC-001 browser check tabs to disabled Previous and focus leaves Next at the last page: adjust journey (not runnable here, Chromium forbidden; static review only).
* PC-002 pager absent when all rows fit: sync() guards absent buttons; test single page.
* PC-003 mypy: narrow object-typed results in tests (typed helper / cast), require zero errors.
* PC-004 manifest hashes workbench_browser_check.py, not the paging check: verify before touching.
* PC-005 test_role_screens pins limit=20 literal: keep literal.
