<!-- markdownlint-disable-file -->
# Issue 107 R1 proactive forecast: review (one pass, self-review)

Outcome: conformant for the slice; independent exact-head review and human approval still required.

* Read-only: verified by a test that the task count is unchanged and the provider call count is zero.
* Roles: contractors and unknown roles get PermissionError / HTTP 403; a coordinator does not see funding-evidence.
* No raw content: test asserts private markers are absent.
* Minor: the HTTP route clamps an out-of-range period (existing `num` convention) while the core method rejects it.
* Routed to later work: usage attribution (Tokenomics 2); RAI items need owner, Azure and legal evidence.
