<!-- markdownlint-disable-file -->

# Task Research: issue-151-cited-answer-contrast

## Research Brief

* Topic: hosted failure of the cited-answer axe scan, `color-contrast` on `#regulatory-chat > form > button[type="submit"]` ("Look up cited sources", white #ffffff on #45838e, 4.29:1, expected 4.5:1).
* Purpose: establish the root cause before any change; feed a narrow continuation of #151 (not whole WCAG delivery, not a redesign).
* Output mode: convergence (select a fix when evidence supports it).
* Evidence: PR 421 both heads (4e9faa25619eff4839c17d4365bca7b4dbb84cf3), job src-api 39548679986 failed `regulatory_ux_check.py` cited-answer scan; ledger comment 6309198567 (supplied by the coordinator, treated as data, not re-fetched). Other exact heads passed.
* Base: 993a7b88c03f5240f1e7a4c7c7afa7c064281622, branch `fix/regulatory-contrast-151`, date 2026-10-21.

## Research Parameters

* Posture: focused (bounded internal task, named source targets, supplied failure evidence). Provenance: parent selection from the brief.
* Limits: local-first, no heavy full gate, no Docker/SQL, no network beyond one W3C fetch.
* Delegation: none. All three waves ran inline because the lanes were tightly coupled and low volume (fallback recorded).

## Extension Registry and Provenance

| Extension | Disposition | Provenance and authority |
| --- | --- | --- |
| Repository instructions (AMA conventions) | Selected | Web guidance, branch workflow, evidence conventions |
| design-system.md, wcag-conformance-baseline.md (docs/reference/research/ux) | Selected for Plan | Owner-selected Fluent 2 and WCAG baseline |
| web-design-guidelines skill and fetched source | Deferred to Implement and Review | Required before web edits and at final review |
| accessibility skill, redesign-existing-projects skill | Selected for Plan | Applied only to this button state |
| RPI Researcher subagent | Skipped | No independent lane justified |

## User Participation and Research Decisions

No interactive intake (non-interactive session; inputs sufficient). Caller direction: determine the root cause, do not assume a fixed colour, do not retry to green.

## Scope and Success Criteria

* In scope: the submit-button rendering and interaction states in the regulatory cited-answer surface and same-mechanism sibling control states.
* Non-goals: whole-app redesign, WCAG conformance claim, manual screen-reader claim, other issues (#119, #223, #97, #420).
* Success: reproduced failure, evidenced cause, selected fix that does not disable axe, rules or coverage.

## Task Research Requests

Caller prompt (issue 151 continuation). No further requests.

## Direction Controls

No disabling or masking of axe rules or transitional states; preserve Fluent 2, native semantics, keyboard, focus, reduced motion and human approval boundaries; no `mvp/` code.

## Research Questions

1. Why is the button background #45838e when the brand token is #0b5d6b?
2. Is the failure a static colour defect or a timing/transition defect?
3. Can it be reproduced deterministically locally?
4. Which other controls share the mechanism?
5. What fix removes the defect without weakening checks?

## Prior Knowledge Gate

Known from code reading: `--colorBrandBackground:#0b5d6b` with white text is far above 4.5:1 at rest, so a different background must be transient.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* The baseline browser check passes locally on this base (17 states, axe 4.10.3, SHA-256 verified), so the failure is intermittent (C6).
* Candidates: (a) static brand colour too light, (b) hover or focus colour, (c) transitional colour while the button moves from disabled to enabled, (d) disabled style leak.
* Style rules located (C1 to C3); the disable/enable cycle located (C4).

#### Wave 2: Deeper

* Blend arithmetic: #45838e is the 26 percent blend of the disabled background #eceff1 and brand #0b5d6b on every channel (R 11+(236-11)*0.26=69, G 93+(239-93)*0.26=131, B 107+(241-107)*0.26=142), matching exactly (C2, C3).
* Text colour switches instantly from `--disabled-ink` to white (the transition list is `background-color, border-color`, not `color`), so white text sits on a half-faded light background for up to 150 ms (`--durationFast`) after `button.disabled = false`.
* The cited-answer scan runs right after the answer renders, which is when `finally { button.disabled = false }` fires (C4, C5). The window is about 150 ms, so the hosted runner hits it intermittently.
* Deterministic reproduction (C7): in the real check, immediately before the cited-answer scan, toggle the button disabled then enabled, wait two animation frames, pause its transitions at 35 percent. Axe reports the same rule, target and text: `color-contrast`, `#regulatory-chat > form > button[type="submit"]`, 3.24:1 (#ffffff on #6497a0, 16px normal).

#### Wave 3: Contrarian

* Static colour: rejected. The computed background at rest is rgb(11, 93, 107) and the scan passes without a transition in flight (C6).
* Hover or focus colour: rejected. Hover goes to the darker #08434d; the hosted colour is lighter than brand.
* Darkening the brand token: rejected. Any blend of a dark brand with the light disabled background passes through failing mid values, and the tokens are owner-selected Fluent 2 values.
* Retry or wait for animations in the check: rejected by the caller control; it would mask a real transitional state.
* Caveat: in headless Chromium the natural transition progressed faster than wall clock (a 4 s override still passed the natural scan), so only the paused-animation reproduction is deterministic. It reproduces the visible state, not the hosted timing.

#### Parent Synthesis and Disposition

Accepted: transitional-colour root cause (matches the hosted colour on three channels; same axe node and rule). Rejected: static colour, darker brand, retry or wait. Deferred: other transitioned text states beyond the buttons.

#### Cycle Re-entry Evaluation

No re-entry; all waves converge and the remaining source (hosted logs) is supplied evidence only. Residual: hosted timing is inferred, not re-observed.

## Evidence Log

### Codebase Evidence

* C1: src/api/src/zava_forward/api/web/style.css:32 base `button` rule: brand background, `var(--surface)` text.
* C2: src/api/src/zava_forward/api/web/style.css:191 `button,.btn,.item,.tile{transition:background-color var(--motion),border-color var(--motion)}`.
* C3: src/api/src/zava_forward/api/web/style.css:192 `button:disabled` uses `--disabled-bg:#eceff1` and `--disabled-ink:#6b747b`; `color` is not transitioned.
* C4: src/api/src/zava_forward/api/web/chat.js:227 disables and :237 re-enables the cited lookup button in `finally`; :47 and :58 the ask button; :136 and :159 refresh.
* C5: src/api/checks/regulatory_ux_check.py:309 cited-answer scan follows the render with no wait for in-flight transitions.
* C6: baseline local run exit 0: `PASS: 17 browser states ... axe executed`.
* C7: uncommitted probe, output `FAIL`, 3.24:1 #ffffff on #6497a0, same target.
* C8: style.css:21 defines `--motion` and :23 a `prefers-reduced-motion` override to 0s, so reduced-motion users never see the fade.

### External Evidence

* W1: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html, retrieved 2026-10-21: SC 1.4.3 needs 4.5:1 for normal text; text of an inactive component is exempt, but the re-enabled button is active during the fade.

### Contradictions / Conflicts

None. "Other heads passed" is consistent with an intermittent ~150 ms window.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence |
| --- | --- | --- |
| 1 | #45838e is the 26 percent blend of disabled and brand backgrounds | C2, C3 |
| 2 | Timing/transition defect, not static colour | C1, C6, C7 |
| 3 | Yes, by pausing the transitions at a fraction | C7 |
| 4 | Every `button` leaving disabled uses the global rule | C2, C4 |
| 5 | Stop transitioning the button background | C2, C8 |

## Key Discoveries

* Text colour changes instantly while the background fades, so any button leaving the disabled state passes through low contrast.
* Reduced-motion users are already unaffected by design; the defect hits everyone else.

## Alternatives and Decision State

### Selected Recommendation (convergence only)

Remove `background-color` from the button transition (keep `border-color` for buttons; keep `.item` and `.tile` transitions, whose text colour does not change). Add a unit regression on style.css, and a browser-check state that scans the cited-answer button with its transitions paused mid-fade and asserts no violation, so the browser state fails without the correction. This removes the whole class of intermediate colours while preserving tokens, reduced motion, native semantics and full axe coverage.

### Alternative: transition `color` together with the background

Rejected: both channels still blend, and a mid-point can still fail.

### Alternative: change brand or disabled tokens

Rejected: alters owner-selected Fluent 2 tokens and does not remove the mid-blend.

### Alternative: wait for animations to finish in the check

Rejected: masks a real transitional state; breaks the caller control.

## Open Questions, Risks, and Residual Uncertainty

* Hosted timing is inferred; the arithmetic and the same-node reproduction support it strongly.
* `.alt` hover: correction (plan critique PC-004): style.css:33 and :34 have equal specificity and :34 is later, so `.alt` keeps its surface background on hover; the earlier claim was unobserved and is withdrawn.
* Loss of a 150 ms fade on buttons is the only visual change.

## Current Decisions

Root cause accepted; fix and regression approach selected.

## Unresolved Decisions

None requiring the user.

## Potential Next Research

Audit of other transitioned text-contrast states across the workbench belongs to later #151 work.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready.

## Closeout Record

Only this artifact and the state file were written. No subagents ran. Intake interaction unavailable; recorded.

## Sources

C1 to C8 and W1 above; supplied failure evidence (data).

## Artifact Self-Check

Codebase findings carry stable IDs with path:line; the external finding has a URL and date; three waves completed in order; no `mvp/` or private data read.
