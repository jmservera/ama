# Plan: #225/#226 static UX verification (tracking-only)

* [ ] P1 Copy the 2 prior .copilot-tracking files byte-identically from bfc8ab5c5 (git show, read-only).
* [ ] P2 Line-by-line static audit of asset-board and finance-invoices renderers and CSS against semantics, keyboard, non-colour signals, reduced motion, plain language (exclude HELD_CHECK_ERRORS, #96 D8) and approval boundaries; record file:line.
* [ ] P3 Attempt web-design-guidelines source fetch; record outcome.
* [ ] P4 Run the 3 unit modules via unittest -v in /tmp/venv-225-1045 (pip editable core/agents/api, verify __file__ under worktree); capture true exit code; remove venv.
* [ ] P5 Independent code-review, review file, clean commit (Refs #225, #226, #149).
* Tier: Focused. Write surface: .copilot-tracking only. No push, PR, issue edit.
