# Issue 125 live run 4 research (2026-11-19)

Refs #125. Main 1dddac2e0. Prior notes: run 1-3 under docs/reference/research/issue-125-live-*.
Research disposition: executed (re-probe). Planning Readiness: Ready.

* Unticked: readiness list; no write access to operational systems; comparison against manual and conventional reporting.
* Offline: 47 of 47 discovery assistant tests pass. discovery-demo: company_connection DENY, approved_solution false, write/contact/rank denied, all attempted:false.
* Azure (read only): ca-cutover-test-demo-api revision 0000033, same image digest prefix sha256:5368f4e4 as run 3; running. No resource created.
* Evidence: .copilot-tracking/evidence/2026-11-19/issue-125-live-r4/
* Finding: no criterion is provable by new demo code without duplicating #1355 or fabricating a comparison.
