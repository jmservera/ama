<!-- markdownlint-disable-file -->
# Critique: issue 230 paging coverage plan (single final-candidate critique)

* Execution: ONE critique, performed by the implementing agent itself because the brief forbids nested agents. It is NOT an independent critique; independent exact-head assessment remains required before publication.
* Verdict: approve-with-changes. Findings applied directly; no user decision required (none conflicts with a confirmed decision, none is significant or divergent).

## Findings and dispositions

* C1 (medium) Default-scope rows could be empty or full on a page because page membership follows ranking, making the page-local filter assertions vacuous. Disposition: applied. The checker derives actual membership from the real API and asserts each page has at least one default-visible and one default-hidden row; otherwise it fails with the exact unsupported fixture contract. It does not weaken the assertion or edit rank inputs outside the private fixture.
* C2 (medium) The side "Choose a home" queue also has "Previous page"/"Next page" links; role-name locators would hit the wrong control. Disposition: applied. Programme controls are addressed by `#programme-prev`/`#programme-next` and `button` role; the side links are asserted to remain GET-only links.
* C3 (low) Tab starting point: starting Tab from the last side-queue link assumes the pager is the first focusable in main. Disposition: applied as an actual assertion (focused element id after each Tab). If it is not the case, the check fails and is reported; no loosening after the review.
* C4 (low) Abort produces a browser console network error. Disposition: only `pageerror` and non-GET requests are failure signals; console network errors from the one constructed abort are expected and counted (route consumed exactly once is asserted).
* C5 (low) Claims: "page 1 returned" after Previous could be satisfied by stale DOM. Disposition: applied; rows are compared with the real page-1 membership and the page-2 ids must be absent.
* C6 (info) No axe file is available, and no real or AT evidence exists. Disposition: axe is printed as not run; no accessibility conformance claim.
* C7 (info) Correction balance is UNKNOWN. Disposition: no post-review repair; any failure is reported frozen.

## Decision

Proceed to Implement with the details as amended above. Critique is not repeated for this task.
