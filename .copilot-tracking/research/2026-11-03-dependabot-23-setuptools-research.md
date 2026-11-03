---
title: Dependabot alert 23 setuptools research
ms.date: 2026-11-03
---

Disposition: executed. Planning readiness: Ready. Tier: focused (build tooling only).

## Findings

* Alert 23 (low): setuptools vulnerable range `>= 38.2.2, < 84.1.0`, first patched 84.1.0, manifest `src/build-requirements.txt`, created 2026-10-24. The API still reports state `open` with no `fixed_at` on 2026-11-03.
* Merged PR #452 bumped setuptools 84.0.0 to 84.1.0 (2026-10-24). Merged PR #622 bumped it to 84.2.1 with regenerated hashes (2026-10-31).
* `src/build-requirements.in` and `src/build-requirements.txt` both pin `setuptools==84.2.1`. No other lock or pin mirrors setuptools; each `src/*/pyproject.toml` declares only `setuptools>=77` as a build floor.
* 84.2.1 is above the patched 84.1.0, so the alert's vulnerable range is already excluded. The owner decision text says "bump to 84.1.0"; setting 84.1.0 would downgrade and reintroduce a pin below the current Dependabot-proposed version, so it is not done.

## Focused build check (run 2026-11-03)

* `pip install --require-hashes -r src/build-requirements.txt` in a fresh venv: installed setuptools 84.2.1, wheel 0.48.0, packaging 26.3.
* `pip wheel --no-deps --no-build-isolation` for src/core, src/agents and src/importer: all three wheels built.
* src/api and src/orchestrator builds were not run (no setuptools pin differences; floor only).

## Conclusion

No file change is needed to satisfy the alert. The open state is most likely a stale Dependabot scan; it should close on the next scan or can be dismissed as fixed by the owner.
