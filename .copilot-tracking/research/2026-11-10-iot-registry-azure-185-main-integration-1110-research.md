<!-- markdownlint-disable-file -->
# Research: #185 main integration of frozen E1 (2026-11-10)

Task: `185-iot-registry-azure-main-integration`, parent E1 `185-iot-registry-azure-e1`. Research disposition: executed (narrow, merge-impact only).

## Evidence

* Frozen E1 head `105d479aec8f4b19705356c53bd9d554f14e577d`, tree `b4ca322112139d269cd0075908f34e54434f0042`, clean. Independently approved (SAME0483c34d) with zero findings, scope limited to the frozen E1 and not future-main composition.
* Freshly fetched `origin/main` = `06374dfcac47cf6bcce9e7b91f573e8565ab45e8` at 2026-11-10T14:22Z, 22 commits ahead of merge-base `2bfd5e07545db18380f48a9854654c8393d0e9bc`. Latest commit is rubric metadata after real fix `111847191`.
* `git merge-tree --write-tree` of HEAD and origin/main reports a clean tree (`4c9bfbbc13962b38d864f49fc930a2972f24382f`), no conflict paths.
* Main changes under `src/core` since the base: `README.md` (+58), `__main__.py`, `discovery_assistant_demo.py`, `exception_register.py`, `import_refusals.py`, `learning_test_bundles.py`, `sqlstore.py`, `store.py` and tests. `pyproject.toml` is unchanged on main relative to the base, so the topic's optional-extra declaration merges without overlap.
* No main change mentions `device_identity`, `device_provision`, `device_registry` or Azure. No additional directly impacted caller of the adapter was found; `store.py` gained only an `ImportRefusalsMixin`.

## Limits preserved

* The prior full Core discovery timed out; it is not a pass and is not rerun. The API selector was not applicable and is not run.
* `RegistryError.__context__` stays reachable; no live Azure, Registry, credential or token operation.
* No E2, new SDK, exception, provisioning or credential logic; E1 spent, extension remaining 4, none selected.

## Planning Readiness

Ready: an ordinary `--no-ff` merge of the fetched main SHA is expected to be mechanical. A substantive conflict or discovered defect stops for Root.
