<!-- markdownlint-disable-file -->

# Task Research: climate-paired-alt-source-178-attribution-corr2

| Field | Value |
| --- | --- |
| Date | 2026-10-22 |
| Researcher / agent | rpi-research, inline |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-22/climate-paired-alt-source-178-attribution-corr2-research.md |

## Research Brief

* What: establish how retained NASA POWER API identity/version reaches the generated report.
* Why: independent published-head review found the non-precise `2.x.x` attribution.
* Audience: correction implementer and independent reviewer of #178 / draft PR #425.
* Scope: adapter, focused tests, generated report and directly related evidence.
* Non-goals: licence/reuse approval, malformed-input changes, station-grade accuracy, issue acceptance, merge.
* Criteria: precise source-bound provenance or explicit unverified status; reproducibility; existing decisions preserved.
* Requested outputs: dated research, plan, implementation and Review artifacts for this distinct correction.
* Output mode: convergence.

## Research Parameters

* Posture: focused (bounded supplied defect and fixture).
* Internal candidates: tools/climate_paired_bounds.py, tools/test_climate_paired_bounds.py, retained sample/report and prior RPI artifacts.
* External scope: read-only PR context; no fresh climate/licence research needed.
* Evidence root: .copilot-tracking/.
* Research is read-only except this artifact and required workflow state.
* Publication constraint: wait for /tmp/ama-rpi-heavy.lock, then exact-head/current-origin-main gate and official verifier before push.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instructions | Repository AMA instructions, all paths | Selected: branch/privacy, evidence, local-gate boundaries |
| Skill | rpi-research | Selected: ordered wider/deeper/contrarian cycle |
| Specialist | hve-core-all:rpi-researcher | Skipped: one tightly coupled trace, inline investigation |
| Domain | Web/design/legal skills | Skipped: no web UI or legal determination |

## User Participation and Research Decisions

Explicit user request authorizes this complete ordered loop and later gated commit/push.
Non-interactive execution needs no routine phase questions. Preserve prior task states rather than rewrite them.

## Direction Controls

* Retain branch feat/paired-climate-source-178 and draft/open PR #425; clean intake.
* Published and local head at intake: 09f2127ef3c068fc619e8ae2afd112731b80e7a0.
* Keep #178 open with every acceptance criterion unchanged.
* Licence/reuse and owner/legal decisions remain UNMET; production precision remains pending.
* No modifications outside this worktree, no force-push, no merge.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Where is provenance lost between raw fixture and report? | Straightforward | Open |
| Q2 | How can source-specific precision be tested without changing malformed-input behavior? | Depth | Open |
| Q3 | What existing decisions and publication constraints must remain? | Straightforward | Answered by intake and prior artifacts |

## Prior Knowledge Gate

Read the original case study, addendum opening/exercise boundaries, knowledge-base index opening,
memory, parent alternative-source Research, corr1 state and Review.
Parent research already records NASA v2.10.3 and explicitly unverified licence;
corr1 preserves outstanding licence, precision and representativeness work.
No prior artifact is superseded by an attribution-only correction.

## Research Cycle Log

### Cycle 1, Wave 1: Wider

Inspected the complete adapter and tests, report metadata, raw header, synthesis regeneration
command and local gate contract. Inline investigation was appropriate for this coupled trace.
Reflection: the defect is not missing evidence: parse_power discards header.api and
build_report uses a static attribution dictionary. Correcting only committed JSON would
leave regeneration wrong.

### Cycle 1, Wave 2: Deeper

Read the retained header using JSON parsing: api.name is `POWER Hourly API`, api.version
is `v2.10.3`; both derive from the same existing hash-pinned bytes as the data.
The report already carries retrieved_on `2026-10-22`, URL, byte count and SHA-256.
Reflection: carry source name/version alongside those fields and generate attribution
from each parsed series, including its retrieval date. Do not hardcode v2.10.3 as a default.

### Cycle 1, Wave 3: Contrarian

Existing synthetic POWER payloads have no api block, and the parser previously ignores it.
Making api mandatory or applying _object to it would expand malformed-input rejection.
Missing, non-object, incomplete, non-string or imprecise metadata must instead produce
explicit UNVERIFIED provenance without altering climate validation. A dotted numeric
major.minor.patch version, with optional leading v, is sufficient for this fixture;
unrecognised forms remain unverified rather than guessed. Report construction must not
mutate the module-level licence dictionary or leak one source's attribution into another.
Reflection: test distinct constructed versions/dates, absence and malformed optional metadata,
and the real fixture, not only a self-consistent report regeneration.

### Parent Synthesis and Disposition

* Accepted (C3-C6): carry optional source API identity/version and render per-report attribution.
* Rejected (C3-C5): JSON-only edit, hardcoded precise version, mandatory API metadata, inferred reuse approval.
* Deferred (C1-C2): licence/reuse, owner/legal determination, production accuracy and representativeness.
* Re-entry: no further cycle needed; source and dataflow answer Q1-Q3 within scope.

## Evidence Log

| ID | Evidence | Location |
| --- | --- | --- |
| C1 | Parent distinguishes NASA cross-check metadata from unverified reuse | .copilot-tracking/research/2026-10-22/climate-paired-alt-source-178-research.md:70 |
| C2 | Prior Review leaves original residuals unchanged | .copilot-tracking/reviews/logs/2026-10-22/climate-paired-alt-source-178-corr1-review.md:1 |
| C3 | Static wildcard attribution and static report binding | tools/climate_paired_bounds.py:42; tools/climate_paired_bounds.py:328 |
| C4 | POWER parser validates data but drops header.api | tools/climate_paired_bounds.py:171-223 |
| C5 | Retained precise API name/version | docs/reference/research/climate-paired-sample-178/nasa-power-merra2-durham-2023-raw.json:1 (JSON header.api) |
| C6 | Existing hash-pinned full-report regeneration test | tools/test_climate_paired_bounds.py:292-317 |
| C7 | Current-base/exact-head local gate and official verifier contract | src/README.md:49-105 |

All codebase evidence was directly read; confidence High. No fresh external claim.

## Findings, Alternatives and Decisions

Q1 answered by C3-C5: static text replaces retained metadata.
Q2 answered by C4-C6: optional provenance with explicit UNVERIFIED output preserves data rejection.
Q3 answered by C1-C2/C7 and the user direction: no acceptance or human/legal approval changes.
Selected approach is dynamic source-bound attribution, not a static typo correction.
Existing raw fixtures and statistical outputs must remain byte-identical/structurally equal.
Open questions: no correction-specific evidence gap; original external approval gaps remain.

## Planning Readiness

Ready (C3-C7). Research disposition: executed.
Self-check: ordered waves completed, questions answered, alternatives and limits recorded.
Parent-owned next action: Plan, then one independent critique, Implement, one independent Review.
