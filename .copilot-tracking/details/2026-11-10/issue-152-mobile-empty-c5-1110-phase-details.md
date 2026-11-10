<!-- markdownlint-disable-file -->

# Phase Details: issue-152-mobile-empty-c5-1110

## P01 implement

* Helper: after the existing horizontal-overflow check add `if not empty.evaluate(CLIP_JS)` appending `"empty explanation is clipped vertically"`. CLIP_JS: `el => { if (el.scrollHeight > el.clientHeight + 1) return false; const r = el.getBoundingClientRect(); for (let a = el.parentElement; a && a !== document.body && a !== document.documentElement; a = a.parentElement) { if (getComputedStyle(a).overflowY === 'visible') continue; const p = a.getBoundingClientRect(); if (r.top < p.top - 1 || r.bottom > p.bottom + 1) return false; } return true; }`.
* Negative: for the first empty-queue role at 320 px, record `el.getAttribute('style')`, set `height:12px; overflow:hidden` via CSSOM, call the helper, then in `finally` restore the exact attribute (remove it when it was null). The check passes only when the failures include the clipping message and the helper passes after restore. The display:none negative is kept with the same restore discipline.
* README: one added sentence qualifying the C4 count (15 empty-queue, 6 populated-queue observations) and the clipping negative. Log entry and recipe SHA through the existing mechanism (literal file digest).
* No changes to app.js, CSS, domain, roles, accounts or data.

## P02 checks

Served harness, Core 3 modules (35), API 4 modules (37), mypy, ruff check and format check in src/api, recipe identity compare.
