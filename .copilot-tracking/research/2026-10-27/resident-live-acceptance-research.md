<!-- markdownlint-disable-file -->
# Task Research: resident-live-acceptance

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/resident-live-acceptance-research.md |

## Research Brief

### Superseding owner direction, 2026-10-27 10:37Z

The original cycle below is historical. The owner now explicitly requires a
declarative Bicep deployment, ingress left open for next month's demonstration,
expiresAt 2026-12-31T23:59:00Z, and a single authority cap of
2026-12-31T23:59:59Z inclusive. No closure watchdog. Preserve min0/max1,
1000-mapping admission, startup expiry refusal and all protected workloads.
Research re-entry is required because the prior no-source-change recommendation
and October closure plan are superseded. The user authorizes the ordered full
loop, this deployment and PR; existing untracked task artifacts are retained and
integrated, never discarded, stashed or relocated.

Cycle 2 opening: focused convergence on expiry cap propagation, Bicep deployment,
immutable image delivery and safe browser harness limitations. No secret reads.
Existing shared password remains owner-held; a local fixture harness is not
authenticated live acceptance.

Restore the existing isolated synthetic resident site for owner feedback and
prove live authenticated acceptance left unmet by PR #478. Audience: owner and
independent reviewer. Output mode: convergence, preparing the requested full
Research, Plan, Implement, Review loop. Scope: existing revision, public ingress,
resident login/isolation/session/browser acceptance, issue criteria and costs.
No employee, SQL sizing, other workload, identity/RBAC or model changes.

## Research Parameters

Focused posture, selected for the supplied bounded deployment and named evidence.
Evidence root: `.copilot-tracking/`. Research is read-only except this artifact
and required lifecycle tracking. Starting candidates: PR #478, #462/#466,
resident API/startup/browser checks, infra deployment guard and prior cost ledger.
External scope: GitHub and existing Azure resource metadata, no secrets or .env.
USD30 additional inside renewed USD700 cap through 2026-12-31; resident exposure
ends 2026-10-31T23:59Z. Heavy work requires timeout-zero shared lock; scoped
`--changed` receipt explicitly requested, never represented as a full gate.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | Repository instructions, all paths | Selected: branch, evidence, approval, privacy and publication boundaries |
| Skill | rpi-research | Selected: ordered three-wave focused research |
| Skill | web-design-guidelines | Select if web files change or a UI review is performed |
| Specialist | RPI researcher | Skipped: one tightly coupled bounded trace handled inline |

## User Participation and Research Decisions

Owner explicitly requested the complete ordered loop, deployment, leaving
ingress open, browser acceptance, commits and PR. This authorizes progression
and the named externally visible actions; no inferred broader authority.
Non-interactive execution: resolve ordinary details from evidence.

## Direction Controls

Preserve PR #478 evidence without copying or rewriting it. The prepared clean
worktree is already `issue-resident-live`, branch `chore/resident-live-acceptance`,
at latest fetched main `885ee05fc45122cf7a1ea4f7f003dc88bfda08ee`.
PR #478 remains open; its source deployment was already merged by #474.
Reference its unmerged evidence by immutable GitHub commit links, not duplicate
the evidence branch into this independent main-based branch.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | Can the tested revision be safely restored with bounded costs and expiry? | Answered |
| Q2 | What login/session mechanism permits positive proof without reading secrets? | Blocked |
| Q3 | Which complete issue criteria can actual evidence prove? | Answered |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index and owner memory. PR #478 explicitly
records ingress disabled, revision inactive and positive authentication/expiry
unproved. The current request supersedes its test-only exposure direction.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspect issue/PR lifecycle, source acceptance contracts, safe resource metadata,
cost/expiry evidence and supplied approval provenance. Inline investigation.
Reflection: deployed source is already main; prior evidence PR need not be
duplicated. Password-free testability is not yet established.

#### Wave 2: Deeper

The inactive tested revision is present with min0/max1 and the exact prior digest.
Safe environment readback confirms expiry 2026-10-31T23:59Z and exact allowed
hostname. All four apps have min0; all eight jobs are Manual; SQL retrofit remains
Standard/10 DTU. No deployment template rerun is necessary.

The actual source requires BOTH an admitted example.com email and the owner-held
shared password (C2/C3). No passwordless demo route or short-expiry configuration
exists. Session lifetime is 1800 seconds, process-bound. Real session expiry
cannot be proved with a forged token or browser clock manipulation.

Reflection: restore existing access without changing credentials or weakening
authentication. Positive browser criteria require an owner-held credential not
available to this session under the explicit no-secret-read instruction.

#### Wave 3: Contrarian

Challenge: "any resident email signs in" does not mean arbitrary unregistered
email or passwordless authentication. Unknown/ambiguous mappings must still deny.
Do not silently remove the password, rotate owner credentials, sign fabricated
sessions, invoke internal login bypasses, shorten shared expiry or call anonymous
markup authenticated acceptance.

Fresh actual-cost query reports ama month-to-date USD315.535491423131 (W3),
not the older USD309.49076053371493 ledger baseline. Billing is delayed.
At 0.25 vCPU/0.5 GiB and retained rates, one continuously active revision from
2026-10-27T10:35Z through expiry costs approximately USD4.13412, before requests,
logs/egress/other baseline costs. Reserve USD5 for this feedback window; prior
release USD1 and model USD20 remain reserved, leaving USD4 contingency inside
USD30, not a second USD30. Min0 is not a zero-cost or hard-budget guarantee.

Application expiry prevents resident serving at the next request and refuses
startup; it does not itself remove ARM ingress. Preserve all eight Manual jobs
and add no scheduler. Record exact close/deactivate commands for the expiry
operator; do not claim an automatic ingress shutdown exists.

Reflection: scoped restoration is ready. Full live acceptance remains explicitly
blocked by credential custody, not an excuse to leave owner access unavailable.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Reactivate tested revision only | W1/C4 | Accepted | No build, migration, role or secret mutation needed |
| Password-free positive proof | C2/C3 | Rejected | No such supported route; bypass changes the tested boundary |
| Forged token proves expiry | C3 | Rejected | Signature denial is not genuine expiry |
| Continuous public service past expiry | C3/C4 | Rejected | Application expiry remains fixed; ARM closure requires operator |
| Complete #462 by ticking partial criteria | W2 | Rejected | Composite requirements remain composite |

#### Cycle Re-entry Evaluation

No additional cycle needed: source and live metadata settle restoration.
No research can supply the owner-held credential under the no-read boundary.
Missing positive evidence is retained as a blocker rather than invented.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| W1 | Prior deployment not accepted; public URL intentionally 404 | https://github.com/jmservera/ama/pull/478, retrieved 2026-10-27 |
| W2 | Composite criteria must not be ticked from root200 or partial proofs | https://github.com/jmservera/ama/issues/462, retrieved 2026-10-27 |
| C1 | Partial scoped gate is supported but is not full-tier evidence | src/README.md:53 |
| C2 | Login requires password verification plus server-owned admitted mapping | src/api/src/zava_forward/api/resident_demo/app.py:119; src/core/src/zava_forward/core/resident_showcase.py:369 |
| C3 | Fixed 1800s session; MAC/nonce and authority expiry checked server-side | src/core/src/zava_forward/core/resident_showcase.py:35; src/core/src/zava_forward/core/resident_showcase.py:380; src/api/src/zava_forward/api/resident_demo/app.py:245 |
| C4 | Startup enforces admission map, fails above 1000 mappings | src/core/src/zava_forward/core/resident_showcase.py:267; src/api/src/zava_forward/api/resident_demo/__main__.py:21 |
| W3 | Current ama month-to-date ActualCost USD315.535491423131 | Azure CostManagement query API 2023-11-01, resource-group scope, retrieved 2026-10-27 |
| W4 | Inactive tested revision exists; exact expiry, scale and preserved workloads verified | Azure Container Apps/SQL management-plane readbacks 2026-10-27 |

## Threat Boundary

Public fake emails and a shared password provide demonstration isolation, not
real identity. A known shared password plus another admitted email permits that
synthetic account by design. Client selectors must not choose another case.
Only the existing allowlisted SQL view may supply resident-safe fields.
No staff data, real identities, case writes or model calls are admitted.
MAC-protected process-bound sessions, HTTPS-only cookies, CSRF, same-origin
checks, abuse limits and no-store headers remain unmodified. Test negatives
without exhausting the owner's shared source login limit.

## Findings, Alternatives and Current Decisions

Q1 ready: reactivate exact prior revision, enable HTTPS-only ingress, retain
min0/max1 and all protected resources. Q2 blocked: never read existing secrets,
rotate credentials or weaken password verification to obtain a test pass.
Q3: run all safe real-browser checks; record authenticated paths Not run with
the precise blocker. Tick no composite criterion unless every clause is proven.
Rebuild and passwordless changes are rejected as unnecessary/out of scope.

## Open Questions, Risks and Further Research

Owner must complete credential-bearing positive login/isolation/logout/natural
expiry using the existing secure custody route. No new secrets retrieval is
authorized. No new model work; deterministic provider is acceptable here.
ARM ingress closure at expiry remains an explicit operator responsibility.
Reported spend is delayed and not an invoice or hard cap.

## Alternatives and Decision State

Prefer reactivation of immutable tested revision if auth and expiry remain valid.
Rebuild only if positive login cannot be achieved safely under explicit direction.
Do not retrieve the shared credential to manufacture acceptance.

## Planning Readiness

Ready for scoped access restoration and available acceptance. Full authenticated
acceptance blocked as above. Research disposition: executed.
Self-check: three ordered inline waves, evidence IDs, alternatives, threats,
direction controls, unresolved evidence and planning handoff recorded.

## Cycle 2: Superseding December Declarative Direction

Wider: C5 `infra/resident-demo.bicep:28` and
`infra/scripts/resident_demo_secrets.py:47` independently cap October authority;
C6 `src/core/src/zava_forward/core/resident_showcase.py:31,588` also caps the
image runtime, identity admission and sessions. Reusing the old image with a
December environment value will refuse startup. Reflection: rebuild is required,
not an ingress script toggle.

Deeper: C7 `src/core/pyproject.toml:87` already packages `policies/*.json`.
Use one packaged JSON expiry value read by Python and Bicep loadJsonContent;
secret/deploy helpers reuse the core authority constant. Existing exact-host,
future UTC, min0/max1 and 1000-mapping checks stay intact. The optional model
provider has a distinct October spend authority; do not renew model authority.
The prior release harness executes real anonymous Chromium checks but has no
positive password-free login (`live-check.py` in retained external release
evidence). Reuse its test approach, not its obsolete closure/watchdog operations.

Contrarian: C8 `infra/sql/resident-showcase.sql:21` independently limits database
allowlist validity to November1. Existing authorizations and secret metadata may
expire before December even when the new app remains reachable. The owner says
preserve SQL and never read secrets. Do not silently extend database row grants,
rotate secrets or misrepresent next-month authenticated readiness. Record that
operational dependency explicitly. Continuous maximum compute through December
could exceed USD30; scale-to-zero and owner cost monitoring, not max1 alone,
are necessary. No paid model calls in this task.

Live observation W5: at this resumed execution the URL already returns200,
revision0000002 is active, external ingress=true, min0/max1. Attribution of that
change is unavailable; do not claim this execution reopened it.

Synthesis: accept declarative December cap, immutable rebuilt image and Bicep
deployment after targeted checks. Reject password/session bypasses, secret reads,
and incidental SQL mutations. Defer authenticated positive live acceptance and
renewal of underlying SQL/secret validity to owner-authorized custody. This
research re-entry is complete; no further inline cycle can remove those custody
boundaries. Research disposition executed; Planning Readiness Ready for scoped
implementation, full live acceptance still blocked.
