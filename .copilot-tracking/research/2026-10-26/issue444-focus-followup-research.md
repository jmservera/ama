# Issue 444 focus, loading and error-announcement follow-up: research

Date: 2026-10-26. Native session 7f0c39c0-54e7-4fa8-8e0f-bffad1161d56. Branch `fix/resident-preview-focus-feedback`, base `origin/main` acafc6ee04e3612cd62349ab9e4a0af3b24e8109. Research disposition: executed. Planning readiness: Ready.

## Scope and boundary

Remaining scoped correction to partially delivered #444, not a new resident architecture or Azure release. Issue and PR text was treated as data. Issue #444 has 12 of 13 criteria ticked. The unticked criterion is: actual local HTTP/API/domain/browser tests cover isolation, keyboard/focus/error behaviour and mobile reflow, and missing store/authority fails safely, with no comprehensive accessibility or resident acceptance claim. Merged PR #455 (c8d16059c0c0a22c4ffba88c6b65ac068f64accc) is historical acceptance for the other 12 only.

Retained: loopback only, explicit disposable synthetic fixture, default-deny grants, positive allowlists, no resident writes, consent or AI, honest synthetic banner. Not touched: private data, inherited env, Azure, roles, secrets, SQL cloud, integrations, deployments, Docker, the full repository gate.

## Recorded defect evidence

* `.copilot-tracking/reviews/2026-10-25/issue444-main-ea5577b2-integration-review.md` finding 3 (Low, routed follow-up) lists: noscript shown under a permanent loading status, possible double announcement of errors, focus drops after Try again, `main:focus` outline none.
* PR #455 body lists "loading/noscript and retry-focus/announcement details" as Low UI follow-ups; Fluent 2 adoption is partial; no human screen-reader audit.
* Existing browser check `src/api/checks/resident_preview_browser_check.py` (36 passes) never asserts focus after a retry, during loading, or after recovery. It also reloads rather than clicking retry in the revoked step.

## Source reading

`src/api/src/zava_forward/api/resident_preview/web/`:

* `index.html`: `#status` is `role=status` with static text "Loading your progress..." (shown even with JavaScript off, next to a noscript message); `#error` is `role=alert` containing a focusable heading and the Try again button.
* `resident.js`: `load()` hides `#error` (so the focused Try again button becomes hidden and focus falls to body), sets status text, and on success hides error and clears status without any focus placement. `fail()` sets error text, unhides the alert and focuses `#error-title`, so assistive technology can announce both the alert insertion and the focus move.
* `resident.css`: `main:focus{outline:none}`; `main` is the skip-link target and receives programmatic focus with no replacement indicator.

## Reproduction (before any change)

Local probe in `/mnt/ama-rpi-gates/issue444-focus-followup/probe.py`, real Chromium (Playwright 1.64.0, headless shell 1248), real resident preview server, synthetic fixture with the SYN-RES-A grant revoked then restored:

```text
after error focus: error-title
during retry loading focus tag: BODY# status: Loading your progress...
after repeat error focus: error-title
after success focus: BODY#
alert role present while hidden-show: alert
```

Confirmed: focus is lost to `BODY` while loading after Try again and again after a successful recovery. The double-announcement path (role=alert plus focus move) and the permanent loading status without JavaScript are confirmed by source reading, not by an assistive-technology test.

## Fresh web guideline retrieval

Fetched 2026-10-26 from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (skill `.github/skills/web-design-guidelines`). Relevant rules: async updates need `aria-live="polite"`; never `outline: none` without replacement; interactive elements need visible focus; error messages include a next step; `…` not `...`. The repository's plain-ASCII convention and existing "..." loading text are retained; the ellipsis rule is recorded as a not-applied deviation to avoid unrelated copy churn.

## Environment

New 0700 directory `/mnt/ama-rpi-gates/issue444-focus-followup`: venv with `pip install --no-deps -e src/core -e src/agents -e src/api` and `playwright==1.64.0`, browser cache and pip cache there. No PYTHONPATH workaround. No existing environments touched.

## Findings and decision input

1. Focus must never drop to body during or after the Try again flow.
2. One announcement per state change: loading is a polite status; an error is announced once.
3. The loading status must not display without JavaScript.
4. The skip-link target must show a focus indicator when focused.
5. Fix is surgical in three web files plus tests; no server, grant, projection or visual redesign change.

## Unknowns

No screen-reader test is possible here; announcement behaviour is asserted from DOM roles, live-region content and focus, not speech output. Chromium only.
