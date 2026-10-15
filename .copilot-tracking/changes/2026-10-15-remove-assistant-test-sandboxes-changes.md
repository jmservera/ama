---
title: Changes - remove assistant test sandboxes
---

* Removed 450 tracked files under `mvp/.assistant-test-*/`.
* `mvp/tests/test_assistants.py`: temp directory outside the repository, `addCleanup` removal, `tearDown` rmtree dropped.
* `.gitignore`: `/mvp/.assistant-test-*/`.
* `.github/workflows/mvp-ci.yml`: tracked-sandbox guard step.
* Validation: 719 tests OK (skipped=92), same as main. `git status` shows only intended changes and no `/tmp/assistant-test-*` leftovers.
