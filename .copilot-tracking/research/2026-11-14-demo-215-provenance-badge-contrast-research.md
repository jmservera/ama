# Research: #215 badge contrast tokens (2026-11-14)

Disposition: executed. Planning Readiness: Ready. Refs #215. Tier: focused (test-only, `src/api/tests/`).

## Evidence

* `src/api/src/zava_forward/api/web/style.css` `:root`: `--ink`, `--muted`, `--surface`, `--bg` alias Fluent 2 neutral tokens (#242424, #424242, #fff, #f5f7f8).
* Alert severity chips are `.regulatory-state state-*` headings. They set no colour, so text inherits `--ink`. Cues: 4px `currentColor` border-left, per-state glyph, visible `Status:` text.
* Chat provenance badges are `small.chat-widget-meta` (`--muted`) in `.chat-widget-message` (`--bg`). Variants come from `attribution()` in `chat.js`: decision model, decision model with withheld draft, model-generated, withheld, workflow-only. Each has distinct visible text and an `Outcome:` line.
* The app ships no dark theme. Dark contrast therefore uses Fluent 2 web dark neutral reference values held in the test, not shipped CSS.

## Gaps and limits

* Rendered colour, screen reader and conformance evidence are not produced. Static source and arithmetic only.
* No icon exists on provenance badges; text is the non-colour cue.
