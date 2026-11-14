# Review: Epic #165 cohort provenance and boundary tests

Execution: executed once. Outcome: conformant for the Focused tier; no material findings open.

* Scope matches the request; tests fail if synthetic flags, boundaries, categories or splits regress.
* No private data read; no fairness or approval claim.
* Routed follow-ups: add per-entry `is_synthetic` flags to manifest profiles and workflows (needs hash and version bump); source categories from an approved cohort manifest once owner approval exists (#222).
* Human review and hosted CI remain required and are not claimed.
