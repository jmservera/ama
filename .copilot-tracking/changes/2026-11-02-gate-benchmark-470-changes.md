<!-- markdownlint-disable-file -->
# Changes: gate benchmark for #470 (2026-11-02)

* `src/README.md` (Local RPI gate): added a table of three incomplete serial benchmark attempts, the `--jobs 2` admission cap, the tty-stdin hang cause and contention caveats.
* Evidence: attempt 1 receipt `/tmp/rpi470-j1/receipt.json` (failed, infra timeout), attempt 3 `/tmp/rpi470c-j1/receipt.json` (SIGTERM). Attempt 2 left no receipt.
* Divergence: the goal (passing before/after full runs) was not achieved; no numbers were estimated or backfilled. The parallel arm never ran.
