# Issue 2195 review

Date: 2026-11-21. One review of the working-tree diff. Outcome: conformant with routed follow-ups; no blocking finding.

## Assessment

* Routing is additive: refusal, consent, approval and AI-unavailable paths are untouched, and the reply keeps its existing fields.
* The UI tolerates a missing `routing` field and adds plain text inside the existing live log.
* Tests cover tie, role gating, refusal, fallback, unstored and legacy calls.

## Findings routed to follow-ups

* F1 (low): keyword scoring is simple; unusual phrasing stays general.
* F2 (medium): live demo apps run the earlier image, so the feature is not visible there until deployment.
* F3 (low): employee agents are evidence lenses, not separate model runs.

## Outcome

Conformant for the local demo. The assessed boundary is the working tree before commit. Human review stays open.
