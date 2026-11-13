<!-- markdownlint-disable-file -->
# Details: Issue 1530 case safety usability

Source of truth for copy and markup: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/ux-spec-1530.md` (Part A, Part B, CSS block).

## P1 app.js decisions

* `readyToRestart = Boolean(x.repaired && x.repair_evidence && x.accepted_at) && !x.released`; the restart form only renders when ready and the signed-in user has the required role and is not the raiser or repair recorder. Otherwise a read-only explanation names the owner role.
* Receiver-only steps (receive, accept, repair, times) show a waiting sentence naming `x.destination` for others.
* Step 1 refer form shows when `!x.referral_version`; legacy rows pre-fill `x.job`. A locked note explains why restart is not yet available (A1).
* Each action is its own `<form>` + `<fieldset class="safety-step">`, submit via `onsubmit` with `reportValidity`, and posts only its own evidence input. Closing `refresh()` field list covers only that form.
* Status text replaces `hazardState` for legacy repaired rows ("older tracker shows a repair, verification not recorded").
* Facts are a 4-row `<dl class="safety-facts">`; audit fields and `Unknown (external service owns timing)` live in `<details class="safety-details">`.
* Raise form: `<form>` + fieldset, hints with `aria-describedby`, `Significant` selected by default, button text `Record safety observation and stop retrofit work`.
* Safety staff select lists Building Safety Liaison first.
* No banned words, no dashes, no new `aria-invalid` or table sites.

## P2 CSS and docs

Spec CSS block, using existing tokens; add `overflow-wrap:anywhere` on `.safety-item`; `.status-line.ok/.wait` glyph-prefixed text. Document classes in `design-system.md`.

## P3 Tests

Static assertions on `app.js` (no unlabelled controls via node DOM render if node and a DOM shim are available, else static parsing) plus behavioural scenarios: legacy row, receiver, non-receiver, ready-to-restart conflicted and independent, raise form.
