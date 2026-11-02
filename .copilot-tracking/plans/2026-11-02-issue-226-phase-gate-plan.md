# Plan: issue 226 phase gate and benefits view (2026-11-02)

* [x] Add assetGates table to the Benefits and phase check panel in role-screens.js (all states Unknown, owners, decider).
* [x] Add unit test: six rows, Unknown, deciders, no controls.
* [x] Run focused gate with --changed and --lock-timeout 600.
* [x] Commit with noreply email, push, open PR with Refs #226.

Critique (executed once, inline): compatible. Table reuses screenTable (focusable named region, caption, text states). Owner roles are suggestions, not facts about Zava; "Board or delegated owner" avoids naming an invented body. Keep the Unknown block so the boundary stays visible. Not in slice: browser or axe check, validation in #155.
