---
title: Issue 96 saved export check amendment independent critique
description: Independent critique of the prospective amendment and adoption plan, run in a separate agent context
ms.date: 2026-11-12
---

## Execution and verdict

Critique executed once by a separate `rubber-duck` agent context (not the author) against committed plan `656581e7a` before any new change. The author recorded the findings and dispositions below; the critic did not edit files and ran no tests. Verdict: Approve with revisions. All findings are compatible with confirmed scope; none needs a user decision. The earlier author-only critique and review of the original task are unchanged and remain non-independent.

## Findings and dispositions

* CR-1 (Significant): a client can forge a self-consistent copy because `content_sha256` is tamper evidence, not provenance. Fabricated or mixed-type field ids can reach the sort in `export_freshness` and fail with a server error, and the README says edited copies are always Invalid. Disposition: accept. Add a controlled Invalid answer for a copy the comparison cannot process (API layer only, no core change); add forged-copy tests; correct the README so the digest is not described as provenance and `Current` is conditional on the supplied copy.
* CR-2 (Moderate): precedence is misstated. Parsing precedes sign-in and the feature guard; an empty body becomes `{}` and fails the draft-id check; trusted-proxy requests without the CSRF header get 403 before the guard 404. Disposition: accept. Correct the plan record and README to describe precedence; keep the redundant dict check as defence in depth; no parser change.
* CR-3 (Moderate): case and draft binding evidence is incomplete (nonexistent case used, not an existing different case; no missing-draft case; the "writes nothing" claim ignores shared sign-in identity linkage). Disposition: accept. Test an existing other case, a missing draft with matching ids, and a mismatch, asserting no field disclosure and unchanged form and audit state; qualify the no-write wording.
* CR-4 (Moderate): per-request revocation and anonymous access are not tested on this route. Disposition: accept. Test anonymous 401 and role revocation after a successful check with the feature enabled.
* CR-5 (Low): verification omits shared CSRF, administrator and oversized-body tests, and error `no-store`. Disposition: accept. Run those focused suites; assert error responses on this route are not cacheable beyond what the server already sets, or record the limit.

## Rejected

None.
