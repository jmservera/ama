<!-- markdownlint-disable-file -->
# Review: gate benchmark for #470 (2026-11-02)

* Execution: self-review only; engineering evidence, not independent approval.
* Outcome: documentation records only measured values and states they are incomplete; the #470 timing criterion remains unmet, so the PR uses `Refs #470`.
* Routed follow-ups: (1) make `test_setup_entra` count=2 case non-interactive when stdin is a tty (gate hangs 30 min); (2) rerun serial then `--jobs 2` full gate when the shared lock can be held uninterrupted (about 60 to 90 min).
