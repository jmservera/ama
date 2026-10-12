---
title: Public Workbench Welcome and Entra Account Menu Research
description: Evidence for explicit sign-in, protected workbench access, own-user photo and credential-free tenant provisioning
ms.date: 2026-10-12
---

<!-- markdownlint-disable-file -->

## Research Brief

* Topic: Public branded welcome, explicit sign-in, Entra account photo/menu
  and a clear explanation of the isolated tenant provisioning profile.
* Purpose: Prepare a secure, evidence-based implementation of the owner's
  requested UX without weakening workbench authorization.
* Audience: Owner, implementation and acceptance review.
* Scope: mvp/web, MVP auth/server/projection, Container Apps auth configuration,
  related initialization/creation guidance and targeted tests.
* Non-goals: Collecting passwords or tokens, replacing the registration,
  granting broad Graph application permissions, revisiting the reset Review,
  changing resident workflows or treating owner-reported sign-in as assistant
  browser acceptance.
* Criteria: Anonymous root shows only public branding; workbench/API remain
  protected; user explicitly enters; real own-user photo has an evidenced,
  least-privilege source; account switching and logout have safe return paths.
* Requested output: Converged approach, implementation-ready evidence and
  remaining authority/consent gates.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Posture | Focused; bounded owner UX request with named existing app |
| Internal candidates | mvp/web/index.html, app.js, style.css; auth.py, server.py, projection.py; infra/modules/containerapps.bicep; registration/initializer scripts |
| External candidates | Official Container Apps authentication docs/schema, Entra account selection and Microsoft Graph profile-photo documentation |
| Limits/deadline | None supplied |
| Resolved evidence root | .copilot-tracking/research/2026-10-12 |
| Source edits during research | None |

## Extension Registry and Provenance

| Extension | Disposition | Boundary |
| --- | --- | --- |
| Repository instructions | Selected | Preserve original case/history and private local files; use existing active topic/PR and privacy-safe publication |
| rpi-research | Selected | Ordered Wider, Deeper and Contrarian evidence cycle; research/state writes only |
| accessibility | Relevant | Keyboard-operable public sign-in and account menu, photo alternatives and visible focus |
| Microsoft Learn | Selected source | Verify current cloud/auth/Graph contracts from official documentation |
| Context7 | Relevant source | Use if a concrete library/SDK contract requires it |
| Research/UX specialists | Skipped for now | This is one tightly coupled, bounded auth/UI trace; direct investigation suffices |

## User Participation and Direction Controls

* Owner reports workbench sign-in works. Preserve that report and do not
  continue describing it as a confirmed broken sign-in.
* Owner asks for a branded anonymous entry screen and sign-in only on entering
  the platform, plus Entra photo with sign-out/change-profile actions.
* Owner asks whether provisioning requires a username/password. It does not:
  an isolated CLI session uses normal Microsoft sign-in/MFA and appropriate
  directory authority, separate from the deployment identity.
* RPI session mode is currently manual. Automatic continuation requires an
  explicit mode choice; no password or token will be requested.

## Research Questions

| Question | Priority | Status |
| --- | --- | --- |
| Q1: Exact anonymous path exemptions and protected app entry? | High | Open |
| Q2: Own-user photo under Container Apps auth, delegated permission and token availability? | High | Open |
| Q3: Reliable account chooser and safe logout/return routing? | High | Open |
| Q4: Explain provisioning profile and authority without credentials disclosure? | High | Partly answered |

## Prior Knowledge Gate

* Existing initializer, child Review and owner report establish that runtime
  sign-in and tenant administration are different concerns.
* Active #65 remains open. Its latest upstream addition is the automated rubric
  record e418aae; current working tree was clean at intake.
* Existing auth requires tenant, app role and provisioned staff identity.
  These requirements remain invariant.

## Research Cycle Log

### Cycle 1

#### Wider

* Candidate mechanisms: Separate public welcome and protected app route;
  exact static exemptions; delegated Graph own-photo retrieval through
  documented platform tokens; normal provider account-selection/logout flow.
* Initial code evidence: Current root is a workbench page, and ingress excludes
  only probes, so opening it immediately redirects to Entra. Current header
  has text identity and a sign-out button; there is no photo/menu implementation.
* Reflection: Landing separation is straightforward; photo token availability
  and account selection need official verification before selecting a design.

#### Deeper

* Official Container Apps docs confirm exact excluded-path control,
  post-login/logout relative redirects, and platform-injected access tokens
  only when token store is enabled (W1).
* The existing auth configuration has no token store or extra login parameters.
  A photo cannot be truthfully sourced from a nonexistent picture claim.
* Token store requires a private Blob container and a SAS secret (W2/W3).
  The chosen design retains identity-only storage access: a narrowly scoped
  managed-identity maintenance job renews a user-delegation SAS before its
  seven-day maximum, stores it in Key Vault and leaves account keys disabled.
* Graph supports delegated User.Read for /me/photo/$value (W4). Use only that
  own-user endpoint, never caller-selected users or broad application grants.
  No photo is normal 404; missing tokens, consent/network failures are explicit.
* Static prompt=select_account in provider loginParameters makes fresh sign-in
  after app logout an account chooser. Logout returns to root or public
  /sign-in; no caller-controlled return URL is accepted.
* Reflection: The landing and menu are small UI changes; real photo support
  additionally needs supported token storage and credential lifecycle.

#### Contrarian

* Rejected ID-token picture-claim assumption: the platform supplies claims,
  not a guaranteed usable Microsoft photo URL.
* Rejected Graph app-only ProfilePhoto.Read.All: it grants tenant-wide photo
  access unnecessarily and requires external admin consent.
* Rejected enabling shared account keys or a one-off expiring token-store SAS:
  these weaken existing storage controls or risk a future sign-in outage.
* Rejected opening all paths/AllowAnonymous: retain middleware protection on
  workbench/API and exempt only landing, its two public assets, /sign-in and
  the existing probes.
* Rejected token retrieval through browser /.auth/me: use a server-side own
  photo proxy; keep Graph tokens out of UI payloads/logs and block redirects.
* Reflection: A renewable user-delegation SAS and separate private auth
  storage are necessary supporting infrastructure, not delivered agent work.
  Actual new-session consent/photo remains a human acceptance boundary.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | infra/modules/containerapps.bicep:169-190 | Current exclusions are probes only; login/token-store configuration absent |
| C2 | mvp/zavaforward_mvp/auth.py:108-151 | Tenant/role/staff requirements must remain intact |
| C3 | mvp/web/app.js:41-74 | Current UI has local password fallback and text identity, not public welcome or account photo |
| C4 | infra/scripts/initialize-api-auth.py:55-79 | Isolated device-code profile is administrative, not a shared password |
| W1 | https://learn.microsoft.com/en-us/azure/container-apps/authentication (retrieved 2026-10-12) | Excluded paths, return routes, trusted headers and required token store |
| W2 | https://learn.microsoft.com/en-us/azure/container-apps/token-store (retrieved 2026-10-12) | Private Blob token store and read/write/delete SAS; expiry must be managed |
| W3 | https://learn.microsoft.com/en-us/azure/templates/microsoft.app/2025-07-01/containerapps/authconfigs (retrieved 2026-10-12) | loginParameters and azureBlobStorage.sasUrlSettingName schema |
| W4 | https://learn.microsoft.com/en-us/graph/api/profilephoto-get?view=graph-rest-1.0 (retrieved 2026-10-12) | Delegated User.Read supported; own-user photo binary and no-photo 404 |
| W5 | https://learn.microsoft.com/en-us/azure/app-service/configure-authentication-oauth-tokens (retrieved 2026-10-12) | Token header, offline_access and supported auth refresh; Container Apps explicitly links this token contract |

## Findings and Decision State

Selected: public static root and exact asset exemptions; protected /app;
explicit /sign-in; native keyboard-accessible account details with own Entra
photo fetched server-side and transparent initials/status when unavailable;
safe app logout/chooser; private token-only storage with a daily maintenance
job renewing a five-day user-delegation SAS, Key Vault secret and staged
activation. No passwords/tokens requested, no tenant-wide Graph grant and
no existing evidence-storage key relaxation.

The owner explicitly asks for autonomous completion. That confirms the earlier
offered automatic-mode choice for this child; phases may advance after their
gates, without repeating the blocked parent Review.

## Planning Readiness

* Status: Ready.
* Research disposition: Executed; all three waves complete.
* Remaining acceptance: Fresh user sign-in/consent and the actual user photo
  cannot be fabricated. Inspect/record any tenant-policy restriction when
  encountered, without broadening privileges.
* Self-check: One bounded auth/UI trace, authoritative current schema and photo
  sources, contrarian risks addressed; source writes not performed in Research.
