# Review: issue349 preflight correction 1

Execution: executed once inline. Outcome: conformant for the bounded slice; the medium finding is closed in code and test. Independent re-review of the new head remains required and is not claimed.

* Attacker-host substring and the other malformed issuers can no longer report ready (tested).
* Valid tenant issuer behaviour preserved.
* Live AC (tenant setup, credentials, staff binding, real-user tests) remain blocked.
