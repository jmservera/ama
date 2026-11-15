# 215 keyboard, focus and provenance details

New strictly typed unittest module using regex and substring checks on chat.js, chat-widget.js, chat-widget.css:

* Alerts and lookup controls are native: no `div`/`span` with `role="button"` or `onclick` on non-buttons; buttons set `type`; links are `a` with `href`.
* Widget: launcher `aria-expanded`/`aria-controls`/`aria-haspopup`, toggled in `open` and `hide`; dialog `aria-labelledby`; Escape and Close call `hide()`; `hide` unhides the launcher before `launcher.focus()`; open moves focus to the heading; live regions `log`, `status`, `alert`.
* Regulatory lookup: Escape, status and usage live regions, doubt button native with `aria-disabled` (not `disabled`).
* Provenance: attribution labels for model, decision rules, withheld; `Sources (n)` summary; no-source warning; `statusFor` distinct text for answer, withheld, refused; no-source cue; "cannot approve" warnings.
* Guard: `aria-invalid` absent from chat scripts.
No web files change, so the manifest is untouched.
