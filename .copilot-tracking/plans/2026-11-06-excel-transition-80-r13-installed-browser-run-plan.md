---
title: Issue 80 r13 plan, owned installed environment and schema download browser run
description: Plan for validating the prepared schema download browser check in an owned pip-installed external environment, with one independent critique
ms.date: 2026-11-06
---

* Research: [research](../research/2026-11-06-excel-transition-80-r13-installed-browser-run-research.md). Details: [details](../details/2026-11-06-excel-transition-80-r13-installed-browser-run-details.md).
* [ ] Phase 1: create new `/mnt/ama-gates/e80-r13-r67-1106/` (refuse overwrite) with external venv, TMPDIR, pip cache, XDG, tool caches, bytecode prefix, browser scratch, logs.
* [ ] Phase 2: inspect the interpreter and import provenance before installing; install only what is shown missing or misbound, with pip and the pinned manifests; record versions, import origins and hashes.
* [ ] Phase 3: fresh resource check, nonqueued lock, unmodified `worker_limit(1)`, run the unchanged module from `src/api`, retain raw output and exit, normal harness lifecycle, release lock.
* [ ] Phase 4: pre/post ignored status, production, harness and check byte identity against a6bc5af2.
* [ ] Phase 5: Changes, separate later author Review, state after Review, commit; record execution HEAD versus final record HEAD.

## Decisions

* Candidate distributions are built as wheels from a `git archive` of the execution HEAD into the external area and installed into the external venv. No editable or in-tree build touches the checkout. Dependencies come from the pinned `requirements.txt` hash sets of core, agents and api, then `--no-deps` install of the three candidate wheels; playwright is taken from the dev pin only if missing.
* The Chromium cache is used if its revision matches the installed playwright; a mismatch is a recorded failure first, then an external-only browser install is the single permitted correction (needs a stated actual failure).
* Failure semantics: any missing unobtainable prerequisite, busy lock or refused capacity blocks only this run, with the raw failure preserved. No fake success, no skipped assertion, no PYTHONPATH-only parent.
* Cleanup is limited to this run's transient runtime files under this run's external temp via the normal harness lifecycle. Nothing else is removed.

## Critique

* Executed once, independent (rubber-duck sub-agent, read-only), before any environment preparation. Six findings, dispositions applied directly:
  * 1 browser cache mislocated (XDG_CACHE_HOME redirect): accepted. `PLAYWRIGHT_BROWSERS_PATH` is set explicitly to the verified existing `~/.cache/ms-playwright`, read only.
  * 2 provenance bypass: accepted. Inherited `PYTHONPATH` and other `PYTHON*` variables are cleared for the parent; the venv must resolve concrete modules (for example `zava_forward.api.server`, `zava_forward.core.store` or equivalent real modules) inside the venv site-packages. The child server's `PYTHONPATH` to checkout sources is reported as a harness limitation, not as parent provenance.
  * 3 plan writes into the checkout: rejected. The owner explicitly requires Changes, a separate later Review, state and a commit in the checkout; the browser run itself writes nothing there and pre/post ignored status proves it.
  * 4 manifest claim wrong: accepted. api requirements do not pin candidate distributions; candidate wheels are installed explicitly and their versions and hashes recorded, and playwright's installed version is compared with the 1.64.0 pin.
  * 5 archive versus checkout divergence: accepted. Before building, require tracked status clean, ignored status empty and HEAD equal to the intended commit; record execution commit and fixture hashes.
  * 6 lock lifetime: accepted. The wrapper starts the subprocess in its own process group, terminates it and waits on any wrapper exception or signal before releasing the lock.
