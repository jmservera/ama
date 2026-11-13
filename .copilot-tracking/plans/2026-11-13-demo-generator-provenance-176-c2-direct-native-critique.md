---
title: "#176 C2 direct-native plan critique (independent rubber-duck, returned inline)"
date: 2026-11-13
---

Verdict: REVISE (reviewer could not write the file; text transcribed by the worker).

1. Blocking: generators gain a core import; specify and test a supported install path in a clean environment.
2. Blocking: consumer reads must exercise freshly generated output, not only unchanged committed fixtures; check for strict-key rejection.
3. Non-blocking: compare repeated builds against an independent pre-change baseline (all content except the header, both payload hashes).
Historical fixtures left untouched is sound; their revision stays Unknown.

Disposition: all accepted. Install path = `.venv-176c2` with core installed (zf_manifest.py precedent). Consumers checked for key strictness. Baseline hashes captured pre-change in the logs directory.
