# Issue 156 changes (2026-11-01)

Plan: [../../plans/2026-11-01/issue-156-design-trace-gate-executable-plan.md](../../plans/2026-11-01/issue-156-design-trace-gate-executable-plan.md)

* Added `tools/check-design-trace.py` and `tools/test_check_design_trace.py`.
* Documented "Run the design gate" in the prototype profile review; indexed in `docs/reference/README.md`; appended `docs/reference/log.md`.

Validation (focused tier): 7 unittest tests pass (from `tools/`); ruff check and ruff format --check pass on both files; mypy clean on both. Real register: 74 screen issues, 0 designs supplied, verdict blocked. No heavy local gate; CI is the evidence.

PR #665 Copilot review follow-up (2026-11-01):

* Register rows: every table row is collected (only the header/separator pair is skipped), so `|[#74]...` and malformed rows are validated.
* Supplied design now requires a versioned (`vN`) artefact link; `TBD` or unlinked text is malformed.
* Issue label must match the URL issue number and the link must close with `)`.
* Bare relative link targets (for example `gone.md`) are extracted and checked for existence.
* Tests: 11 pass; ruff check and format clean. Real register still 74 screen issues, blocked.
