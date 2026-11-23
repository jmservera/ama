# Details 2026-11-23

* `RECEIPT_INERT_PREFIXES = (".copilot-tracking/", "support/")`; `receipt_inert_path(path)` returns startswith.
* `base_relaxation` inert_only: qualify only when `receipt_inert_path(path)`.
* `moved_path_blocker`: `path in pr_paths` check precedes inert shortcut.
* Tests: root README.md, infra/README.md, docs/x.md moved on main now rejected for a full receipt; .copilot-tracking and support moves allowed with kind disjoint-move; same docs path changed by both is rejected by blocker.
