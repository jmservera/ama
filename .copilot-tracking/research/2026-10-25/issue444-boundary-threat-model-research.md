# Issue 444 boundary threat model documentation: research

Date: 2026-10-25. Task slug issue444-boundary-threat-model. Written before any content change. Parent: #444 / PR 455 (draft). Earlier research, plans, critiques, reviews and the round-3 chronology are preserved unchanged.

## Trigger and authority

* PR 455 bot head b82a7c4c (rubric 72/100 vs baseline 73, A3 table 5 to 4; the scorer summary says "raised 3 to 4", which contradicts the table). No exploit or regression is named. The owner explicitly authorised bounded, genuine boundary threat-model documentation to resolve the blocker, and states that new issue 462 (Azure synthetic resident showcase) depends on #444 and must not widen #444, which stays loopback-only.
* The repository rubric review (docs/reference/research/company/capstone-brd-rubric-review.md line 45) lists a stated threat model as the A3 gap. No resident-boundary threat model exists in the committed 444 artifacts, src/api/README.md or src/core/README.md (grep for "threat" found none). This is a genuine documentation evidence omission, not a score chase.
* No score, baseline, scorer, workflow or prompt is edited. No unchanged rerun. No score increase is promised; if the assessor still fails, the actual finding is reported.

## Verified state

* origin/main ea5577b2 (fetched). Local was e36ffdee; remote is b82a7c4c (e36ffdee plus the bot commit touching only .github/rubric/scores). Worktree clean, so a fast-forward alignment is allowed and was done before this research.
* The e36ffdee receipt (SHA 6c89acc9...) is historical for any head containing the bot commit.
* The shared heavy lock file exists; admission is decided by the gate tool at run time.

## Evidence read (actual code, this session)

* Core boundary src/core/src/zava_forward/core/resident_preview.py: Grant, resolve_grant (re-reads the fixture, default-deny codes unknown_subject, no_grant, malformed, ambiguous, revoked, expired, fixture_unavailable), resident_view (field-by-field positive allowlist, no staff payload, no projection.py, representative tasks gated by _authority_current via the domain), safe_start (refuses ZF_, AI_, IDENTITY_, MSI_, AZURE_, MSSQL, APPLICATIONINSIGHTS, OPENAI, SQL env prefixes, non-loopback host, symlink, normal data and ~/.zava-forward paths, unmarked or mismatched files), open_store (private temporary copy).
* API src/api/src/zava_forward/api/resident_preview/app.py and __main__.py: identity is the --subject start-up argument only; Host header must be a loopback name with the bound port; unavailable paths return 403 for any method; other writes 405; strict CSP (default-src none, script/style/connect self, form-action none, frame-ancestors none), nosniff, X-Frame-Options DENY, no-referrer, no-store, CORP same-origin; only fixed asset paths are served; no outbound client code exists in the resident modules.
* Tests: core test_resident_preview.py (grants, expiry, revocation, representative authority, canary, allowlist, unknown stays unknown, offers vs confirmed, start-up refusals) and api test_resident_preview_api.py (server-owned identity, claimed identity ignored, host header, staff routes absent, writes refused and store unchanged, denied subjects, revocation next request, canary-free bodies, staff server not loaded, unsafe configuration), plus the browser check (36 PASS earlier, real local server).
* Residuals found in code: dataset, case and representative-authority data load once at start-up (only the grants file is re-read per request); there is no authentication beyond the process-owned subject; the fixed loopback trust relies on the OS user and localhost; log_message is silenced so there is no request audit trail; there is no TLS, session, rate limit or password.

## Boundary of this task

Documentation only: a new subsection in src/api/README.md (resident preview section) stating assets, trust boundaries, actors, threats, controls with test references, residuals, and explicit not-suitable-for-public-hosting, no password auth, restart limit and #462 separation. Link from src/core/README.md. No source, test, web or staff change. No claim of accessibility conformance, human review, live acceptance or that a threat model proves the rubric score.

## Planning readiness: Ready.
