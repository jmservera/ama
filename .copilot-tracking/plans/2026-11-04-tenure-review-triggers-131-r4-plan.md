# Plan: tenure review triggers (Refs #131, R4)

Research: [research](../research/2026-11-04-tenure-review-triggers-131-r4-research.md). Details: [details](../details/2026-11-04-tenure-review-triggers-131-r4-details.md).

* [x] Phase 1: `tenure_review_trigger` and `tenure_trigger_resolve` actions
* [x] Phase 2: core and API tests
* [x] Phase 3: READMEs and log entry
* [x] Phase 4: focused validation

Tier: focused; resident-record code only, no security, infrastructure, SQL schema or deployment change. Gate not run.

Critique (single pass, author-recorded): a trigger never decides a lease question (applied); open trigger makes pack stale and blocks Verified and redraft (applied); ambiguous identity resets route and verification to Unknown and needs the data owner to resolve (applied); resolution is by a named other person and restores nothing (applied). Later slices: household enumeration, offer gate consuming the route.
