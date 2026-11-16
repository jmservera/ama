---
title: "Task Research: resident-demo-local-gate-462"
description: "Prospective research and threat model for the local engineering, RPI artifact and full-gate criteria of Issue #462 (synthetic resident Azure showcase)"
ms.date: 2026-11-16
---

| Field         | Value                                                                    |
|---------------|--------------------------------------------------------------------------|
| Date          | 2026-11-16                                                               |
| Researcher    | rpi-research (RPI Agent automatic mode)                                  |
| Status        | Complete                                                                 |
| Base          | origin/main 5e0c7f74432ffce73cfeaa672e4e40a605ca6274                     |
| Branch        | feat/resident-demo-rpi-gate-462                                          |
| Artifact path | .copilot-tracking/research/2026-11-16/resident-demo-local-gate-462-research.md |

## Research Brief

* What: determine what already exists on current main for Issue #462, which unchecked criteria are local and engineering-only, and what a prospective threat model must conclude about the public fake-email login, shared demo credential, session handling, cross-case access, database fields and deployment isolation.
* Why: the issue requires genuine prospective RPI artifacts, verified dependencies, local SQL Server parity, Docker non-root startup, browser journeys, lint/type/unit checks and the complete exact-head gate.
* Non-goals: any Azure mutation, deployment or spend (needs owner pre-spend approval, out of scope); changing SQL S0 sizing, employee login or the #444 loopback harness; real credentials; push, PR or merge.
* Posture: focused. Edits during research: none to source. Evidence root: `.copilot-tracking/`.

## Research Disposition

Disposition: executed. Planning Readiness: Ready.

## Findings

### F1 Dependencies (criterion 2)

* #444 is CLOSED ("feat(resident): add isolated synthetic resident feedback preview").
* PR #455 is MERGED at 2026-10-25T21:25:42Z ("synthetic read-only resident feedback preview (refs #444)").
* The resident preview and the showcase both exist on main. The preview guards (`resident_preview.py`, loopback-only harness) are not imported by the showcase except for read-only text constants (`resident_showcase.py` module docstring).
* The issue text still mentions an earlier failed rubric on #444/#455. Main HEAD is `chore(rubric): record score 79/100`. This task makes no score edit, no unchanged-rerun fishing and no gate bypass; it records current dependency state only. Whether the historical rubric failure counts as resolved is a coordinator judgement left to review.
* Existing local previews remain: `src/api/checks/resident_preview_browser_check.py` and the #444 harness files are untouched by this task.

### F2 Implementation present on main

| Area | Evidence |
|------|----------|
| Domain (identity, scrypt verifier, session codec, limiter) | `src/core/src/zava_forward/core/resident_showcase.py` |
| SQL reader (two fixed SELECTs on one view) | `src/core/src/zava_forward/core/resident_showcase_sql.py` (`LIST_SQL`, `ONE_SQL`, 17 named columns) |
| HTTP app, cookies, CSRF, headers | `src/api/src/zava_forward/api/resident_demo/app.py`, `__main__.py` |
| SQL boundary template | `infra/sql/resident-showcase.sql` (DENY on `dbo.cases`, GRANT SELECT on the one view only) |
| Deployment composition | `infra/resident-demo.bicep`, `infra/scripts/resident_demo_deploy.py`, `resident_demo_secrets.py` |
| Image | `src/api/Dockerfile.resident-demo` (digest-pinned base, uid 10001, `USER 10001:10001`) |
| Tests | `src/core/tests/test_resident_showcase*.py`, `src/api/tests/test_resident_demo_*.py`, `infra/tests/test_resident_demo_*.py` |
| Local browser, image and SQL checks | `src/api/checks/resident_demo_browser_check.py`, `resident_demo_image_check.py`, `resident_account_check.py` |
| Documentation | `src/api/README.md` section "Synthetic resident showcase (#462)"; `infra/README.md` SQL boundary section |

Criteria already checked on the issue (login mapping and denials; secret provisioning docs; deployed record) are not re-claimed. No code gap is known; this task verifies the code and adds the missing prospective threat model and RPI evidence.

### F3 Threat model

Scope: the public internet reaches an HTTPS Container App (`allowInsecure: false`, `maxReplicas: 1`, `minReplicas: 0`) that holds one shared demo credential for all listed fake residents. Everything is a synthetic demonstration; none of it is production resident identity, enrolment or security acceptance. Control references are to current main code.

Assets: the synthetic home record projection (address, town, postcode, stage, measures, documents, sensors); the shared password verifier and session key (Key Vault secrets); SQL availability; the Azure budget cap.

Trust boundaries: (1) internet to Container App ingress; (2) app to Azure SQL as a user-assigned managed identity; (3) app to Key Vault secret references; (4) browser origin and cookie boundary.

| ID | Surface | Threat (STRIDE) | Current control | Residual risk and verification |
|----|---------|-----------------|-----------------|--------------------------------|
| T1 | Public fake-email login | Spoofing: anyone with a listed email and the shared password opens that synthetic case | Documented demo authentication; banner states sign-in does not prove identity; only ASCII `@example.com` accepted (`EMAIL_FORM`); server-owned `IdentityMap` from the allowlist view | Accepted by design: a shared credential is not identity. Mitigated by synthetic-only data and an owner-held password. Verified by domain and API tests |
| T2 | Email enumeration | Information disclosure: distinguishing known from unknown email | One scrypt run per attempt for unknown, malformed and wrong (`verify_login`); one generic denial `GENERIC_DENIAL`; same 401 | Timing is equalised by work, not proven constant; low residual |
| T3 | Password guessing | Spoofing, denial of service | Limiter of 5 failures per source and 60 overall per 10 minutes with 429 and Retry-After; scrypt N=2^15; body cap 2 KiB; concurrency cap 8; client address mode `ingress-rightmost` so a forged `X-Forwarded-For` cannot choose the key | A strong generated password is the main control; the global lockout can deny legitimate demo users (accepted for a demonstration) |
| T4 | Shared credential handling | Information disclosure | Only a scrypt verifier is configured, never the plaintext; secrets only via Key Vault references with a user-assigned identity; `infra/secret-inventory.json`; tests use an unmistakable fake constant; no real password exists in the repository | Operational: the owner retrieves and rotates it by the documented route; this task generates and prints no credential |
| T5 | Session handling | Tampering, fixation, theft, replay | HMAC-signed token with 1800 s expiry capped by the authority end; `__Host-` cookie with `Secure`, `HttpOnly`, `SameSite=Strict`, `Path=/`; CSRF double-submit cookie plus header and same-origin check on POSTs; per-session id header must match the signed token (409 otherwise); `Cache-Control: no-store`; logout; `Host` allowlist | Stateless tokens cannot be revoked before expiry except by rotating the session key; accepted for a 30 minute demonstration |
| T6 | Cross-case access (IDOR) | Elevation of privilege | Case id comes only from the signed session, never from client input; `authorise` re-checks the identity map and re-reads one case with parameterised `WHERE case_id = ?`; provenance, revoked, window, email-form and duplicate exclusions fail closed | Verified by two-resident tests with forged and expired sessions |
| T7 | Database fields | Information disclosure | Reader limited to 17 named columns of `resident_showcase.v_resident_case`; `ROW_KEYS` allowlist in `parse_row`; view filters `source_type = 'SYNTHETIC'`; no staff notes, safeguarding, finance, staff identity, chat/memory; SQL errors reduced to a type name; canary-field tests | The view is the sole boundary; an operator widening it would widen exposure. The `.sql` template and tests are reviewed; live schema is not inspected here |
| T8 | Deployment isolation | Elevation, tampering, cost | Separate Container App, identity, image, secrets and Bicep from the employee site; SQL principal has DENY on `dbo.cases` and GRANT SELECT on one view; any `ZF_STORE*`, `ZF_ENTRA*`, `ZF_AI*`, `AZURE_OPENAI*`, `ZF_DATA*`, `ZF_STATE*` setting aborts start; non-root uid 10001; no data or state volume; `externalIngress=false` rollback; expiry capped by packaged `resident-demo.json` (2028-01-01T00:00:00Z) | Actual Azure resources, roles and spend headroom are not verified (no cloud access by design) and stay as unmet issue criteria |
| T9 | Web surface | XSS, clickjacking, MIME sniffing | CSP `default-src 'none'; script-src 'self'`, `frame-ancestors 'none'`, `X-Frame-Options: DENY`, `nosniff`, `no-referrer` | Local browser check only; no penetration test |
| T10 | AI and write paths | Unintended actions | Read-only; assistant gated by `ZF_DEMO_ASSISTANT_ENABLED=false` by default; no booking, consent, upload or download | Optional AI is separately gated and out of scope |

Conclusion: for a time-boxed, synthetic, owner-controlled demonstration the controls are proportionate, with the shared credential and stateless tokens explicitly accepted. This is a design threat assessment, not a security acceptance, penetration test, legal or DPO approval, and it authorises no deployment.

Errata (2026-11-16, after the independent review): rows T1, T2, T3, T5, T7 and T10 above were first written with overstated claims. The review found that case rows are not filtered by a synthetic flag in the view (only sensor rows are), that a shared-password holder can still distinguish listed from unlisted emails, that limiter counters are in memory with no `Retry-After` on 429, that logout and restart revoke tokens, that the Origin check compares the authority to Host, that an optional local agenda and chat log can write, and that email normalisation can fold Unicode into an accepted value. The corrected wording is in the [threat model](../../../docs/reference/research/resident-demo-threat-model-2026-11-16.md); the original rows are kept here as written.

### F4 Validation capabilities (criterion 3)

* Docker is available locally (`docker ps` works), so a SQL Server container, `Dockerfile.resident-demo` non-root startup and Chromium journeys can be attempted. They have not been run yet; results go into the changes artifact.
* The full gate is `python3 tools/rpi-checks.py --all --base <sha> --out <dir>` then `--verify-receipt`. It needs a clean committed tree and original RPI evidence.
* The worktree is clean at 5e0c7f744 on `feat/resident-demo-rpi-gate-462`.

### F5 Risks to the plan

* Evidence must be committed before the gate and any later commit invalidates the receipt. The review and state files are therefore finalised and committed before the gate; the receipt stays external.
* Hosted CI, human approval and coordinator assessment cannot be claimed from a local candidate.
* Missing Docker, SQL image pull or Chromium blocks publication (never a cloud fallback).

## Planning Readiness

Ready. Scope: (1) a durable threat-model document linked from `src/api/README.md` and the knowledge-base index and log; (2) execution of every local check named in the issue, with recorded results; (3) single-pass critique and review; (4) full gate with external receipt.

## Follow-ups (provisional)

* Owner pre-spend approval and cloud deployment (criteria 6 and 7).
* Hosted checks and coordinator assessment of the exact head.
* Human accessibility, copy and DPO review.
