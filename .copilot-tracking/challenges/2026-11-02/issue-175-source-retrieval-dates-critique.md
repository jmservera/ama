# Critique: issue #175 source retrieval dates (2026-11-02)

* Execution: one final-candidate critique, performed inline
* Verdict: proceed

## Findings and dispositions

* Risk: a commit date is not an actual retrieval date. Disposition: accepted as an explicit owner decision; the verification text names the basis so it is not read as an observed retrieval.
* Risk: removing the failing audit expectation could hide the remaining gap. Disposition: the test now asserts the exact remaining finding, `SRC-ONS-BOUNDARIES:provisional_attribution`.
* Risk: closing #175 prematurely. Disposition: the PR uses `Refs #175` because the OS copyright year is unconfirmed.
