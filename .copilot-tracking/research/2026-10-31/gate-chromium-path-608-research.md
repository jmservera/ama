<!-- markdownlint-disable-file -->

# Task Research: gate-chromium-path-608

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/gate-chromium-path-608-research.md |

## Research Brief

* What to research: #608 Chromium singleton pathname failure and gate admission.
* Why it matters: prevent expensive, predictably failing full local runs.
* Audience or intended use: tooling maintainers, implementation and independent review.
* Scope: tools/rpi-checks.py, tools/test_rpi_checks.py, associated gate documentation.
* Non-goals: application changes, scanner changes, workflow changes, browser/SQL skips, partial receipts.
* Criteria: actionable preflight bound or legitimately owned short scratch; preserve ownership, privacy, cleanup, source and receipt boundaries.
* Requested outputs: evidence-backed recommendation and full dated RPI loop.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Where is TMPDIR set; what bound admits Chromium; how to test before checks? |
| Codebase scope | Gate tooling and directly related documentation |
| External scope | Chromium singleton implementation if needed |
| Initial internal candidate areas | Output admission, scratch setup, receipt verification, tooling tests |
| Initial external candidate areas | Chromium POSIX singleton source |
| Research posture | focused |
| Posture provenance | Named failure and bounded caller task |
| Explicit limits | Focused unittest and ruff only; CI is the gate; no heavy-lock full run |
| Completion basis | Scope coverage and evidence sufficient to choose a safe fix |
| Edits allowed during research | Research evidence and required workflow state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | Repository custom instructions | All inputs | Boundaries, artifacts, privacy-safe commits | Selected; explicit focused validation overrides heavy local publication gate |
| Skill | rpi-research | Full-loop request | Three-wave evidence | Selected |
| Specialist | RPI Researcher | Registered | Independent research lanes | Skipped: one tightly coupled trace, handled inline |
| Skill | Web design skills | No web edits | Web surfaces only | Skipped |

## User Participation and Research Decisions

User explicitly requests the entire loop and push/PR in a non-interactive run.
This is automatic intake, not an inferred manual-to-automatic switch.
No additional questions are needed; either proposed fix is authorized.

## Direction Controls

* Preserve browser/SQL, scanner, receipt and source boundaries.
* No workflow edits unless necessary; change hash pins only with workflow edits.
* Focused validation; criterion 3 requires a later actual full run. Use Refs #608.

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | How does output admission establish ownership and browser TMPDIR? | depth | High | Open |
| Q2 | Can pathname admission reject incompatibility with a defensible byte bound? | depth | High | Open |
| Q3 | What tests preserve cleanup, receipt and source contracts? | straightforward | High | Open |

## Prior Knowledge Gate

Issue read with `gh issue view 608`; its reported SIGABRT is supplied evidence,
not independently reproduced. Clean worktree on requested topic branch,
no matching open PR, starting commit 87bf629c. Required project documents,
knowledge-base index, memory and housing primer read for context.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline inventory traced CLI admission, Runner environment, browser entry wrapper,
cleanup, receipt verification, and existing tests (C1-C4). No independent lane
was needed. Reflection: gate owns TMPDIR under output, so changing ambient
TMPDIR cannot fix this; output admission is the smallest relevant surface.

#### Wave 2: Deeper

Prioritized exact socket suffix and pre-allocation admission. Chromium creates
an owned temporary singleton directory with a six-character random component
under TMPDIR, then appends SingletonSocket (W1-W2). Linux sun_path is 108 bytes;
Chromium requires a NUL terminator (W1, W3). The suffix is 45 bytes, so TMPDIR
must be at most 62 bytes, and output plus `/tmp` requires output <=58 bytes.
Reflection: measure filesystem-encoded bytes, not Python character count, and
resolve CLI paths before checking. Admit before tool probes, locking or writes.

#### Wave 3: Contrarian

Challenged rejection against owned short scratch: the latter could support long
outputs but introduces independent allocation/cleanup and environment identity
work, unnecessary for the caller-authorized rejection alternative (C2-C4).
Challenged blanket rejection: browser-free changed selections do not need this
bound, so gate admission should be selection-aware. Resume may reuse preflight;
checking CLI plus Runner construction prevents bypass. Unicode and symlink
aliases must use resolved filesystem byte length. Reflection: retain existing
output ownership and receipt semantics rather than relocating scratch.

#### Parent Synthesis and Disposition

* Accepted: early selection-aware output pathname rejection with <=58-byte
  resolved output bound (C1-C4, W1-W3).
* Rejected: new independent short scratch; added lifecycle risk without need.
* Deferred: actual browser/SQL full gate, explicitly excluded from this run.
* Re-entry: no additional cycle needed; all design questions have evidence.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | CLI resolves output and enforces new external directory before mkdir/lock | tools/rpi-checks.py:2403 | High |
| C2 | Runner sets TMPDIR to output/tmp and browser wrapper pins temporary directories there | tools/rpi-checks.py:1175, tools/rpi-checks.py:130 | High |
| C3 | Journey persistent Chromium launches extension/profile in temporary scratch | src/api/checks/case_journey_browser_check.py:1535 | High |
| C4 | Cleanup retains dirty owned snapshots; schema-4 receipts bind sources, tools and required groups | tools/rpi-checks.py:1931, tools/rpi-checks.py:2208 | High |
| C5 | Tools tests use temporary Git fixture and mocked CLI dispatch; browser/SQL prerequisite tests already exist | tools/test_rpi_checks.py:498, tools/test_rpi_checks.py:890, tools/test_rpi_checks.py:1541 | High |
| C6 | Focused tooling is owner policy; hosted CI remains required | src/README.md:62 | High |

| ID | External source | URL | Retrieved | Confidence |
| --- | --- | --- | --- | --- |
| W1 | Chromium POSIX singleton, lines 284-289 and 1045-1063 | https://chromium.googlesource.com/chromium/src/+/main/chrome/browser/process_singleton_posix.cc | 2026-10-31 | High |
| W2 | Chromium POSIX temporary naming, lines 127-129 and 1166-1173 | https://chromium.googlesource.com/chromium/src/+/main/base/files/file_util_posix.cc | 2026-10-31 | High |
| W3 | Linux unix(7), sockaddr_un sun_path[108] | https://man7.org/linux/man-pages/man7/unix.7.html | 2026-10-31 | High |

Sources were read through bounded curl/decode and HTML retrieval. Upstream main
is mutable; reported Chromium 156 failure has the same pathname shape.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Status |
| --- | --- | --- | --- |
| Q1 | Output owns TMPDIR; no alternate allocation required | C1-C4 | Answered |
| Q2 | 107-byte socket path maximum minus 45-byte suffix minus /tmp =58 output bytes | W1-W3 | Answered |
| Q3 | CLI rejection before writes/probes plus Runner backstop, exact boundary/Unicode/symlink tests and unchanged receipt/cleanup tests | C1, C4-C5 | Answered |

## Alternatives and Decision State

Selected: reject browser-containing selections exceeding the bound. Actionable
error must state measured output and TMPDIR byte lengths, bounds, owned path
derivation, and a short new external output example. No skip switch or receipt
is introduced. Browser-free selection continues to permit long output paths.

Alternative: short separate owned scratch. Rejected because safe allocation,
cleanup and receipt/environment representation would widen the change (C2-C4).

## Risks and Residual Uncertainty

* Actual full browser and SQL execution remains unproven (issue criterion 3).
* Chromium temporary naming can change in a future version; constants, explicit
  formula and tests make the current supported Linux bound maintainable.
* No application or regulatory claim changes.

## Planning Readiness

Ready. Research disposition executed. C1-C6 and W1-W3 support a complete bounded
plan; no implementation blocker. Automatic RPI parent continues to Plan.

## Artifact Self-check and Closeout

All three waves completed inline in order; questions answered, alternatives
preserved, evidence IDs and locations recorded, exclusions preserved. No
source edits performed during Research. No further research selected.
