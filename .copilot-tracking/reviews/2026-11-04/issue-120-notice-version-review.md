<!-- markdownlint-disable-file -->
# Review: issue 120 slice 1

Execution: one self-review by the implementing agent (not independent). Independent exact-head review, hosted CI and human approval remain required.

## Critique (plan stage, one pass)

* Operational break: deployments that already set `ZF_TIME_NOTICE_APPROVED` without the version now show capture off. Accepted: capture is off by default and not live; the reason text names the missing setting.
* Alternative (store version in DDL) rejected: adds SQL migration for no extra guarantee.

## Outcome

* Conformant for the slice: behaviour matches plan; focused tests, ruff and mypy pass.
* Findings routed to later work: audit detail text does not yet include the approved version (small follow-up); replacing the draft wording needs human approval.

## Acceptance criteria status for #120

* C1 DPIA reference gate: previously proven (PR #408); unchanged, tests still pass.
* C2 minimum group aggregates: previously proven; unchanged.
* C3 staff notice approved and enabling audited: UNMET. Audit mechanics exist and this slice ties approval to wording version, but the actual notice approval, consultation and administrator ratification are human/legal steps not evidenced. Use `Refs #120`.
