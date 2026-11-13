# Details: #229/#230 renderer verification

* Harness derives from `PAGING_SCRIPT` in test_programme_screen.py with `total` parameterised (0, 50, 120) and offset driven by clicking Next/Previous; button attributes captured via `Object.keys(attrs)` minus `onclick`, plus `attrs.disabled` and `attrs["aria-disabled"]`.
* Expected from source: no disabled/aria-disabled anywhere; Previous at offset 0 and Next at last page make no `/api/cases` call; last page status reads "Showing cases 101 to 120 of 120"; total 0 or total <= first page yields no pager.
* Command exit codes saved via `$?` to a file; outputs hashed with sha256.
* Test environment: pip only, no PYTHONPATH=mvp, no browsers, no network.
* Stop: any failure is recorded as an observation; no src edits.
