# Issue 81 live research (2026-11-19)

Task: issue-81-live. Disposition: executed. Planning Readiness: Ready (documentation-only outcome).

* Issue 81 has two unticked criteria: (1) #440 stabilization checkpoint, (2) all children closed or deferred.
* Children: #82-#88 and #131 closed; #130 open. #440 open with two unticked criteria (triage with owner approval; PR artifacts).
* The 2026-11-18 audit blocked both on #1837 (nomination forms 400 live). Main (e91b6fa81, PR 2105) now carries the #1837 source fix: forms are posted as JSON with the CSRF header by script; native urlencoded posts are deliberately refused (test_native_form_encoding_is_refused_and_writes_nothing).
* Deployed app ca-cutover-test-demo-api revision 0000033 still runs digest sha256:5368f4e4...c17e5fb, which predates the fix. Redeploy changes the live app and is outside the "no production changes" boundary; not attempted.
* No source gap exists for criterion 1 or 2 that code can close; #130 remaining unticked item needs authorised human evidence (waived/not needed for demo but not a code item).
