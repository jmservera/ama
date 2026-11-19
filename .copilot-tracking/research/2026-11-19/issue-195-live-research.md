---
title: Issue 195 live RPI research 2026-11-19
---

Task: issue-195-live. Disposition: reused (prior evidence in docs/reference/research/cutover-gate-live-r2-2026-11-18.md and issue-195-live-epic-evidence-2026-11-18.md).

Unticked #195 criteria: (1) #440 stabilization checkpoint (human-blocked, not code); (2) all children closed or deferred (owner decision); (3) deployed image rebuilt from src and verified running.

First criterion that code can advance: (3). Live check 2026-11-19: ca-cutover-test-demo-api revision 0000033 Running, digest sha256:5368f4e4...e5fb. Residual gap from r2: no provenance ties the digest to a source commit (registry network-disabled, ACR tasks failed, no src-deploy runs).

Finding: Dockerfile has no commit build argument; the server logs no build identity. Proposal: ARG ZF_BUILD_COMMIT to ENV, a validated build_info helper, one startup log line readable via container logs.

Planning Readiness: Ready.

Critique (single pass): a new unauthenticated endpoint would widen the surface; use a log line only. Applied directly.
