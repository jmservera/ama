# Details: issue 954 C1 checker detector correction (2026-11-09)

## Detector design

The in-page observer watches `childList`, `characterData` and attributes `hidden`, `style`, `class`, `open`, `aria-hidden`, so a node filled or revealed after insertion is also evaluated. For each added node, mutation target and its closest candidate ancestor it evaluates candidates matching the existing selector set and records one of:

* disruptive (recorded in `__zfDisruptive`) when the node is rendered (`display` not none, `visibility` not hidden, no `hidden`/`aria-hidden=true` ancestor, non-zero box) and
  * it is a severe overlay (`dialog`, `[role=alertdialog]`, `[aria-modal=true]`, toast/snackbar class or id): visible is sufficient, even when empty, because an empty modal or backdrop still blocks the employee; or
  * it is an ordinary `[role=alert]` with meaningful content: non-empty trimmed text, an accessible name (`aria-label`, `aria-labelledby`, `title`) or an interactive or graphic child (`img`, `svg`, `button`, `a`, `input`).
* ignored (recorded in `__zfIgnored`, surfaced in the receipt) when an ordinary `[role=alert]` is empty with no accessible name, or any candidate is not rendered.

Critique amendments (applied directly):

* Candidates add `[role=dialog]`, `[class*=modal]`, `[class*=backdrop]`, `[class*=overlay]` (the app has none of these except a native `dialog`; visibility gates them).
* On every observer batch the detector sweeps all candidates in the document (not only the target's closest candidate), so revealing a container with an alert inside is caught. A 50 ms interval sweep additionally catches CSS-only visibility changes. Disruptive hits are captured as `outerHTML` strings at evaluation time, so later clearing does not erase them. Remaining limitation: a transient that appears and disappears within one 50 ms interval with no delivered mutation batch is not captured; stated in the receipt note and the review.
* Visual rendering is separate from the accessibility tree: `aria-hidden=true` does not make a visible overlay or backdrop ignorable. Only `display:none`, `visibility:hidden`, the `hidden` attribute (self or ancestor) or a zero box counts as not rendered.
* Self-test fixtures use explicit dimensions, await observer delivery (two animation frames plus the interval), reset the page body between cases and assert both positive and negative outcomes. Added cases: reveal of a hidden container holding an alert with text, a transient toast removed before the next sweep after delivery, a visible `aria-hidden` backdrop and an empty `[role=dialog]`.

A final sweep of `querySelectorAll` candidates runs at the end of each status observation. The empty `#account-error` placeholder is therefore ignored, while any text placed in it, a visible toast, dialog, modal or backdrop still fails. The existing explicit `#account-error` empty-text assertion is kept. Native dialogs (`page.on("dialog")`), page errors and console recording are unchanged and unfiltered.

## Detector self-test (in the same single browser launch)

Before the 503/403 observations the checker opens a blank page, installs the same observer script and asserts: empty `role=alert` ignored; the same node filled with text flagged; hidden alert with text ignored; visible empty `<dialog open>` flagged; visible empty `aria-modal` backdrop flagged; visible empty named `role=alertdialog` flagged; toast with text flagged. Each case is a `check()` line so the receipt shows the regression result. The detector JS is a module constant shared by the self-test and the page runs.

## Receipt

Add `ignored_empty_alerts` per status to the receipt JSON; keep every other field.

## Commands (worktree `PYTHONPATH` first on every command)

* `ruff check` and `ruff format --check` on the checker with the repository-pinned versions.
* Holder check once: `flock -n /tmp/ama-rpi-heavy.lock` wrapping the checker; busy means pause.
* `python3 -m unittest test_photo_availability` in `src/api`; Core `test_scenario_manifest` and `test_needs_inventory`.

## Acceptance for C1

Self-test passes, 503 and 403 each reach quiet classification true with raw receipt retained, selected unit tests exit 0, lint passes. Anything else is reported as not proven.
