# Critique: issue 2188 live (2026-11-27)

Executed once on the final candidate. Verdict: proceed.

* Require `sha256` as 64 lowercase hex and `log` present in `files`; both match the writer's output, so no valid receipt breaks.
* Scope stays in tools/; no src change, so the focused tier applies. Stricter only; no gate semantics weakened.
* Demo constraints: no Azure, no `--all` run.
