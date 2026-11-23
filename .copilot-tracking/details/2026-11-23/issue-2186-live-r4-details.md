# Details 2026-11-23 r4 (issue 2186)

Use `self.move_main` for the first commit, then add commits on side-main by git directly; update origin/main ref; assert via `gate.base_relaxation(..., inert_only=True)`; reset refs in finally as the sibling test does.
