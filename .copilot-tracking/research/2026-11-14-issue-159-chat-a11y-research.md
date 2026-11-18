# Issue #159 criterion 6 research: chat panel accessibility

Research disposition: executed. Planning Readiness: Ready.

Inspected `src/api/src/zava_forward/api/web/chat-widget.js`, `chat-widget.css`, `chat.js`, `index.html` and `style.css`. The `index.html` page only hosts the launcher; the shared widget builds the panel.

Findings:

* Panel is `role="dialog"` with `aria-labelledby` (non-modal, no focus trap). Existing tests assert this role, so it is kept rather than changed to `region`.
* Log already had `role="log"`, `aria-live="polite"`, `aria-relevant="additions text"` and a label. Gap: no explicit `aria-atomic="false"`.
* Status uses `role="status"`, polite and atomic; errors use `role="alert"`.
* Escape closes and returns focus to the launcher. Enter submits, Shift+Enter inserts a newline. `busy()` moves focus from Send to the composer only when Send held focus; message append never moves focus.
* Gap: only the global `:focus-visible` rule in `style.css` covered widget controls; no widget-scoped rule.
* Evidence boundary: Node-DOM harness checks, not assistive-technology testing. No WCAG conformance claim.
