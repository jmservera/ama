<!-- markdownlint-disable-file -->
# Review: Chat storage approval (one pass)

* Execution: completed once, 2026-11-01. Outcome: Conformant with open items routed (below).
* Boundary: commit 84d508fd0 (rebased) plus live change on two apps.

## Findings

* R1 (Medium, routed to a later user-selected task): the focused local gate could not complete because another session holds the global heavy lock; independent exact-head review, hosted CI and human approval remain required. Publication gate is not satisfied by this review.
* R2 (Medium, later work): live cross-user isolation needs a second signed-in employee identity; unproven live.
* R3 (Low, later work): the resident demo app stores no chat, so the resident CHAT_* settings are inert; consider removing them or adding resident storage under its own decision.
* R4 (Low): demo and dpia docs "Not recorded" cells predate the decision; intentionally left, pointer added.
* R5 (Info): the repo changes and live settings match (same five values); `ca-cutover-test-api` is not updated live and would stay refused until redeployed.

## Checks

* No production/real-data approval claimed; no closing keyword; min replicas and jobs Manual unchanged; no secrets in artifacts.
