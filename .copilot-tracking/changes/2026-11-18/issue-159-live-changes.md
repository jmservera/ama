# Issue 159 live changes

Tier: FOCUSED (no `src/` change; evidence, scripts, documentation only). `rpi-checks.py --all` not run.

## Files

* docs/reference/research/assistant-ux-live-159-2026-11-18.md (new research note)
* docs/reference/research/assistant-ux-live-159-2026-11-18/ (login.py, probe-keyboard-announce.py and output, shots-keyboard.py and output, cleanup-own-threads.py, three cropped screenshots)
* docs/reference/README.md (index row), docs/reference/log.md (entry)

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Panel available from a permitted case, never required (ticked) | Not reopened | Launcher present on the case route; ticked earlier |
| Citations, abstain, AI label (ticked) | Not reopened | Observation only: rules-only answers carry the "Decision model (case rules)" label |
| Follow-up keeps case context, re-checks permissions (ticked) | Not reopened | A second typed turn on the case was answered in the same thread |
| Proposal-only (ticked) | Not reopened | |
| Model failure fallback (ticked) | Not reopened | The unmatched follow-up returned "workflow-only help" |
| Tokenomics per-turn record (ticked) | Not reopened | |
| Panel is keyboard operable | Proven live (desktop) | Tab to launcher, Enter, heading focus, tab order through all controls, Enter sends, Escape closes and returns focus |
| Announces new messages | Proven live as DOM and ARIA behaviour | role=log, aria-live polite, additions; four nodes added; status region text per turn |
| Screen-reader tested | Unproven | Needs a person using a screen reader; excluded for the demo by owner decision 2026-11-18; local browser axtree test passes (5 tests; observed, raw output not retained) |

The box stays unticked: the screen-reader part is not proven.

## Validation

* `test_assistant_panel_a11y_159.py` from `src/api`: 5 tests; observed, raw output not retained.
* mypy, ruff and web-UI tests: not applicable, no source or web file changed.
* Hosted CI: not observed; no push.
* Live cleanup: the one thread the probe created was deleted; `<tmp>` session state removed. No Azure resource created or changed.
