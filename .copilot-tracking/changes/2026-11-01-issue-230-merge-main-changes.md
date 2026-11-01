# Issue 230 merge of origin/main (PR 662)

* Research: conflict only in role-screens.js; main's role screens lacked registration closers.
* Plan/Implement: kept programme-manager and all main screens, restored closers, kept branch rubric score.
* Correction cycle 2: the earlier merge had deleted main-side #163 and #176 work (log entries, tracking evidence, DPIA provider position, determinism audit support generators, answer-key provenance). Restored all of it byte-for-byte from origin/main; nothing of it is reversed.
* Finance gate: an unmatched Received invoice now blocks; funding_ok no longer masks withheld budget evidence (Coordinator). Tests added in test_programme_screen.py.
* Review: node --check passes; programme screen tests pass; the diff against origin/main now contains only issue 230 files.
