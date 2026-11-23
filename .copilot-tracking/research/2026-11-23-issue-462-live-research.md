# Research: issue 462 close-out (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Findings:
* Live revisions match the brief: `ca-cutover-test-demo-api--0000054` (min 1, max 4) and `ca-resident-demo--0000026` (min 1, max 1), image digests in `evidence/2026-11-23-resident-showcase-live/az-state.txt`.
* Owned resident resources in `ama`: `ca-resident-demo`, `id-resident-demo`. No `aoai-resident-*` account.
* #444 is CLOSED and PR #455 MERGED (2026-10-25T21:25:42Z); the failed rubric run and manual-edit absence cannot be shown without hosted data.
* No HSTS header on the resident app; HTTP redirects to HTTPS and the session cookie is Secure. Not a stated criterion; no source change made.
* Prior r5 live script re-run unchanged against 0000026: 36 checks ok.
