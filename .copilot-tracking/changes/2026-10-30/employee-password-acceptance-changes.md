---
title: Employee password acceptance changes
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

Task ID: employee-password-acceptance-2026-10-30.
Declared scope: complete child plan; original parent evidence preserved.

## Implementation Opening

Plan and phase details are Ready after the one original Revise critique;
PC-001..005 applied directly. Implement P01 safe employee-only runner and
constructed offline tests first, then bounded live execution. P02 records every
criterion, one independent Review and a local Refs-only commit/gate attempt.
No application, Azure resource/policy/role/roster change or resident retry.

## Current Status

P01-T01 complete: separate employee-only runner and 11 constructed offline
tests pass; Ruff check and formatting pass. P01-T02 complete as a bounded
blocked attempt. P02-T01 matrix/checks and one independent Review complete.
P02-T02 local commit and external gate attempt remain pending.
Default Python lacked Playwright; restored in task-owned external virtual
environment `/tmp/ama-employee-accept-6d309f30-venv`, Chromium install succeeded.
No credential file was read during research, planning or critique.

## Plan Maintenance

PC-004 capture-safety correction applied with zero screenshots and no raw
authenticated text/answer/record retention. Its proposed synthetic-evidence
gate before any interaction is rejected against explicit owner authorization
to exercise this exact demo UI, not treated as an unresolved decision.
Synthetic record provenance remains unknown. No source or old runner edits.

## Initial Live Attempt and In-Phase Correction

`employee-102251-940125-evidence.json` is preserved adverse evidence, bound to
its own executed script hash. Its `password_submitted=true` is disqualified as
password-authentication proof: an autofill password input was considered
visible on the username page; Next was pressed with username still absent.
The offered page explicitly said "Enter a valid email address, phone number,
or Skype name." This is not a rejected-password diagnosis or a successful
password-route observation. No capture was enabled or secret output emitted.

Corrected the runner before Review: username Next always precedes password
handling; password filling requires the actual visible password heading and
Sign in submit, not merely a visible password input. Added a constructed
decoy-field regression; all 11 offline tests and Ruff pass. This is a local
automation correction preserving the approved single actual password-submit
boundary, not a tenant change or a response to an independent Review.
Do not attribute current runner bytes to this earlier run.

The corrected `employee-102404-659893-evidence.json` reached a logo-only
login.microsoft.com interstitial after submitting username, with no loaded
challenge controls. Its `password_route_not_offered` classification is
inconclusive, not proof that the passkey alternatives were exhausted.
Corrected the in-phase readiness wait to require a visible meaningful auth
heading/control rather than observing a fixed 1.5-second redirect shell.
Retain this intermediate run and hash; only a fully rendered challenge can
satisfy the owner's no-password-route stop. No password was submitted.

`employee-102432-233346-evidence.json` reached the real passkey challenge
("Face, fingerprint, PIN or security key") and offered Back only. Mouse
activation of Back timed out; no password was submitted. In-phase correction:
activate the visible Back/options controls by Enter, the ordinary keyboard
method used in the original evidence. This failed activation does not prove
the alternatives are unavailable. All intermediate adverse files remain.

## Definitive Employee Outcome

Evidence E1:
`.copilot-tracking/changes/2026-10-30/employee-password-acceptance/employee-102500-185604-evidence.json`.
Run: 2026-10-30 10:25:00-10:25:07 UTC, Chromium 156.0.8078.4.
Exact executed script SHA-256:
`dd3f27b501ec3fb232bb1d138ef7b827a6889b664e107d623ca194ebe3832ffb`.
The sibling uniquely named manifest binds the evidence bytes and script hash.

Actual path: employee /app -> Entra username Next -> passkey challenge ->
Escape -> keyboard Back -> Sign-in options. Credential parsing succeeded
inside automation, including trimmed first-line support; password validity
was not tested because no actual password-entry route was offered.

Exact offered passkey text, with the supplied identity replaced:

```text
[redacted]
Face, fingerprint, PIN or security key
Your device will open a security window. Follow the instructions there to sign in.
Zava
Terms of usePrivacy & cookies...
```

Its only actionable sign-in control was Back. No Cancel, Other ways to sign
in or Use your password instead was offered in that page's DOM. Escape was
used for a possible native dialog, not claimed as proof of a native Cancel.

Final offered wording (blank/tab whitespace preserved exactly in E1):

```text
Sign-in options
Face, fingerprint, PIN or security key
Use your device to sign in with a passkey.
Sign in with GitHub
Zava
Terms of use Privacy & cookies ...
```

Also offered: passkey help, Terms of use, Privacy & cookies and troubleshooting.
No password, Other ways to sign in or Cancel route was offered. Did not select
GitHub, recovery/help or guessed provider endpoints. Stopped all live work at
this terminal outcome. No policy/MFA/role diagnosis follows from this UI.
The owner's MFA-exclusion and ProgrammeManager statements remain supplied
context, not independently verified tenant settings.

Actual password submission: false in E1. Employee session: not obtained.
`/api/me` binding/authentication booleans: unavailable, not false/absent.
No resident attempt. No screenshot, trace, video, HAR, session export or
network response logging; no field/image masking needed because no pixels
were captured. Context/browser closure and owned scratch removal recorded.

## Criterion Acceptance Matrix

This is the complete original 9/4/6 compound inventory. "Unmet" means missing
proof, not a diagnosed product defect. No whole issue is accepted.

| ID | Criterion and current decision | Evidence or missing proof |
| --- | --- | --- |
| 550-01 | Unmet: both-site shared bottom-right launcher/popups | E1 blocks employee surface; old resident public shell cannot prove shared rendered use |
| 550-02 | Unmet: persistent scrolling multi-turn thread, newest bottom, pinned composer, stays open | No authenticated employee conversation or sends |
| 550-03 | Unmet: Enter-send, Shift+Enter newline and Send | Auth controls are not chat-send proof |
| 550-04 | Unmet: compact employee selector in input area changes agent/skill and shows active choice | Employee composer inaccessible |
| 550-05 | Unmet: attach/voice controls or stated disabled reasons | Neither authenticated composer observed in this child |
| 550-06 | Unmet: actual AI content thin label and collapsed sources | No employee response; source/rules-only content is not actual AI proof |
| 550-07 | Unmet: resident consent before any record/data use | Resident excluded; inherited unmet consent boundary unchanged |
| 550-08 | Unmet: relevant rat question answer or honest contact fallback, not home summary | Resident excluded; no authenticated answer |
| 550-09 | Unmet: loading after 200ms, visible errors, keyboard/screen-reader semantics, reduced motion | No authenticated chat; native AT and actual timing/error/motion not observed |
| 551-01 | Unmet: compact top-edge header filters on expanded map | No employee map observed |
| 551-02 | Unmet: filter updates markers and consistent header state/restoration | No live filter/marker/state execution |
| 551-03 | Unmet: keyboard, non-colour selected state and narrow readability | No live map or narrow map |
| 551-04 | Proven, inherited source coverage only: behavior covered by browser test | Prior Review C9, src/api/checks/map_fullscreen_browser_check.py; no new run or deployed parity |
| 552-01 | Unmet: presentation icon set with text labels | No case rendered or served icon provenance |
| 552-02 | Unmet: visibly thinner steps and less vertical space | No live geometry or trusted deployed-before baseline |
| 552-03 | Unmet: one-line blocker summary plus full keyboard/touch disclosure | No blocker observation, native touch unperformed |
| 552-04 | Unmet: attached tabs/panel outside inner scroll, panel beneath | No live case ancestry or scroll geometry |
| 552-05 | Unmet: preserved Fluent 2 and scoped WCAG baseline | No live case, contrast/focus/reflow/zoom/touch/AT/motion acceptance |
| 552-06 | Unmet: desktop and narrow case browser evidence | No case viewport observations; auth text cannot substitute |

Total: one inherited source-coverage criterion proven, eighteen unmet/blocked.
No closing keyword is justified. Refs #550, Refs #551, Refs #552 only.

## Validation and Reproducibility

* Eleven constructed-only offline tests passed after corrections: deterministic
  parsing/CRLF/punctuation, invalid/ambiguous inputs, exact origin guards,
  redaction, finite alternatives, deadline, callback, single-submit and decoy
  password-field regression. No credential file read by tests.
* Ruff check/format and AST parse passed; final lint/hash checks recorded at
  Review handoff. No application test run or deployment parity claimed.
* Four distinct sanitized evidence JSONs and four sibling manifests preserve
  each actual executed-script hash. The current runner matches only E1's hash;
  intermediate script snapshots were not retained, so their exact source
  reconstruction remains unavailable. Do not equate their current source.
* Exact evidence file hashes are checked against all manifests. No image
  artifacts exist; no blanket secret-scan or profile forensic claim.
* Current runner's authenticated feature branch was never exercised live.
  Its presence is not acceptance, verified capture eligibility or test success.
* Full exact-head local gate remains post-Review/post-commit work, with known
  prior non-ancestor base risk. No receipt or gate pass is claimed.
* Final Review handoff: 11/11 offline tests, Ruff check and format-check passed;
  all four evidence byte hashes and definitive executed script hash verified.
  `git diff --check` passed for tracked changes; new files separately parsed
  and inspected, since an untracked diff alone does not lint them.

## Blockers, Remaining Work and Follow-Up

Employee provider route remains blocked: only passkey and GitHub are offered.
Named identity operator must establish a supported route without this task
altering policy/roles. Binding stays unknown until real authenticated /api/me.
Resident access is a separate inherited follow-up; no new resident evidence.
Missing authenticated criteria need later selected execution, not inferred
success. The old runner's RV-003 safety defect is untouched and not reused.

Independent Review is complete with original outcome preserved below.
No repairs or repeated Review in this child after that assessment.
Next: privacy-safe local Refs-only commit and complete external gate attempt.
No push, rebase/merge, issue update, Azure/policy/role/private dataset edit.

## Original Independent Review and Dispositions

Review execution: Complete. Outcome: Not accepted. Execution: Partial.
Review:
.copilot-tracking/reviews/logs/2026-10-30/employee-password-acceptance-review.md.
Findings: 1 High, 3 Medium, 1 Low, all preserved and open:

* RV-001 High: absent authenticated acceptance, later bounded research after
  identity operator establishes a supported route.
* RV-002 Medium: dormant callback branch uses identity-shaped fields instead
  of a confirmed employee/authentication contract; later runner implementation.
* RV-003 Medium: total 180s deadline is not hard across waits/actions; later
  runner implementation before reuse. Actual definitive run was seven seconds.
* RV-004 Medium: submit timeout can retain false not-submitted flag despite
  uncertain delivery; later runner implementation before reuse. Definitive
  run never reached password handling.
* RV-005 Low: intermediate executable snapshots unavailable; preserve original
  limitation and improve future snapshot retention, later research.

No finding repaired during/after Review, no second Review, no full acceptance
or human approval. Current runner is evidence only, not approved for reuse.
Reviewer independently verified definitive script and four evidence hashes;
its checks did not import runner, read secret or perform live authentication.

## Local Persistence Preparation

Authenticated GitHub identity resolved with `gh api user`: id 8036360,
login jmservera. Author and committer use repository-local privacy-safe
`8036360+jmservera@users.noreply.github.com`; no global configuration change.
Fetched main: `63422cdf9fd477dd8892a27ac8b11487bc3a2429`.
No heavy-gate lock holder was listed at the pre-commit read-only inspection.
Candidate commit and full external gate remain pending here; final result
will be retained externally without invalidating a successful receipt.
