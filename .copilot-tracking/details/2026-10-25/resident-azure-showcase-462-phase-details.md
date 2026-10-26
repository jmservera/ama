# Phase details: synthetic resident Azure showcase (issue 462)

Date: 2026-10-25, written with the plan and before critique and implementation. Plan: `.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-plan.md`. Research: `.copilot-tracking/research/2026-10-25/resident-azure-showcase-462-research.md`.

## Phase 0: dependency wait

* Entry: now. Exit: PR #455 merged, merge SHA supplied by the coordinator in this same session.
* Do nothing else: no code, no Azure change, no credential. Read-only re-checks allowed.

## Phase 1: re-baseline and preflight (read-only)

1. `git fetch`; rebase or branch from the merged main (no stacking on the #444 branch). Confirm overlap in `src/api/pyproject.toml`, READMEs, `docs/reference/README.md`, `log.md`.
2. Read merged `core/resident_preview.py` and `api/resident_preview/app.py`; confirm `resident_view`, `Grant` and the forbidden-environment guard are unchanged by this work.
3. Cost record (file under `.copilot-tracking/changes/`): current resource list, Cost Management by resource type and day, cumulative previous incremental spend and baseline definition from the coordinator (G1), remaining cap, finite resource list with retail prices, stop conditions, cleanup ownership.
4. Close G2: obtain a counts-only provenance probe (non-empty `resident.email`, distinct normalised, duplicates, non-synthetic domain, missing synthetic marker). Run only inside a private, owner-approved path after the cost record. If it fails, stop and report; do not invent emails or write to the database.
5. Close G3 and G4: confirm who can create the identity, the role assignments, the SQL principal and view, and how the owner reads the secret.
6. Exit only if G1 to G4 are resolved or explicitly accepted by the owner in writing.

## Phase 2: failing-first tests then core and app

Files: `src/core/src/zava_forward/core/resident_demo.py`, `src/core/tests/test_resident_demo.py`, `src/api/src/zava_forward/api/resident_demo/{__init__,__main__,app}.py`, `web/{index.html,demo.css,demo.js}`, `src/api/tests/test_resident_demo_api.py`.

Tests to write first:

* Mapping: unique mapped email; duplicate, missing, whitespace/case/Unicode-equivalent duplicates, non-synthetic domain and unmarked cases excluded; empty source refuses login; mapping never from client input.
* Credential: verifier round trip, wrong password, empty, very long input bounded, dummy-verify timing class for unknown email (no early return), no plaintext in any object, `repr`, log or exception.
* Session: valid, tampered MAC, wrong version, expired, future-dated, replay after logout, rotated key, cookie attributes, `__Host-` rules, fixed handle not exposing case id.
* CSRF and origin: missing/wrong token, cross-site Origin, GET login rejected.
* Limiter: per-source and global windows, 429 and `Retry-After`, generic body identical for all failures, clock injected, bounded memory.
* View: golden positive allowlist; canary fields (notes, safeguarding reason, finance, staff, contractor, chat, memory, raw error) planted in records never appear; offered versus confirmed wording; unknown stage text.
* HTTP: only declared routes; staff paths 404; unknown method 405; body size and timeout; headers and CSP; no raw errors on SQL failure (fixed text); no secret environment value appears in any response or log capture.
* Employee regression: existing `src/api` tests unchanged and passing.

Then implement the smallest code that passes. Use the standard library and existing dependencies only.

## Phase 3: parity, Docker, browser

* Real SQL Server: owned local container on an unused port with the existing local-server guard; seed only clearly synthetic records with canaries; run the read-only reader, the view (if approved) and a denied-write probe (INSERT/UPDATE/DDL by the resident principal must fail).
* Docker: build with `docker build -f src/api/Dockerfile.resident-demo src`, verify `USER 10001`, read-only root file system start, health, no `ZF_*` secrets in the image, Trivy config used by `src/trivy.yaml`.
* Browser: load `.github/skills/web-design-guidelines/SKILL.md` and fetch its source before web edits and again before review; read the selected `.agents/skills` entries (not the public-page taste skill for an app screen; Fluent 2 design system, WCAG baseline and content standard stay). Journeys: login success, wrong password, unknown email, lockout message, session expiry, logout, keyboard only, 200 percent zoom, reduced motion, screen-reader labels, banner and limits visible. Existing screenshot/validation checks as in #444's browser check.

## Phase 4: infrastructure and documentation

* Bicep module `infra/modules/residentDemo.bicep` (app, identity, role assignments, tags), parameters pin the image by digest, `minReplicas 0`, `maxReplicas 1`, 0.25 vCPU/0.5 GiB, ingress external, target port 8088, `allowInsecure false`, no secret values, KV references to two secrets only, health probes.
* Deploy helper test with offline what-if fixtures that prove: exactly the named creates, no change to employee apps, SQL, vault network, registry or other roles; resource group deletion impossible by construction.
* Secret script `infra/scripts/resident_demo_credential.py` with a fake vault in tests: generates with `secrets`, hashes with scrypt, sends through SecureString parameters, prints only names, versions, lengths; tests assert no value in stdout, stderr, files, arguments, environment or exception text.
* Docs: `src/api/README.md` resident-demo section, `infra/README.md` runbook (provision, retrieve without revealing, rotate, stop), threat model file (public login, shared credential, session, cross-case, DB fields, deployment isolation) committed with the code, `docs/reference/README.md` and `log.md` entries.

## Phase 5: gates and publication

* Unit/type/lint for `core`, `api`, `infra/tests` and `tools`; `python3 tools/rename-zava-tests.py` regression if touched.
* Commit implementation and dated original RPI evidence, fetch main, then `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-dir>`; keep the receipt external; `--verify-receipt <receipt.json> --base <current-origin-main-sha>` immediately before push. Any later commit, base change or dirty/ignored input invalidates it.
* One independent review (original outcome preserved), PR with author/committer noreply identity, hosted checks, coordinator assessment. No merge, force-push or score edits.

## Phase 6: deploy and accept (only after gates and prospective cost plan acceptance)

1. Refresh the cost record; abort on unknown headroom.
2. Generate and write the credential (secret script), build the image by the private kaniko route, record digest and source SHA.
3. What-if, review exact delta, incremental apply in `ama`, readback.
4. Browser acceptance against the real HTTPS URL: actual login for two mapped residents seeing only their own case, wrong password, unknown, forged cookie, expired session, cross-case, staff route and canary denials, lockout, logout. Root 200 alone is not acceptance.
5. Record image/source identity, URL, owned resources by exact name, validation, residual accessibility and approval limits, expiry and stop plan. Preserve earlier evidence. Do not close #462 with unmet criteria.

## Rollback and stop

Per the plan's stop action; every deletion by exact name after reading the tag `ama-issue=462`. A failed apply leaves existing resources unchanged because the template names only new resources.

## Critique amendments (2026-10-25, before implementation)

* Phase 1 step 5 adds: confirm delete/revoke authority and deterministic names for the identity's role assignments, the SQL principal and the view.
* Phase 2 tests add: restart-after-logout (boot nonce) denies a previously valid token.
* Phase 3 replaces the base-table probe with: resident principal SELECT on `cases` fails, SELECT on the view returns only allowlisted columns, INSERT/UPDATE/DELETE/DDL fail. There is no base-table fallback.
* Phase 4 and rollback add: post-delete readback queries for SQL principal, view and role assignments; secret expiry at or before 2026-10-26T12:00Z.
