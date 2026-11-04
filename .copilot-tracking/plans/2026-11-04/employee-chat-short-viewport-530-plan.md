<!-- markdownlint-disable-file -->
# Employee chat short viewport Send: plan (2026-11-04)

Details: [../../details/2026-11-04/employee-chat-short-viewport-530-details.md](../../details/2026-11-04/employee-chat-short-viewport-530-details.md)

* [x] Phase 1: sticky tools row in `chat-widget.css` (scoped to the composer).
* [x] Phase 2: widget browser check asserts Send inside the panel at 320x480 and 640x360.
* [x] Phase 3: focused validation (unit, ruff, mypy, widget browser check) and README note.

Critique (executed once, inline): compatible. A CSS-only sticky row keeps native semantics, tab order and Fluent tokens; no change to approval, consent or AI-unavailable behaviour. Alternative of hiding the intro on short windows rejected as it removes the AI-suggestion and sources context. Applied directly; no owner decision needed.

Stacked slices: none further for this item; criterion 8 live half is owner action.
