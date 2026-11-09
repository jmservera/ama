# Research: issue 954 photo flag browser validation (2026-11-09)

Task: `issue-954-photo-validation`. Mode automatic, owner-selected DEMO targeted tier. Local only: no push, PR, issue, board, deployment, live provider, credential, Entra, Azure, model or spend.

## Disposition

Research executed on 2026-11-09 (read-only). Base `ef28d4da42d83b111d48f14df9b70e3c4932a477` (generated rubric advance from reviewed SQL main `8d6f029c`); branch `test/demo-photo-validation-954-1109`. Backlog manager confirmed no matching open PR and no unmerged implementation dependency.

## Evidence

* Issue 954 is open. Criterion 1 (flag updates without full reload) is ticked. Criterion 2 "Console stays quiet for predictable 503/403" is unticked and needs actual proof.
* Owner clarification (2026-11-09): quiet means no disruptive employee-facing toast and no unhandled application error after an expected 503/403. Inline unavailable/permission status, the initials fallback, the manual path and browser-native diagnostics are acceptable.
* Implementation is already on main (PR 993 `05e93deae`, single commit; record PR 1112). `src/api/src/zava_forward/api/web/app.js` `loadPhoto` turns the flag off on 503/403 without throwing or retrying; `recheckPhotoService` re-checks `/api/me` on tab return, at most once per `PHOTO_RECHECK_MS` (60 s). `app.js` defines no toast; status text is an inline `role="status"` paragraph (`#photo-status`), the avatar falls back to `#account-initials`.
* `src/api/tests/test_photo_availability.py` runs the real functions in Node stubs. It is not a browser observation.
* Old local branch `chore/photo-service-evidence-audit-954` at `1dc30f39` holds a prospective plan (`49b22511`) and a synthetic Chromium checker `src/api/checks/photo_flag_stale_browser_check.py`. Its recorded run: application assertions passed, native `Failed to load resource` diagnostics present (2 per status), literal `quiet_console=false`; review outcome "literal criterion 2 unmet as worded pending owner definition". The checker was ruff-formatted after its only execution and was not re-run. That history is preserved and is not regraded here.
* The existing scenario manifest recipe binding is `src/api/checks/workbench_browser_check.py` (`src/core/src/zava_forward/core/synthetic/scenario_manifest.py`). No photo path is bound, so no recipe SHA change is expected; the manifest and needs-inventory tests are still selected as the owner's integrity checks.
* Environment: Playwright 1.64.1 and Chromium 1248 installed under the user profile; editable installs of `zava-forward-*` point at the primary checkout, so worktree `PYTHONPATH` must be put first and proven. Heavy lock `/tmp/ama-rpi-heavy.lock`.
* Web guidelines source fetched 2026-11-09 from the Vercel `command.md` (8055 bytes) before any web review or edit; the relevant rules are inline async status with `aria-live`/`role=status`, no focus or semantics regression, and honest fallbacks.

## Correction budget (historical)

Productive source-correction cycles recorded for issue 954: 0 review-correction cycles. PR 993 was one implementation commit with no correction commits; PR 1112 was a docs record; the 2026-11-07 local observation made no source change. Repository default is five total scoped review-correction cycles per issue; 0 are spent and none are reset or added. Unchanged-source validation is not a productive correction.

## Gap

Criterion 2 under the clarified definition has never been observed with the clarified assertions (no toast, no disruptive error, no full reload, native diagnostics recorded separately). Nothing has shown a reproduced product bug.

## Constraints

* Synthetic intercepted `/api/me` services and photo responses only; denials stay 503/403, never converted to success; native diagnostics recorded, not suppressed.
* No product fix without a reproduced scoped bug.

Planning Readiness: Ready.
