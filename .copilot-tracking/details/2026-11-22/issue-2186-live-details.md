# Issue 2186 live details

Phase 1: after `self.commit("pr", ...)` and `relaxed_receipt("full")`, move main with `docs/other.md`, patch `tool_identity` (returns `{}`) and `require_fresh_images`, call `gate.verify(root, full, moved)`, assert stdout has `VERIFIED full` and `BASE RELAXED (disjoint-move)`. If receipt["tools"] comparison blocks, patch accordingly.
