# Plan: HAX design note for #531

* Scope: acceptance criterion 3 residual (design note). Code, behaviour and approval boundaries unchanged. Criterion 7 (live verification) out of scope and stays unmet.
* Phases:
  * [x] Re-run focused unit tests, ruff, mypy; run browser/axe check on constructed data.
  * [x] Add `docs/reference/research/ux/briefing-hax-design-note.md`.
  * [x] Index it in `docs/reference/README.md` and append a `docs/reference/log.md` entry.
  * [x] Link the note from the HAX mapping in `src/api/README.md`.
  * [ ] Commit, push, open PR with `Refs #531` naming criterion 7.
* Critique (single pass, direct): re-implementing UI would duplicate merged work and risk approval boundaries; guideline claims limited to behaviour verified in `app.js`; note must not claim specialist input or accessibility acceptance. Verdict: proceed docs-only.
* Validation: unit tests, ruff, mypy, browser/axe check; link review of the note.
