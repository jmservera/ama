# Plan r14

1. Build five release bodies from live bindings; POST once each as the signed-in demo user.
2. Re-read GET /api/assistants; confirm releases in force.
3. Run harness `run()` once in live mode with injected az-cli provider, caps 200k tokens.
4. Record per-assistant tokens; write research note under docs/reference/research/, changes record, review, commit.
