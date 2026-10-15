# Details: M1 isolated leaves

* Moves: `mvp/zavaforward_mvp/{ai,profile,rulecards}.py` to `src/core/src/zava_forward/core/`; `mvp/tests/test_profile.py`, `test_rulecards.py` to `src/core/tests/`; `mvp/tests/test_ai_identity.py` to `src/agents/tests/`.
* Import rewrites: `store`, `sqlstore`, `assistants` use `from zava_forward.core.ai import ...`; `server` uses `from zava_forward.core import profile`; tests and mock.patch strings use `zava_forward.core.*`.
* CI: `mvp-ci` and `mvp-validation` add `pip install --no-deps -e src/core` and `src/core/**` path filters; image job runs `docker build -f mvp/Dockerfile -t zavaforward-mvp:ci .`. Check names unchanged.
* Image: two-stage build (hashed build tools, core wheel); the final stage installs hashed requirements then the wheel with `--no-deps`; `mvp/Dockerfile.dockerignore` allowlist replaces `mvp/.dockerignore`.
* Validation gates: src project suites and lint, mvp suite (719 total, 92 skipped), `node --check`, compileall.
