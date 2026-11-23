# Research, issue 220 r13 (2026-11-23)

Research disposition: executed. Planning Readiness: Ready.

Only unticked criterion: "No retaliation, inferred refusal or delayed hazard response". Earlier runs (r11, r12) proved the constructed case live and hardened key case, space and hyphen handling. New angle: the guard still accepts camelCase (`hazardPause`, `retaliationFlag`, `noAccess`), dotted, slashed, repeated-separator, full-width, zero-width and en-dash variants of forbidden keys (probe 2026-11-23). Fix: canonical key form splits camelCase, applies NFKC, drops format characters and collapses any non-alphanumeric run to one underscore. Owner-only items skipped. No live change needed; demo apps still run the earlier guard.
