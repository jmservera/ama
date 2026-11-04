# Details: issue 151 slice 2

* Test scans web/*.js lines containing the invalid-field marker; passes when `aria-describedby` is within 3 lines or the file builds fields with a describedby attribute; asserts exactly seven sites so a new site forces an audit.
* Critique (executed once): the test is a static proxy, not announcement evidence; recorded as such in the doc. The file-level fallback is weak and accepted for a guard. No conflict with confirmed decisions.
