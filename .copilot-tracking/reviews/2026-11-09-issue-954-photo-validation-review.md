# Review: issue 954 photo flag browser validation (2026-11-09)

Execution: one self-review after implementation; independent exact-head assessment is still required.

## Outcome

Not conformant for the second acceptance criterion. The browser checker fails at `503: no disruptive toast, alert, dialog or modal` in its single admitted run.

## Findings

* F1 (checker, routed to a later user-authorized cycle): the disruptive-node detector counts an empty persistent `role=alert` container (`#account-error`) as a toast. Proposed fix: ignore nodes whose text is empty, keep failing on non-empty alerts, toasts and dialogs. Needs one new admission to prove; not applied here.
* F2: 503 and 403 behavioural assertions (request count, flag, initials fallback, inline status, refresh, no reload, denials not converted) passed for 503 and for 403 up to the point 503 failed the final classification. 403 classification and receipt rows for it were not produced by this run.
* F3: lock-busy attempts and the interrupted retry loop are admission evidence only.

## Routing

Later work: apply F1, one nonqueued admission, rerun targeted tests. Issue #954 criterion 2 stays unproven: use `Refs #954`.

## Qualification (dated 2026-11-09, C2; original text above is unchanged)

F2 above is imprecise. The original raw observation (`evidence-954/obs/photo-flag-stale-console.json`, session files) contains both a 503 row and a 403 row. The final classification loop asserted 503 first and failed there, so the 403 classification assertions never executed; "403 receipt rows were not produced" should read "the 403 classification was never reached". The adverse original outcome (not conformant at that run) stands.
