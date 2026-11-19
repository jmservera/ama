# Details

* Test 1: principal = roster row plus display name and tenant claims; nomination_record succeeds; case stage, hazards, closed, score, urgent and the portfolio ranking are identical afterwards.
* Test 2: principal with a different code is refused with PermissionError and no record is written.
* Live proof stays blocked: the deployed digest predates fix e91b6fa81; no image build or redeploy is in scope.
