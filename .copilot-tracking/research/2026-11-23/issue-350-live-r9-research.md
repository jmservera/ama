# Issue 350 r9 research (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

r6 to r8 left all ten criteria unticked. This pass re-measured live (edge tool, staff Playwright probe, non-secret Azure state, six-minute retry loop). Findings are in [docs/reference/research/issue-350-live-r9-2026-11-23.md](../../../docs/reference/research/issue-350-live-r9-2026-11-23.md). One real defect: GET `/api/assistants` swallowed a SQL write-lock timeout into a fixed 503 with no `Retry-After` and no logged cause, while `/api/briefing` handled the same condition correctly. Forecast 503 is the designed bounded timeout owned by #2304. Criterion 1 stays an edge (infra) matter; no exemption is safe without trusted-principal proof.
